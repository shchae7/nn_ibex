#include <iostream>
#include "ibex.h"

using namespace std;
using namespace ibex;

int main(int argc, char** argv)
{
    System system("../bch_files/tests/test_2.bch");

   /* Build a default solver for the system and with a precision set to 0.0001*/
   DefaultSolver solver(system,0.0001);

   solver.solve(system.box); // Run the solver

   /* Display the solutions. */
    cout << solver.get_data() << endl;
}