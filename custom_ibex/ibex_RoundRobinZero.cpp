#include "ibex_RoundRobinZero.h"
#include "ibex_NoBisectableVariableException.h"

using namespace std;

namespace ibex
{

RoundRobinZero::RoundRobinZero(double prec, double ratio) : Bsc(prec), ratio(ratio) {}

RoundRobinZero::RoundRobinZero(const Vector& prec, double ratio) : Bsc(prec), ratio(ratio) {}

BisectionPoint RoundRobinZero::choose_var(const Cell& cell)
{
    // index of the last bisection point
    int last_var = cell.bisected_var;

    const IntervalVector& box = cell.box;

    int n = box.size();

    if (last_var == -1)
    {
        last_var = n - 1;
    }

    int var = (last_var + 1) % n;

    while (var != last_var && too_small(box, var))
    {
        var = (var + 1) % n;
    }

    if (var == last_var && too_small(box, var))
    {
        throw NoBisectableVariableException();
    }
    else
    {
        if (box[var].lb() < 0 && 0 < box[var].ub()) // interval contains 0 (split on zero)
        {
            return BisectionPoint(var, 0, false);
        }
        else
        {
            return BisectionPoint(var, ratio, true);
        }
    }
}

}