#include <EgiMgrCls.h>

EgiMgrCls::EgiMgrCls(/* args */)
{
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

EgiLruMgrCls& EgiMgrCls::GetEgiLruMgr()
{
    return EgiLruMgr;
}
