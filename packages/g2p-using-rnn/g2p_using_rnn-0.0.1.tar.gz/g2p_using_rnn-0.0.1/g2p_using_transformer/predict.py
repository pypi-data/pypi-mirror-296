"""
This script generates end-to-end phoneme transcriptions on input data file with words using a
saved transformer encoder-decoder model and saves the predictions to CSV format.
"""
import pandas as pd
import argparse
from transformers import T5ForConditionalGeneration, AutoTokenizer


def predict_on_test_data(test_data_path, model_path, save_predictions_path):
    # model_path = 'charsiu/g2p_multilingual_byT5_tiny_16_layers_100'

    model = T5ForConditionalGeneration.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')
    print('Loaded model and tokeniser')
    # test_data_path = 'data/lexicon_ldist_representation_test.txt'
    # test_data = pd.read_csv(test_data_path, encoding='utf-8')
    test_data = pd.read_csv(test_data_path, encoding='utf-8', sep='\t')  # in case test data is TSV file
    words = test_data['word'].tolist()  # ['Protokollauswertungen', 'Darminfektionen', 'hinzuzählet', 'alonso', 'jährigem']
    # print(words[:50])
    words = ['<ger>: '+i for i in words]
    out = tokenizer(words, padding=True, add_special_tokens=False, return_tensors='pt')
    print('Generated tokens')
    # out_tokens = tokenizer.decode(out['input_ids'][0])
    # print(out_tokens)
    preds = model.generate(**out, num_beams=1, max_length=150)  # We do not find beam search helpful. Greedy decoding is enough.
    print('Generated predictions')
    phones = tokenizer.batch_decode(preds.tolist(), skip_special_tokens=True)
    # print(phones)
    print('Converted tokens to phones')

    test_data['predicted_text'] = phones
    test_data.to_csv(save_predictions_path, index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--test_data_path', type=str, default='/home/soumyabarikeri/data/grapheme_to_phoneme/lexicon_ldist_representation_test.txt')
    parser.add_argument('--model_path', type=str, default='results_pretrain_e10_retry/')
    parser.add_argument('--save_predictions_path', type=str, default='results/predictions_from_transformer_e10_e2e.csv')
    args = parser.parse_args()

    predict_on_test_data(args.test_data_path, args.model_path, args.save_predictions_path)
