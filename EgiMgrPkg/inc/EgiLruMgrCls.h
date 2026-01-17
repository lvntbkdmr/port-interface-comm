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

    void SetEgiOut(EgiExtDataIfc* port);

    EgiCmpCls& GetEgiCmp();

private:
    EgiCmpCls m_EgiCmpCls;
    EgiExtDataIfc* m_egiOut;

};
#endif