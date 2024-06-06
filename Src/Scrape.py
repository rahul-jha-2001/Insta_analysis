import requests
import asyncio
import aiohttp
import copy
import pandas as pd
from datetime import datetime
from Src.db_connector import DB
from Src.logger import logging
from dotenv import load_dotenv
import os
from Src.Exception import CustomException



class Scrape():
    Insta_Link = 'https://www.instagram.com/{x}/'

    


    def __init__(self) -> None:
        load_dotenv()
        self.Task_URL = os.getenv("Task_URL")
        self.Scrape_Link_dataset =   os.getenv("Scrape_Link_dataset")
        self.Flag = True
        self.Scanned_count = 0
        self.inputs  =  requests.get(self.Task_URL).json()
        self.DB = DB()
        logging.info("DB connected at Scraper")
        
        
        
    def url_maker(self) -> list:
        url_list = []
        for i in self.To_scan_list:
            url_list.append(self.Insta_Link.format(x=i))
        return url_list   
    def input_obj_maker(self) -> None:
        self.obj_list = []
        list_of_usernames = self.url_maker()
        block_size = 10
        blocks = [list_of_usernames[i:i+block_size] for i in range(0, len(list_of_usernames), block_size)]
        for i in blocks:
            temp = copy.deepcopy(self.inputs)
            temp["directUrls"] =  i
            self.obj_list.append(temp)


    def To_scan(self,update_old_accs:bool) -> list:
        if update_old_accs:
            final_list = self.DB.pull(db = "Clean",document="To_scan",filter= {"priority":1},colunm={"_id":0,"priority":0},limit= 300)
            final_list = [x["id"] for x in final_list]
            final_list = set(final_list)
            final_list = list(final_list)
            if len(final_list) == 0:
                self.Flag = False
                logging.warning("No Accs left to update")
        elif not update_old_accs:
                
                final_list = self.DB.pull(db = "Clean",document="To_scan",filter= {"priority":2},colunm={"_id":0,"priority":0},limit= 300)
                final_list = [x["id"] for x in final_list]
                final_list = set(final_list)
                final_list = list(final_list)

                To_get_filter = {'username': {'$in':final_list}}
                Acc_not_to_scan = self.DB.pull(db = "Clean",document="Creators",filter= To_get_filter,colunm={"_id":0})
                
                for i in [x["username"] for x in Acc_not_to_scan]:  
                    final_list.remove(i)
                if len(final_list) == 0:
                    self.Flag = False
                    logging.warning("No Accs left to scan")

        
        self.To_scan_list = final_list

        remove_filter = {'id': {'$in': final_list }}
        self.DB.delete(db = "Clean",document="To_scan",filter= remove_filter)    
        logging.info("To_scan listed Created")
        self.input_obj_maker()

    
    async def get(self,session: aiohttp.ClientSession,input_obj:dict,url : str) -> dict:

        logging.info(f"Requesting {url}")
        resp = await session.request('POST', url=url,json=input_obj)

        # Note that this may raise an exception for non-2xx responses
        # You can either handle that here, or pass the exception through
        data = await resp.json()
        logging.info(f"Received data for {url}")
        return data


    async def main(self,input_objs,url):
        # Asynchronous context manager.  Prefer this rather
        # than using a different session for each GET request
        async with aiohttp.ClientSession() as session:
            tasks = []
            for obj in input_objs:
                tasks.append(self.get(session=session, url=url,input_obj=obj))
            # asyncio.gather() will wait on the entire task set to be
            # completed.  If you want to process results greedily as they come in,
            # loop over asyncio.as_completed()
            data = await asyncio.gather(*tasks, return_exceptions=True)
            return data
    def Cleaner(self,data) -> None:
        """
            The Scrape function produces a data in the form of 2-d nested Lists -> list[list] 
            To pull the lists out of the main list we use 2 loops to pull them out
            can be done with recrusion but will try later,
            Also traverse the data to find more related profiles to further scan       
        """
        cleaned_data = []
        for i in data:
            for j in i:
                try:
                    j["Date"] = datetime.today() 
                    cleaned_data.append(j)
                    self.DB.push(data=j,db="Raw_data",document="Creator")
                except:
                    logging.warning("Some Error encounterd")
                    logging.warning(f"{j}")
                    continue
        self.Scanned_count = self.Scanned_count + len(cleaned_data)        
        
        logging.info("data Cleaned")

        for i in cleaned_data:

            for j in i["relatedProfiles"]:
                    to_scan_dict = {"id":j["username"],"priority":2}
                    try:

                        self.DB.push(to_scan_dict,"Clean","To_scan")
                    except:
                        continue
                        
      
                
    
  
    async def scrape(self,Update_old_accs:bool =False):
    
        self.To_scan(Update_old_accs)
        if self.Flag:
                data = await self.main(self.obj_list,self.Scrape_Link_dataset)
                self.data = data
                logging.info("Scrapping Done and cleaning statred")
                self.Cleaner(self.data)
    
    async def async_main(self, Update_old_accs:bool =False):
        await asyncio.gather(self.scrape(Update_old_accs))    
    def run(self,Update_old_accs:bool =False):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.async_main(Update_old_accs))
        
if __name__ == "__main__":
    
    obj = Scrape()
    obj.run()