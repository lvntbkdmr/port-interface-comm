#include <EgiLruMgrCls.h>

#include <PortMacros.h>

EgiLruMgrCls::EgiLruMgrCls()
{
}

EgiLruMgrCls::~EgiLruMgrCls()
{
}

void EgiLruMgrCls::Initialize()
{
    Egi1ModController.Initialize();
    Egi2ModController.Initialize();
}

void EgiLruMgrCls::setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    ItsDataOutPortEgiExtDataIfc = ifc;
}

void EgiLruMgrCls::SetItsEgi1ControlOutPortAns611ControlIfc(Ans611ControlIfc* ifc)
{
    ItsEgi1ControlOutPortAns611ControlIfc = ifc;

    Egi1ModController.SetItsControlOutPortAns611ControlIfc(ifc);
}

void EgiLruMgrCls::SetItsEgi2ControlOutPortAns611ControlIfc(Ans611ControlIfc* ifc)
{
    ItsEgi2ControlOutPortAns611ControlIfc = ifc;

    Egi2ModController.SetItsControlOutPortAns611ControlIfc(ifc);
}

void EgiLruMgrCls::PeriodicRun()
{
    Egi1ModController.PeriodicRun();
    Egi2ModController.PeriodicRun();

    Ans611ControlEgiModeType EgiControlCmd;
    EgiControlCmd.exampleField = 42; // Example data assignment

    OUT_PORT(Egi1ControlOutPort, Ans611ControlIfc)->SetAns611ControlData(EgiControlCmd);
    OUT_PORT(Egi2ControlOutPort, Ans611ControlIfc)->SetAns611ControlData(EgiControlCmd);

    EgiExtDataType EgiExtData;
    EgiExtData.exampleField = 42; // Example data assignment

    OUT_PORT(DataOutPort, EgiExtDataIfc)->SetEgiExtData(EgiExtData);
}

