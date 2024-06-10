"""Build the vectorstore to use for the RAG"""
#!/usr/bin/env python3

import sys
import os
import logging

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


logger.info("Starting to build vectorstore")
folder = sys.argv[1]
loader = DirectoryLoader(folder, glob="**/*.txt")
documents = loader.load()

text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=1000,
    chunk_overlap=200,
)
docs = text_splitter.split_documents(documents)
vectorstore = FAISS.from_documents(docs, embedding=OllamaEmbeddings())
vectorstore.save_local(os.environ["VECTORSTORE_PATH"])
logger.info("Saved vectorstore")
