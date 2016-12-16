from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

from six import text_type
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                       help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=500,
                       help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default=u' ',
                       help='prime text')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample(args)

def isHeader(line):
    prefixes = ['X','T','M','L','Q','K', 'MELODY', 'HARMONY']
    for prefix in prefixes:
        if line.startswith(prefix):
            return True
    return False

def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars1, vocab1 = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab2.pkl'), 'rb') as f:
        chars2, vocab2 = cPickle.load(f)

    model1 = Model(saved_args, mel=True, infer=True)
    model2 = Model(saved_args, mel=False, infer=True)

    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            # args.n controls generate how many characters

            state1 = sess.run(model1.initial_state)
            state2 = sess.run(model2.initial_state)
            def weighted_pick(weights):
                t = np.cumsum(weights)
                s = np.sum(weights)
                return(int(np.searchsorted(t, np.random.rand(1)*s)))

            ret1 = ""
            ret2 = ""
            switch1 = 0
            switch2 = 0
            melOver = False
            harmOver = False
            prime1 = 'MELODY\n'
            prime2 = 'HARMONY\n'

            while True:
                x1 = np.zeros((1, 1))
                x1[0, 0] = vocab1[prime1]

                x2 = np.zeros((1, 1))
                x2[0, 0] = vocab2[prime2]

                feed1 = {model1.input_data: x1, model1.input_data2: x2, model1.initial_state:state1}
                feed2 = {model2.input_data: x2, model2.input_data2: x1, model2.initial_state:state2}
                
                [probs1, state1] = sess.run([model1.probs, model1.final_state], feed1)
                [probs2, state2] = sess.run([model2.probs, model2.final_state], feed2)

                p1 = probs1[0]
                p2 = probs2[0]

                sample1 = weighted_pick(p1)
                sample2 = weighted_pick(p2)

                pred1 = chars1[sample1]
                pred2 = chars2[sample2]

                if melOver and harmOver:
                    break
                if pred1.startswith('MELODY') and switch1:
                    melOver = True
                if pred2.startswith('HARMONY') and switch2:
                    harmOver = True
                if pred1.startswith('X: '):
                    switch1 = 1
                if pred2.startswith('X: '):
                    switch2 = 1
                if switch1 and not melOver:
                    if isHeader(pred1) or pred1.endswith('\n'):
                        ret1 += pred1
                    else:
                        ret1 += pred1 + '|'
                if switch2 and not harmOver:
                    if isHeader(pred2) or pred2.endswith('\n'):
                        ret2 += pred2
                    else:
                        ret2 += pred2 + '|'
                prime1 = pred1
                prime2 = pred2

            print(ret1)
            print ("====================================")
            print(ret2)

if __name__ == '__main__':
    main()
