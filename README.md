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

# Technical planning

owner: Eoin Hurrell
reviewers: WorkHuman interview panel
team: Eoin Hurrell

## Objectives / Scopes
This is planning for the module and eventual service that will provide the RAG-based chatbot functionality to other services.

## High-level non-functional requirements
This module will provide the interface to a RAG chatbot, allowing people to chat with a history that is maintained and references documentation.

This service will provide access to chat threads, i.e. past or ongoing messages between a user and the system. It will be possible to look up past conversations, send a message to a thread, and get a response. Other functionality like deleting threads could be added.

## API

GET /chat - the primary exposed endpoint, it manages the state of current chats and updates 

POST /chat - send a message, to get a reply from the model. Should support websockets to stream messages too.

## Security
- Limit access to services that have been whitelisted or are on the VPC. Possibly RBAC too, if needed (i.e. if PII is present in the RAG)

## Storage
The service will use SQLAlchemy so it can interface with most SQL databases, I'd say use Postgres, as it is a good sane default and there is the possibility of using pg-vector to store the embeddings for the RAG, centralising storage rather than having multiple databases.

## Queries we should be able to handle

Streaming should be well-supported as LLMs can be slow to generate long responses otherwise.

## 3rd parties

AWS Bedrock is the big 3rd party connection, which uses Claude3. It is possible an open source model might perform better for our purposes, or that Claude3 could become inaccessible, but in both cases langchain has good support for easily switching out the dependency.

## Analytics

We should measure chat activity, both in terms of number of chats and frequency, but also how terse people are being with the chatbot, in case maybe they are not enjoying chat as an interface.

## Testing strategy

- Build a set of evals - Chat messages with known good answers we want to see or bad answers we want to avoid - that we can measure the performance of any change against.
## Questions / Risks

This is a general RAG with no special tailoring to its task, yet.
