import azure.functions as func
import logging
import json
import os
import random
import uuid
import tempfile
import calendar
from datetime import datetime

import pandas as pd
from services.emotion_generator import generate_month_records
from services.blob_interactor import upload_to_blob
from services.Keyvault_reader import get_secret

from services.fabric_pipeline import trigger_fabric_pipeline

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)






@app.function_name(name="GenerateEmotionData")
@app.route(route="GenerateEmotionData")
def GenerateEmotionData(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request for Generate Emotions Data.')
    # Environment variables from local.settings.json or Azure app settings
    STORAGE_CONNECTION_STRING = get_secret("storage-connstring")
    CONTAINER_NAME = get_secret("emotion-container")
    try:
        # Read ?count=500
        count = req.params.get("count")
        if not count:
            try:
                body = req.get_json()
                count = body.get("count", 10000)
            except:
                count = 10000

        count = int(count)

        # Generate records
        records = generate_month_records(count)
        df = pd.DataFrame(records)

        # Temporary CSV
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"emotion_data_{timestamp}_{count}.csv"
        temp_path = os.path.join(tempfile.gettempdir(), filename)

        df.to_csv(temp_path, index=False)

        # Upload file
        blob_name = f"emotion_data/{filename}"
        upload_to_blob(temp_path, blob_name,STORAGE_CONNECTION_STRING,CONTAINER_NAME)

        return func.HttpResponse(
            # f"Uploaded {count} records to blob: {blob_name}",
            # status_code=200
            json.dumps({
                "status": "Success",
                "recordsUploaded": len(records),
                "FileName": filename,
                "FolderName":"emotion_data",
                "blobUri": f"https://<storageaccount>.blob.core.windows.net/<container>/{blob_name}"
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as ex:
        return func.HttpResponse(
            json.dumps({
                "status": "Error",
                "message": str(ex)
            }),
            status_code=500,
            mimetype="application/json"
        )

@app.function_name(name="BlobCreatedEvent")
@app.event_grid_trigger(arg_name="event")
def BlobCreatedEvent(event: func.EventGridEvent):

    logging.info("BlobCreatedEvent triggered.")

    try:
        data = event.get_json()
        blob_url = data.get("url")

        logging.info(f"Blob created: {blob_url}")


        # 1. CAPTURE the result of your trigger function
        result = trigger_fabric_pipeline(blob_url)

        if "Failed with status" in result:
             # This marks the function as Failed in the portal
             raise Exception(result)

        logging.info(f"Function completed successfully with result: {result}")
        # 3. Explicitly return a success message
        #return  None

    except Exception as ex:
        logging.error(f"Error processing event: {ex}")
        raise ex