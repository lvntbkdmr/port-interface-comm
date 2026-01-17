#ifndef PARTITIONCLS_H
#define PARTITIONCLS_H

#include <EgiMgrCls.h>
#include <RadaltMgrCls.h>

#include <EgiExtDataIfc.h>
#include <RadaltExtDataIfc.h>

class PartitionCls
{
public:
    PartitionCls();
    ~PartitionCls();
    void Initialize();
    void PeriodicRun();

    void InitRelations();

    const EgiExtDataType& GetLastReceivedEgiData() const;
    int GetReceivedEgiDataCount() const;

    const RadaltExtDataType& GetLastReceivedRadaltData() const;
    int GetReceivedRadaltDataCount() const;

private:
    EgiMgrCls EgiMgr;
    RadaltMgrCls RadaltMgr;
protected:
};
#endif