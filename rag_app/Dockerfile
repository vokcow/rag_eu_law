FROM public.ecr.aws/lambda/python:3.10

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Needs this for chroma
RUN  yum install -y \
    build-essential \
    gcc \
    g++ 

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt ./requirements.txt

# Install dependencies 
RUN pip install -r requirements.txt --upgrade 

# Copy all files
COPY src/*.py  ./src/
COPY data ./data
COPY data/vector_db/ ./data/vector_db/


# to find out if we are inside the image
ENV IS_IMAGE_RUNTIME=True

# define the ports
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

# set
CMD ["python", "src/app.py"]