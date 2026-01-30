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
    RadaltExtDataIfc * ItsEgiExtDataIfc = EgiMgr.GetItsRadaltInPortRadaltExtDataIfc();
    RadaltMgr.SetItsDataOutPortRadaltExtDataIfc(ItsEgiExtDataIfc);

    EgiExtDataIfc* ItsRadaltEgiExtDataIfc = RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc();
    EgiMgr.SetItsDataOutPortEgiExtDataIfc(ItsRadaltEgiExtDataIfc);
}