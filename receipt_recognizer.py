from keys import API_NINJAS_KEY
from keys import OPENAI_KEY
import requests
import openai

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
#print(text_blurb)



# ------------------- UP: IMG TO TEXT, DOWN: TEXT CLEANUP
def ask_expiry(blurb):
  
  # Define the data payload
  openai.api_key = OPENAI_KEY
  #print(blurb)
  response = openai.ChatCompletion.create(
    model="gpt-4",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    messages=[
    {
      "role": "user",
      "content": "I have a receipt with this information. Interpret the entries to get a name of only what you consider to be food items, all lowercase and separated by commas. Expand abbreviations into real words, for example trky brgr would become turkey burger. Output the list of the names of the food items. Put the adjectives before the type of food. For example, it's preferred to say red apple over apple red. Do not explain what you are doing, just output a list and no other words: "+blurb
    }
    ]
  )
  return response

"""data = {
      'prompt': prompt,
      'model': 'davinci-002',
      'max_tokens': 200  # Adjust as needed for your use case
  }
  headers = {
      'Authorization': "Bearer "+gpt_key,
      'Content-Type': 'application/json'
  }
  # Make the API request
  response = requests.post(gpt_endpoint, json=data, headers=headers)

  # Handle the API response
  if response.status_code == 200:
      response_data = response.json()
      generated_text = response_data['choices'][0]['text']
      return generated_text
  else:
      print(f"Request failed with status code: {response.status_code}")
      return response.text


def ask_expiry(blurb):
  for i in range(3):
    try:
      response = co.generate(
        prompt=f'',
        model='command',
        max_tokens=300,
        temperature=0.7,
      )
      return response.generations[0].text
    except cohere.CohereAPIError:
      print(f"Failed to query cohere API for item, trying again...")
      continue"""

print(ask_expiry(text_blurb)["choices"][0]["message"]["content"])
