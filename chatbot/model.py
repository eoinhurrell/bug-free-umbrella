""" Manages all interaction with the language model
"""
import os
import logging

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_aws import ChatBedrock
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
load_dotenv()

# This is using embeddings for similarity search not the LLM, so can use
# local embeddings, but could load Claude-compatible ones in prod
try:
    # This throws an exception in testing
    RETRIEVER = FAISS.load_local(
        os.environ["VECTORSTORE_PATH"],
        allow_dangerous_deserialization=True,  # becuase it loads a pickle file
        embeddings=OllamaEmbeddings()).as_retriever()
except RuntimeError as e:
    logger.warning(f"Vectorstore is not available: {e}")
    RETRIEVER = RunnablePassthrough()
logger.info("Loaded vectorstore")


def get_chain():
    """Get initial chain for chat"""
    if os.environ["ENV"] == "production":
        llm = ChatBedrock(model=os.environ["LLM_MODEL"])
    else:
        llm = ChatOllama(model=os.environ["LLM_MODEL"])

    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question that may reference context from the chat history, rewrite the question so that it can be understood independently without the chat history. Do not provide an answer to the question; simply reformulate it if necessary, otherwise, return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, RETRIEVER, contextualize_q_prompt
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             "You are a helpful assistant. When answering questions consider the following context:\n\n {context} "),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    chain = create_retrieval_chain(
        history_aware_retriever, question_answer_chain)

    return RunnableWithMessageHistory(
        chain,
        lambda session_id: SQLChatMessageHistory(
            session_id=session_id, connection=os.environ["DB_CONNECTION"]),
        input_messages_key="input",
        history_messages_key="history",
    )
