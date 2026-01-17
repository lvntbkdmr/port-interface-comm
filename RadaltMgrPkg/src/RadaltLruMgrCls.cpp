#include <RadaltLruMgrCls.h>

#include <PortMacros.h>

RadaltLruMgrCls::RadaltLruMgrCls() : ItsDataOutPortRadaltExtDataIfc(nullptr)
{
}

RadaltLruMgrCls::~RadaltLruMgrCls()
{
}

void RadaltLruMgrCls::Initialize()
{
}

void RadaltLruMgrCls::PeriodicRun()
{
    if (ItsDataOutPortRadaltExtDataIfc != nullptr) {
        RadaltExtDataType RadaltExtData;
        RadaltExtData.altitudeField = 100; // Example altitude data

        OUT_PORT(DataOutPort, RadaltExtDataIfc)->SetRadaltExtData(RadaltExtData);
    }
}

void RadaltLruMgrCls::SetEgiExtData(const EgiExtDataType& data)
{
    m_lastReceivedData = data;
    m_receivedDataCount++;
}

EgiExtDataIfc * RadaltLruMgrCls::GetItsRadaltEgiInPortEgiExtDataIfc()
{
    return this;
}

void RadaltLruMgrCls::SetItsDataOutPortRadaltExtDataIfc(RadaltExtDataIfc* ifc)
{
    ItsDataOutPortRadaltExtDataIfc = ifc;
}

const EgiExtDataType& RadaltLruMgrCls::GetLastReceivedData() const
{
    return m_lastReceivedData;
}

int RadaltLruMgrCls::GetReceivedDataCount() const
{
    return m_receivedDataCount;
}
