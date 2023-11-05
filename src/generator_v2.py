from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import json
import openai

# read openai api
with open("../api_keys.json", 'r') as config_file:
    config = json.load(config_file)
    api_key = config.get('api_key', '')

openai.api_key = api_key

# Initialize the OpenAIEmbeddings instance
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# Load pregame information and add it to FAISS
loader = TextLoader("../data/pregame.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
main_db = FAISS.from_documents(docs, embeddings)

# Load additional game information and add it to FAISS
loader = TextLoader("../data/game_info.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)
intro_db = FAISS.from_documents(docs, embeddings)

# Combine the two databases into a single database
main_db.merge_from(intro_db)
retriever = intro_db.as_retriever()

def generate_game_intro(db):
    retriever = db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .8, "k": 10})

    prompt = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a commentator at an NBA match, answer the question based only on the following context:{retriever}"
            },
            {
                "role": "user",
                "content": "Generate an NBA game opener that a commentator would say"
            }
        ],
        temperature=1,  # Adjust temperature as needed
        max_tokens=256  # Adjust max_tokens as needed
    )

    game_intro = prompt.choices[0].message["content"]
    return game_intro

#print(generate_game_intro(intro_db))
#get current line in game play json 
def get_current_game_play():
    with open("../data/play_by_play.json", "r") as data_file:
        for line in data_file:
            game_play_data = json.loads(line)
            return game_play_data

def current_game_event(curr_event):
    event_description = openai.ChatCompletion.create(
                                                    model="gpt-3.5-turbo",
                                                    messages=[
                                                        {
                                                        "role": "system",
                                                        "content": "describe this as an event happening"
                                                        },
                                                        {
                                                        "role": "user",
                                                        "content": f"{curr_event}"
                                                        }
                                                    ],
                                                    temperature=1,
                                                    max_tokens=256,
                                                    top_p=1,
                                                    frequency_penalty=0,
                                                    presence_penalty=0,
                                                    )
    return event_description["choices"][0]["message"]["content"]

# Function to retrieve the last n responses from the vector store
def get_context_from_vector_store(curr_game_play_data):
    # Get the last n responses from the vector store
    #context = db.similarity_search(curr_game_play_data)
    context = main_db.as_retriever(curr_game_play_data, search_type="similarity_score_threshold", search_kwargs={"score_threshold": .8, "k": 10})
    return context


def generate_commentary(curr_gameplay, curr_context):

    #get curre_gameplay and all associated context
    curr_context = get_context_from_vector_store(curr_gameplay)

    curr_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": f"You are a sports commentator narrating an NBA game event by event. Given this {curr_context} for this game, generate commentary for the game"
            },
            {
                "role": "user",
                "content": curr_gameplay
            }
        ],
        temperature=0.93,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return curr_response["choices"][0]["message"]["content"]
 
def add_to_vector_store(response):
    splitter = CharacterTextSplitter(
        separator="\n", # Split the text by new line
        chunk_size=100, # Split the text into chunks of 1000 characters
        chunk_overlap=5, # Overlap the chunks by 200 characters
        length_function=len # Use the length function to get the length of the text
    )
    # Get the chunks of text
    chunks = splitter.split_text(response)

    #add to vector store
    main_db.add_texts(texts = chunks,embeddings= embeddings )
    return None

def main():
    data = get_current_game_play()

    n = 1
    while n < 5:

        print("#"*100)
        print(generate_game_intro(intro_db))
        print("#"*100)

        event = data[n]
        curr_event = current_game_event(event)
        print(f"Current event: {curr_event}")
        print("*"*100)

        context = get_context_from_vector_store(curr_event)
        print(f"Context: {context}")
        curr_commentary = generate_commentary(curr_event, context)

        #add it to vector store 
        add_to_vector_store(curr_commentary)

        #print (new_commentary)
        print(f"Commentary: {curr_commentary}")
        print("#"*100)
        
        #average lag time
        n +=1
    return None

if __name__ == "__main__":
    main()

