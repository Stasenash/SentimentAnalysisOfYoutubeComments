import os
from abc import ABC
import numpy as np
from keras.layers import *
from keras import Sequential, models
from keras.datasets import imdb
from langdetect import detect

from Model import Model
from translator import Translator


class EngModel(Model, ABC):

    @staticmethod
    def _read_data():
        (training_data, training_targets), (testing_data, testing_targets) = imdb.load_data(num_words=10000)
        data = np.concatenate((training_data, testing_data), axis=0)
        targets = np.concatenate((training_targets, testing_targets), axis=0)
        return data, targets

    @staticmethod
    def _vectorize(sequences, dimension=10000):
        results = np.zeros((len(sequences), dimension))
        for i, sequence in enumerate(sequences):
            results[i, sequence] = 1
        return results

    @staticmethod
    def _prepare_train_data(data, targets, dimension=10000):
        data = EngModel._read_data(data)
        data = EngModel._vectorize(data)
        targets = np.array(targets).astype("float32")
        return data, targets

    @staticmethod
    def _split_data(data, targets):
        test_x = data[:10000]
        test_y = targets[:10000]

        train_x = data[10000:]
        train_y = targets[10000:]
        return test_x, test_y, train_x, train_y

    @staticmethod
    def _create_model():
        model = Sequential()
        # Input - Layer
        model.add(Dense(50, activation="relu", input_shape=(10000,)))
        # Hidden - Layers
        model.add(Dropout(0.3, noise_shape=None, seed=None))
        model.add(Dense(50, activation="relu"))
        model.add(Dropout(0.2, noise_shape=None, seed=None))
        model.add(Dense(50, activation="relu"))
        # Output- Layer
        model.add(Dense(1, activation="sigmoid"))
        model.summary()

        model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"]
        )
        return model

    @staticmethod
    def _train_model(model, train_x, train_y, test_x, test_y):
        model.fit(
            train_x, train_y,
            epochs=2,
            batch_size=500,
            validation_data=(test_x, test_y)
        )
        model.save("my_model")

    @staticmethod
    def _execute_teaching():
        data, targets = EngModel._read_data()
        data = EngModel._vectorize(data)
        targets = np.array(targets).astype("float32")
        train_x, train_y, test_x, test_y = EngModel._split_data(data, targets)
        EngModel._train_model(EngModel._create_model(), train_x, train_y, test_x, test_y)

    @staticmethod
    def _get_words_list(words):
        words_list = []
        imdb_dict = imdb.get_word_index()
        for word in words:
            if word in imdb_dict and imdb_dict[word] < 10000:
                words_list.append(imdb_dict[word] + 3)
            else:
                words_list.append(2)
        return words_list

    @staticmethod
    def _prepare_real_data(texts):
        comments_list = []
        for text in texts:
            words = text.split()
            comments_list.append(list(EngModel._get_words_list(words)))
        comments_list = np.array(comments_list)
        return comments_list

    @staticmethod
    def get_prediction(texts):
        if len(texts) < 1:
            raise Exception("Wrong Data")
        if not os.path.exists('my_model'):
            EngModel._execute_teaching()
        data = []
        lang = detect(texts[0])
        if lang == 'ru' or lang == 'uk' or lang == "bg":
            for text in texts:
                data.append(Translator._get_translate(text))
        else:
            data = texts
        comments_list = EngModel._prepare_real_data(data)
        new_model = models.load_model("my_model")
        data = EngModel._vectorize(comments_list)
        results = new_model.predict(data)

        predictions = []
        for result in results:
            if result > 0.70:
                predictions.append(1)
            else:
                predictions.append(0)
        return predictions