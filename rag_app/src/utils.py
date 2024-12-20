from langchain_community.embeddings.bedrock import BedrockEmbeddings

# define the get embedding function
def get_bedrowck_emb_fun():
    return BedrockEmbeddings(credentials_profile_name="default",
                             region_name='eu-west-2', 
                             model_id='amazon.titan-embed-text-v2:0')
