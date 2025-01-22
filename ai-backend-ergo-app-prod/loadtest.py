import logging
import requests
import time

# Configure logging
logging.basicConfig(filename='upload_test.log', level=logging.INFO,
                    format='%(asctime)s - Request %(message)s')

# URL of the Django application endpoint that handles the image upload
url = "http://54.169.254.152:80/api/images/seatedposture/"

# Path to the image file you want to upload
image_path = "/home/yuvaraj0702/aipose/media/images/alan4.jpg"

# Number of requests to send
num_requests = 100

# Interval between requests (in seconds)
interval = 0

for i in range(num_requests):
    with open(image_path, 'rb') as image_file:
        files = {'image_file': image_file}
        response = requests.post(url, files=files)
        log_message = f"{i + 1}: Status Code: {response.status_code}, Response: {response.text}"
        logging.info(log_message)
        print(log_message)
        time.sleep(interval)
