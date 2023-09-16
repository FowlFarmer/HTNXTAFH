from keys import COHERE_API_KEY

import re
import cohere
co = cohere.Client(COHERE_API_KEY)

def processs_text_answer(in_text):

  # first, clean it up by lowercasing etc
  text = in_text.lower().strip()

  # other pressing we might want to do would be to replace common other ways of expressing ranges to just the -
  text = text.replace(" to ", "-")

  # Formats of answers it can give are usually: N days, N-M days (where we will take the average of the two), N weeks, N-M weeks, N months, N-M months, N years, N - N years
  timeframe_mapping_to_days = {
    "day": 1,
    "week": 7,
    "month": 30,
    "year": 365,
  } # this is ok because it already includes the plural forms

  time_options = timeframe_mapping_to_days.keys()

  found_option = None
  for option in time_options:
    if option in text: found_option = option

  if found_option == None: # we didnt find an option, it probably didnt give us a good answer
    print(f"No option found in {in_text}")
    return -1

  # step two is to extract the digits, we will take only digits therefore, and - incase the AI gave a range
  numbers_only_string = ''.join(re.findall(r'[0-9-]', text))

  # range detection
  if "-" not in numbers_only_string:
    value = int(numbers_only_string)
  else:
    numbers = numbers_only_string.split("-")
    v1 = int(numbers[0])
    v2 = int(numbers[1])
    value = (v1 + v2)//2

  # finally, we apply the conversion factor to get it to a number of days
  days_answer = value * timeframe_mapping_to_days[found_option]

  return days_answer


def ask_expiry(item_name):
  # ask the AI
  try:
    response = co.generate(
      prompt=f'How long this food item take to expire in the fridge, in the format, exactly "N days", even for months or weeks, no extra content, or a range of times. Ex: as a response to bananas: 7 days not 8-10 days. Item: {item_name}',
      model='command',
      max_tokens=5,
    )
  except cohere.CohereAPIError:
    print(f"Failed to query cohere API for item {item_name}")

  # get the answer text and process it
  #print(response)
  response_text = response.generations[0].text
  #rint(f"Expiry time text:{response_text}")

  # check that the AI didnt say that it was mad
  days = processs_text_answer(response_text)
  return days

tests = [
  "canned beans",
  "fresh appples",
  "fresh strawberries",
  "strawberries",
  "bananas",
  "lettuce",
  "sliced ham",
  "raw salmon",
  "canned tuna",
  "butter",
  "milk",
  "open jam",
  "peanut butter",
]

confirmation = input("You sure you wanna run the cohere thingy? [y/N]:")
if confirmation != "y":
  exit()
else:
  for test in tests:
    expiry_days = ask_expiry(test)
    print(f"{test}: {expiry_days} days")


#ask_expiry("canned beans")

# print(processs_text_answer("3 days"))
# print(processs_text_answer("3-5 days"))
# print(processs_text_answer("2 weeks"))
# print(processs_text_answer("3-4 weeks"))
# print(processs_text_answer("3 - 4 weeks"))
# print(processs_text_answer("2 months"))
# print(processs_text_answer("3-6 months"))
# print(processs_text_answer("2 years"))
# print(processs_text_answer("5-10 years"))

