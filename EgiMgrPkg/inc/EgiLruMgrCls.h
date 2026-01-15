#ifndef EGILRUMGR_H
#define EGILRUMGR_H

#include <EgiCmpCls.h>

#include <EgiExtDataIfc.h>

class EgiLruMgrCls
{
public:
    EgiLruMgrCls();
    ~EgiLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);

private:
    EgiCmpCls m_EgiCmpCls;
protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;

};
#endif