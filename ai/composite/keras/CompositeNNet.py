from keras.models import *
from keras.layers import *
from keras.optimizers import *

TPU_WORKER = 'grpc://' + os.environ['COLAB_TPU_ADDR']


class CompositeNNet:
    def __init__(self, game, args):
        # game params
        try:
            self.board_x, self.board_y = game.getBoardSize()
        except AttributeError:
            self.board_x, self.board_y = game[0].getBoardSize()
        try:
            self.action_size = [game[0].getActionSize(), game[1].getActionSize()]
        except TypeError:
            self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))

        x = Reshape((self.board_x, self.board_y, 1))(self.input_boards)
        x = self.conv_block(x, 256)
        for _ in range(8):
            x = self.res_block(x, 256)
        self.c4pi = self.policy_head(x, self.action_size[0])
        self.c4v = self.value_head(x)
        self.c4model = Model(inputs=self.input_boards, outputs=[self.c4pi, self.c4v])
        self.c4model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(args.lr))
        # self.c4model = tf.contrib.tpu.keras_to_tpu_model(
        #     self.c4model,
        #     strategy=tf.contrib.tpu.TPUDistributionStrategy(
        #         tf.contrib.cluster_resolver.TPUClusterResolver(TPU_WORKER)))

        self.othpi = self.policy_head(x, self.action_size[1])
        self.othv = self.value_head(x)
        self.othmodel = Model(inputs=self.input_boards, outputs=[self.othpi, self.othv])
        self.othmodel.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(args.lr))
        # self.othmodel = tf.contrib.tpu.keras_to_tpu_model(
        #     self.othmodel,
        #     strategy=tf.contrib.tpu.TPUDistributionStrategy(
        #         tf.contrib.cluster_resolver.TPUClusterResolver(TPU_WORKER)))
        self.model = [self.c4model, self.othmodel]

    def conv_block(self, x, kernel):
        x = Conv2D(kernel, 3, padding='same', use_bias=False, trainable=self.args.train)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        return x

    def res_block(self, inp, kernel):
        x = Conv2D(kernel, 3, padding='same', use_bias=False, trainable=self.args.train)(inp)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Conv2D(kernel, 3, padding='same', use_bias=False, trainable=self.args.train)(x)
        x = BatchNormalization()(x)
        x = Add()([inp, x])
        x = Activation('relu')(x)
        return x

    @staticmethod
    def policy_head(x, action_size):
        x = Conv2D(2, 1, use_bias=False)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = Flatten()(x)
        x = Dropout(0.5)(x)
        x = Dense(action_size, activation='softmax', name='pi')(x)
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
