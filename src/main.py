import os
# import openai
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from langchain_community.vectorstores.chroma import Chroma



TENANT= ""
CLIENT_ID = ""
CLIENT_SECRET= ""
credential = ClientSecretCredential(TENANT,CLIENT_ID,CLIENT_SECRET)
VAULT_URL= ""
client = SecretClient(vault_url=VAULT_URL, credential=credential)
openai_key = client.get_secret("GenAIBIMInternalCapabilityOpenAIKey")

os.environ["OPENAI_API_TYPE"] = ""
os.environ["AZURE_OPENAI_ENDPOINT"] = ""
os.environ["AZURE_OPENAI_API_KEY"] = openai_key.value
os.environ["AZURE_OPENAI_API_VERSION"] = "2023-07-01-preview"


# initialize the LLM & Embeddings
llm = AzureChatOpenAI(
            temperature=0,
            deployment_name="gpt-4",
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
            streaming=True,
            model_name='gpt-4'
        )
embeddings = AzureOpenAIEmbeddings(deployment="embeddings", chunk_size=1)

# set prompt template
prompt_template_database = """Use the following pieces of context to answer the question at the end.
If you are able to answer the question then provide the site path for more details regarding the answer. If you are unable to answer the question then don't add the site path to your answer at the end.
site_path: {site_path}
Strictly follow these steps to answer the questions:
1. Read the question properly and find the important keywords in the question for answering.
2. Figure out smartly the questions preposition and generate the answer based entirely on question's keywords then contextualise it to the users need
3. Give answer with word limit greater than 200 words.
4. Give any key value pair in statements along with statistiscal data. These key value pairs will contain column and row from which they were taken so clearly understand them for better answer creation.
    1. Do not give any code and comments for the kay value answers.
5. Do not return an answer without the site path for reference documents unless you are unable to answer the question.
6. Do not try to make up an answer if you can't find any information regarding it.
7. If you are unable to find the answer then find the closest answer possible. Only when you are not able to find the closest answer as well say unable to answer. Don't try to make up an answer in this case.


{context}
Question: {question}
Answer:"""

prompt_data = PromptTemplate(template=prompt_template_database, input_variables=["context", "question", "site_path"])
llm_chain_data = LLMChain(llm=llm, prompt=prompt_data)
# llm_chain1 = ( prompt_data | llm )

# Load database
db = Chroma(persist_directory=Database_Path, embedding_function=embeddings)
site_map={}



def generate_response(question):

    similar_docs = db.similarity_search(question, k=10)
    context = " ".join([doc.page_content for doc in similar_docs])
    if len(similar_docs)==0:
        return context
    file_path = similar_docs[0].metadata['file_path']
    query_llm = llm_chain_data
    response = query_llm.run({"context": context, "question": question, "site_path": file_path})
    return response







#LLMChain for CodeGenerator

prompt_template_coding_assistant = """ You are a coding assistant.
Answer the Question: {question}
Strictly follow these steps to answer the questions:
1. Read the question properly and find the important keywords in the question for answering.
2. Figure out smartly the questions preposition and generate the answer based entirely on question's keywords then contextualise it to the users need
3. Give a brief context of the approach and working used in the code before the start of the code.
4. Provide name of every package and module imported in the code.
5. Every line of code must have comments that clearly explains the working of that line.
6. Provide an input ouput example appropriate for this code.
7. Naming of variables should follow proper convention.
8. Properly state the algorithm names used in the code at the end of the answer for reference.

Answer:"""

prompt_code = PromptTemplate(template=prompt_template_coding_assistant, input_variables=["question"])
llm_chain_code = LLMChain(llm=llm, prompt=prompt_code)
# llm_chain1 = ( prompt_code | llm )

def generate_code(question):
    query_llm = llm_chain_code
    response = query_llm.run({ "question": question })
    return response

