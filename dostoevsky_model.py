from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel


class DostoevskyModel:

    @staticmethod
    def _prepare_model():
        tokenizer = RegexTokenizer()
        model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        return model

    @staticmethod
    def get_prediction(messages):
        model = DostoevskyModel._prepare_model()
        predictions = model.predict(messages, k=1)
        results = []
        for predict in predictions:
            if 'negative' in predict:
                results.append(0)
            else:
                results.append(1)
        return results
