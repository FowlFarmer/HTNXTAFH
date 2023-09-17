from keys import COHERE_API_KEY
import time
import re
import cohere
co = cohere.Client(COHERE_API_KEY)


const cohere = require('cohere-ai');
cohere.init('XH6WEkN6940HTNO4hl1517Hpl1pX7gW8hpS3RisW'); // This is your trial API key
(async () => {
  const response = await cohere.generate({
    model: 'command',
    prompt: 'give me a recipe using the ingredients: parmesan wedge, milk,  chicken wings, and banana',
    max_tokens: 2366,
    temperature: 1,
    k: 0,
    stop_sequences: [],
    return_likelihoods: 'NONE'
  });
  console.log(`Prediction: ${response.body.generations[0].text}`);
})();