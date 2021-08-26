#ifndef __IBEX_ROUND_ROBIN_ZERO_H__
#define __IBEX_ROUND_ROBIN_ZERO_H__

#include "ibex_Bsc.h"

namespace ibex
{

class RoundRobinZero : public Bsc 
{
public:
    RoundRobinZero(double prec, double ratio=Bsc::default_ratio());

    RoundRobinZero(const Vector& prec, double ratio=Bsc::default_ratio());

    virtual BisectionPoint choose_var(const Cell& cell);

    const double ratio;
};

}

#endif // __IBEX_ROUND_ROBIN_ZERO_H__