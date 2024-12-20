from setuptools import setup 

setup(
    name="aws_rag_tutorial",
    version="1.0",
    description="a simple tutorial implementing rag model and deploying it to AWS lambda",
    author='Angel Victor Juanco Muller',
    author_email='vokyjuanko@gmail.com',
    packages=['src'],
    install_requires=['langchain==0.3.11',  # llm library 
                      'langchain-community==0.3.11',  # more llm  stuff
                      'langchain-aws', # yet more llm stuff
                      'chromadb==0.5.23',  # vector database
                      'pypdf==5.1.0',  # to read pdf
                      'pytest==8.3.4',  # testing
                      'boto3==1.35.81',  # AWS Pyhon SDK
                      'awscli==1.36.22',  # AWS client
                      'fastapi==0.115.6',  # to make the api
                      'uvicorn==0.32.1',  # server to test the API,
                      'gradio==5.9.0'
                      ]
)
