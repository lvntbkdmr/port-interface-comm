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
    VorIlsMgr.Initialize();
}

void PartitionCls::PeriodicRun()
{
    EgiMgr.PeriodicRun();
    RadaltMgr.PeriodicRun();
    VorIlsMgr.PeriodicRun();
}

void PartitionCls::InitRelations()
{
    // Forward: EgiLruMgr -> RadaltLruMgr
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());

    // Reverse: RadaltLruMgr -> EgiCmpCls
    RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiCmp());

    // EgiCmp -> VorIlsLruMgr
    EgiMgr.GetEgiCmp().SetVorIlsOut(&VorIlsMgr.GetVorIlsLruMgr());
}
