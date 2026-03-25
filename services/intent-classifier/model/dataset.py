import config
import pandas as pd

df = pd.read_csv(config.DATA_PATH)

print(df.head)