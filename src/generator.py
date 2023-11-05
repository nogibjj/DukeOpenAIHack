from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
import json
import openai
import time

# read openai api
with open("../api_keys.json", "r") as config_file:
    config = json.load(config_file)
    api_key = config.get("api_key", "")

openai.api_key = api_key

# Initialize the OpenAIEmbeddings instance
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

# Load pregame information and add it to FAISS
loader = TextLoader("../data/pregame_info.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
main_db = FAISS.from_documents(docs, embeddings)

# Load additional game information and add it to FAISS
loader = TextLoader("../data/game_info.txt", encoding="utf-8")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
intro_db = FAISS.from_documents(docs, embeddings)

# Combine the two databases into a single database
main_db.merge_from(intro_db)
retriever = intro_db.as_retriever()


def generate_game_intro(db):
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.8, "k": 10},
    )

    prompt = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a commentator at an NBA match, answer the question based only on the following context:{retriever}",
            },
            {
                "role": "user",
                "content": "Generate an very brief NBA game opener that a commentator would say in two to three sentences.",
            },
        ],
        temperature=1,  # Adjust temperature as needed
        max_tokens=100,  # Adjust max_tokens as needed
    )

    game_intro = prompt.choices[0].message["content"]
    return game_intro


# print(generate_game_intro(intro_db))
# get current line in game play json
# def get_current_game_play():
#     with open("../data/play_by_play.json", "r") as data_file:
#         for line in data_file:
#             game_play_data = json.loads(line)
#             return game_play_data


def get_current_game_play():
    with open("../data/play_by_play.json", "r") as data_file:
        for line in data_file:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                game_play_data = json.loads(line)
                return game_play_data


def current_game_event(curr_event):
    event_description = f"It's the {curr_event['quarter']} quarter, {curr_event['clock']} minutes on the clock, {curr_event['description']}, the event here is a {curr_event['event_type']}, the home team has {curr_event['home_points']} points, and the away team has {curr_event['away_points']} points."
    return event_description


# Function to retrieve the last n responses from the vector store
def get_context_from_vector_store(curr_game_play_data):
    # Get the last n responses from the vector store
    context = main_db.similarity_search(curr_game_play_data)
    return context


def generate_commentary(curr_gameplay, curr_context):
    # get curre_gameplay and all associated context
    curr_context = get_context_from_vector_store(curr_gameplay)

    curr_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"You are a sports commentator narrating an NBA game event by event. Given this {curr_context} for this game, generate very brief commentary for the game at a point of this {curr_gameplay}. Address this in the present tense as live commentary for a game that is happening.Make it very brief and excited. Dont start the sentence with 'and' and dont say what time of the game it is. Make the responses two to three sentences long.",
            }
        ],
        temperature=0.93,
        max_tokens=100,
        top_p=1,
        frequency_penalty=1.0,
        presence_penalty=0,
    )
    return curr_response["choices"][0]["message"]["content"]


def add_to_vector_store(response):
    splitter = CharacterTextSplitter(
        separator="\n",  # Split the text by new line
        chunk_size=1000,  # Split the text into chunks of 1000 characters
        chunk_overlap=50,  # Overlap the chunks by 200 characters
        length_function=len,  # Use the length function to get the length of the text
    )
    # Get the chunks of text
    chunks = splitter.split_text(response)

    # add to vector store
    main_db.add_texts(texts=chunks, embeddings=embeddings)
    return None


def main():
    data = get_current_game_play()

    intro = generate_game_intro(intro_db)
    with open("commentary.txt", "a") as output_file:
        output_file.write(f"{intro}")

    n = 2
    while n < 10:
        event = data[n]
        curr_event = current_game_event(event)

        context = get_context_from_vector_store(curr_event)
        curr_commentary = generate_commentary(curr_event, context)

        # add it to vector store
        add_to_vector_store(curr_commentary)
        print(curr_commentary)
        # print (new_commentary)
        with open("commentary.txt", "a") as output_file:
            output_file.write(f"{curr_commentary}\n")


        # average lag time
        print(n)
        n += 1
    return None


if __name__ == "__main__":
    main()
