import fasttext

model = fasttext.train_unsupervised('data/ms_syllable_training_data.txt', epoch=1, dim=50)
print(model.words)

print(model.get_word_vector("n"))

print(model.get_word_vector("n ut"))
model.save_model("g2p/sylseg/vector_model_for_phonemes.bin")
