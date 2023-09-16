from keys import API_NINJAS_KEY
from keys import COHERE_API_KEY
import requests
import cohere
co = cohere.Client(COHERE_API_KEY)

key = API_NINJAS_KEY

#print(key)

headers = {
    'X-Api-Key': key  # Include your API key with 'Bearer ' prefix
}

api_url = 'https://api.api-ninjas.com/v1/imagetotext'
image_file_descriptor = open('receipt.jpeg', 'rb')
files = {'image': image_file_descriptor}
r = requests.post(api_url, files=files, headers = headers)

#print(r.json())

long_data = r.json()
text_blurb = " ".join([v['text'] for v in long_data])
print(text_blurb)



# ------------------- UP: IMG TO TEXT, DOWN: TEXT CLEANUP

def ask_expiry(blurb):
  for i in range(3):
    try:
      response = co.generate(
        prompt=f'Interpret these reciept lines to decypher the food items, all lowercase and separated by commas. Expand abbreviations, ex: trky brgr -> turkey burger. Ignore unknown acroynms, or repeats. Do not list non food entries: {blurb}',
        model='command',
        max_tokens=300,
        temperature=0.7,
      )
      return response.generations[0].text
    except cohere.CohereAPIError:
      print(f"Failed to query cohere API for item, trying again...")
      continue

print(ask_expiry(text_blurb))
