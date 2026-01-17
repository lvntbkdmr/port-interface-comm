#include <EgiMgrCls.h>

EgiMgrCls::EgiMgrCls()
{
    InitRelations();
}

EgiMgrCls::~EgiMgrCls()
{
}

void EgiMgrCls::InitRelations()
{
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

EgiLruMgrCls& EgiMgrCls::GetEgiLruMgr()
{
    return EgiLruMgr;
}

EgiCmpCls& EgiMgrCls::GetEgiCmp()
{
    return EgiCmp;
}
