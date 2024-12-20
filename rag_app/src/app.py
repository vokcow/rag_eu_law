import gradio as gr 
from src.run_query import run_query

def get_answer(message: str, history: dict[str, str]) -> str:
    # nothing is done with history, we should consider saving it in a database
    query_response =  run_query(message)
    text, sources = query_response.response_msg, query_response.sources

    # Append the sources to the message
    should_add_title = True
    for s in sources:
        id_, score = s 
        id_ = id_.strip('data/input_data/')
        page = id_.split(":")[1]
        language = id_.split("_")[-2]
        law_type = id_.split("_")[0]
        document = "_".join(id_.split("_")[1:-2])
        if should_add_title:
            text += f"\n\n\n\nSources📚📚📚\n"
        text += f"\n\n[EU AI act page {page}](https://eur-lex.europa.eu/legal-content/{language}/TXT/PDF/?uri={law_type}:{document}#page={page})\t\t-- Score={score:.2f}--\n"
        should_add_title = False

    return text 

get_answer("What does the the EU AI regulation say about AI systems for biometric identification", {})

demo = gr.ChatInterface(
        fn=get_answer,
        description='### Welcome to the EU AI chatbot 🇪🇺🤖🧑‍⚖️ Ask any question about the new European AI law\n 🇪🇸 Bienvenido al chatbot sobre la ley europea de IA. Pregunta cualquier cosa sobre dicha ley',
        type='messages')

demo.launch(
    server_port=7860,
    server_name="0.0.0.0"
)
# def handle(event, context):
#     return {
#         "statusCode": 200,
#         "body": {"message": "Hello from Lambda!"},
#     }