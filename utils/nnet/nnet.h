#ifndef _NNET_H_
#define _NNET_H_

class NNet 
{
public:
    NNet(const char* filename);
    ~NNet();

    int num_layers;     //Number of layers in the network
    int input_size;     //Number of inputs to the network
    int output_size;    //Number of outputs to the network
    int max_layer_size;  //Maximum size dimension of a layer in the network
    int *layer_sizes;   //Array of the dimensions of the layers in the network

    double *mins;      //Minimum value of inputs
    double *maxes;     //Maximum value of inputs
    double *means;     //Array of the means used to scale the inputs and outputs
    double *ranges;    //Array of the ranges used to scale the inputs and outputs
    double ****matrix; //4D jagged array that stores the weights and biases
                       //the neural network.
    double *inputs;    //Scratch array for inputs to the different layers
    double *temp;      //Scratch array for outputs of different layers


    void print_info();
};

#endif // _NNET_H_