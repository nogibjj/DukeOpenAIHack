import json
import openai


#get api key
with open("../api_keys.json", 'r') as config_file:
    config = json.load(config_file)
    openai.api_key = config['api_key']

def get_sentiments(user_input):
    """takes user input and returns assistant output """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a mood detection assistant, the user will give you how they feel and you will tell us what sentiments are in there which can help suggest relevant songs"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    assistant_response = response['choices'][0]['message']['content']
    return assistant_response

# Example usage:
user_input = "I'm feeling really happy today, my car didnot breakdown and my coffee was made perfect"
result = get_sentiments(user_input)
print("Assistant's Response:", result)
