import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "3"

from ai.Coach import Coach
from ai.gobang.GobangGame import GobangGame as Game
from ai.gobang.keras.NNet import NNetWrapper as nn
from ai.utils import *
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

# config = tf.ConfigProto()
# config.gpu_options.per_process_gpu_memory_fraction = 0.4
# set_session(tf.Session(config=config))
args = dotdict({
    'numIters': 100,
    'numEps': 2048,
    'tempThreshold': 15,
    'updateThreshold': 0.6,
    'maxlenOfQueue': 2000000,
    'numMCTSSims': 25,
    'arenaCompare': 100,
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model': True,
    'load_folder_file': ('ai/temp/', 'checkpoint_18.pth.tar'),
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
