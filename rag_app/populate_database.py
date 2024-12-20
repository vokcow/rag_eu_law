from langchain_core.documents.base import Document
from langchain_community.vectorstores.chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

from  src.utils import get_bedrowck_emb_fun
import src.config as cf
'''
This script will split into chunks and load any documents in DATAPATH into
the chroma vector database, which is stored in DATABASE_PATH
'''

def assing_ids_to_chunks(chunks: list[Document]) -> list[Document]:
    ''' 
    Assigns ids to chunks as 'path/to/pdf:page_id:chunk_index' 
    '''
    last_page_id = None
    chunk_index = 0

    for c in chunks:
        source = c.metadata.get("source")
        page = c.metadata.get('page')
        page_id = f'{source}:{page}'

        if page_id == last_page_id:
            chunk_index += 1
        else:
            chunk_index = 0 
        
        c.metadata['id'] = f'{page_id}:{chunk_index}'
        last_page_id = page_id
    return chunks 


def add_to_chroma(chunks: list[Document]) -> None:
    ''' 
    Creates a chroma database if it doesn't exists and adds
    documents to it .
    '''
    # load existing database
    db = Chroma(persist_directory=cf.CHROMA_PATH, embedding_function=get_bedrowck_emb_fun())
    
    existing_docs = db.get(include=[])
    existing_ids = set(existing_docs['ids'])
    print(f"database contains {len(existing_ids)} documents")

    chuks_to_add = [c for c in chunks if c.metadata['id'] not in existing_ids]
    num_new_chuks = len(chuks_to_add)

    if num_new_chuks:
        print(f'Adding {num_new_chuks} new docs')
        db.add_documents(chuks_to_add, ids=[c.metadata['id'] for c in chuks_to_add])
        # db.persist()  uneeded since chroma 0.4.x
    else:
        print('No new documents found to be added')


def main():
    # load docs
    doc_loader = PyPDFDirectoryLoader(cf.DATASOURCE_PATH)
    docs = doc_loader.load()
    print(docs[0])

    # split them
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
                                                   chunk_overlap=80,
                                                   length_function=len,
                                                   is_separator_regex=False)
    chunks = text_splitter.split_documents(docs)

    # assig id to chunks
    chunks = assing_ids_to_chunks(chunks)

    # add chunks to chroma database if they aren't there already 
    add_to_chroma(chunks)

if __name__ == "__main__":
    main()
