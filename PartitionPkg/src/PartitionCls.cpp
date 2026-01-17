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

// Wire port connections between manager components
void PartitionCls::InitRelations()
{
    // EgiLruMgr sends EGI external data to RadaltLruMgr
    EgiMgr.GetEgiLruMgr().SetEgiOut(&RadaltMgr.GetRadaltLruMgr());

    // RadaltLruMgr sends radar altimeter data to EgiCmp
    RadaltMgr.GetRadaltLruMgr().SetRadaltOut(&EgiMgr.GetEgiCmp());

    // EgiCmp sends VOR/ILS navigation data to VorIlsLruMgr
    EgiMgr.GetEgiCmp().SetVorIlsOut(&VorIlsMgr.GetVorIlsLruMgr());
}
