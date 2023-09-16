from keys import COHERE_API_KEY
import time
import re
import cohere
co = cohere.Client(COHERE_API_KEY)

TESTING = True
ASK_TRIES = 3
TRY_DELAY_S = 20

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
    "inf":10000000000000,
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

  # special case for infinity
  if found_option == "inf":
    return timeframe_mapping_to_days["inf"]

  value = 0
  # range detection
  if "-" not in numbers_only_string or len(numbers_only_string.split("-")) == 1: # the second arugment is in case of answers like "3 days to expire", which becomes "3 -" becuase of the to filter
    value = int(numbers_only_string)
  else:
    numbers = numbers_only_string.split("-")
    try:
      v1 = int(numbers[0])
    except:
      v1 = None
    try:
      v2 = int(numbers[1])
    except:
      v2 = None

    if not v1 == None and not v2 == None:
      value = (v1 + v2)//2
    elif v1 == None:
      value = v2
    elif v2 == None:
      value = v1

  # finally, we apply the conversion factor to get it to a number of days
  days_answer = value * timeframe_mapping_to_days[found_option]

  return days_answer


def ask_expiry(item_name):
  tryCount = 0
  while tryCount < ASK_TRIES:
    tryCount += 1
    # ask the AI
    try:
      response = co.generate(
        prompt=f'How long this food item take to expire in the fridge, in the format, exactly "N days". Be acurate. Assume things are in store bought condition, in their usual packaging. If it does not expire, return "inf". As a response to "bananas": "7 days". Item: {item_name}',
        model='command',
        max_tokens=10,
        temperature=0.7,
      )
    except cohere.CohereAPIError:
      print(f"Failed to query cohere API for item {item_name}")
      # if it fails, we wait the time and then try again
      if tryCount < ASK_TRIES: # we can go again, then wait
        print(f"Trying again in {TRY_DELAY_S}s")
        time.sleep(TRY_DELAY_S)
      continue

    if TESTING:
      print(response)

    response_text = response.generations[0].text

    # check that the AI didnt say that it was mad
    days = processs_text_answer(response_text)

    if days == -1: # try again if we didnt find an interpreted answer
      continue
    
    return days
  
  return -1 # we didn't get an answer in the end

if __name__ == "__main__":
  tests = [
    "bok choy",
    "fresh appples",
    "fresh strawberries",
    "dead human body",
    "orphan",
    "rocks",
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