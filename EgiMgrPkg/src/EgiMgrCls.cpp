#include <EgiMgrCls.h>

EgiMgrCls::EgiMgrCls()
{
    InitRelations();
}

EgiMgrCls::~EgiMgrCls()
{
}

// Wire internal port connections between sub-components
void EgiMgrCls::InitRelations()
{
    // EgiLruMgr sends commands to EgiCmp
    EgiLruMgr.SetCommandOut(&EgiCmp);
}

void EgiMgrCls::Initialize()
{
    EgiLruMgr.Initialize();
    EgiCmp.Initialize();
}

void EgiMgrCls::PeriodicRun()
{
    EgiLruMgr.PeriodicRun();
    EgiCmp.PeriodicRun();
}

// Accessor for external port wiring
EgiLruMgrCls& EgiMgrCls::GetEgiLruMgr()
{
    return EgiLruMgr;
}

// Accessor for external port wiring
EgiCmpCls& EgiMgrCls::GetEgiCmp()
{
    return EgiCmp;
}
