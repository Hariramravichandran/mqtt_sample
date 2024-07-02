
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from datetime import datetime

from db import initialize_db, get_collection, close_db_connection
from mqtt_handler import start_mqtt_client, close_mqtt_client

app = FastAPI()

@app.on_event("startup")
def startup_event():
    initialize_db()
    start_mqtt_client()

@app.on_event("shutdown")
def shutdown_event():
    close_mqtt_client()
    close_db_connection()

# Data model for the API request
class TimeRange(BaseModel):
    start_time: datetime
    end_time: datetime


@app.post("/status-count/")
async def status_count(time_range: TimeRange):
    collection = get_collection()
    
    pipeline = [
        {"$match": {"timestamp": {"$gte": time_range.start_time, "$lte": time_range.end_time}}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]
    
    result = list(collection.aggregate(pipeline))
    return result
