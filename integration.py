"""Integration test for chatbot"""
import chatbot

chat = chatbot.start_chat()
# to add a message, invoke the chatbot with the message
resp = chatbot.invoke(
    """Hi! Can you tell me about the hatter? Tell me three things about him""",
    chat
)
print(resp["answer"])

print("=========")

for chunk in chatbot.stream("Tell me more", chat):
    print(chunk, end='')
