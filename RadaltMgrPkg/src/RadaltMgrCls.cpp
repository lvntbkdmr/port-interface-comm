#include <RadaltMgrCls.h>

RadaltMgrCls::RadaltMgrCls()
{
    InitRelations();
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

void RadaltMgrCls::InitRelations()
{
}

RadaltLruMgrCls& RadaltMgrCls::GetRadaltLruMgr()
{
    return RadaltLruMgr;
}
