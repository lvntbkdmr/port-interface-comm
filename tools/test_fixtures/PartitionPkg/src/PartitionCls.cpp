#include <PartitionCls.h>

PartitionCls::PartitionCls()
{
    InitRelations();
}

PartitionCls::~PartitionCls()
{
}

void PartitionCls::Initialize()
{
    EgiMgr.Initialize();
    RadaltMgr.Initialize();
}

void PartitionCls::PeriodicRun()
{
    EgiMgr.PeriodicRun();
    RadaltMgr.PeriodicRun();
}

void PartitionCls::InitRelations()
{
    EgiMgr.SetItsDataOutPortEgiExtDataIfc(RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc());
}
