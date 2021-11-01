HOME=/home/shchae7/nn_ibex
BCH_FILES=$HOME/bch_files
RESULTS=$HOME/results

make

./verify $BCH_FILES/tiny_acasxu/tiny_2.bch $RESULTS/tiny_acasxu/tiny_2.txt