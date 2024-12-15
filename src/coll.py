from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime
from datetime import timedelta
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()

def get_coll(db: str, coll: str):
    try:
        uri = os.getenv('MDB_URI')
        client = MongoClient(uri, server_api=ServerApi('1'))

        return client[db][coll]
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")

def create_index(coll, on):
    try:
        coll.create_index(on)
    except Exception as e:
        print(f"Error creating index: {e}")

def register(user_id, name):
    coll = get_coll("members", "base")
    try:
        coll.insert_one({
            "_id": user_id,
            "name": name
        })
    except Exception as e:
        print(f"Error registering user: {e}")
    
def log(user_id, amount):
    now = datetime.datetime.now()
    coll = get_coll("meal_allowance", f"month_{now.month}")
    try:
        coll.insert_one({
            "member_id": user_id,
            "amount": int(amount),
            "date": now.date().strftime("%Y-%m-%d")
        })
    except Exception as e:
        print(f"Error logging: {e}")

def get_logs(user_id):
    now = datetime.datetime.now()
    coll = get_coll("meal_allowance", f"month_{now.month}")

    try:
        logs = coll.find({"member_id": user_id})
        df = pd.DataFrame(logs)
        df["date"] = pd.to_datetime(df["date"])

        return df, now
    except Exception as e:
        print(f"Error getting logs: {e}")

def get_summary(user_id):
    df, now = get_logs(user_id)
    td_df = df[df["date"] == now.date().strftime("%Y-%m-%d")]
    
    if now.month == 2:
       allowed = 11340
      
    elif now.month in [4, 6, 9, 11]:
       allowed = 12150
        
    elif now.month in [1, 3, 5, 7, 8, 10, 12]:
       allowed = 12555
    
    left_td = 405 - int(td_df["amount"].sum())
    left = allowed - int(df["amount"].sum())

    return left_td, left


def main():
    pass
 
    # for testing

if __name__ == "__main__":
    main()