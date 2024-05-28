from db_connector import DB

db = DB()
To_remove =  db.pull(db="Clean",document="Creators",filter={},colunm={"_id":0,"username":1})

Temp = [x["username"] for x in To_remove]
remove = {"id":{"$in":Temp},"priority":2}
db.remove(db="Clean",document="To_scan",filter=remove)

