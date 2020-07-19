import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

from dostoevsky_model import DostoevskyModel
from eng_model import EngModel
from rus_model import RusModel


class TestNeurons:
    @staticmethod
    def _read_data():
        data = pd.read_excel("comments.xlsx")
        data = data.sample(frac=1).reset_index(drop=True)
        return data

    @staticmethod
    def _prepare_test_data(data):
        comments = np.array(data['comment'])
        types = np.array(data['type'])
        return comments, types

    @staticmethod
    def _get_predictions(comments):
        rus_answ = RusModel.get_prediction(comments)
        en_answ = EngModel.get_prediction(comments)
        dost_answ = DostoevskyModel.get_prediction(comments)
        return en_answ, rus_answ, dost_answ

    @staticmethod
    def _get_metrics(real_answ, test_answ):
        accuracy = accuracy_score(real_answ, test_answ) * 100
        recall = recall_score(real_answ, test_answ) * 100
        precision = precision_score(real_answ, test_answ) * 100
        F1 = f1_score(real_answ, test_answ) * 100
        return {'accuracy': accuracy, 'recall': recall, 'precision': precision, 'F1': F1}

    @staticmethod
    def get_test_result():
        data = TestNeurons._read_data()
        comments, types = TestNeurons._prepare_test_data(data)
        en_answ, rus_answ, dost_answ = TestNeurons._get_predictions(comments)
        en_res = TestNeurons._get_metrics(types, en_answ)
        rus_res = TestNeurons._get_metrics(types, rus_answ)
        dost_res = TestNeurons._get_metrics(types, dost_answ)
        return en_res, rus_res, dost_res
