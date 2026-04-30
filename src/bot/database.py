from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from bot.config import settings
from bot.ingestion import ingest
from pathlib import Path
import time
from tqdm.auto import tqdm

def initiate_vector_db(docs: List[Document]) -> Chroma:
	
	# Fetch huggingface and vector_db configs.
	vector_db_path = settings.VECTOR_DB['path']
	collection_name = settings.VECTOR_DB['collection_name']
	docs_batch_size = settings.VECTOR_DB['docs_batch_size']
	model_name = settings.EMBEDDING_MODEL
	hf_api_key = settings.HF_TOKEN
			
	model = HuggingFaceEndpointEmbeddings(model=model_name,
										  huggingfacehub_api_token=hf_api_key)
	
	# If the directory is not created the create it.
	if not os.path.exists(vector_db_path):
		Path(vector_db_path).resolve().mkdir(parents=True, exist_ok=True)
	
	vector_db = Chroma(embedding_function=model,
					   persist_directory=vector_db_path,
					   collection_name=collection_name)
	
	# If the directory has already been created, check if it has the documents loaded. If not, load them batch-wise.
	n_docs = len(docs)
	if vector_db._collection.count() == 0:
		for start in tqdm(range(0, n_docs, docs_batch_size), desc="Adding documents batch-wise into the vector_db"):
			
			end = min(start+docs_batch_size, n_docs)
			batch = docs[start:end]
			
			# Make multiple attempts if the first upload fails.
			for attempt in range(3):
				try:
					vector_db.add_documents(batch)
					break
				except Exception as e:
					if attempt < 2:
						print(f"API call failed, \nError:{e} \nretrying in 5 sec...")
						time.sleep(5)
					else:
						print(f"API call permantly failed, couldn't upload batch: {(start+docs_batch_size+1)//docs_batch_size}")
	

	return vector_db	

if __name__ == "__main__":
	docs = ingest(settings.RAW_DATA_PATH)
	vector_db = initiate_vector_db(docs)
	
	print(f"No. of chunks: {len(docs)} \nNo. of documents: {vector_db._collection.count()}")	
