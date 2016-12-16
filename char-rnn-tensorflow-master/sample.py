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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                       help='model directory to store checkpointed models')
    parser.add_argument('--save_dir2', type=str, default='save2',
                       help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=500,
                       help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default=u' ',
                       help='prime text')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample2(args)

def sample2(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    with open(os.path.join(args.save_dir2, 'chars_vocab2.pkl'), 'rb') as f:
        chars2, vocab2 = cPickle.load(f)

    model1 = Model(saved_args, mel=True, True)
    model2 = Model(saved_args, mel=False, True)

    with tf.Session() as sess1, tf.Session() as sess2:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        ckpt2 = tf.train.get_checkpoint_state(args.save_dir2)
        if ckpt and ckpt.model_checkpoint_path and ckpt2 and ckpt2.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            saver.restore(sess2, ckpt2.model_checkpoint_path)
            # args.n controls generate how many characters

            state1 = sess.run(model1.initial_state)
            state2 = sess2.run(model2.initial_state)

            x = np.zeros((1, 1))
            x[0, 0] = vocab['X: 1']
            feed1 = {model.input_data: x, model1.input_data2: x, model1.initial_state:state1}
            feed2 = {model2.input_data: x, model2.input_data2: x, model2.initial_state:state2}

            [state1] = sess.run([model1.final_state], feed1)
            [state2] = sess2.run([model2.final_state], feed2)

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
            prime1 = 'X: 1'
            prime2 = 'X: 1'

            while True:
                x1 = np.zeros((1, 1))
                x1[0, 0] = vocab[prime1]

                x2 = np.zeros((1, 1))
                x2[0, 0] = vocab2[prime2]

                feed1 = {model1.input_data: x1, model1.input_data2: x2, model1.initial_state:state1}
                feed2 = {model2.input_data: x2, model2.input_data2: x1, model2.initial_state:state2}
                
                [probs1, state1] = sess.run([model1.probs, model1.final_state], feed1)
                [probs2, state2] = sess2.run([model2.probs, model2.final_state], feed2)

                p1 = probs1[0]
                p2 = probs2[0]

                sample1 = weighted_pick(p1)
                sample2 = weighted_pick(p2)

                pred1 = chars1[sample1]
                pred2 = chars2[sample2]

                if melOver and harmOver:
                    break
                if pred1.startswith('X:') and switch1:
                    melOver = True
                if pred2.startswith('X:') and switch2:
                    harmOver = True
                if pred1.startswith('X:'):
                    switch1 = 1
                if pred2.startswith('X:'):
                    switch2 = 1
                if switch1 and not melOver:
                    ret1 += pred1
                if switch2 and not harmOver:
                    ret2 += pred2
                prime1 = pred1
                prime2 = pred2

            print(ret1)
            print ("====================================")
            print(ret2)

def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab2.pkl'), 'rb') as f:
        chars2, vocab2 = cPickle.load(f)

    model = Model(saved_args, True)
    model2 = Model(saved_args, True)

    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            # args.n controls generate how many characters
            print(model.sample(sess, chars, vocab, 1000, 'X: 1', args.sample))
            print ("====================================")
            print(model2.sample(sess, chars2, vocab2, 1000, 'X: 1', args.sample))

if __name__ == '__main__':
    main()
