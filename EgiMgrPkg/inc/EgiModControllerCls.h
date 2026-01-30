#ifndef EGIMODCONTROLLERCLS_H
#define EGIMODCONTROLLERCLS_H

#include <Ans611ControlIfc.h>

class EgiModControllerCls
{
public:
    EgiModControllerCls();
    ~EgiModControllerCls();

    void Initialize();
    void PeriodicRun();

    void SetItsControlOutPortAns611ControlIfc(Ans611ControlIfc* ifc);

private:

protected:
    Ans611ControlIfc* ItsControlOutPortAns611ControlIfc;

};
#endif