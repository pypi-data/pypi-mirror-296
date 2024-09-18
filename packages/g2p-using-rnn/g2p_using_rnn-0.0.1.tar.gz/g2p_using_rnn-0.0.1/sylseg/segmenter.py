from .syllable_model import Model


class Segmenter:
    def __init__(self, model):
        self.model = model

    def segment(self, phones):
        """
        Segments a list of phones, inserting syllable boundaries where appropriate.

        :param phones: a list of strings, each representing a phone
        :return: a list of phones
        """
        boundaries = self.model.predict(phones)
        phone_idx = 0
        out_phones = []
        for tag in boundaries:
            out_phones.append(phones[phone_idx])
            if tag != 0:
                out_phones.append('.')
            phone_idx += 1
        return out_phones

    @staticmethod
    def load(model_file_name):
        return Segmenter(Model.load(model_file_name))
