import requests
import asyncio
import aiohttp
import copy
import pandas as pd
from datetime import datetime
from db_connector import DB
from logger import logging

class Scrape():
    Task_URL = "https://api.apify.com/v2/actor-tasks/yellow_saint~instagram-scraper-task/input?token=apify_api_qIc4Lwctqfr2WAFjmyQZ2mwd1zYhwO0JFLvE"
    Scrape_Link_dataset = "https://api.apify.com/v2/actor-tasks/yellow_saint~instagram-scraper-task/run-sync-get-dataset-items?token=apify_api_qIc4Lwctqfr2WAFjmyQZ2mwd1zYhwO0JFLvE"
    Insta_Link = 'https://www.instagram.com/{x}/'
    


    def __init__(self) -> None:
        self.inputs  =  requests.get(self.Task_URL).json()
        self.DB = DB()
        logging.info("DB connected at Scraper")
        self.To_scan()
        
        
    def To_scan(self) -> list:
        Unsorted_list = self.DB.pull(db = "Clean",document="To_scan",filter= {},colunm={"_id":0,})
        sorted_data = sorted(Unsorted_list, key=lambda x: x['priority'])
        final_list = []
        for i in sorted_data:
            final_list.append(i["id"])
        self.To_scan = final_list    
        logging.info("To_scan listed Created")

    
    async def get(self,session: aiohttp.ClientSession,input_obj:dict,url : str) -> dict:

        print(f"Requesting {url}")
        resp = await session.request('POST', url=url,json=input_obj)

        # Note that this may raise an exception for non-2xx responses
        # You can either handle that here, or pass the exception through
        data = await resp.json()
        print(f"Received data for {url}")
        return data


    async def main(self,input_objs,url):
        # Asynchronous context manager.  Prefer this rather
        # than using a different session for each GET request
        async with aiohttp.ClientSession() as session:
            tasks = []
            for obj in input_objs:
                print(session)
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
                j["Date"] = datetime.today() 
                cleaned_data.append(j)
        self.DB.push_many(data=cleaned_data,db="Raw_data",document="Creator")

        for i in cleaned_data:
            if  not (i["error"] =="Page not found"):

                for j in i["relatedProfiles"]:
                    to_scan_dict = {"id":j["username"],"priority":2}
                    self.DB.push(to_scan_dict,"Clean","To_scan")
            
      
                
    
    def url_maker(self) -> list:
        url_list = []
        for i in self.To_scan:
            url_list.append(Insta_Link.format(x=i))
        return url_list   
    def input_obj_maker(self) -> None:
        self.obj_list = []
        list_of_usernames = self.url_maker()
        block_size = 10
        print(block_size)
        blocks = [list_of_usernames[i:i+block_size] for i in range(0, len(list_of_usernames), block_size)]
        for i in blocks:
            temp = copy.deepcopy(self.inputs)
            temp["directUrls"] =  i
            self.obj_list.append(temp)  
    async def scrape(self):
        data = await self.main(self.obj_list,self.Scrape_Link_dataset)
        self.data = data
        self.Cleaner(self.data)