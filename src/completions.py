import json
import openai


#get api key
with open("../api_keys.json", 'r') as config_file:
    config = json.load(config_file)
    api_key = config['api_key']


api_key = 'YOUR_API_KEY'
prompt = "I am feeling tired,"

response = openai.Completion.create(
    engine="text-davinci-002",  
    prompt=prompt,
    max_tokens=10, 
    api_key=api_key
)
print(response.choices[0].text)