from abc import ABC, abstractmethod

import sys
sys.path.append('../')
from utils.readNNet import readNNet

# Input Format : [d, i] (d: depth, i: index)

class Component(ABC):
    def __init__(self, input_num, output_num):  # Take number of inputs and outputs as input
        self.input_num = input_num
        self.output_num = output_num

    @abstractmethod
    def print_info(self):
        print('# of inputs: ' + str(self.input_num))
        print('# of outputs: ' + str(self.output_num))

    @abstractmethod
    def encode(self):
        pass


class Network(Component):
    def __init__(self, input_num, output_num, weights, biases, numLayers, layerSizes, inputMins, inputMaxes):
        super().__init__(input_num, output_num)

        # Additional Network Info
        self.weights = weights
        self.biases = biases
        self.numLayers = numLayers
        self.layerSizes = layerSizes

        # For consideration --> Specific only to NNet format?
        self.inputMins = inputMins
        self.inputMaxes = inputMaxes

        self.layers = [Layer(layerSizes[i], layerSizes[i + 1] , weights[i], biases[i], i + 1) for i in range(numLayers)] # Depth starting from 1 (depth 0: input layer)

    def print_info(self):
        print('Network Information')
        super().print_info()
        print('# of layers: ' + str(self.numLayers))
        for i in range(self.numLayers):
            self.layers[i].print_info()

    def encode(self, file_pth):
        bch_file = open(file_pth, "w")

        bch_file.write('function relu(x)\n')
        bch_file.write('    return max(0,x)\n')
        bch_file.write('end\n')


        # Variables
        bch_file.write('\nvariables\n')
        for i in range(self.input_num):
            bch_file.write('x' + str(i + 1) + ';\n')

        for j in range(self.numLayers - 1):
            bch_file.write('z' + str(j + 1) + '[' + str(layerSizes[j + 1]) + '];\n')

        bch_file.write('y[' + str(self.output_num) + '];\n')


        # Constraints
        bch_file.write('\nconstraints\n')

        self.layers[0].encode(bch_file, True, False)
        for k in range(1, self.numLayers - 1):
            self.layers[k].encode(bch_file, False, False)
        self.layers[self.numLayers - 1].encode(bch_file, False, True)


        bch_file.write('\nend\n')
        bch_file.close()

class Layer(Component):
    def __init__(self, input_num, output_num, weight, bias, d):
        super().__init__(input_num, output_num)
        self.weight = weight
        self.bias = bias
        self.depth = d

        self.nodes = [Node(input_num, 1, weight[i], bias[i], d, i) for i in range(output_num)]

    def print_info(self):
        print(str(self.depth) + 'th Layer Information')
        super().print_info()
        print(self.weight)
        print(self.bias)

    def encode(self, bch_file, first_layer, last_layer):
        for i in range(self.output_num):
            self.nodes[i].encode(bch_file, first_layer, last_layer)



class Node(Component):
    def __init__(self, input_num, output_num, weight, bias, d, i):
        super().__init__(input_num, output_num)
        self.weight = weight
        self.bias = bias
        self.depth = d
        self.index = i

    def print_info(self):
        print(str(self.index) + 'th Node at ' + str(self.depth) + 'th Layer Information')
        super().print_info()
        print(self.weight)
        print(self.bias)

    def encode(self, bch_file, first_layer, last_layer):
        if first_layer == True:
            sum_str = ''
            for i in range(len(self.weight) - 1):
                sum_str += 'x' + str(i + 1) + ' * ' + str(self.weight[i]) + ' + '
            sum_str += 'x' + str(len(self.weight)) + ' * ' + str(self.weight[len(self.weight) - 1])

            bch_file.write('z' + str(self.depth) + '[' + str(self.index) + '] = relu(' + sum_str + ');\n')
        elif last_layer == True:
            sum_str = ''
            for i in range(len(self.weight) - 1):
                sum_str += 'z' + str(self.depth - 1) + '[' + str(i) + '] * ' + str(self.weight[i]) + ' + '
            sum_str += 'z' + str(self.depth - 1) + '[' + str(len(self.weight) - 1) + '] * ' + str(self.weight[len(self.weight) - 1])

            bch_file.write('y[' + str(self.index) + '] = ' + sum_str + ';\n')
        else:
            sum_str = ''
            for i in range(len(self.weight) - 1):
                sum_str += 'z' + str(self.depth - 1) + '[' + str(i) + '] * ' + str(self.weight[i]) + ' + '
            sum_str += 'z' + str(self.depth - 1) + '[' + str(len(self.weight) - 1) + '] * ' + str(self.weight[len(self.weight) - 1])

            bch_file.write('z' + str(self.depth) + '[' + str(self.index) + '] = relu(' + sum_str + ');\n')


if __name__ == '__main__':
    weights, biases, numLayers, layerSizes, inputMins, inputMaxes = readNNet('../networks/tiny_acasxu/ACASXU_run2a_1_1_tiny_5.nnet')

    network = Network(layerSizes[0], layerSizes[-1], weights, biases, numLayers, layerSizes, inputMins, inputMaxes)
    #network.print_info()

    network.encode('../bch_files/tiny_acasxu/tiny_5.bch')