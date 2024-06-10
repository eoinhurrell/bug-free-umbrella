from chatbot import start_chat, invoke, stream


def test_start_chat():
    chat = start_chat()
    assert chat['id'] == chat['config']['configurable']['session_id']


def test_invoke():
    # invoke(message, chat):
    pass


def test_stream():
    # stream(message, chat)
    pass
