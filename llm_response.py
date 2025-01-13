# from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import faiss

from langchain.chains import RetrievalQA
# from langchain.prompts import PromptTemplate
import pandas as pd
import openai
from openai import OpenAI
#from openai import OpenAI
import numpy as np
import os
#from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Setting the working directory
script_dir = 'Your CSV file dir'
# Changing to working directory
os.chdir(script_dir)

# Defining the credentials and Models


#Get environment variables
openai.api_key = os.getenv("OPENAI_KEY")
gpt_model = os.getenv("GPT_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")

# Create an instance of the ChatOpenAI class
client = OpenAI(api_key = "your API key")

df = pd.read_csv(os.path.join(script_dir, 'input_dataframe', 'scraped_text_only.csv'))
#df = pd.read_csv('D:\Work\Implementations\SYL chatbot\codes\OpenAI chat\input_dataframe\scraped_text_only.xlsx')

# Assuming that you've created eMBEDDINGS AND using embedding_vectorstore.py file 
# Let's use that saved indexes of the ceated embedding  

# To load the index from a file
index = faiss.read_index(os.path.join(script_dir, 'vector_DB', 'vector_store.index'))

#convert the text column in dataframe of scraped data to a list
texts_list = df['text'].tolist() 

#def generate_response(query_text, texts_list, index):
def generate_response(query_text):    
    
    ###...Creating embedding for the input query...###
    embed_response = client.embeddings.create(
        model=embedding_model,
        input=[query_text]
    )

    # Extract the embedding of the query text
    query_embedding = embed_response.data[0].embedding #response['embeddings'][0]

    ###...Use the FAISS index to find the most similar embeddings to the query embedding...###
    k = 10  # Number of similar items to retrieve
    distances, indices = index.search(np.array([query_embedding]), k)

    ###.....Generate a response using the llm.....###
    # Get the most similar texts
    similar_texts = [texts_list[i] for i in indices[0]]

    # Generate a response
    # response = llm.generate_response(query_text, similar_texts)

    template = """
    you are an instructor for students preparing for design and other competitive exams and your task
    is to provide a detailed suggestion, tips, strategy, steps, ideas, and solutions for the question given to you.
    Fetch the relevant responses (as it is) from the provided texts for the asked question. If the question is about 
    finding an answer to previous question paper then fetch the answer only from that year solution if available.
    If there is no relevant answer/response in the provided text then just say "sorry, this information is not available in the blog".  
    Question: {question}
    """

    #prompt_template = PromptTemplate.from_template(template)
    prompt_template = template.format(question=query_text)

    # Generate a response
    #prompt = ' '.join(similar_texts)
    openai_response = client.chat.completions.create(
        model=gpt_model,
        messages = [ {"role": "assistant", "content": """you are an instructor for students preparing for design and other competitive exams and your task
    is to provide a detailed suggestion, tips, strategy, steps, ideas, and solutions for the question given to you.
    Fetch the relevant responses (as it is) from the provided texts for the asked question. If the question is about 
    finding an answer to previous question paper then fetch the answer only from that year solution if available.
    If there is no relevant answer/response in the provided text then just say 'sorry, this information is not available in the blog'""" 
                      },
                      {"role": "user", "content": query_text}
                      ],
        #prompt=prompt_template,
        #max_tokens=500
        temperature = 0 
    )

    return openai_response.choices[0].message.content

#generate_response("steps to prepare for CEED exam?", texts_list, index)

