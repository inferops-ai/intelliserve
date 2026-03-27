import config
import numpy as np
from dataset import get_datasets, tokenizer
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, EvalPrediction
from sklearn.metrics import accuracy_score, f1_score

train_ds, eval_ds = get_datasets()

model = AutoModelForSequenceClassification.from_pretrained(config.MODEL_CHECKPOINT, num_labels=config.NUM_LABELS, id2label=config.ID_TO_LABEL, label2id=config.LABEL_TO_ID)
training_args = TrainingArguments(
    output_dir = config.MODEL_OUTPUT_DIR,   #output dir from model checkpoint
    num_train_epochs = 4,                   #total number of training epoches
    per_device_train_batch_size = 16,       #how many example the model sees per gradient
    per_device_eval_batch_size = 16,        #how many example the model sees per gradient
    learning_rate = 2e-5,                   #how aggressively the model weights are updated
    eval_strategy = "epoch",                #when to run evaluation during training
    save_strategy = "epoch",                #save checkpoint to disk
    load_best_model_at_end = True,          #restores the checkpoint that had the best evaluation metric
    metric_for_best_model = "f1",           #metric to use when deciding which checkpoint is best
)

def compute_metrics(eval_pred: EvalPrediction):
    predictions = eval_pred.predictions[0] if isinstance(eval_pred.predictions, tuple) else eval_pred.predictions
    predictions = np.argmax(predictions, axis=1)
    labels = eval_pred.label_ids
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average="macro")
    return {
        "accuracy_score":acc,
        "f1":f1
    }
    

trainer = Trainer(
    model = model,                      # the instantiated Transformers model to be trained
    args = training_args,               # training arguments, defined above
    train_dataset = train_ds,           # training dataset - needs to be a Dataset object
    eval_dataset = eval_ds,             # evaluation dataset
    compute_metrics = compute_metrics   #function you write that takes raw predictions and returns accuracy and F1
)

trainer.train()
trainer.save_model(config.MODEL_OUTPUT_DIR)
tokenizer.save_pretrained(config.MODEL_OUTPUT_DIR)

print("Starting evaluation ...")
result_eval = trainer.evaluate()
print(result_eval)


    

