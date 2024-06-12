# Import necessary modules
from dotenv import load_dotenv
import os
import anthropic
import pprint
import openai
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

def generate_response(messages, model):
    # Initialize spinner to show while waiting for response
    spinner = Halo(text='Loading...', spinner='dots')
    spinner.start()
    
    if model == "claude3":
	    # Create an Anthropic using the provided API key
	    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_KEY"))
	    # Send a completion request to the Claude model
	    response = client.messages.create(
	        model=os.getenv("CLAUDE_MODEL_NAME"),
	        max_tokens=1024,
	        messages=[
	        	{"role": "user", "content": messages}
	    	]
	    )
    if model == "gpt4":
	    # Create an OpenAI GPT client
	    gpt_client = openai.Client(api_key=os.getenv("OPENAI_KEY"))
	    # Send a completion request to the GPT model
	    response = gpt_client.chat.completions.create(
	        model=os.getenv("OPENAI_MODEL_NAME"), 
	        messages=[
	        	{"role": "user", "content": messages}
	    	]
	    )
	    
    # Stop the spinner after getting response
    spinner.stop()
    # Return the response
    return response

def main():
	embedding_function = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_KEY"), model_name=os.getenv("EMBEDDING_MODEL"))
	chroma_client = chromadb.PersistentClient()
	collection = chroma_client.get_collection(name="knowledgment", embedding_function=embedding_function)
	
	# Get user input
	input_text = input("\nPlease provide the file in which the feature engineering is stored : \n")
	featurePrompts = read_text_file(input_text)
	
	model = input("\nPlease specify the model to use for diagnostics :  claude3 or gpt4\n")
	
	results = collection.query(query_texts=[featurePrompts],n_results=18)
	knowledge_base = []
	for res in results['documents'][0]:
		knowledge_base.append(res)
	knowledge_base_str = ", ".join(knowledge_base)
	
	starterPrompt = read_text_file('starterPrompt.txt')
	diagnosisGuidance = f"Please take this data on electrocardiography(ECG) professional knowledgment and refer to it when I ask you about the ECG: {knowledge_base}."+read_text_file('diagnosisGuidance.txt')
	formatPrompts = read_text_file('formatPrompts.txt')
	
	if model == "claude3":
		# Prepare the prompt for the Claude model
		messages=  f"{anthropic.HUMAN_PROMPT}{starterPrompt}{diagnosisGuidance} This is the ECG data to be diagnosed:{ featurePrompts} {formatPrompts}{anthropic.AI_PROMPT} "
	if model == "gpt4":
		messages=  f"{starterPrompt}{diagnosisGuidance} This is the ECG data to be diagnosed: {featurePrompts}{formatPrompts}"

	# Generate a response from the Claude model
	response = generate_response(messages, model)
	
	# Print the model's response
	if model == "claude3":
		print(f"\nClaude: {response.content[0].text}")
	if model == "gpt4":
		print(f"\nGPT:{response.choices[0].message.content}") 

# Run the main function if the script is run directly
if __name__ == "__main__":
	load_env_file("API-Key.env")
	main()
