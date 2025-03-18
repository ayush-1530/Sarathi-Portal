from pymongo import MongoClient

class operation:
    def __init__(self, mydatabase, collections):
         self.client = MongoClient("mongodb://localhost:27017/")
         self.db = self.client[mydatabase]
         self.collections = self.db[collections]

    def create(self, data):
        self.collections.insert_one(data)

    def read(self, query, required=None):
        return self.collections.find_one(query, required)
    
    def update(self, filter, data):
        u_data = {"$set":data}
        self.collections.update_one(filter, u_data)
        
    def delete(self, query):
        self.collections.delete_one(query)

    

if __name__ == "__main__":
 mydb =  operation("databasess", "employee")
 mydb.create({"firstname": "jjustinnn", "age": 30, "department": "notokie"}) 
 mydb.read() 
 mydb.update({"firstname": "ayush"}, {"age": 305})
 mydb.read() 
 mydb.delete({"firstname": "ayush"}) 
 mydb.read()



