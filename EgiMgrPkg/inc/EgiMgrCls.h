#ifndef EGIMGR_H
#define EGIMGR_H

#include <EgiLruMgrCls.h>
#include <EgiCmpCls.h>

class EgiMgrCls
{
public:
    EgiMgrCls();
    ~EgiMgrCls();

    void InitRelations();
    void Initialize();
    void PeriodicRun();

    EgiLruMgrCls& GetEgiLruMgr();
    EgiCmpCls& GetEgiCmp();

private:
    EgiLruMgrCls EgiLruMgr;
    EgiCmpCls EgiCmp;
};

#endif
