
from typing import List

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:	
	chunks = []
	text_len = len(text)
	
	for start in range(0, text_len, chunk_size - overlap):
		
		if start + chunk_size <= text_len:
			end = start + chunk_size
			
		else:
			end = text_len
				
		chunks.append(text[start:end])
	
	return chunks
		
