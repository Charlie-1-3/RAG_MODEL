import os
# import openai
from langchain.chains import LLMChain
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient



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

# set prompt template
prompt_template = """Use the following pieces of context to answer the question at the end.
If you are able to answer the question then provide the file path for more details regarding the answer. If you are unable to answer the question then don't add the file path to your answer at the end.
file_path: {file_path}
Strictly follow these steps to answer the questions:
1. Read the question properly and find the important keywords in the question for answering.
2. Figure out smartly the questions preposition and generate the answer based entirely on question's keywords then contextualise it to the users need
3. Give answer with word limit greater than 200 words.
4. Give any key value pair in statements along with statistiscal data. These key value pairs will contain column and row from which they were taken so clearly understand them for better answer creation.
    1. Do not give any code and comments for the kay value answers.
5. Do not return an answer without the file path for reference documents unless you are unable to answer the question.
6. Do not try to make up an answer if you can't find any information regarding it.
7. Use this piece of code to extract the folder name from the file path and return it as well at the end after the file path. Code Snipet: os.path.basename(os.path.dirname(file_path))
8. If you are unable to find the answer then find the closest answer possible. Only when you are not able to find the closest answer as well say unable to answer. Don't try to make up an answer in this case.


{context}
Question: {question}
Answer:"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "file_path"])



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
llm_chain = LLMChain(llm=llm, prompt=prompt)
llm_chain1 = ( prompt | llm )
