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
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());

    // Reverse: RadaltLruMgr -> EgiCmpCls
    RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiLruMgr().GetEgiCmp());
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
