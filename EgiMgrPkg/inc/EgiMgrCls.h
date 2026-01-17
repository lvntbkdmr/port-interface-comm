#ifndef EGIMGR_H
#define EGIMGR_H

#include <EgiLruMgrCls.h>

class EgiMgrCls
{
private:
    /* data */
public:
    EgiMgrCls(/* args */);
    ~EgiMgrCls();

    void Initialize();
    void PeriodicRun();

    EgiLruMgrCls& GetEgiLruMgr();

private:
    EgiLruMgrCls EgiLruMgr;
};

#endif
