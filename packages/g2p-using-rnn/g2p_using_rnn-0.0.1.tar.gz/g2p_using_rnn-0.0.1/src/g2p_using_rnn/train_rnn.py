"""
This script takes in a training data and trains an encoder-decoder RNN (LSTM) model for end-to-end
phoneme transcription. Saves the trained model in a specified path.
"""
import numpy as np
import keras
import os
import pandas as pd
from tqdm import tqdm
import random
from pathlib import Path
from tensorflow.keras.utils import Sequence
from sklearn.model_selection import train_test_split

keras.utils.set_random_seed(42)

batch_size = 32  # Batch size for training.
epochs = 100  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.
num_samples = 700000  # 24600  # Number of samples to train on.
# Path to the data txt file on disk.
data_path = os.path.join("data/", "lexicon_ldist_representation_train.txt")  # "new_testing_data_from_mstts_lexicon_cleaned_ax_ar_train.txt")
save_model_path = "s2s_model.keras"

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
    # input_text = input_text.strip("(\'")
    # target_text = target_text.strip("\')")
    # target_text = target_text.replace("- ", "")
    # target_text = target_text.replace("1 ", "")
    # We use "tab" as the "start sequence" character
    # for the targets, and "\n" as "end sequence" character.
    target_text = target_text.replace(" ", "")
    target_text = "\t" + target_text + "\n"
    input_texts.append(input_text)
    target_texts.append(target_text)
    target_texts_with_syllables_stress.append(target_text)
    for char in input_text:
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text:
        if char not in target_characters:
            target_characters.add(char)


input_characters = sorted(list(input_characters))
input_characters.append(' ')
target_characters = sorted(list(target_characters))
target_characters.append(' ')
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])

print("Number of samples:", len(input_texts))
print("Number of unique input tokens:", num_encoder_tokens)
print("Number of unique output tokens:", num_decoder_tokens)
print("Max sequence length for inputs:", max_encoder_seq_length)
print("Max sequence length for outputs:", max_decoder_seq_length)

input_token_index = dict([(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict([(char, i) for i, char in enumerate(target_characters)])

encoder_input_data = np.zeros(
    (len(input_texts), max_encoder_seq_length, num_encoder_tokens),
    dtype="float32",
)
decoder_input_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype="float32",
)
decoder_target_data = np.zeros(
    (len(input_texts), max_decoder_seq_length, num_decoder_tokens),
    dtype="float32",
)

for i, (input_text, target_text) in enumerate(zip(input_texts, target_texts)):
    for t, char in enumerate(input_text):
        encoder_input_data[i, t, input_token_index[char]] = 1.0
    encoder_input_data[i, t + 1:, input_token_index[" "]] = 1.0  # pad the remaining characters with a space
    for t, char in enumerate(target_text):
        # decoder_target_data is ahead of decoder_input_data by one timestep
        decoder_input_data[i, t, target_token_index[char]] = 1.0 # first character is a tab
        if t > 0:
            # decoder_target_data will be ahead by one timestep
            # and will not include the start character.
            decoder_target_data[i, t - 1, target_token_index[char]] = 1.0
    decoder_input_data[i, t + 1 :, target_token_index[" "]] = 1.0
    decoder_target_data[i, t:, target_token_index[" "]] = 1.0


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

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = keras.Model([encoder_inputs, decoder_inputs], decoder_outputs)

model.compile(
    optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"]
)


class DataGenerator(keras.utils.Sequence):
    def __init__(self, x_set_1, x_set_2, y_set, batch_size):
        self.x1, self.x2, self.y = x_set_1, x_set_2, y_set
        self.batch_size = batch_size

    def __len__(self):
        return int(np.ceil(len(self.x1) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x1 = self.x1[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_x2 = self.x2[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_y = self.y[idx * self.batch_size:(idx + 1) * self.batch_size]
        return (batch_x1, batch_x2), batch_y


X1_train, X1_test, y_train_, y_test_, X1_train_i, X1_test_i = train_test_split(encoder_input_data,
                                                                               decoder_target_data,
                                                                               np.arange(len(encoder_input_data)),
                                                                               test_size=0.33, random_state=42)
X2_train, X2_test, y_train, y_test, X2_train_i, X2_test_i = train_test_split(decoder_input_data,
                                                                             decoder_target_data,
                                                                             np.arange(len(decoder_input_data)),
                                                                             test_size=0.33, random_state=42)

encoder_input_gen = DataGenerator(X1_train, X2_train, y_train, batch_size)
encoder_input_gen_test = DataGenerator(X1_test, X2_test, y_test, batch_size)

model.fit(
    encoder_input_gen,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=encoder_input_gen_test,
    verbose=True,
)
# Save model
model.save(save_model_path)

model = keras.models.load_model(save_model_path)

# encoder_inputs = model.input[0]  # input_1
# encoder_outputs, state_h_enc, state_c_enc = model.layers[2].output  # lstm_1
# encoder_states = [state_h_enc, state_c_enc]
# encoder_model = keras.Model(encoder_inputs, encoder_states)
#
# decoder_inputs = model.input[1]  # input_2
# decoder_state_input_h = keras.Input(shape=(latent_dim,))
# decoder_state_input_c = keras.Input(shape=(latent_dim,))
# decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
# decoder_lstm = model.layers[3]
# decoder_outputs, state_h_dec, state_c_dec = decoder_lstm(
#     decoder_inputs, initial_state=decoder_states_inputs
# )
# decoder_states = [state_h_dec, state_c_dec]
# decoder_dense = model.layers[4]
# decoder_outputs = decoder_dense(decoder_outputs)
# decoder_model = keras.Model(
#     [decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states
# )
#
# # Reverse-lookup token index to decode sequences back to
# # something readable.
# reverse_input_char_index = dict((i, char) for char, i in input_token_index.items())
# reverse_target_char_index = dict((i, char) for char, i in target_token_index.items())
#

# def decode_sequence(input_seq):
#     # Encode the input as state vectors.
#     states_value = encoder_model.predict(input_seq, verbose=0)
#
#     # Generate empty target sequence of length 1.
#     target_seq = np.zeros((1, 1, num_decoder_tokens))
#     # Populate the first character of target sequence with the start character.
#     target_seq[0, 0, target_token_index["\t"]] = 1.0
#
#     # Sampling loop for a batch of sequences
#     # (to simplify, here we assume a batch of size 1).
#     stop_condition = False
#     decoded_sentence = ""
#     while not stop_condition:
#         output_tokens, h, c = decoder_model.predict(
#             [target_seq] + states_value, verbose=0
#         )
#
#         # Sample a token
#         sampled_token_index = np.argmax(output_tokens[0, -1, :])
#         sampled_char = reverse_target_char_index[sampled_token_index]
#         decoded_sentence += sampled_char
#
#         # Exit condition: either hit max length
#         # or find stop character.
#         if sampled_char == "\n" or len(decoded_sentence) > max_decoder_seq_length:
#             stop_condition = True
#
#         # Update the target sequence (of length 1).
#         target_seq = np.zeros((1, 1, num_decoder_tokens))
#         target_seq[0, 0, sampled_token_index] = 1.0
#
#         # Update states
#         states_value = [h, c]
#     return decoded_sentence
#
#
# for seq_index in range(20):
#     # Take one sequence (part of the training set)
#     # for trying out decoding.
#     input_seq = encoder_input_data[seq_index : seq_index + 1]
#     decoded_sentence = decode_sequence(input_seq)
#     print("-")
#     print("Input sentence:", input_texts[seq_index])
#     print("Decoded sentence:", decoded_sentence)
#
#
# output_dict_list = []
# print(X1_test_i)
# sample_x1_test_indices = random.sample(sorted(X1_test_i), 5000)
# for i in tqdm(sample_x1_test_indices):
#     input_seq = encoder_input_data[i: i + 1]
#     decoded_sentence = decode_sequence(input_seq)
#     row = {'input_text': input_texts[i].strip(),
#            'target_text_with_syllables_stress': target_texts_with_syllables_stress[i].strip(),
#            'target_text': target_texts[i].strip(),
#            'predicted_text': decoded_sentence.strip()}
#     output_dict_list.append(row)
#
# df = pd.DataFrame.from_dict(output_dict_list)
# df.to_csv("predictions_from_phoneme_detector_model.csv")
