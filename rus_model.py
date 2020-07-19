import os
import random
from abc import ABC

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
from keras import models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tqdm import tqdm

from Model import Model


class RusModel(Model, ABC):
    @staticmethod
    def _read_data():
        data = pd.read_csv('GoodFile1.csv', sep=';')

        data["review"] = data["Review"]
        data["type"] = data["review_type"]

        data = data[["review", "type"]]
        return data


    @staticmethod
    def _prepare_train_data(data):
        good_reviews = data[data.type == "good"]
        bad_reviews = data[data.type == "bad"]

        good_reviews = good_reviews.sample(n=len(bad_reviews), random_state=random.seed())
        bad_reviews = bad_reviews
        data = good_reviews.append(bad_reviews).reset_index(drop=True)
        return data

    @staticmethod
    def _split_data(data):
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

        type_one_hot = OneHotEncoder(sparse=False).fit_transform(
            data.type.to_numpy().reshape(-1, 1)
        )

        train_reviews, test_reviews, train_y, test_y = \
            train_test_split(
                data.review,
                type_one_hot,
                test_size=.1,
                random_state=random.seed()
            )

        train_x = []
        for r in tqdm(train_reviews):
            emb = embed(r)
            review_emb = tf.reshape(emb, [-1]).numpy()
            train_x.append(review_emb)

        train_x = np.array(train_x)

        test_x = []
        for r in tqdm(test_reviews):
            emb = embed(r)
            review_emb = tf.reshape(emb, [-1]).numpy()
            test_x.append(review_emb)

        test_x = np.array(test_x)
        return train_x, train_y, test_x, test_y



    @staticmethod
    def _create_model(train_x):
        model = Sequential()

        model.add(
            Dense(
                units=256,
                input_shape=(train_x.shape[1],),
                activation='relu'
            )
        )
        model.add(
            Dropout(rate=0.5)
        )

        model.add(
            Dense(
                units=128,
                activation='relu'
            )
        )
        model.add(
            Dropout(rate=0.5)
        )

        model.add(Dense(2, activation='softmax'))
        model.compile(
            loss='categorical_crossentropy',
            optimizer=tf.keras.optimizers.Adam(0.001),
            metrics=['accuracy']
        )
        return model

    @staticmethod
    def _train_model(model, train_x, train_y, test_x, test_y):
        history = model.fit(
            train_x, train_y,
            epochs=10,
            batch_size=16,
            validation_split=0.1,
            verbose=1,
            shuffle=True
        )

        model.evaluate(test_x, test_y)
        model.save_weights("model1.h5")
        model.save("my_rus_model")

    @staticmethod
    def _execute_teaching():
        data = RusModel._read_data()
        data = RusModel._prepare_train_data(data)
        train_x, train_y, test_x, test_y = RusModel._split_data(data)
        model = RusModel._create_model(train_x)
        RusModel._train_model(model, train_x, train_y, test_x, test_y)

    @staticmethod
    def get_prediction(texts):
        if len(texts) < 1:
            raise Exception("Wrong Data")
        if not os.path.exists('my_rus_model') or not os.path.exists('model1.h5'):
            RusModel._execute_teaching()
        embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")
        model = models.load_model('my_rus_model')
        model.load_weights('model1.h5')
        texts = embed(texts)
        results = model.predict(np.array(texts))

        predictions = []
        for result in results:
            if result[0] > 0.30:
                predictions.append(0)
            else:
                predictions.append(1)
        return predictions
