# Chatbot - takehome

This is a module to implement a RAG chatbot, for use in an API. 

## Configuration
This chatbot uses an env file for configuration. All options are set, and can be configured. 

I have set up the code to use a locally served model when the ENV variable is not 'production'. This is for ease of use and testing as I have not set up Bedrock for personal use. The local server is Ollama, using llama2.

## Files

- `.env` - Configuration
- `build_vectorstore.py` - Create the initial vectorstore. This data pipeline is very simple, it creates a local vectorestore by ingesting the text data in a folder and generating embeddings from it.
- `integration.py` - the integration test, a full run through of a chat. Can add further chat messages as needed.
- `chatbot/__init__.py` - core chatbot logic
- `chatbot/model.py` - langchain chain logic


## Testing - How

    python -m pytest

Pytest will run all the unit-tests, but only small unit-tests are in place, as much of the logic is essentially passing through to the LLM, relying on langchain's methods rather than my own code.

I built a RAG using [Alice in Wonderland](https://www.gutenberg.org/cache/epub/11/pg11.txt) as a text, and used the integration test as the main point of testing. 

## Deployment / Usage

Right now there's no functionality to deploy, but this can be install with 

    pip install -e .

and then `chatbot` can be imported.

The interface should work cleanly with a flask or aio API

## Possible improvements

Further testing would be good, the dependence on an LLM makes testing difficult, but with more time I would have mocked this and written more unit tests.

The retrieval portion of the RAG has had no special attention. Results are pulled based on similarity rather than relevance, so the option to rerank is there and a lot could be done to improve quality using that.

No prompt tuning has been done.
