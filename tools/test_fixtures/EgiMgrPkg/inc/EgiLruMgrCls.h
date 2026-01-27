#ifndef EGILRUMGR_H
#define EGILRUMGR_H

#include <EgiExtDataIfc.h>

class EgiLruMgrCls
{
public:
    EgiLruMgrCls();
    ~EgiLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);

private:
protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
};

#endif
