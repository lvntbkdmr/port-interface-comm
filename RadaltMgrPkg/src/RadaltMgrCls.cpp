#include <RadaltMgrCls.h>

RadaltMgrCls::RadaltMgrCls(/* args */)
{
    InitRelations();
}

RadaltMgrCls::~RadaltMgrCls()
{
}

void RadaltMgrCls::Initialize()
{
    RadaltLruMgr.Initialize();
}

void RadaltMgrCls::PeriodicRun()
{
    RadaltLruMgr.PeriodicRun();
}

void RadaltMgrCls::SetItsDataOutPortRadaltExtDataIfc(RadaltExtDataIfc* ifc)
{
    RadaltLruMgr.SetItsDataOutPortRadaltExtDataIfc(ifc);
}

EgiExtDataIfc * RadaltMgrCls::GetItsRadaltEgiInPortEgiExtDataIfc()
{
    return ItsItsRadaltEgiInPortEgiExtDataIfc;
}

void RadaltMgrCls::InitRelations()
{
    ItsItsRadaltEgiInPortEgiExtDataIfc = RadaltLruMgr.GetItsRadaltEgiInPortEgiExtDataIfc();
}
