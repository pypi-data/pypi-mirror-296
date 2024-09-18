import argparse
import re
import sys

from g2p.primstress.detector import Detector
from g2p.primstress.train_stress import remove_stress


def main(parsed_args):
    seg = Detector.load(parsed_args.sylmodelcls)
    correct = 0
    total = 0
    with open(parsed_args.input) as input_file:
        for line in input_file:
            line = re.sub('\ufeff', '', line).strip()
            stressed_syllables = line.split(' . ')
            stripped_syllables = [remove_stress(syl) for syl in stressed_syllables]
            predicted = ' . '.join(seg.detect(stripped_syllables))
            if predicted != line:
                print('correct: ' + line)
                print('predict: ' + predicted)
                print()
            else:
                correct += 1
            total += 1
        print('{} / {} correct ({} %)'.format(correct, total, (float(correct) / total * 100.0)), file=sys.stderr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test a statistical model for primary stress detection.')
    parser.add_argument('--input', required=True,
                        help='Name of an input file containing segmented X-SAMPA strings, one per line.')
    parser.add_argument('--model', type=str, required=True,
                        help='Path to load the model from.')
    args = parser.parse_args()
    main(args)
