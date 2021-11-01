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


    // redirect cout to file
    ofstream out(argv[2]);
    auto *coutbuf = cout.rdbuf();
    cout.rdbuf(out.rdbuf());

    solver.report();
    cout << solver.get_data();

    return 0;
}