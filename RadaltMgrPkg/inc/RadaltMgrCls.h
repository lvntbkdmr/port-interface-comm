#ifndef RADALTMGR_H
#define RADALTMGR_H

#include <RadaltLruMgrCls.h>

class RadaltMgrCls
{
private:
    /* data */
public:
    RadaltMgrCls(/* args */);
    ~RadaltMgrCls();

    void Initialize();
    void PeriodicRun();

    EgiExtDataIfc * GetItsRadaltEgiInPortEgiExtDataIfc();
    
    void SetItsDataOutPortRadaltExtDataIfc(RadaltExtDataIfc* ifc);

    void InitRelations();
private:
    RadaltLruMgrCls RadaltLruMgr;
protected:
    EgiExtDataIfc * ItsItsRadaltEgiInPortEgiExtDataIfc;
};
#endif
