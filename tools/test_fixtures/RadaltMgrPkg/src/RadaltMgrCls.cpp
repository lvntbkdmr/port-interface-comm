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
}

EgiExtDataIfc* RadaltMgrCls::GetItsRadaltEgiInPortEgiExtDataIfc()
{
    return ItsRadaltEgiInPortEgiExtDataIfc;
}

void RadaltMgrCls::InitRelations()
{
    ItsRadaltEgiInPortEgiExtDataIfc = RadaltLruMgr.GetItsRadaltEgiInPortEgiExtDataIfc();
}
