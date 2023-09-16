from keys import API_NINJAS_KEY
import time
import re
import requests

key = API_NINJAS_KEY

#print(key)

headers = {
    'X-Api-Key': key  # Include your API key with 'Bearer ' prefix
}

api_url = 'https://api.api-ninjas.com/v1/imagetotext'
image_file_descriptor = open('receipt.jpg', 'rb')
files = {'image': image_file_descriptor}
r = requests.post(api_url, files=files, headers = headers)

#print(r.json())

long_data = r.json()
text_blurb = ""
for i in range(len(long_data)):
    text_blurb += long_data[i]['text']
    text_blurb += " "

print(text_blurb)