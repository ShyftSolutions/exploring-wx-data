from fastapi import FastAPI
import boto3
from botocore import UNSIGNED
from botocore.client import Config


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/latest_runs")
def get_latest_model_runs():
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    result = s3_client.list_objects_v2(Bucket='noaa-gfs-bdp-pds',
                                    Prefix ='gfs.',
                                    Delimiter='/')
    runs = []
    dates = []
    latest_runs = []
    for item in result.get('CommonPrefixes'):
        model, date = item.get('Prefix').strip('/').split('.')
        dates.append(item.get('Prefix'))
    
    for latest_date in dates[-2:]:
        new_result = s3_client.list_objects_v2(Bucket='noaa-gfs-bdp-pds',
                                    Prefix =f'{latest_date}',
                                    Delimiter='/')
        for item in new_result.get('CommonPrefixes'):
            latest_runs.append(item.get('Prefix'))
    return latest_runs

