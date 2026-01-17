#include <RadaltMgrCls.h>

RadaltMgrCls::RadaltMgrCls(/* args */)
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

EgiExtDataIfc * RadaltMgrCls::GetItsRadaltEgiInPortEgiExtDataIfc()
{
    return ItsRadaltEgiInPortEgiExtDataIfc;
}

void RadaltMgrCls::InitRelations()
{
    ItsItsRadaltEgiInPortEgiExtDataIfc = RadaltLruMgr.GetItsRadaltEgiInPortEgiExtDataIfc();
}
