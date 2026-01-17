#ifndef VORILSMGR_H
#define VORILSMGR_H

#include <VorIlsLruMgrCls.h>

class VorIlsMgrCls
{
private:
    /* data */
public:
    VorIlsMgrCls(/* args */);
    ~VorIlsMgrCls();

    void Initialize();
    void PeriodicRun();

    VorIlsLruMgrCls& GetVorIlsLruMgr();

private:
    VorIlsLruMgrCls VorIlsLruMgr;
};
#endif
