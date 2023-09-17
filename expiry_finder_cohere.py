from keys import COHERE_API_KEY
import time
import re
import cohere
co = cohere.Client(COHERE_API_KEY)

TESTING = True

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
    try:
      response = co.generate(
        prompt=f'You are a robot. How long this food item take to expire in the fridge, in the format, exactly "N days". Be acurate. Assume things are in store bought condition, in their usual packaging. If it does not expire, return "inf", but be conservative with these calls. As a response to "bananas": "7 days". Item: {item_name}',
        model='command',
        max_tokens=10,
        temperature=0.7,
        num_generations=5,
      )
    except cohere.CohereAPIError:
      print(f"Failed to query cohere API for item {item_name}")
      return -1

    if TESTING:
      print(response)

    days = []
    for generation in response.generations:
      days.append(processs_text_answer(generation.text))

    print(days)

    # if its 3/5 or more -1s, we just return -1
    if days.count(-1) >= 3:
      return -1
    
    # if its 3/5 or more inf, we just return inf
    if days.count(10000000000000) >= 3:
      return 10000000000000
    
    # if its 3/5 or more infs or -1s, we just return -1
    if days.count(10000000000000) + days.count(-1) >= 3:
      return -1
    
    # otherwise, we take the average of the non -1s and non infs
    numbered_day_values = [x for x in days if x != -1 and x != 10000000000000]
    if len(numbered_day_values) == 0:
      return -1
    else:
      return (sum(numbered_day_values)//len(numbered_day_values)) + 1 # we add one to make it more conservative
  
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