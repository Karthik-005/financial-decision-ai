import os
from bot.config import settings
from bot.chunker import chunk_text
import pdfplumber
from langchain_core.documents import Document
from typing import List
from tqdm.auto import tqdm

# Extract text, create chunks and return a list of documents. 
def ingest(pdf_path: str) -> List[Document]:
	chunk_size = settings.CHUNK_SIZE
	overlap = settings.OVERLAP
	documents = []
	
	with pdfplumber.open(pdf_path) as pdf:
		for page_no, page in tqdm(enumerate(pdf.pages), desc="Creating chunks"):
			text = page.extract_text() or ""
	
			chunks = chunk_text(text, 
							    chunk_size=chunk_size, 
							    overlap=overlap)
	
			chunk_docs = [Document(page_content=chunk, metadata={'chunk_id':i, 
																'file_path': "pdf_path", 
																'file_type': 'tax_law_2025',
																'page':page_no}) for i, chunk in enumerate(chunks)]
			
			documents.extend(chunk_docs)
			
	return documents
