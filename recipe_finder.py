from keys import OPENAI_KEY
import requests
import openai

openai.api_key = OPENAI_KEY

<<<<<<< HEAD
const cohere = require('cohere-ai');
cohere.init('XH6WEkN6940HTNO4hl1517Hpl1pX7gW8hpS3RisW');
(async () => {
  const response = await cohere.generate({
    model: 'command',
    prompt: f'give me a recipe using the ingredients: {prompt}',
    max_tokens: 2366,
    temperature: 1,
    k: 0,
    stop_sequences: [],
    return_likelihoods: 'NONE'
  });
  console.log(`Prediction: ${response.body.generations[0].text}`);
})();
=======
def generate_recipes(ingredients, prompt):
    ingredients_str = ', '.join(ingredients)  # Convert the list of ingredients to a comma-separated string
    prompt = f" {prompt} .{ingredients_str}"
    response = openai.Completion.create(
        engine="davinci",  # Choose the GPT-3 engine you want to use
        prompt=prompt,
        max_tokens=150  # Adjust based on your requirements
    )
    return response.choices[0].text

ingredients = ["chicken", "rice", "broccoli"]
prompt = "What are some creative recipes I can make with these ingredients? Please also state the recipe name."
recipe = generate_recipes(ingredients, prompt)
print(recipe)
>>>>>>> 24f6a87d5042834d2a5a281cef4fb87783a7fc75
