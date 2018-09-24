import sys

sys.path.append('..')
from ...utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *


class Connect4NNet:
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
    def conv2d_bn(x,
                  filters,
                  num_row,
                  num_col,
                  padding='same',
                  strides=(1, 1),
                  name=None):
        if name is not None:
            bn_name = name + '_bn'
            conv_name = name + '_conv'
        else:
            bn_name = None
            conv_name = None
        if K.image_data_format() == 'channels_first':
            bn_axis = 1
        else:
            bn_axis = 3
        x = Conv2D(
            filters, (num_row, num_col),
            strides=strides,
            padding=padding,
            use_bias=False,
            name=conv_name)(x)
        x = BatchNormalization(axis=bn_axis, scale=False, name=bn_name)(x)
        x = Activation('relu', name=name)(x)
        return x

    @staticmethod
    def inception_block(x, kernel):
        branch1x1 = conv2d_bn(x, kernel, 1, 1)

        branch5x5 = conv2d_bn(x, kernel * 2 // 3, 1, 1)
        branch5x5 = conv2d_bn(branch5x5, kernel, 5, 5)

        branch3x3dbl = conv2d_bn(x, kernel, 1, 1)
        branch3x3dbl = conv2d_bn(branch3x3dbl, kernel * 3 // 2, 3, 3)
        branch3x3dbl = conv2d_bn(branch3x3dbl, kernel * 3 // 2, 3, 3)

        branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
        branch_pool = conv2d_bn(branch_pool, 32, 1, 1)
        x = Add()[x, layers.concatenate(
            [branch1x1, branch5x5, branch3x3dbl, branch_pool])]
        return x

    @staticmethod
    def inception_res_block(x, kernel):
        branch1x1 = conv2d_bn(x, kernel, 1, 1)

        branch5x5 = conv2d_bn(x, kernel * 2 // 3, 1, 1)
        branch5x5 = conv2d_bn(branch5x5, kernel, 5, 5)

        branch3x3dbl = conv2d_bn(x, kernel, 1, 1)
        branch3x3dbl = conv2d_bn(branch3x3dbl, kernel * 3 // 2, 3, 3)
        branch3x3dbl = conv2d_bn(branch3x3dbl, kernel * 3 // 2, 3, 3)

        branch_pool = AveragePooling2D((3, 3), strides=(1, 1), padding='same')(x)
        branch_pool = conv2d_bn(branch_pool, 32, 1, 1)
        x = layers.concatenate(
            [branch1x1, branch5x5, branch3x3dbl, branch_pool],
            axis=channel_axis,
            name='mixed0')
        return x

    def conv_block(self, x, kernel):
        x = Conv2D(kernel, 3, padding='same', use_bias=False, trainable=self.args.trainable)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        return x

    def res_block(self, inp, kernel):
        x = Conv2D(kernel, 3, padding='same', use_bias=False, trainable=self.args.trainable)(inp)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Conv2D(kernel, 3, padding='same', use_bias=False, trainable=self.args.trainable)(x)
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
