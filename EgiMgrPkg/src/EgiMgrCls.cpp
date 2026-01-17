#include <EgiMgrCls.h>

EgiMgrCls::EgiMgrCls(/* args */)
{
    InitRelations();
}

EgiMgrCls::~EgiMgrCls()
{
}

void EgiMgrCls::Initialize()
{
    EgiLruMgr.Initialize();
}

void EgiMgrCls::PeriodicRun()
{
    EgiLruMgr.PeriodicRun();
}

void EgiMgrCls::InitRelations()
{
}

EgiLruMgrCls& EgiMgrCls::GetEgiLruMgr()
{
    return EgiLruMgr;
}
