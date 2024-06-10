from langchain_core.runnables.history import RunnableWithMessageHistory

from chatbot import model


def test_get_chain():
    llm = model.get_chain()
    assert isinstance(llm, RunnableWithMessageHistory)
