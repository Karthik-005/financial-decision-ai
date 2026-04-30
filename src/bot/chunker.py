
from typing import List

def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:	
	chunks = []
	text_len = len(text)
	
	for start in range(0, text_len, chunk_size - overlap):
		
		end = min(start+chunk_size, text_len)
				
		chunks.append(text[start:end])
	
	return chunks
		
