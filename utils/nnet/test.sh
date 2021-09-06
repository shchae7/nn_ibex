#!/bin/bash

NETWORK_HOME="/home/shchae7/nn_ibex/networks"

g++ ./nnet.cpp ./read_nnet.cpp

./a.out $NETWORK_HOME/tiny_acasxu/ACASXU_run2a_1_1_tiny_2.nnet