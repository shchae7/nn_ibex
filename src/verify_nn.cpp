#include <iostream>
#include "ibex.h"

using namespace std;
using namespace ibex;

int main(int argc, char** argv)
{
    System system(argv[1]);

    DefaultSolver solver(system,0.0001);

    // stop_at_first option used
    solver.solve(system.box, true);

    ofstream result_file;
    result_file.open(argv[2]);
    result_file << "cpu time used: " << solver.get_time() << endl
                << "number of cells: " << solver.get_nb_cells() << endl << endl
                << solver.get_data() << endl;
    result_file.close();

    return 0;
}