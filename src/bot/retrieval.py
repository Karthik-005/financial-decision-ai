from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import get_buffer_string
from bot.config import settings
from bot.database import initiate_vector_db
from bot.prompts import CHAT_TEMPLATE, CONDENSE_PROMPT_TEMPLATE


class ChatBot():
	def __init__(self):
		# Initialize vector_db
		self.vector_db = initiate_vector_db()
		
		# Initialize llm object and chat object
		llm = HuggingFaceEndpoint(repo_id=settings.LLM)
		self.model = ChatHuggingFace(llm=llm)
		
		self.history = InMemoryChatMessageHistory()
	
	def retrieve_context(self, query):
		# Do a similarity search
		docs = self.vector_db.similarity_search(query=query)
		docs = [doc.page_content for doc in docs]
		
		# Create a prompt using the context and the query.
		context = '\n'.join(docs)
		final_prompt = CHAT_TEMPLATE.invoke({'chat_history':self.history.messages, 
							  				 'context':context, 
							  				 'query':query})
		return final_prompt
	
	def ask(self, query):
		if len(self.history.messages) != 0:
			f_history = get_buffer_string(self.history.messages)
			
			condenser_prompt = CONDENSE_PROMPT_TEMPLATE.invoke({'chat_history':f_history,
																'question':query})
				
			search_str = self.model.invoke(condense_prompt).content.strip()
			
		else:
			search_str = query
		
		
		final_prompt = self.retrieve_context(search_str)
		ans = self.model.invoke(final_prompt)
		
		return ans
			

