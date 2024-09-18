# Syllable Segmenter

Segments phone strings into syllables using a learned model.

## Usage

Provided you already have a model, just load it and segment away:

    from g2p.sylseg import Segmenter
    seg = Segmenter.load('seg_model')
    seg.segment('" ? a: R O n h aI m'.split(' '))
    ['"', '?', 'a:', '.', 'R', 'O', 'n', '.', 'h', 'aI', 'm']

## Training

Use something like this:

```shell
# assumes you are in project root directory, NOT in g2p/sylseg
python -m g2p.sylseg.train --input data/ms_xs_converted.train.3k.txt --input data/Manual.X-SAMPA.Transcriptions_3k.txt --dev-proportion 0.1 --model-dest mymodel
```

Training for a few iterations can take some time.
After training the now trained model is pickled (serialized) and written to the
(possibly newly created) directory `mymodel`.

    
## Evaluation

Use something like this:

    python -m g2p.sylseg.test --input data/Manual.X-SAMPA.Transcriptions_3k.txt --model seg_model > test.txt
    2978 / 3018 correct (98.67461895294898 %)
    
This will output the percentage of perfectly recognized examples and write a log of all erroneous predictions to `test.txt`.

Or for your own model (`mymodel`) trained with the command referenced in the previous section:
```shell
# assumes you are in project root directory, not in g2p/sylseg
python -m g2p.sylseg.test --input data/Manual.X-SAMPA.Transcriptions_3k.txt --model mymodel > test.txt
# output:
# 2983 / 3018 correct (98.84029158383035 %)
```
