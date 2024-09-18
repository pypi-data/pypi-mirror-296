"""
This script generates phoneme transcriptions (phonemes, syllables and stress) on a given word
using a trained and saved RNN model for phoneme transcription.
"""
import numpy as np
import keras
import os
import time


def create_encoder_decoder_model():
    # Define an input sequence and process it.
    encoder_inputs = keras.Input(shape=(None, num_encoder_tokens))
    encoder = keras.layers.LSTM(latent_dim, return_state=True)
    encoder_outputs, state_h, state_c = encoder(encoder_inputs)

    # We discard `encoder_outputs` and only keep the states.
    encoder_states = [state_h, state_c]

    # Set up the decoder, using `encoder_states` as initial state.
    decoder_inputs = keras.Input(shape=(None, num_decoder_tokens))

    # We set up our decoder to return full output sequences,
    # and to return internal states as well. We don't use the
    # return states in the training model, but we will use them in inference.
    decoder_lstm = keras.layers.LSTM(latent_dim, return_sequences=True, return_state=True)
    decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
    decoder_dense = keras.layers.Dense(num_decoder_tokens, activation="softmax")
    decoder_outputs = decoder_dense(decoder_outputs)

    model = keras.models.load_model("s2s_model_updated_data1_e2e.keras") #s2s_model_new_data_umlauts_e2e.keras")

    encoder_inputs = model.input[0]  # input_1
    encoder_outputs, state_h_enc, state_c_enc = model.layers[2].output  # lstm_1
    encoder_states = [state_h_enc, state_c_enc]
    encoder_model_ = keras.Model(encoder_inputs, encoder_states)

    decoder_inputs = model.input[1]  # input_2
    decoder_state_input_h = keras.Input(shape=(latent_dim,))
    decoder_state_input_c = keras.Input(shape=(latent_dim,))
    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
    decoder_lstm = model.layers[3]
    decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
        decoder_inputs, initial_state=decoder_states_inputs
    )
    decoder_states = [state_h_dec, state_c_dec]
    decoder_dense = model.layers[4]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model_ = keras.Model(
        [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
    )

    return encoder_model_, decoder_model_


def decode_sequence(input_, input_texts_len=613507, input_texts_test_len=6198):
    print(f'Input {input_}')
    encoder_input_data = np.zeros(
        (input_texts_len, max_encoder_seq_length, num_encoder_tokens),
        dtype="float32",
    )
    encoder_input_data_test = np.zeros(
        (input_texts_test_len, max_encoder_seq_length, num_encoder_tokens),
        dtype="float32",
    )
    for i, input_text_1 in enumerate([input_]):
        for t, char_ in enumerate(input_text_1):
            encoder_input_data_test[i, t, input_token_index[char_]] = 1.0
        encoder_input_data_test[i, t + 1:, input_token_index[" "]] = 1.0

    # Encode the input as state vectors.
    states_value = encoder_model.predict(encoder_input_data_test[0:1], verbose=0)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1, 1, num_decoder_tokens))
    # Populate the first character of target sequence with the start character.
    target_seq[0, 0, target_token_index["\t"]] = 1.0

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ""
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict(
            [target_seq] + states_value, verbose=0
        )

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_target_char_index[sampled_token_index]
        decoded_sentence += sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if sampled_char == "\n" or len(decoded_sentence) > max_decoder_seq_length:
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1, 1, num_decoder_tokens))
        target_seq[0, 0, sampled_token_index] = 1.0

        # Update states
        states_value = [h, c]
    return decoded_sentence

latent_dim = 256
num_samples = 700000 # 481090
data_path = os.path.join("version_control_lexicon_update_10_LDist_train.txt") #"new_testing_data_from_mstts_lexicon_cleaned_ax_ar_train.txt") # the data used for training
data_path_test = os.path.join("version_control_lexicon_update_10_LDist_test.txt")#"new_testing_data_from_mstts_lexicon_cleaned_ax_ar_test.txt") # data used for testing

# Vectorize the data.
input_texts = []
target_texts = []
target_texts_with_syllables_stress = []

input_characters = set()
target_characters = set()

with open(data_path, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
for line in lines[: min(num_samples, len(lines) - 1)]:
    index, input_text, target_text = line.split(",")
    if input_text == 'word':
        continue
    # We use "tab" as the "start sequence" character
    # for the targets, and "\n" as "end sequence" character.
    target_text = "\t" + target_text + "\n"
    input_texts.append(input_text)
    target_texts.append(target_text)
    for char in input_text:
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text:
        if char not in target_characters:
            target_characters.add(char)

input_texts_test = []
# target_texts_test = []
with open(data_path_test, "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
for line in lines[: min(num_samples, len(lines) - 1)]:
    index, input_text_, target_text_ = line.split(",")
    if input_text_ == 'word':
        continue

    input_texts_test.append(input_text_)
    # target_texts_test.append(target_text_)

input_characters = sorted(list(input_characters))
input_characters.append(' ')
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])
input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())

encoder_model, decoder_model = create_encoder_decoder_model()


if __name__ == '__main__':

    t1 = time.time()
    decoded_sentence = decode_sequence('universität', len(input_texts), len(input_texts_test))
    t2 = time.time()
    print(f'Decoded sentence in {t2 - t1} sec --> {decoded_sentence}')
