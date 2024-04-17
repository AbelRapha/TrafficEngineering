from rag_config import invoke_chain
import streamlit as st 
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title = 'Bot EngTrafego', page_icon = '👷‍♂️')

st.title('Bot EngTráfego 👷‍♂️')

st.write('## Clique no player abaixo para ouvir o áudio livro completo')

audio_file = open("./ingest/docs/audiobook.mp3", "rb")
audio_bytes = audio_file.read()

st.audio(audio_bytes, format="audio/mp3")

st.write("## ChatBot :robot_face:")
st.info('Escreva sua pergunta abaixo e converse com o capítulo 2 sobre Polos Geradores de Tráfego')

# query = st.text_input('Pergunta', 'Ex: Faça um resumo sobre o capítulo inteiro de forma coesa utilizando até 5 mil palavras')
# if st.button('Gerar Resposta'):
#     with st.spinner('Gerando resposta, aguarde...'):
#         response = invoke_chain(query)
#         if response:
#             st.write(response)

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Olá, como posso ajudar?"),
    ]

    
# conversation
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Digite sua pergunta aqui...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(invoke_chain(user_query))

    st.session_state.chat_history.append(AIMessage(content=response))

# Button to clear chat history

if st.button('Limpar histórico'):
    del st.session_state.chat_history
    st.rerun()