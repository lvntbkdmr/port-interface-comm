#ifndef PARTITIONCLS_H
#define PARTITIONCLS_H

#include <EgiMgrCls.h>
#include <RadaltMgrCls.h>

class PartitionCls
{
public:
    PartitionCls();
    ~PartitionCls();

    void Initialize();
    void PeriodicRun();
    void InitRelations();

private:
    EgiMgrCls EgiMgr;
    RadaltMgrCls RadaltMgr;

protected:
};

#endif
