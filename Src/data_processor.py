
from db_connector import DB
from Exception import CustomException
import pandas as pd
import numpy as np
from logger import logging
from datetime import datetime

class ETL():

    flag = True
    def __init__(self) -> None:
        self.DB = DB()
        self.data = self.DB.pull(filter={},colunm={"_id":0},db="Raw_data",document="Creator") 
        if self.data == None:
            self.flag = False
        self.df = pd.DataFrame(self.data)
        logging.info(f"Intializatoin done flag = {self.flag} {self.data}")

    def ETL(self):
        if self.flag == False:
            print("Database empty no data to process")
            return 1
        df = self.df.copy(deep= True)
        posts = []
        for i in df["latestPosts"]:
            if type(i) == float:
                continue
            posts = posts + i
        df_post = pd.DataFrame(posts)


        drop_labels_post = ['shortCode', 'url', 'dimensionsHeight', 'dimensionsWidth','displayUrl','images', 'videoUrl', 'childPosts'
                            ,'locationName', 'locationId',"mentions","alt","ownerUsername","isPinned","id"]
       
        df_post.rename({"id":"media_id"},inplace= True)
            


        df_post.rename(columns = {"id":"media_id"},inplace= True)
        if "isPinned" in df_post.columns: 
            df_post = df_post[df_post["isPinned"] != True]
    
        df_post["timestamp"] = df_post["timestamp"].apply(datetime.fromisoformat,1)
 
          


        df_post = df_post.merge(df[["id","followersCount"]],left_on="ownerId",right_on= "id")

        df_post["ER_per"] = ((df_post["likesCount"] + df_post["commentsCount"])/df_post["followersCount"])*100
        df_post["Reach_per"] = ((df_post["videoViewCount"])/df_post["followersCount"])*100
        df_post["Likes_per"] = ((df_post["likesCount"])/df_post["followersCount"])*100
        df_post["Cmnts_per"] = ((df_post["commentsCount"])/df_post["followersCount"])*100
        df_post["LC_ratio"] = df_post["commentsCount"]/df_post["likesCount"]
        #Creating Different measure of enagement of an acc

        df = df.merge(df_post.groupby(["ownerUsername","ownerId"])
                .agg(avg_likes =("Likes_per","mean"),avg_cmnt =("Cmnts_per","mean"),avg_reach = ("Reach_per","mean"),avg_ER =("ER_per","mean"),avg_LC =("LC_ratio","mean"))
                ,left_on= "id",right_on= "ownerId")

        id_to_hash = {}
        id_to_related = {}

        for i  in df['id']:
            lis = []
            for j in df_post[df_post["ownerId"] == i]["hashtags"]:
                lis = lis + j
            id_to_hash[i] = lis
        temp_lis_1 = []
        temp_lls_2 = []
        for i in id_to_hash.keys():
            temp_lis_1.append(i)
            temp_lls_2.append(id_to_hash[i])
        df_hash = pd.DataFrame({"id":temp_lis_1,"hashtags":temp_lls_2})    
       
       
        df = df.merge(df_hash,left_on = "id",right_on = "id")    




        for i in df["id"]:
            lis = []
            for j in df[df["id"] == i]["relatedProfiles"]:
                for k in j:
                    lis.append(k["id"])
            id_to_related[i] = lis
        temp_lis_1 = []
        temp_lls_2 = []    
       
       
        for i in id_to_related.keys():
            temp_lis_1.append(i)
            temp_lls_2.append(id_to_related[i])
        df_related = pd.DataFrame({"id":temp_lis_1,"related":temp_lls_2})
        
        
        
        for i in drop_labels_post:
            try:
                df_post.drop(i,axis=1,inplace=True)
            except KeyError:
                continue
        
        
        def Category_cleaner(label:str):
            try:
                if "None," in label:
                    label=label.replace("None,","")
            except:
                return "NA"
            return label
        df["businessCategoryName"] = df["businessCategoryName"].apply(Category_cleaner)
        
        
        def day(date):
            return datetime.fromisoformat(str(date)).weekday()
        def hour(date):
            return datetime.fromisoformat(str(date)).hour
        
        df_post["day"] = df_post["timestamp"].apply(day)
        df_post["hour"] = df_post["timestamp"].apply(hour)
        df_post["Date_Updated"] = datetime.today()


        df = df.merge(df_related,left_on = "id",right_on = "id")
       
       
        df_final = df[['Date', 'fullName', 'followersCount', 'verified',
        'followsCount', 'private', 'username',
        'isBusinessAccount', 'id', 'businessCategoryName', 'biography',
        'postsCount','avg_likes', 'avg_cmnt',
        'avg_reach', 'avg_ER', 'avg_LC', 'hashtags', 'related']]
        
        # for j in df_final["username"]:
        #     to_scan_dict = {"id":j,"priority":1}
        #     self.DB.push(to_scan_dict,"Clean","To_scan")
        To_remove =  self.DB.pull(db="Clean",document="Creators",filter={},colunm={"_id":0,"username":1})

        Temp = [x["username"] for x in To_remove]
        remove = {"id":{"$in":Temp},"priority":2}
        self.DB.delete(db="Clean",document="To_scan",filter=remove)    
        
        
        self.DB.push_many(data = df_final.to_dict(orient = "records"),db = "Clean",document = "Creators")
        self.DB.push_many(data = df_post.to_dict(orient = "records"),db = "Clean",document = "Posts")
        remove_filter = {'username': {'$in': list(df_final["username"]) }}
        self.DB.delete(db = "Raw_data",document="Creator",filter= remove_filter) 