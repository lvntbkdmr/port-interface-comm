#include <EgiMgrCls.h>
#include <PortMacros.h>

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
    Egi1Cmp.Initialize();
    Egi2Cmp.Initialize();
}

void EgiMgrCls::PeriodicRun()
{
    Egi1Cmp.PeriodicRun();
    Egi2Cmp.PeriodicRun();
    EgiLruMgr.PeriodicRun();
}

void EgiMgrCls::SetRadaltExtData(const RadaltExtDataType& data)
{
    // Implementation for handling the Radalt external data
    OUT_PORT(Egi1RadaltInPort, RadaltExtDataIfc)->SetRadaltExtData(data);
    OUT_PORT(Egi2RadaltInPort, RadaltExtDataIfc)->SetRadaltExtData(data);
}

void EgiMgrCls::InitRelations()
{
    Ans611ControlIfc* Egi1CmpControlIfc = Egi1Cmp.GetItsAns611ControlInPortAns611ControlIfc();
    EgiLruMgr.SetItsEgi1ControlOutPortAns611ControlIfc(Egi1CmpControlIfc);

    Ans611ControlIfc* Egi2CmpControlIfc = Egi2Cmp.GetItsAns611ControlInPortAns611ControlIfc();
    EgiLruMgr.SetItsEgi2ControlOutPortAns611ControlIfc(Egi2CmpControlIfc);

    ItsEgi1RadaltInPortRadaltExtDataIfc = Egi1Cmp.GetItsRadaltInPortRadaltExtDataIfc();
    ItsEgi2RadaltInPortRadaltExtDataIfc = Egi2Cmp.GetItsRadaltInPortRadaltExtDataIfc();
}

void EgiMgrCls::SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    EgiLruMgr.setItsDataOutPortEgiExtDataIfc(ifc);
}

RadaltExtDataIfc* EgiMgrCls::GetItsRadaltInPortRadaltExtDataIfc()
{
    return this;
}


