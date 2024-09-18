"""
This script generates phoneme transcription predictions on a list of input words.
"""
# from transformers import pipeline
#
# pipe = pipeline(task="text2text-generation", model="cisco-ai/mini-bart-g2p")
# text = "hello world"
# # DO NOT DO ```pipe(text)``` as this will produce unexpected results.
#
# pipe(text.split())

from transformers import T5ForConditionalGeneration, AutoTokenizer

model = T5ForConditionalGeneration.from_pretrained('charsiu/g2p_multilingual_byT5_tiny_16_layers_100')
tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')

# tokenized English words
# words = ['Char', 'siu', 'is', 'a', 'Cantonese', 'style', 'of', 'barbecued', 'pork']
# words = ['<eng-us>: '+i for i in words]
words = ['Protokollauswertungen', 'Darminfektionen', 'hinzuzählet', 'alonso', 'jährigem']
words = ['<ger>: '+i for i in words]
out = tokenizer(words,padding=True,add_special_tokens=False,return_tensors='pt')
out_tokens = tokenizer.decode(out['input_ids'][0])
print(out_tokens)
preds = model.generate(**out, num_beams=1, max_length=50) # We do not find beam search helpful. Greedy decoding is enough.
phones = tokenizer.batch_decode(preds.tolist(), skip_special_tokens=True)
print(phones)
