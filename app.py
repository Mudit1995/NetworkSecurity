import sys 
import os 
import certifi
from pymongo import collection
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import pymongo
from networksecurity.exception.exceptin import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from uvicorn import run as app_run
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
import pandas as pd
import traceback

from networksecurity.utils.main_utils.utils import load_object

# MongoDB setup
try:
    client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
    client.server_info()  # This will raise an exception if connection fails
    logging.info("MongoDB connection successful")
except Exception as e:
    logging.error(f"MongoDB connection failed: {str(e)}")
    raise

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def test():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        logging.info("Starting training pipeline")
        training_pipeline = TrainingPipeline()
        
        try:
            artifact = training_pipeline.run_pipeline()
            logging.info("Training pipeline completed successfully")
            return JSONResponse(
                status_code=200,
                content={"message": "Training successful!", "artifact": str(artifact)}
            )
        except Exception as e:
            logging.error(f"Error in training pipeline: {str(e)}")
            logging.error(traceback.format_exc())
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Training Pipeline Error",
                    "message": str(e),
                    "traceback": traceback.format_exc()
                }
            )
            
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        logging.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Server Error",
                "message": str(e),
                "traceback": traceback.format_exc()
            }
        )

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)