import random
import json
import pickle
import numpy as np

import nltk

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer  # Reduces the word to stem.

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())  # Reads the intents json file.

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:  # ['intents'] is used to access the key 'intents' (line 1) in the json file.
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)  # Splits a phrase into individual words.
        words.extend(word_list)
        documents.append((word_list, intent['tag']))  # To know the 'tag' of the word_list appended. E.g. 'Hi, hello' belongs to 'greetings'.
        if intent['tag'] not in classes:
            classes.append(
                intent['tag'])  # Appending tags to the list which stores the names of classes i.e. 'classes'.

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))  # 'set' eliminates duplicates and sorted turns it back into a sorted list.

classes = sorted(set(classes))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)  # Copying the list, not type-casting.
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()  # A Sequential model is appropriate for a plain stack of layers where each layer has exactly one input tensor and one output tensor.
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))  # Dropping out some random neurons. Dropout prevents over-fitting.
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),
                activation='softmax'))  # Softmax function scales the output such that they all add up to 1. So we'll have sort of percentage of the likelihood of each output.

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)  # Stochastic Gradient Descent
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
print("Done")
