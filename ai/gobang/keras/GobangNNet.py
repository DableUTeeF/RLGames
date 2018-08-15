import sys
sys.path.append('..')
from ai.utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *


class GobangNNet:
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))

        x = Reshape((self.board_x, self.board_y, 1))(self.input_boards)
        x = self.conv_block(x, 256)
        for _ in range(4):
            x = self.res_block(x, 256)
        self.pi = self.policy_head(x)
        self.v = self.value_head(x)

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(args.lr))

    @staticmethod
    def conv_block(x, kernel):
        x = Conv2D(kernel, 3, padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        return x

    @staticmethod
    def res_block(inp, kernel):
        x = Conv2D(kernel, 3, padding='same', use_bias=False)(inp)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Conv2D(kernel, 3, padding='same', use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Add()([inp, x])
        x = Activation('relu')(x)
        return x

    def policy_head(self, x):
        x = Conv2D(2, 1, use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Flatten()(x)
        x = Dropout(0.5)(x)
        x = Dense(self.action_size, activation='softmax', name='pi')(x)
        return x

    @staticmethod
    def value_head(x):
        x = Conv2D(1, 1, use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Flatten()(x)
        x = Dropout(0.5)(x)
        x = Dense(256, use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(1, activation='tanh', name='v')(x)
        return x

