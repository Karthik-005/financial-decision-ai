from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

sys_message = """You are a financial decision assistant. Based on user's query and the given context answer the query.
If the provided context is not enough to asnwer the user's query then just say "Insufficient information". Do not hallucinate information.
"""

human_message = """Context: 
{context}

query:
{query}
"""

CONDENSE_PROMPT_TEMPLATE = PromptTemplate.from_template(
    """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone search query. Do not answer the question, just reformulate it.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone query:"""
)



CHAT_TEMPLATE = ChatPromptTemplate([
	('system', sys_message),
	MessagesPlaceholder(variable_name="chat_history"),
	('human', human_message)
])
