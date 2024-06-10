import uuid
import logging

from chatbot import model

logger = logging.getLogger(__name__)


def start_chat():
    session_id = f"{uuid.uuid4()}"
    chain = model.get_chain()
    config = {"configurable": {"session_id": f"{session_id}"}}

    return {
        'id': session_id,
        'chain': chain,
        'config': config
    }


def invoke(message, chat):
    question = {"input": message}
    resp = chat["chain"].invoke(question, config=chat["config"])
    return resp


def stream(message, chat):
    question = {"input": message}
    for chunk in chat['chain'].stream(question, config=chat["config"]):
        if 'answer' in chunk:
            yield (chunk['answer'])
