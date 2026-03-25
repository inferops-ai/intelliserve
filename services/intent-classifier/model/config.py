#Declare the constants so other file can use it 
#Lable mappings 
LABEL_TO_ID = {
    "text_generation": 0,
    "summarization": 1,
    "question_answering": 2,
    "code_generation": 3,
    "translation": 4,
    "chitchat": 5
}

#Length of the labels
NUM_LABLES = len(LABEL_TO_ID)

#Tokenizer trancation length 
MAX_LENGTH = 128

#Paths for different files 
DATA_PATH = "data/intents_dataset.csv"
MODEL_OUTPUT_DIR = "models/intent-classifier"

#Model for loading 
MODEL_CHECKPOINT = "distilbert-base-uncased"