import os
import yaml
from dotenv import load_dotenv
from pathlib import Path
	
class Settings():
	def __init__(self):
		ROOT_DIR = Path(__file__).resolve().parents[2]
		
		# Load environmental variables
		try:
			load_dotenv()
			self.HF_TOKEN = os.getenv('HF_TOKEN')
			
		except Exception as e:
			print(f"Couldn't load .env file. \nError: {e}")
		
		
		# Load the config.yaml file
		with open(ROOT_DIR / 'config.yaml', "r") as f:
			config = yaml.safe_load(f)
		
		self.RAW_DATA_PATH = ROOT_DIR / config['data']['raw_data_path']
		self.VECTOR_DB = {'path': ROOT_DIR / config['data']['vector_db']['path'],
						  'collection_name': config['data']['vector_db']['collection_name'],
						  'docs_batch_size': config['data']['vector_db']['docs_batch_size']}
		self.CHUNK_SIZE = config['data']['chunks']['chunk_size']
		self.OVERLAP = config['data']['chunks']['overlap']
		self.EMBEDDING_MODEL = config['huggingface']['embedding_model']
		
settings = Settings()
		
			
