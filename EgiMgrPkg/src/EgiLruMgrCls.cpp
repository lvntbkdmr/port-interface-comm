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
    m_EgiCmpCls.Initialize();
}

void EgiLruMgrCls::setItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    ItsDataOutPortEgiExtDataIfc = ifc;
}

void EgiLruMgrCls::PeriodicRun()
{
    m_EgiCmpCls.PeriodicRun();

    EgiExtDataType EgiExtData;
    EgiExtData.exampleField = 42; // Example data assignment

    OUT_PORT(DataOutPort, EgiExtDataIfc)->SetEgiExtData(EgiExtData);
}

