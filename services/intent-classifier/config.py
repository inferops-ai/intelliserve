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

ID_TO_LABEL = {
    0: "text_generation",
    1: "summarization",
    2: "question_answering",
    3: "code_generation",
    4: "translation",
    5: "chitchat"
}

#Length of the labels
NUM_LABELS = len(LABEL_TO_ID)

#Tokenizer trancation length 
MAX_LENGTH = 128

#Paths for different files 
DATA_PATH = "data/intents_dataset.csv"
MODEL_OUTPUT_DIR = "/intent_classifier/models/intent-classifier"
#Local path
MODEL_PATH_LOCAL = "models/intent-classifier"
LOGGING_DIR = "logs"

#Model for loading 
MODEL_CHECKPOINT = "distilbert-base-uncased"