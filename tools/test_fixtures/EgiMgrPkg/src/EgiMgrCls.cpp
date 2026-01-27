#include <EgiMgrCls.h>

EgiMgrCls::EgiMgrCls()
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
    ItsDataOutPortEgiExtDataIfc = nullptr;
}

void EgiMgrCls::SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    ItsDataOutPortEgiExtDataIfc = ifc;
}
