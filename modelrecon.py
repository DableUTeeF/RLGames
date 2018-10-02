
from keras.models import *
from keras.layers import *
from keras.optimizers import *


def createmodel(size):
    input_boards = Input(shape=(size, size))

    x = Reshape((size, size, 1))(input_boards)
    x = conv_block(x, 256, 1)
    for _ in range(4):
        x = res_block(x, 256, _+2)
    pi = policy_head(size*size+1, x)
    v = value_head(x)

    model = Model(inputs=input_boards, outputs=[pi, v])
    # model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(1e-4))
    return model


def conv_block(x, kernel, block_id):
    x = Conv2D(kernel, 3, padding='same', use_bias=False, name=f'block{block_id}_conv')(x)
    x = BatchNormalization(name=f'block{block_id}_bn')(x)
    x = Activation('relu', name=f'block{block_id}_relu')(x)
    return x


def res_block(inp, kernel, block_id):
    x = Conv2D(kernel, 3, padding='same', use_bias=False, name=f'block{block_id}_conv1')(inp)
    x = BatchNormalization(name=f'block{block_id}_bn1')(x)
    x = Activation('relu', name=f'block{block_id}_relu1')(x)
    x = Conv2D(kernel, 3, padding='same', use_bias=False, name=f'block{block_id}_conv2')(x)
    x = BatchNormalization(name=f'block{block_id}_bn2')(x)
    x = Add(name=f'block{block_id}_add')([inp, x])
    x = Activation('relu', name=f'block{block_id}_relu2')(x)
    return x


def policy_head(action_size, x):
    x = Conv2D(2, 1, use_bias=False, name='policy_conv')(x)
    x = BatchNormalization(name='policy_bn')(x)
    x = Activation('relu', name='policy_relu')(x)
    x = Flatten(name='policy_flatten')(x)
    x = Dropout(0.5, name='policy_dropout')(x)
    x = Dense(action_size, activation='softmax', name='pi')(x)
    return x


def value_head(x):
    x = Conv2D(1, 1, use_bias=False, name='value_conv1')(x)
    x = BatchNormalization(name='value_bn1')(x)
    x = Activation('relu', name='value_relu1')(x)
    x = Flatten(name='value_flatten')(x)
    x = Dropout(0.5, name='value_dropout1')(x)
    x = Dense(256, use_bias=False, name='value_dense')(x)
    x = BatchNormalization(name='value_bn2')(x)
    x = Activation('relu', name='value_relu2')(x)
    x = Dropout(0.5, name='value_dropout2')(x)
    x = Dense(1, activation='tanh', name='v')(x)
    return x


if __name__ == '__main__':
    # Neural Net
    model8 = createmodel(8)
    model8.trainable = False
    model8.load_weights('ai/weights/othello_8x8x73_best.pth.tar')
    xs = model8.get_layer('block5_relu2').output
    pis = policy_head(8, xs)
    vs = value_head(xs)
    model10 = Model(model8.input, outputs=[pis, vs])
    print(model10.summary())
    model10.save_weights('ai/weights/connect4o.h5')
