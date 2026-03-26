import config
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer 

from sklearn.model_selection import train_test_split

df = pd.read_csv(config.DATA_PATH)

df_lable = df['label']
df = df.drop(columns='label')
df['labels'] = df_lable.map(config.LABEL_TO_ID)

train_df, eval_df = train_test_split(df, test_size=0.2, shuffle=True, random_state=42)

train_ds = Dataset.from_pandas(train_df)
eval_ds = Dataset.from_pandas(eval_df)

tokenizer = AutoTokenizer.from_pretrained(config.MODEL_CHECKPOINT)

def tokenize_function(data_set, col_name='text'):
    return tokenizer(
        data_set[col_name],
        padding='max_length',
        truncation=True,
        max_length=config.MAX_LENGTH
    )
    
tokenized_trainDS = train_ds.map(
    tokenize_function,
    batched=True,
    remove_columns=['text']
)
tokenized_evalDS = eval_ds.map(
    tokenize_function,
    batched=True,
    remove_columns=['text']
)

def get_datasets():
    return tokenized_trainDS, tokenized_evalDS



