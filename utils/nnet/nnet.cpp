#include <iostream>
#include <cstdio>
#include <cstring>
#include "nnet.h"

using namespace std;

NNet::NNet(const char* filename)
{
    FILE *fstream = fopen(filename, "r");
    if (fstream == NULL)
    {
        cout << "network file not provided or doesn't exist" << endl;
        exit(1);
    }

    int buffer_size = 10240;
    char *buffer = new char[buffer_size];
    char *record, *line;
    int i(0), layer(0), row(0), j(0), param(0);

    line = fgets(buffer, buffer_size, fstream);
    while (strstr(line, "//") != NULL)
    {
        line = fgets(buffer, buffer_size, fstream);
    }
    record = strtok(line, ",\n");

    this->num_layers        = atoi(record);
    this->input_size        = atoi(strtok(NULL, ",\n"));
    this->output_size       = atoi(strtok(NULL, ",\n"));
    this->max_layer_size    = atoi(strtok(NULL, ",\n"));

    this->layer_sizes = new int[this->num_layers + 1];
    line = fgets(buffer, buffer_size, fstream);
    record = strtok(line,",\n");
    for (i = 0; i < this->num_layers + 1; i++)
    {
        this->layer_sizes[i] = atoi(record);
        record = strtok(NULL, ",\n");
    }
    line = fgets(buffer, buffer_size, fstream);

    
    this->mins = new double[this->input_size];
    line = fgets(buffer, buffer_size, fstream);
    record = strtok(line, ",\n");
    for (i = 0; i < this->input_size; i++)
    {
        this->mins[i] = atof(record);
        record = strtok(NULL, ",\n");
    }


    this->maxes = new double[this->input_size];
    line = fgets(buffer, buffer_size, fstream);
    record = strtok(line, ",\n");
    for (i = 0; i < this->input_size; i++)
    {
        this->maxes[i] = atof(record);
        record = strtok(NULL, ",\n");
    }


    this->means = new double[this->input_size + 1];
    line = fgets(buffer, buffer_size, fstream);
    record = strtok(line, ",\n");
    for (i = 0; i < this->input_size + 1; i++)
    {
        this->means[i] = atof(record);
        record = strtok(NULL, ",\n");
    }


    this->ranges = new double[this->input_size + 1];
    line = fgets(buffer, buffer_size, fstream);
    record = strtok(line, ",\n");
    for (i = 0; i < this->input_size + 1; i++)
    {
        this->ranges[i] = atof(record);
        record = strtok(NULL, ",\n");
    }



    this->matrix = new double ***[this->num_layers];
    for (layer = 0; layer < this->num_layers; layer++)
    {
        this->matrix[layer] = new double **[2];
        this->matrix[layer][0] = new double *[this->layer_sizes[layer + 1]];
        this->matrix[layer][1] = new double *[this->layer_sizes[layer + 1]];
        for (row = 0; row < this->layer_sizes[layer + 1]; row++)
        {
            this->matrix[layer][0][row] = new double[this->layer_sizes[layer]];
            this->matrix[layer][1][row] = new double[1];
        }
    }


    layer = 0;
    param = 0;
    i = 0;
    j = 0;

    while ((line = fgets(buffer, buffer_size, fstream)) != NULL)
    {
        if (i >= this->layer_sizes[layer + 1])
        {
            if (param == 0)
            {
                param = 1;
            }
            else
            {
                param = 0;
                layer++;
            }
            i = 0;
            j = 0;
        }
        record = strtok(line, ",\n");
        while(record != NULL)
        {
            this->matrix[layer][param][i][j++] = atof(record);
            record = strtok(NULL, ",\n");
        }
        j = 0;
        i++;
    }
    this->inputs = new double[this->max_layer_size];
    this->temp = new double[this->max_layer_size];

    delete[] buffer;
}


NNet::~NNet()
{
    int i(0), row(0);
    for (i = 0; i < this->num_layers; i++)
    {
        for(row = 0; row < this->layer_sizes[i + 1]; row++)
        {
            delete[] this->matrix[i][0][row];
            delete[] this->matrix[i][1][row];
        }

        delete[] this->matrix[i][0];
        delete[] this->matrix[i][1];

        delete[] this->matrix[i];
    }

    delete[] this->layer_sizes;
    delete[] this->mins;
    delete[] this->maxes;
    delete[] this->means;
    delete[] this->ranges;
    delete[] this->matrix;
    delete[] this->inputs;
    delete[] this->temp;
}

void NNet::print_info()
{
    cout << "# of layers: " <<this->num_layers << "    "
        << "# of inputs: " << this->input_size << "    "
        << "# of outputs: " << this->output_size << "    "
        << "Max dimension: " << this->max_layer_size << endl;

    cout << "Layer sizes: ";
    for(int i = 0; i < this->num_layers; i++)
    {
        cout << this->layer_sizes[i] << " ";
    }
    cout << endl;

    cout << "Matrix" << endl;
    for(int layer = 0; layer < this->num_layers; layer++)
    {
        for(int row = 0; row < this->layer_sizes[layer + 1]; row++)
        {
            for(int col = 0; col < this->layer_sizes[layer]; col++)
            {
                cout << this->matrix[layer][0][row][col] << " ";
            }
            cout << endl;
        }

        for(int row = 0; row < this->layer_sizes[layer + 1]; row++)
        {
            cout << this->matrix[layer][1][row][0] << endl;
        }
    }
}