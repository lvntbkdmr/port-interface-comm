#ifndef EGILRUMGR_H
#define EGILRUMGR_H

#include <EgiExtDataIfc.h>
#include <EgiModControllerCls.h>
#include <Ans611ControlIfc.h>

class EgiLruMgrCls
{
public:
    EgiLruMgrCls();
    ~EgiLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);
    void SetItsEgi1ControlOutPortAns611ControlIfc(Ans611ControlIfc* ifc);
    void SetItsEgi2ControlOutPortAns611ControlIfc(Ans611ControlIfc* ifc);

private:
    EgiModControllerCls Egi1ModController;
    EgiModControllerCls Egi2ModController;

protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
    Ans611ControlIfc* ItsEgi1ControlOutPortAns611ControlIfc;
    Ans611ControlIfc* ItsEgi2ControlOutPortAns611ControlIfc;

};
#endif