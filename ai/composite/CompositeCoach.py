from collections import deque
from concurrent.futures import ThreadPoolExecutor
from ..Arena import Arena
from .CompositeMCTS import CompositeMCTS as MCTS
import numpy as np
from ..Bar import Bar, AverageMeter
import time
import os
import sys
from pickle import Pickler, Unpickler
from random import shuffle
import threading


threadLock = threading.Lock()


class SaveExample(threading.Thread):
    def __init__(self, example, checkpoint, odd):
        threading.Thread.__init__(self)
        self.odd = odd
        self.example = example
        self.checkpoint = checkpoint
        self.loaded = 0

    def run(self):
        threadLock.acquire()
        self.save()
        # Free lock to release next thread
        threadLock.release()

    def save(self):
        folder = self.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, 'last' + str(self.odd) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.example)
        self.loaded = 1
        print("save example complete")
        return


class CompositeCoach:
    # noinspection PyUnresolvedReferences
    """
        This class executes the self-play + learning. It uses the functions defined
        in Game and NeuralNet. args are specified in main.py.

        Should be:
            >>> games = CompositeGame(8)
            >>> nnet = CompositeNNet(games)
            >>> coach = CompositeCoach(games, nnet, args)
    """

    def __init__(self, game, nnet, args):
        self.games = game
        self.game = self.games.games
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.games)  # the competitor network
        self.args = args
        self.curPlayer = [0, 0]
        self.mcts = [MCTS(self.game[0], self.nnet, self.args, 0),
                     MCTS(self.game[1], self.nnet, self.args, 1)]
        self.trainExamplesHistory = [[], []]  # history of examples from args.numItersForTrainExamplesHistory latest iterations
        self.skipFirstSelfPlay = False  # can be overriden in loadTrainExamples()

    def executeEpisode(self, i):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        trainExamples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in trainExamples.

        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.

        Returns:
            trainExamples: a list of examples of the form (canonicalBoard,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        trainExamples = []
        board = self.game[i].getInitBoard()
        self.curPlayer[i] = 1
        episodeStep = 0

        while True:
            episodeStep += 1
            canonicalBoard = self.game[i].getCanonicalForm(board, self.curPlayer[i])
            temp = int(episodeStep < self.args.tempThreshold)

            pi = self.mcts[i].getActionProb(canonicalBoard, temp=temp)
            sym = self.game[i].getSymmetries(canonicalBoard, pi)
            for b, p in sym:
                trainExamples.append([b, self.curPlayer[i], p, None])

            action = np.random.choice(len(pi), p=pi)
            # print(action, pi)
            board, self.curPlayer[i] = self.game[i].getNextState(board, self.curPlayer[i], action)

            r = self.game[i].getGameEnded(board, self.curPlayer[i])

            if r != 0:
                return [(x[0], x[2], r * ((-1) ** (x[1] != self.curPlayer[i]))) for x in trainExamples]

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in trainExamples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.numIters + 1):
            trainExamples = [[], []]
            # bookkeeping
            print('------ITER ' + str(i) + '------')
            for gidx in range(2):
                # examples of the iteration
                if not self.skipFirstSelfPlay or i > 1:
                    iterationTrainExamples = deque([], maxlen=self.args.maxlenOfQueue)

                    eps_time = AverageMeter()
                    bar = Bar(f'{"Othello" if gidx==1 else "Connect4"} Play', max=self.args.numEps)
                    end = time.time()

                    for eps in range(self.args.numEps):
                        self.mcts[gidx] = MCTS(self.game[gidx], self.nnet, self.args, gidx)  # reset search tree
                        # with ThreadPoolExecutor(max_workers=self.args.max_processes) as executor:
                        #     for j in range(self.args.max_processes):
                        #         print('hello human')
                        #         # iters.append(executor.submit(executeEpisode, self.game, self.curPlayer, self.args, self.mcts))
                        #         # iterationTrainExamples += executor.submit(self.executeEpisode).result()
                        #
                        #         # tempiter = executor.submit(executeEpisode, self).result()
                        iterationTrainExamples += self.executeEpisode(gidx)
                        # bookkeeping + plot progress
                        eps_time.update(time.time() - end)
                        end = time.time()
                        bar.suffix = '({eps}/{maxeps}) Eps Time: {et:.3f}s | Total: {total:} | ETA: {eta:}'.format(
                            eps=eps, maxeps=self.args.numEps, et=eps_time.avg,
                            total=bar.elapsed_td, eta=bar.eta_td)
                        bar.next()
                    bar.finish()

                    # save the iteration examples to the history
                    self.trainExamplesHistory[gidx].append(iterationTrainExamples)

                if len(self.trainExamplesHistory[gidx]) > self.args.numItersForTrainExamplesHistory:
                    print("len(trainExamplesHistory) =", len(self.trainExamplesHistory[gidx]),
                          " => remove the oldest trainExamples")
                    self.trainExamplesHistory[gidx].pop(0)
                # backup history to a file
                # NB! the examples were collected using the model from the previous iteration, so (i-1)

                # shuffle examlpes before training a005835
                trainExamples[gidx] = []
                for e in self.trainExamplesHistory[gidx]:
                    trainExamples[gidx].extend(e)
                shuffle(trainExamples[gidx])
            # with ThreadPoolExecutor() as executor:
            #     executor.submit(self.saveTrainExamples, i % 2 == 0)
            saves = SaveExample(self.trainExamplesHistory, self.args.checkpoint, i % 2 == 0)
            saves.start()
            # training new network, keeping a copy of the old one
            print('Start swap weights')
            self.pnet.nnet.model[0].set_weights(self.nnet.nnet.model[0].get_weights())
            self.pnet.nnet.model[1].set_weights(self.nnet.nnet.model[1].get_weights())
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            print('Swap weights complete')
            self.nnet.train(trainExamples)
            pwins, nwins, draws = [0, 0], [0, 0], [0, 0]
            gname = ["Connect4", "Othello"]
            for gidx in range(2):

                pmcts = MCTS(self.game[gidx], self.pnet, self.args, gidx)
                nmcts = MCTS(self.game[gidx], self.nnet, self.args, gidx)

                print(f'{gname[gidx]} evaluating')
                arena = Arena(lambda x: np.argmax(pmcts.getActionProb(x, temp=0)),
                              lambda x: np.argmax(nmcts.getActionProb(x, temp=0)),
                              self.game[gidx])
                pwin, nwin, draw = arena.playGames(self.args.arenaCompare)
                pwins[gidx], nwins[gidx], draws[gidx] = pwins[gidx] + pwin, nwins[gidx] + nwin, draws[gidx] + draw

                print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwin, pwin, draw))
            if sum(pwins) + sum(nwins) > 0 and float(sum(nwins)) / (sum(pwins) + sum(nwins)) < self.args.updateThreshold:
                print('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            elif float(nwins[0]) / (pwins[0] + nwins[0]) < self.args.updateThreshold*0.8 or \
                    float(nwins[1]) / (pwins[1] + nwins[1]) < self.args.updateThreshold*0.8:
                print('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename=self.getCheckpointFile(i))
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')
            while True:
                time.sleep(2)
                if saves.loaded == 1:
                    break
            saves.join()

    @staticmethod
    def getCheckpointFile(iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def saveTrainExamples(self, even):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, 'last' + str(even) + ".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.trainExamplesHistory)
        print('saveExample complete')

    def loadTrainExamples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], 'last')
        examplesFile = modelFile + "False.examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with trainExamples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with trainExamples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.trainExamplesHistory = Unpickler(f).load()
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True
