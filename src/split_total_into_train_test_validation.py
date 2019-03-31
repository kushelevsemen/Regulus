#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.read_csv('../csv/total.csv', index_col=0)
print(data.shape)

y = data.y
X = data.x

# train-test-validation 8:1:1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
X_test, X_val, y_test, y_val = train_test_split(X_test, y_test, test_size=0.5, random_state=1)

train = {}
train['x'] = X_train
train['y'] = y_train

test = {}
test['x'] = X_test
test['y'] = y_test

val = {}
val['x'] = X_val
val['y'] = y_val

df = pd.DataFrame(train, index=None)
print("Train shape:", df.shape)
with open('../csv/train.csv', mode='w', encoding='utf-8') as f_csv:
    df.to_csv(f_csv)

df = pd.DataFrame(test, index=None)
print("Test shape:", df.shape)
with open('../csv/test.csv', mode='w', encoding='utf-8') as f_csv:
    df.to_csv(f_csv)

df = pd.DataFrame(val, index=None)
print("Validation shape:", df.shape)
with open('../csv/validation.csv', mode='w', encoding='utf-8') as f_csv:
    df.to_csv(f_csv)