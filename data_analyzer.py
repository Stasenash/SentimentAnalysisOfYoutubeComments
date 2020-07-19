from dostoevsky_model import DostoevskyModel
from eng_model import EngModel
from rus_model import RusModel


class DataAnalyzer:
    @staticmethod
    def _analyze(results):
        positive = 0
        negative = 0
        for result in results:
            if result == 0:
                negative += 1
            else:
                positive += 1
        return {"positive": positive / len(results) * 100, "negative": negative / len(results) * 100}

    @staticmethod
    def get_eng_analysis(texts):
        return DataAnalyzer._analyze(EngModel.get_prediction(texts))

    @staticmethod
    def get_rus_analysis(texts):
        return DataAnalyzer._analyze(RusModel.get_prediction(texts))

    @staticmethod
    def get_dost_analysis(texts):
        return DataAnalyzer._analyze(DostoevskyModel.get_prediction(texts))
