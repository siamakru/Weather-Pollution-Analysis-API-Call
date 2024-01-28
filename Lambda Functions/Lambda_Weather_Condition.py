import json
import boto3
import csv
import os
import gzip
import datetime
from datetime import date
import requests
import io
import pytz

# AWS S3 credentials and bucket information
bucket = 'current-weather-staging'
s3_client = boto3.client('s3')


# Define API-Key
api_key = "f290e4543234e7bd5722844b33e74d2a"

# List of cities
cities = ["Berlin", "Munich", "Hamburg", "Frankfurt", "Nuremberg"]

# Set the Berlin timezone
berlin_tz = pytz.timezone('Europe/Berlin')

def lambda_handler(event, context):

     # Define Object name and address and timestamps
    current_datetime = datetime.datetime.now(berlin_tz)
    current_timestamp = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    formatted_timestamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    date_part = formatted_timestamp.split()[0]
    object_name = f'date={date_part}/{current_timestamp}'

    
    # Initialize the CSV rows with the header
    rows = [['City', 'Longitude', 'Latitude', 'status', 'status_detail', 'Temperature', 'Feels Like', 'Temp Min', 'Temp Max', 'Pressure', 'Humidity', 'Speed', 'Degree', 'Visibility', 'Timestamp']]


    for city_name in cities:
        # Define endpoints for coordinates
        endpoint_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}" 

        # Request coordinates data for the city
        response_geo = requests.get(endpoint_geo) 

        # Extract coordinates from json file
        if response_geo.status_code == 200:
            data_geo = response_geo.json()
            lat = data_geo[0]['lat']
            lon = data_geo[0]['lon']
        else:
            print(f"Request for {city_name} coordinates failed with status code:", response_geo.status_code)
            continue

        # Define endpoints for pollution data
        endpoint_weather = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

        # Request pollution data
        response_weather = requests.get(endpoint_weather)

        # Extract coordinates from json file
        if response_weather.status_code == 200:
            data_weather = response_weather.json()
            coord = data_weather['coord']
            weather = data_weather['weather'][0]
            main = data_weather['main']
            visibility = data_weather["visibility"]
            wind = data_weather["wind"]


            row = [
                city_name,
                coord['lon'],
                coord['lat'],
                weather['main'],
                weather['description'],
                main['temp'],
                main['feels_like'],
                main['temp_min'],
                main['temp_max'],
                main['pressure'],
                main['humidity'],
                wind['speed'],
                wind['deg'],
                visibility, 
                formatted_timestamp
                ]
            rows.append(row)
        
        else:
            print(f"Request for {city_name} pollution data failed with status code:", response_polut.status_code)

    # Create a single CSV file with all data
    csv_filename = f"/tmp/{current_timestamp}.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rows)

    # Create a Gzip file
    gz_filename = f"/tmp/{current_timestamp}.csv.gz"
    with open(csv_filename, 'rb') as f_in:
        with gzip.open(gz_filename, 'wb') as f_out:
            f_out.writelines(f_in)

    # Upload the Gzip file to S3
    s3_client.upload_file(gz_filename, bucket, "data/coming/" + object_name + '.csv.gz')
