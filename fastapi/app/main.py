from typing import Tuple
from fastapi import FastAPI
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import iris



def list_forecast_hours(run_prefix):
    files = []
    hours = []
    run_hour = run_prefix.split('/')[-2]
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    result = s3_client.list_objects_v2(Bucket='noaa-gfs-bdp-pds',
                                       Prefix =f'{run_prefix}atmos/gfs.t{run_hour}z.pgrb2.0p25.f')
    files = result.get('Contents')
    for file_meta in files:
        filename = file_meta['Key']
        if not filename.endswith('.idx'):
            hours.append(int(filename.split('.')[-1].lstrip('f')))
    
    return hours
    

def get_latest_model_run():
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

def get_model_data(param, level, run, hours, merged=True):
    run_hour = run.split('/')[-2]
    s3_client = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    cubes = []
    for forecast in hours:
        forecast_file = f'{run}atmos/gfs.t{run_hour}z.pgrb2.0p25.f{forecast:03d}'
        data_index = s3_client.get_object(Bucket='noaa-gfs-bdp-pds',
                                          Key=f'{forecast_file}.idx')
        body = data_index["Body"]
        contents = body.read().decode(encoding="utf-8", errors="ignore")
        idx_data = parse_index_file(contents)
        
        # param_to_get = idx_data['2 m above ground']['TMP']
        param_to_get = idx_data[level][param]
        
        print(f'Filename = {forecast_file}, param_to_get = {param_to_get}')
        data_response = s3_client.get_object(Bucket='noaa-gfs-bdp-pds',
                                             Key=forecast_file,
                                             Range=f'bytes={param_to_get["start_byte"]}-{param_to_get["end_byte"]}')
        
        data = data_response["Body"].read()
        dl_name = f'/tmp/{forecast}_{level}_{param}'
        with open(dl_name, 'wb') as f:
            f.write(data)
        cubes.append(iris.load(dl_name)[0])
    
    if len(hours) > 1:
        cubes = iris.cube.CubeList(cubes)
        if merged is True:
            merged_cube = cubes.merge_cube()
            return merged_cube
        else:
            return cubes
        
    else:
        return cubes[0]
        
def parse_index_file(index_data):
    data_dict = {}
    last_level = None
    last_param = None
    for row in index_data.splitlines():    
        num, start_byte, model_run, param, level, fcst, dummy = row.split(':')
        if last_param is not None and last_level is not None:
            data_dict[last_level][last_param]['end_byte'] = int(start_byte) - 1
        if level not in data_dict.keys():
            data_dict[level] = {}
        data_dict[level][param] = {'start_byte': start_byte}
        last_level = level
        last_param = param
    return data_dict







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

@app.get("/temperature")
def get_temperature_at_coord(latitude: float, longitude: float):
    runs = get_latest_model_run()
    hours = list_forecast_hours(runs[0])

    run = runs[-1]
    level = '2 m above ground'
    param = 'TMP'
    forecasts = hours[:1]

    cube = get_model_data(param, level, run, forecasts)
    sample_points = [('latitude', latitude), ('longitude', longitude)]
    datar = cube.interpolate(sample_points, iris.analysis.Linear())
    response = {"latitude": latitude, "longitude": longitude, "temperature": datar.data.tolist()}
    return response