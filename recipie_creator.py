from keys import OPENAI_KEY
import requests
import openai

openai.api_key = OPENAI_KEY

def generate_recipe(ingredients, prompt):
    ingredients_str = ', '.join(ingredients)  # Convert the list of ingredients to a comma-separated string
    prompt = f" {prompt}:{ingredients_str}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
        {
            "role": "system",
            "content": "You are a recipe generating machine. Give me a recipe that uses the following ingredients. Respond in HTML only using p and b tags. It must not have any other HTML tags. Keep it medium length and detail. Give it a title at the top. You do not have to use all ingredients, and can choose more to buy. The ingredients will follow."
        },
        {
            "role": "user",
            "content": f"{ingredients_str}"
        },
        ],
        temperature=1,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response)
    return response.choices[0].message.content

if __name__ == "__main__":
    ingredients = ["chicken", "rice", "broccoli"]
    prompt = "You are a recipe generating machine. Give me a recipe that uses the following ingredients. Respond in HTML only using p and b tags. It must not have any other HTML tags. Keep it medium length and detail. Give it a title at the top. You do not have to use all ingredients, and can choose more to buy. The ingredients will follow."
    recipe = generate_recipe(ingredients, prompt)
    print(recipe)
