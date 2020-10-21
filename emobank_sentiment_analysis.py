import pandas as pd 
from collections import namedtuple

emo_df = pd.read_csv("EmoBank/corpus/emobank.csv", index_col=0)
print(emo_df.shape)

Emotion = namedtuple('Emotion', ['V', 'A', 'D'])
# V, A and D represent Valence (negative vs. positive), 
# Arousal (calm vs. excited), and Dominance (being controlled vs. being in control)

train_data = []
test_data = []
for ind, row in emo_df.iterrows(): 
    label = Emotion(row['V'], row['A'], row['D'])
    datapoint = (row['text'], label)
    if (row['split'] == 'train'): train_data.append(datapoint)
    else: test_data.append(datapoint)

print(len(test_data))
print(len(train_data))

