# Import necessary modules
from dotenv import load_dotenv
import os
import anthropic
import pprint
from halo import Halo
import tiktoken
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from pdfminer.high_level import extract_text

# Initialize pretty printer for formatted printing
pp = pprint.PrettyPrinter(indent=4)

def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None

def load_env_file(file_path):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

def create_chunks(text, n, tokenizer):
    tokens = tokenizer.encode(text)
    i = 0
    print("wait for chunks")
    while i < len(tokens):
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith("\n"):
                break
            j -= 1
        yield tokens[i:j]  # Yield the chunk
        i = j  # Move to the next position
    print("chunks done")

def main():
	# Extract text from PDF file
	knowledge_text = extract_text('knowledgment.pdf')

	# Initialise tokenizer
	tokenizer = tiktoken.get_encoding("cl100k_base")
	
	print("Start to makde chunks")
	# Create chunks and decode them
	chunks = create_chunks(knowledge_text, 1000, tokenizer)
	text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
	
	# Connect to Chroma database
	chroma_client = chromadb.PersistentClient()

	# Initialize embedding function
	embedding_function = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_KEY"), model_name=os.getenv("EMBEDDING_MODEL"))

	# Create or retrieve collection
	collection = chroma_client.create_collection(name="knowledgment", embedding_function=embedding_function)

	print("wait for add chunks to collection")
	# Add chunks to collection
	for index, text_chunk in enumerate(text_chunks):
		collection.add(documents=[text_chunk], ids=[f"text_{index}"])
	print("collection done")

# Run the main function if the script is run directly
if __name__ == "__main__":
	load_env_file("API-Key.env")
	main()
