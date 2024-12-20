import os 
from src.utils import get_bedrowck_emb_fun

# define the paths
DATASOURCE_PATH = "data/input_data"
CHROMA_PATH = "data/vector_db"
CHROMA_INSTANCE = None 

# define chat model id
# BEDROCK_MODEL_ID = 'meta.llama3-8b-instruct-v1:0'
BEDROCK_MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'

# define the default prompt
PROMPT_TEMPLATE = ''' 
You are a lawyer specialised in EU law. Your role is to answer questions about EU Artifial Intelligence law.
Avoid using technical words. Use layman terms. Give concise answers. Describe any reasoning steps.
Answer in the language you are asked in.
Base your answer on the following context only:

{context}

----
Question: {question}
'''

# define the runtime flag
IS_IMAGE_RUNTIME = os.environ.get('IS_IMAGE_RUNTIME', False)


# fuction that returns the chroma instance depending on the runtime
def get_chroma_db():
    global CHROMA_INSTANCE
    if not CHROMA_INSTANCE:
        if IS_IMAGE_RUNTIME:
            copy_chroma_to_tmp()
        
        CHROMA_INSTANCE = Chroma(persist_directory=get_runtime_chroma_path(),
                                 embedding_function=get_bedrowck_emb_fun())
        
# function that returns the runtime chroma path
def get_runtime_chroma_path() -> str:
    if IS_IMAGE_RUNTIME:
        return "/tmp/vector_db"
    else:
        return CHROMA_PATH

# function that copies the chroma database to the only writeable directory in lambda
def copy_chroma_to_tmp() -> None:
    tmp_chroma = '/tmp/vector_db'
    if not os.path.exists(tmp_chroma):
        os.makedirs(tmp_chroma)

    tmp_contents = os.listdir(tmp_chroma)
    if not len(tmp_contents):
        print("Copying chroma database to /tmp")
        os.system(f"cp -r {CHROMA_PATH}/* {tmp_chroma}")
    else:
        print(f'Chroma path already exists in /tmp: {tmp_contents}')
