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

    void InitRelations();

    RadaltLruMgrCls& GetRadaltLruMgr();

private:
    RadaltLruMgrCls RadaltLruMgr;
};
#endif
