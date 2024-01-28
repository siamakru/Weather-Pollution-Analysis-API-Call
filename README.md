# Weather-Pollution-Analysis-API-Call
Fetching weather pollution data from OpenWeatherMap API and create ETL pipeline on AWS and data visualisation and analysis
This Lambda functions call weather data from the OpenWeatherMap API for specified cities, process the data, and upload it to an AWS S3 bucket in a compressed CSV format.

## Setup

### Requirements

- Python 3.7 or later
- AWS Lambda
- AWS S3 Bucket
- OpenWeatherMap API Key

### Dependencies

- `boto3`
- `requests`
- `pytz`

### Configuration

Before using the Lambda function, make sure to configure the following:

1. **AWS S3 Bucket**: Ensure you have an S3 bucket to store the fetched weather data.

2. **OpenWeatherMap API Key**: Obtain an API key from OpenWeatherMap to access their APIs. Replace `"f290e4543234e7bd5722844b33e74d2a"` with your API key.

3. **Cities**: Modify the `cities` list with the names of the cities for which you want to fetch weather data.

4. **Timezone**: Adjust the timezone if needed. The current setup uses the Berlin timezone.

## Functionality

1. **Fetching Data**: The function iterates through the list of cities and fetches weather data, including coordinates and pollution data, for each city using the OpenWeatherMap API.

2. **Processing Data**: The fetched data is processed and formatted into CSV rows.

3. **Compression**: The CSV data is compressed into a gzip file.

4. **Upload to S3**: The compressed CSV file is uploaded to the specified S3 bucket under the `"data/coming/"` directory with a dynamic object name based on the current timestamp and date.

## Usage

1. Deploy the Lambda function with the provided code.

2. Ensure the Lambda function has appropriate IAM permissions to access S3 and execute network requests to the OpenWeatherMap API.

3. Set up a trigger for the Lambda function, such as a CloudWatch Events schedule trigger, to execute periodically based on your data-fetching requirements.

4. Monitor the S3 bucket for the uploaded weather data files.

## Notes

- **Error Handling**: The function includes basic error handling for failed API requests.
- **Timestamps**: The function utilizes timestamps for naming the CSV files and organizing data by date.
- **Data Structure**: The CSV data includes various pollution metrics for each city at a specific timestamp.
