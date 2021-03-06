import tensorflow as tf
import numpy as np

class deepEM():
    '''
    Use a seven layer convolution neural network to pick particles
    '''
    def __init__(self,args):
        self.args = args
        self.variables_deepem()
        self.build_model()
            
    def variables_deepem(self):
        # first convolutional layer
        std = 0.01
        w1 = tf.Variable(tf.truncated_normal([self.args.FL_kernelsize, self.args.FL_kernelsize, 1, self.args.FL_feature_map], stddev = std))
        b1 = tf.Variable(tf.zeros([self.args.FL_feature_map]))

        # second pooling layer
        w2 = [1, self.args.SL_poolingsize, self.args.SL_poolingsize, 1]

        # third convolutional layer
        w3 = tf.Variable(tf.truncated_normal([self.args.TL_kernelsize, self.args.TL_kernelsize, self.args.FL_feature_map, self.args.TL_feature_map], stddev = std))
        b3 = tf.Variable(tf.zeros([self.args.TL_feature_map]))

        # forth pooling layer
        w4 = [1, self.args.FOL_poolingsize, self.args.FOL_poolingsize, 1]

        # fifth convolutional layer
        w5 = tf.Variable(tf.truncated_normal([self.args.FIL_kernelsize, self.args.FIL_kernelsize, self.args.TL_feature_map, self.args.FIL_feature_map], stddev = std))
        b5 = tf.Variable(tf.zeros([self.args.FIL_feature_map]))

        # sixth pooling layer
        w6 = [1, self.args.SIL_poolingsize, self.args.SIL_poolingsize, 1]

        input_map_size = self.args.boxsize
        C1_map_size = input_map_size - self.args.FL_kernelsize + 1
        S2_map_size = C1_map_size // self.args.SL_poolingsize
        C3_map_size = S2_map_size - self.args.TL_kernelsize + 1
        S4_map_size = C3_map_size // self.args.FOL_poolingsize
        C5_map_size = S4_map_size - self.args.FIL_kernelsize + 1
        S6_map_size = C5_map_size // self.args.SIL_poolingsize

        fully_para_num = int(self.args.FIL_feature_map * S6_map_size * S6_map_size)
        hidden_neurons = 1

        print("type(fully_para_num):",type(fully_para_num))
        print("type(hidden_neurons):",type(hidden_neurons))

        # output layer
        w7 = tf.Variable(tf.truncated_normal([fully_para_num, hidden_neurons], stddev = std))
        b7 = tf.Variable(tf.zeros([hidden_neurons]))

        self.variables = {
            'w1': w1, 'w2': w2, 'w3': w3, 'w4': w4, 'w5': w5, 'w6': w6, 'w7': w7, 
            'b1': b1, 'b3': b3, 'b5': b5, 'b7': b7, 'fully_para_num': fully_para_num
        }

    def build_model(self):        
        self.X = tf.placeholder(tf.float32, shape = [None, self.args.boxsize, self.args.boxsize, 1])
        self.Y = tf.placeholder(tf.float32, shape = [None,1])
        self.global_step = tf.Variable(0, name='global_step',trainable=False)

        # layer 1
        layer1_conv = tf.nn.conv2d(self.X, self.variables['w1'], [1, 1, 1, 1], padding = 'VALID')
        layer1_actv = tf.nn.sigmoid(layer1_conv + self.variables['b1'])
        print("layer 1 shape is: ",layer1_conv.shape)
        
        # layer 2
        layer2_pool = tf.nn.avg_pool(layer1_actv, self.variables['w2'],self.variables['w2'], padding = 'VALID')
        print("layer 2 shape is: ",layer2_pool.shape)

        # layer 3
        layer3_conv = tf.nn.conv2d(layer2_pool, self.variables['w3'], [1, 1, 1, 1], padding = 'VALID')
        layer3_actv = tf.nn.sigmoid(layer3_conv + self.variables['b3'])
        print("layer 3 shape is: ",layer3_conv.shape)

        # layer 4
        layer4_pool = tf.nn.avg_pool(layer3_actv, self.variables['w4'], self.variables['w4'], padding = 'VALID')
        print("layer 4 shape is: ",layer4_pool.shape)

        # layer 5
        layer5_conv = tf.nn.conv2d(layer4_pool, self.variables['w5'], [1, 1, 1, 1], padding = 'VALID')
        layer5_actv =  tf.nn.sigmoid(layer5_conv + self.variables['b5'])
        print("layer 5 shape is: ",layer5_conv.shape)

        # layer 6
        layer6_pool = tf.nn.avg_pool(layer5_actv, self.variables['w6'], self.variables['w6'], padding = 'VALID')
        print("layer 6 shape is: ",layer6_pool.shape)
        
        # layer 7
        layer7_input = tf.reshape(layer6_pool,[-1,self.variables['fully_para_num']])
        self.l7_input = layer7_input
        
        print("layer 7 shape is: ",layer7_input.shape)
        print("w7 shape is: ",self.variables['w7'].shape)

        # dropout
        if self.args.is_training and self.args.dropout:
            layer7_input = tf.nn.dropout(layer7_input, self.args.dropout_rate)

        self.logits = tf.matmul(layer7_input, self.variables['w7']) + self.variables['b7']

        # calculate the accuracy in the training set
        self.pred = tf.nn.sigmoid(self.logits)

        if not self.args.is_training:
            return

        # regularization
        if not self.args.regularization:
            self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels = self.Y))
        else:
            self.loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=self.logits, labels = self.Y) + \
                    tf.contrib.layers.l2_regularizer(self.args.reg_rate)(self.variables['w1']) + \
                    tf.contrib.layers.l2_regularizer(self.args.reg_rate)(self.variables['w3']) + \
                    tf.contrib.layers.l2_regularizer(self.args.reg_rate)(self.variables['w5']) + \
                    tf.contrib.layers.l2_regularizer(self.args.reg_rate)(self.variables['w7']))

        self.lr = tf.maximum(1e-5,tf.train.exponential_decay(self.args.learning_rate, self.global_step, self.args.decay_step, self.args.decay_rate, staircase=True))
        self.optimizer = tf.train.AdamOptimizer(self.lr).minimize(self.loss, global_step=self.global_step)






