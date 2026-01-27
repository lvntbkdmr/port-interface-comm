#ifndef EGIMGR_H
#define EGIMGR_H

#include <EgiLruMgrCls.h>
#include <EgiExtDataIfc.h>

class EgiMgrCls
{
public:
    EgiMgrCls();
    ~EgiMgrCls();

    void Initialize();
    void PeriodicRun();
    void InitRelations();

    void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);

private:
    EgiLruMgrCls EgiLruMgr;

protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
};

#endif
