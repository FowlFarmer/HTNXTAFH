from keys import API_NINJAS_KEY
from keys import OPENAI_KEY
import requests
import openai

ninja_headers = {
    'X-Api-Key': API_NINJAS_KEY
}

ninja_api_url = 'https://api.api-ninjas.com/v1/imagetotext'

def image_to_text(image_file_path):
  image_file_descriptor = open(image_file_path, 'rb')
  files = {'image': image_file_descriptor}
  r = requests.post(ninja_api_url, files=files, headers = ninja_headers)

  long_data = r.json()
  extractedText = " ".join([v['text'] for v in long_data])
  return extractedText

def interpret_receipt(text):
  # Define the data payload
  openai.api_key = OPENAI_KEY
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
      "content": f"I have a receipt with this information. Interpret the entries to get a name of only what you consider to be food items, all lowercase and separated by commas. Expand abbreviations into real words, for example trky brgr would become turkey burger. Output the list of the names of the food items. Put the adjectives before the type of food. For example, it's preferred to say red apple over apple red. Do not explain what you are doing, just output a list and no other words: {text}"
    }
    ]
  )

  text_answer = response["choices"][0]["message"]["content"]
  return text_answer

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

if __name__ == '__main__':
  text = image_to_text('receipt.jpeg')
  print(text)
  print(interpret_receipt(text))