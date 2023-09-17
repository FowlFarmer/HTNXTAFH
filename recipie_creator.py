from keys import OPENAI_KEY
import requests
import openai

openai.api_key = OPENAI_KEY

def generate_recipe(ingredients, prompt):
    ingredients_str = ', '.join(ingredients)  # Convert the list of ingredients to a comma-separated string
    prompt = f" {prompt}:{ingredients_str}"
    response = openai.Completion.create(
        engine="davinci",  # Choose the GPT-3 engine you want to use
        prompt=prompt,
        max_tokens=2000  # Adjust based on your requirements
    )
    print(response)
    return response.choices[0].text

if __name__ == "__main__":
    ingredients = ["chicken", "rice", "broccoli"]
    prompt = "You are a recipie generating machine. Give me a recipie that uses the following ingredients. Give the recipie a name, and respond in very basic HTML format with bold and headers. Keep it short. The ingredients are: "
    recipe = generate_recipe(ingredients, prompt)
    print(recipe)
