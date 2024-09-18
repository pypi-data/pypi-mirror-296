import numpy as np

from g2p.primstress.train_stress import remove_stress, label_syllable
from .stress_model import StressModel

class Detector:
    def __init__(self, model):
        self.model = model

    def detect(self, syllables):
        """
        Detects the primary stress of a word.

        :param syllables: The input word, segmented into a list of X-SAMPA syllables.
        :return: The same syllables, with a primary stress marker added to exactly one syllable.
        """
        feats = self.model.extract_features_for_stress(syllables)
        xs = self.model.vectorize_example(feats)
        ys = np.asarray([label_syllable(syl) for syl in syllables])
        probs = self.model.learner.predict_proba(xs)
        #print("probs", probs)
        preds = np.zeros(len(ys))
        #print("preds", preds)
        max_index = np.argmax(probs[:, 1])
        #print("max_index", max_index)
        preds[max_index] = 1
        #print("preds", preds)
        result_syllables = [self.augment_syllable(syl, stress) for syl, stress in zip(syllables, preds)]
        formatted_syllables = ' - '.join(result_syllables)
        formatted_syllables = '"' + formatted_syllables + '"'


        return formatted_syllables


    @staticmethod
    # def augment_syllable(syl, stress):
    #     if stress:
    #         return '" ' + syl
    #     else:
    #         return syl

    def augment_syllable(syl, stress): #new version for mstts data
        # Define a list of vowel phonemes
        vowel_phonemes = ['aa', 'a', 'oh', 'ae', 'eh', 'ax', 'iy', 'ih', 'eu', 'ow', 'oe', 'ey', 'uw', 'uh', 'ue', 'uy',
                          'ay', 'aw', 'oy', 'ar']

        # Iterate through the syllable to find the first vowel phoneme
        for i, phoneme in enumerate(syl.split()):
            if phoneme in vowel_phonemes:
                # Insert '1' after the found vowel phoneme if stress is true
                if stress:
                    return ' '.join(syl.split()[:i + 1]) + ' 1 ' + ' '.join(syl.split()[i + 1:])
                else:
                    return syl
        # Return the syllable unchanged if no vowel phoneme is found
        return syl

    @staticmethod
    def load(model_file_name):
        return Detector(StressModel.load(model_file_name))
