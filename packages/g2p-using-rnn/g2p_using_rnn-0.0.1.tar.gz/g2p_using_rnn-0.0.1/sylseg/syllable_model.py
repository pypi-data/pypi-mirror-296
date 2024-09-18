import numpy as np
import os
import pickle
#import pycrfsuite
import sklearn_crfsuite

#from pystruct.learners import FrankWolfeSSVM, StructuredPerceptron
#from pystruct.models import ChainCRF
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.pipeline import Pipeline


class SyllableModel:
    """Wraps a pystruct model."""
    def __init__(self, learner=None, vectorizer=None):
        self.learner = learner if learner else self.create_learner()
        self.vectorizer = vectorizer if vectorizer else DictVectorizer(sparse=False)

    def predict_syllable_boundaries_from_phonemes(self, phones):
        extracted_features = self.extract_features_for_syllables(phones)
        vectorize_example = self.vectorize_example([extracted_features])
        example_arr = np.array([vectorize_example])
        return self.learner.predict(example_arr)[0]

    def extract_features_for_syllables(self, phones):
        """
        Extracts a feature dict from a list of phones.

        :param phones: a list of phones
        :return: a mapping from feature names to values
        """
        fs = []
        for idx in range(0, len(phones)):
            f = {
                'left-1-1': ngram(idx + 1, idx, phones),
                'left-1-2': ngram(idx + 1, idx - 1, phones),
                'left-2-2': ngram(idx, idx - 1, phones),
                'left-1-3': ngram(idx + 1, idx - 2, phones),
                'left-2-3': ngram(idx, idx - 2, phones),
                'left-3-3': ngram(idx - 1, idx - 2, phones),
                'right-1-1': ngram(idx + 1, idx + 2, phones),
                'right-1-2': ngram(idx + 1, idx + 3, phones),
                'right-2-2': ngram(idx + 2, idx + 3, phones),
                'right-1-3': ngram(idx + 1, idx + 4, phones),
                'right-2-3': ngram(idx + 2, idx + 4, phones),
                'right-3-3': ngram(idx + 3, idx + 4, phones),
                'lr-1-1': ngram(idx + 1, idx, phones) + ngram(idx + 1, idx + 2, phones),
                'lr-2-1': ngram(idx + 1, idx - 1, phones) + ngram(idx + 1, idx + 2, phones),
                'lr-1-2': ngram(idx + 1, idx, phones) + ngram(idx + 1, idx + 3, phones),
                'lr-2-2': ngram(idx + 1, idx - 1, phones) + ngram(idx + 1, idx + 3, phones),
            }
            fs.append(f)
        return fs

    def vectorize_example(self, example_dicts):
        return self.vectorizer.transform(example_dicts)

    def vectorize_data_set(self, x_dicts):
        # first fit the vectorizer
        self.vectorizer.fit_transform(d for ds in x_dicts for d in ds)
        # then transform all the dicts again to keep their per-example structure
        testvar = [self.vectorizer.transform(ds) for ds in x_dicts]
        # x = np.array([self.vectorizer.transform(ds) for ds in x_dicts])
        x = np.array([self.vectorizer.transform(ds) for ds in x_dicts], dtype="object"
                 )

        return x

    def create_phoneme_vectors(self, phoneme_features, vector_model):
        phoneme_vector = []
        for phoneme in phoneme_features:
            feature_vectors_of_a_character = []
            for feat in phoneme.values():
                feature_vectors_of_a_character.extend(vector_model.get_word_vector(feat))
            phoneme_vector.append(feature_vectors_of_a_character)
        return phoneme_vector


    def save(self, path_name: str):
        os.makedirs(path_name, exist_ok=True)
        with open(path_name + '/learner.pkl', 'wb') as f:
            pickle.dump(self.learner, f)
        with open(path_name + '/vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)

    @staticmethod
    def load(path_name: str):
        with open(path_name + '/learner.pkl', 'rb') as f:
            learner = pickle.load(f)
        with open(path_name + '/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return Model(learner, vectorizer)

#    @staticmethod #ORIGINAL CODE
#    def create_learner():
#        model = ChainCRF()
#        return StructuredPerceptron(model=model, decay_exponent=-1, average=True,
#                                    max_iter=10, verbose=1)
#         self.learner = FrankWolfeSSVM(model=self.pystruct_model, C=.1, max_iter=10)

#    return model
    @staticmethod
    def create_learner():
        crf = sklearn_crfsuite.CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )
        return crf


        #trainer = pycrfsuite.Trainer()
        #trainer.set_params({
        #    'c1': 1.0,
        #    'c2': 1e-3,
        #    'max_iterations': 50,
        #    'feature.possible_transitions': True
        #})
        #return trainer





def ngram(start, end, chars):
    """
    Extracts the consecutive elements of a list from start to end.

    The element at index start is included in the list, while end is excluded. If end >= start, the indices are swapped.
    """
    start, end = (start, end) if end >= start else (end, start)
    start = 0 if start < 0 else start
    end = len(chars) if end > len(chars) else end
    return ' '.join(chars[start:end])

