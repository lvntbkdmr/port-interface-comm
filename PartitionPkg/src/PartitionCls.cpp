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
    // Forward: EgiLruMgr -> RadaltLruMgr
    EgiExtDataIfc* egiIfc = RadaltMgr.GetRadaltLruMgr().GetItsRadaltEgiInPortEgiExtDataIfc();
    EgiMgr.GetEgiLruMgr().SetItsDataOutPortEgiExtDataIfc(egiIfc);

    // Reverse: RadaltLruMgr -> EgiCmpCls
    RadaltExtDataIfc* radaltIfc = EgiMgr.GetEgiLruMgr().GetEgiCmp().GetItsEgiCmpRadaltInPortRadaltExtDataIfc();
    RadaltMgr.GetRadaltLruMgr().SetItsDataOutPortRadaltExtDataIfc(radaltIfc);
}

const EgiExtDataType& PartitionCls::GetLastReceivedEgiData() const
{
    return const_cast<RadaltMgrCls&>(RadaltMgr).GetRadaltLruMgr().GetLastReceivedData();
}

int PartitionCls::GetReceivedEgiDataCount() const
{
    return const_cast<RadaltMgrCls&>(RadaltMgr).GetRadaltLruMgr().GetReceivedDataCount();
}

const RadaltExtDataType& PartitionCls::GetLastReceivedRadaltData() const
{
    return const_cast<EgiMgrCls&>(EgiMgr).GetEgiLruMgr().GetEgiCmp().GetLastReceivedData();
}

int PartitionCls::GetReceivedRadaltDataCount() const
{
    return const_cast<EgiMgrCls&>(EgiMgr).GetEgiLruMgr().GetEgiCmp().GetReceivedDataCount();
}
