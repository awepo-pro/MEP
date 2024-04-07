#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# --------------------------------------------------
# Description:
# --------------------------------------------------
# Author: Konfido <konfido.du@outlook.com>
# Created Date : April 4th 2020, 17:45:05
# Last Modified: April 4th 2020, 17:45:05
# --------------------------------------------------

import os
from nltk.classify.maxent import MaxentClassifier
from sklearn.metrics import (accuracy_score, fbeta_score, precision_score, recall_score)
import pickle
import time


class MEMM():
    def __init__(self):
        self.train_path = "../data/train"
        self.dev_path = "../data/dev"
        self.beta = 0
        self.max_iter = 0
        self.classifier = None
        self.bound = 0
        self.debug_path = "../data/train"
        self.model = ''

    def features(self, words, previous_label, position):
        """
        Note: The previous label of current word is the only visible label.

        :param words: a list of the words in the entire corpus
        :param previous_label: the label for position-1 (or O if it's the start
                of a new sentence)
        :param position: the word you are adding features for
        """

        features = {}
        """ Baseline Features """
        current_word = words[position]

        # unigram 
        features['has_(%s)' % current_word] = 1

        features['prev_label'] = previous_label
        if position + 2 < len(previous_label):
            features['next_label'] = previous_label[position + 2] 
        if current_word[0].isupper():
            features['Titlecase'] = 1

        #===== TODO: Add your features here =======#

        features['no_of_vowels'] = sum([1 for i in current_word if i in 'aeiou'])

        # TODO: no of consonants = len(current_word) - no of vowels
        # features['no_of_consonants'] = sum([1 for i in current_word if i in 'bcdfghjklmnpqrstvwxyz'])
        features['no_of_consonants'] = len(current_word) - features['no_of_vowels']

        # TODO: if more than two uppercase letters, return false
        features['no_of_caps_greater_2'] = sum([1 for i in current_word[:2] if i.isupper()]) # useful
        features['all_caps'] = 1 if current_word.isupper() else 0

        features['contains_digits'] = 1 if any(i.isdigit() for i in current_word) else 0  # useful

        features['prev_no_of_caps'] = sum([1 for i in words[position-1] if i.isupper()]) if position > 0 else 0
        features['prev_contains_digits'] = 1 if position > 0 and any(i.isdigit() for i in words[position-1]) else 0

        features['length'] = len(current_word)
        features['prev_length'] = len(words[position-1]) if position > 0 else 0
        features['next_length'] = len(words[position+1]) if position < len(words)-1 else 0

        if position > 0:
            features[f'prev_has_{words[position - 1]}'] = 1
        if position < len(words)-1:
            features[f'next_has_{words[position + 1]}'] = 1

        features['consecutive_words'] = 0
        i = position
        while i < len(words):
            if words[i].isalpha():
                features['consecutive_words'] += 1
                i += 1
            else:
                break

        features['prev_consecutive_words'] = 0
        i = position
        while i >= 0:
            if words[i].isalpha():
                features['prev_consecutive_words'] += 1
                i -= 1
            else:
                break

        features[f'prefix_{current_word[:3]}'] = 1
        features[f'suffix_{current_word[-3:]}'] = 1
        if position > 0:
            features[f'prev_prefix_{words[position-1][:3]}'] = 1
            features[f'prev_suffix_{words[position-1][-3:]}'] = 1

        # TODO: check if the word is character or digit
        # Extract character n-grams
        char_bigrams = [''.join(bigram) for bigram in zip(current_word, current_word[1:])]
        char_trigrams = [''.join(trigram) for trigram in zip(current_word, current_word[1:], current_word[2:])]

        # TODO: unigram?
        for char in current_word:
            features[f'char_{char}'] = 1

        # Add n-gram features
        for bigram in char_bigrams:
            features[f'bigram_{bigram}'] = 1
        for trigram in char_trigrams:
            features[f'trigram_{trigram}'] = 1

        features['2_prev_has_(%s)' % words[position - 2]] = 1 if position > 1 else 0

        # TODO: 'Billy' is a PERSON
        features['adjective'] = 1 if self.adjective_like_suffix(current_word) else 0
        features['adverb'] = 1 if self.adverb_like_suffix(current_word) else 0

        # capital with a dot, ie: S. Law is a PERSON
        if len(current_word) == 2 and current_word[1] == '.' and current_word[0].isupper():
            features['capital_with_dot'] = 1 

        # name with Punctuation Marks
        if previous_label == 'PERSON' and current_word[0] == ')':
            features['close_parentheses'] = 1 
        if position + 2 < len(previous_label) and previous_label[position + 2] == 'PERSON' and current_word[0] == '(':
            features['open_parentheses'] = 1 
        if previous_label == 'PERSON' and current_word[0] == '"':
            features['close_quotation'] = 1
        if position + 2 < len(previous_label) and previous_label[position + 2] == 'PERSON' and current_word[0] == '"':
            features['open_quotation'] = 1

        # name with 'De'
        if current_word == 'De':
            features['De'] = 1

        #=============== TODO: Done ================#
        return features

    def load_data(self, filename):
        words = []
        labels = []
        
        for line in open(filename, "r", encoding="utf-8"):
            doublet = line.strip().split("\t")
            if len(doublet) < 2:     # remove emtpy lines
                continue
            words.append(doublet[0])
            labels.append(doublet[1])

        return words, labels

    def train(self):
        print('Training classifier...')
        _, labels, features = self._preprocess_data(self.train_path)

        train_samples = [(f, l) for (f, l) in zip(features, labels)]
        classifier = MaxentClassifier.train(train_samples, max_iter=self.max_iter)
        self.classifier = classifier

        self.dump_model()

        self.record_train(features)

    def test(self):
        print('Testing classifier...')
        _, labels, features = self._preprocess_data(self.dev_path)
        results = [self.classifier.classify(n) for n in features]

        # use micro-average
        f_score = fbeta_score(labels, results, average='macro', beta=self.beta)
        precision = precision_score(labels, results, average='macro')
        recall = recall_score(labels, results, average='macro')
        accuracy = accuracy_score(labels, results)

        print("%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n" %
              ("f_score=", f_score, "accuracy=", accuracy, "recall=", recall,
               "precision=", precision))
        
        self.record_test(f_score, accuracy, recall, precision)

        return True
    
    def show_samples(self):
        """
        Show some sample probability distributions.
        """
        words, labels, features = self._preprocess_data(self.train_path)

        (m, n) = self.bound
        pdists = self.classifier.prob_classify_many(features[m:n])

        print('  Words          P(PERSON)  P(O)\n' + '-' * 40)
        for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
            if label == 'PERSON':
                fmt = '  %-15s *%6.4f   %6.4f'
                if pdist.prob('PERSON') < 0.50:
                    fmt += '  *LOW PROB*'
            else:
                fmt = '  %-15s  %6.4f  *%6.4f'
                if pdist.prob('O') < 0.50:
                    fmt += '  *LOW PROB*'
            print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))

    def dump_model(self):
        history = time.ctime(time.time())[9:-5]
        self.model = f'../models/model{history}.pkl'
        with open(self.model, 'wb') as f:
            pickle.dump(self.classifier, f)

    def load_model(self):
        if self.model == '':
            self.model = '..//models/model4 190008.pkl'
            print('*************** no model ***********************')
        with open(self.model, 'rb') as f:
            self.classifier = pickle.load(f)

    def _preprocess_data(self, path):
        words, labels = self.load_data(path)
        previous_labels = ["O"] + labels
        features = [self.features(words, previous_labels[i], i) for i in range(len(words))]

        return words, labels, features
    
    @staticmethod
    def adjective_like_suffix(word):
        return word[-2:] in ['al', 'ic'] or word[-3:] in ['ous', 'ful', 'ive', 'ish'] or word[-4:] in ['less', 'able']

    @staticmethod
    def adverb_like_suffix(word):
        return word[-2:] in ['ly']
    
    def debug_example(self):
        words, labels, features = self._preprocess_data(self.debug_path)
        cnt = 0

        (m, n) = self.bound
        pdists = self.classifier.prob_classify_many(features[m:n])
        cnt = 0

        print('  Words          P(PERSON)  P(O)\n' + '-' * 40)
        for (word, label, pdist) in list(zip(words, labels, pdists))[m:n]:
            if label == 'PERSON' and pdist.prob('PERSON') < 0.5:
                fmt = '  %-15s *%6.4f   %6.4f' + '  *LOW PROB*'
                print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))
                cnt += 1
            elif label == 'O' and pdist.prob('O') < 0.5:
                fmt = '  %-15s  %6.4f  *%6.4f' + '  *LOW PROB*'
                print(fmt % (word, pdist.prob('PERSON'), pdist.prob('O')))
                cnt += 1
        print(f"Total Low Prob.: {cnt}")

        self.record_debug(cnt)

        

    def record_train(self, features):
        # for those who less than 10 iterations, we don't record them
        if self.max_iter < 10:
            return 
        
        with open('record.txt', 'a') as output:
            output.write('\n************************* config *************************\n')
            output.write(f"beta: {self.beta}\nmax_iter: {self.max_iter}\n")
            output.write(f"model: {self.model}\n")
            output.write('\n************************* train *************************\n')
            output.write('features used:\n')
            for d in features[0]:
                if 'has_' in d:
                    output.write('has_()\n')
                elif 'prefix_' in d:
                    output.write('prefix_\n')
                elif 'suffix_' in d:
                    output.write('suffix_\n')
                elif 'bigram_' in d:
                    output.write('bigram_\n')
                elif '2_prev_has_' in d:
                    output.write('2_prev_has_()\n')
                else:
                    output.write(f"{d}\n") 

    def record_test(self, f_score, accuracy, recall, precision):
        with open('record.txt', 'a') as output:
            output.write('\n************************* config *************************\n')
            output.write(f"beta: {self.beta}\nmax_iter: {self.max_iter}\n")
            output.write(f"model: {self.model}\n")
            output.write('\n************************* test *************************\n')
            output.write("%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n%-15s %.4f\n" %
              ("f_score=", f_score, "accuracy=", accuracy, "recall=", recall,
               "precision=", precision))

    def record_debug(self, cnt):
        with open('record.txt', 'a') as output:
            output.write('\n************************* config *************************\n')
            output.write(f"beta: {self.beta}\nmax_iter: {self.max_iter}\n")
            output.write(f"model: {self.model}\n")
            output.write(f"debug path: {self.debug_path}\n")
            output.write('\n************************* debug *************************\n')
            output.write(f"Total Low Prob.: {cnt}\n")