#include <iostream>
#include "nnet.h"

using namespace std;

int main(int argc, char** argv)
{
    NNet network = NNet(argv[1]);

    network.print_info();

    return 0;
}