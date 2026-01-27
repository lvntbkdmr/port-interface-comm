#ifndef RADALTMGR_H
#define RADALTMGR_H

#include <RadaltLruMgrCls.h>

class RadaltMgrCls
{
public:
    RadaltMgrCls();
    ~RadaltMgrCls();

    void Initialize();
    void PeriodicRun();
    void InitRelations();

    EgiExtDataIfc* GetItsRadaltEgiInPortEgiExtDataIfc();

private:
    RadaltLruMgrCls RadaltLruMgr;

protected:
    EgiExtDataIfc* ItsRadaltEgiInPortEgiExtDataIfc;
};

#endif
