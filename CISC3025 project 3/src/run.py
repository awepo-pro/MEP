#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# --------------------------------------------------
# Description:
# --------------------------------------------------
# Author: Du-Haihua <mb75481@um.edu.mo>
# Created Date : April 3rd 2020, 12:05:49
# Last Modified: April 4th 2020, 10:59:35
# --------------------------------------------------

import argparse
import timeit

from MEM import MEMM


def main(action=None):
    classifier = MEMM()

    classifier.beta = BETA
    classifier.max_iter = MAX_ITER
    classifier.bound = BOUND
    classifier.model_path = MODEL_PATH
    classifier.debug_path = DEBUG_PATH
    classifier.use_custom_features = USE_CUSTOM_FEATURES

    if arg.train or action == 'train':
        current_time = timeit.default_timer()
        classifier.train()
        classifier.dump_model()
        print("Training time: %.2fs" % (timeit.default_timer() - current_time))
    if arg.dev or action == 'dev':
        try:
            classifier.load_model()
            classifier.test()
        except Exception as e:
            print(e)
    if arg.show or action == 'show':
        try:
            classifier.load_model()
            classifier.show_samples()
        except Exception as e:
            print(e)
    if arg.debug or action == 'debug':
        try:
            classifier.load_model()
            print(classifier.classifier.show_most_informative_features(40))
            classifier.debug_example()
        except Exception as e:
            print(e)
    if arg.analyze or action == 'analyze':
        try:
            classifier.model_path = '../models/9646-300iters.pkl'  # current best model
            classifier.load_model()
            classifier.analyze('../data/input.txt')
        except Exception as e:
            print(e)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', nargs='?', const=True, default=False)
    parser.add_argument('-d', '--dev', nargs='?', const=True, default=False)
    parser.add_argument('-s', '--show', nargs='?', const=True, default=False)
    parser.add_argument('-D', '--debug', nargs='?', const=True, default=False)
    parser.add_argument('-a', '--analyze', nargs='?', const=True, default=False)
    arg = parser.parse_args()

    #====== Customization ======
    # change beta doesn't change the result
    BETA = 0.5
    MAX_ITER = 10
    BOUND = (0, 20)
    MODEL_PATH = '../model.pkl'
    DEBUG_PATH = '../data/dev'
    USE_CUSTOM_FEATURES = True
    #==========================

    main()

    # main('train')
    # main('dev')
    # main('show')
    # main('debug')
