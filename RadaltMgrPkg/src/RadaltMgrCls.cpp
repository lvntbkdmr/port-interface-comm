#include <RadaltMgrCls.h>

RadaltMgrCls::RadaltMgrCls()
{
}

RadaltMgrCls::~RadaltMgrCls()
{
}

void RadaltMgrCls::Initialize()
{
}

void RadaltMgrCls::PeriodicRun()
{
    RadaltLruMgr.PeriodicRun();
}

RadaltLruMgrCls& RadaltMgrCls::GetRadaltLruMgr()
{
    return RadaltLruMgr;
}
