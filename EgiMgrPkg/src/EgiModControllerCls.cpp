#include <EgiModControllerCls.h>

#include <PortMacros.h>

EgiModControllerCls::EgiModControllerCls()
{
}

EgiModControllerCls::~EgiModControllerCls()
{
}

void EgiModControllerCls::Initialize()
{

}

void EgiModControllerCls::SetItsControlOutPortAns611ControlIfc(Ans611ControlIfc* ifc)
{
    ItsControlOutPortAns611ControlIfc = ifc;
}

void EgiModControllerCls::PeriodicRun()
{
    Ans611ControlEgiModeType EgiControlCmd;
    EgiControlCmd.exampleField = 1;

    OUT_PORT(ControlOutPort, Ans611ControlIfc)->SetAns611ControlData(EgiControlCmd);
}

