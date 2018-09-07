import os
os.environ["CUDA_VISIBLE_DEVICES"] = "2"

from ai.Coach import Coach
from ai.connect4.Connect4Game import Connect4Game as Game
from ai.connect4.keras.NNet import NNetWrapper as nn
from ai.utils import *
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 1
set_session(tf.Session(config=config))
args = dotdict({
    'numIters': 256,
    'numEps': 512,
    'tempThreshold': 15,
    'updateThreshold': 0.55,
    'maxlenOfQueue': 2000000,
    'numMCTSSims': 25,
    'arenaCompare': 100,
    'cpuct': 1,
    'max_processes': 4,
    'checkpoint': './temp/',
    'load_model': False,
    'load_folder_file': ('./temp/', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__ == "__main__":
    g = Game(8)
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
