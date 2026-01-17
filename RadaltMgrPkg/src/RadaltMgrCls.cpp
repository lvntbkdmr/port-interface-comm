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

// Accessor for external port wiring
RadaltLruMgrCls& RadaltMgrCls::GetRadaltLruMgr()
{
    return RadaltLruMgr;
}
