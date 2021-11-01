from abc import ABCMeta, abstractmethod
from os import fdopen
from interval import *
import numpy
import onnx
import onnx.utils
import sys
from onnx import numpy_helper

from z3 import *

class AbstractComponent(metaclass = ABCMeta):
    @abstractmethod
    def eval(self, inputs):
        pass

    @abstractmethod
    def print_info(self):
        pass

class Network(AbstractComponent):
    def __init__(self, file_path, activation, abstract, threshold):
        self.file_path = file_path
        if activation == 'ReLU':
            self.layer_sizes, self.layers, self.maxes, self.mins, \
            self.means, self.ranges, self.last_layer_weights = load_network_nnet(file_path, activation, abstract)

        self.nn_input_num = self.layer_sizes[0]
        self.nn_output_num = self.layer_sizes[-1]

    def eval(self, inputs):
        for layer in self.layers:
            print(inputs)
            inputs = layer.eval(inputs)
        return inputs

    def to_bch(self, inputs, outputs, bch_file):
        bch_file.write('function ReLU(x)\n')
        bch_file.write('    return max(0,x)\n')
        bch_file.write('end\n\n')

        bch_file.write('variables\n')
        for i in range(self.nn_input_num):
            bch_file.write('x' + str(i + 1) + ' in [-1,1];\n')

        for j in range(len(self.layers) - 1):
            bch_file.write('z' + str(j + 1) + '[' + str(self.layer_sizes[j + 1]) + '];\n')

        for k in range(self.nn_output_num):
            bch_file.write('y' + str(k + 1) + ';\n')
        bch_file.write('\n')

        variables = [inputs]
        for layer_num, layer in enumerate(self.layers[:-1]):
            variables.append(['z%d[%d]' %(layer_num + 1, nodeNum) for nodeNum, node in enumerate(layer.nodes)])
        variables.append(outputs)

        bch_file.write('constraints\n')
        for layer_num in range(len(self.layers)):
            self.layers[layer_num].to_bch(variables[layer_num], variables[layer_num + 1], bch_file)
        bch_file.write('y1 < 0;\n')

        bch_file.write('\nend')
        bch_file.close()

    def print_info(self):
        print('Printing Neural Network Information...')
        for layer in self.layers:
            layer.print_info()


class Layer(AbstractComponent):
    def __init__(self, nodes):
        self.nodes = nodes

    def eval(self, inputs):
        return [node.eval(inputs) for node in self.nodes]

    def to_bch(self, inputs, outputs, bch_file):
        for node_num, node in enumerate(self.nodes):
            node.to_bch(inputs, outputs[node_num], bch_file)

    def print_info(self):
        for node in self.nodes:
            node.print_info()


class Node(AbstractComponent):
    def __init__(self, weights, bias, activation):
        self.weights = weights
        self.bias = bias
        self.activation = activation

        self.inputs = None
        self.output = None

    def eval(self, inputs):
        return self.activation.eval(sum(x * y for x,y in zip(inputs, self.weights)) + self.bias)

    def to_bch(self, inputs, output, bch_file):
        sum_str = ''
        for x, y in zip(inputs, self.weights):
            sum_str += x + ' * ' + str(y) + ' + '
        sum_str += str(self.bias)

        if output[0] != 'y':
            bch_file.write(output + ' = ReLU(' + sum_str + ');\n')
        else:
            bch_file.write(output + ' = ' + sum_str + ';\n')

    def print_info(self):
        print('weights', self.weights,
                '\nbias', self.bias,
                '\nactivation', self.activation)


class Activation(AbstractComponent):
    def eval(self, inputs):
        raise NotImplementedError

    def encode(self, inputs, outputs, bound=None):
        raise NotImplementedError

    def print_info(self):
        raise NotImplementedError

class ReLUActivation(Activation):
    def eval(self, input):
        return max(input, 0)

    def encode(self, input, output, bound=None):
        return If(input['variable'] >= 0, output['variable'] == input['variable'], output['variable'] == 0)

def load_network_nnet(filename, activation_func, abstraction):
    with open(filename) as f:
        line = f.readline()
        cnt = 1
        while line[0:2] == "//":
            line=f.readline()
            cnt+= 1
        # numLayers does't include the input layer!
        numLayers, inputSize, outputSize, _ = [int(x) for x in line.strip().split(",")[:-1]]
        line=f.readline()

        # input layer size, layer1size, layer2size...
        layerSizes = [int(x) for x in line.strip().split(",")[:-1]]

        line=f.readline()
        symmetric = int(line.strip().split(",")[0])

        line = f.readline()
        inputMinimums = [float(x) for x in line.strip().split(",")[:-1]]
        if len(inputMinimums) > inputSize: del inputMinimums[-2:]

        line = f.readline()
        inputMaximums = [float(x) for x in line.strip().split(",")[:-1]]
        if len(inputMaximums) > inputSize: del inputMaximums[-2:]

        line = f.readline()
        inputMeans = [float(x) for x in line.strip().split(",")[:-1]]

        line = f.readline()
        inputRanges = [float(x) for x in line.strip().split(",")[:-1]]

        weights=[]
        biases = []
        for layernum in range(numLayers):
            previousLayerSize = layerSizes[layernum]
            currentLayerSize = layerSizes[layernum+1]
            weights.append([])
            biases.append([])
            weights[layernum] = numpy.zeros((currentLayerSize,previousLayerSize))
            for i in range(currentLayerSize):
                line=f.readline()
                aux = [float(x) for x in line.strip().split(",")[:-1]]
                for j in range(previousLayerSize):
                    weights[layernum][i,j] = aux[j]
            #biases
            biases[layernum] = numpy.zeros(currentLayerSize)
            for i in range(currentLayerSize):
                line=f.readline()
                x = float(line.strip().split(",")[0])
                biases[layernum][i] = x

        layers = []
        for layerNum in range(numLayers):
            if abstraction == 'concrete' and activation_func == 'ReLU':
                nodes = [Node(weights[layerNum][nodeNum], biases[layerNum][nodeNum], ReLUActivation()) for nodeNum in range(len(biases[layerNum]))]
            layers.append(Layer(nodes))

        return [layerSizes, layers, inputMaximums, inputMinimums, inputMeans, inputRanges, weights[numLayers - 1]]

if __name__ == '__main__':
    home = '/home/shchae7/nn_ibex/'
    network = Network(home + 'networks/tiny_acasxu/ACASXU_run2a_1_1_tiny.nnet', 'ReLU', 'concrete', 0) # threshold not used yet

    input_vars = []
    output_vars = []
    for input_i in range(network.nn_input_num):
        input_vars.append('x%d' % (input_i + 1))

    for output_i in range(network.nn_output_num):
        output_vars.append('y%d' % (output_i + 1))

    bch_file = open(home + 'bch_files/tiny_acasxu/tiny_1.bch', "w")

    network.to_bch(input_vars, output_vars, bch_file)