#include <RadaltLruMgrCls.h>

RadaltLruMgrCls::RadaltLruMgrCls() : m_radaltOut(nullptr)
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
    if (m_radaltOut != nullptr) {
        RadaltExtDataType RadaltExtData;
        RadaltExtData.altitudeField = 100; // Example altitude data

        m_radaltOut->SetRadaltExtData(RadaltExtData);
    }
}

void RadaltLruMgrCls::SetEgiExtData(const EgiExtDataType& data)
{
    (void)data;
}

void RadaltLruMgrCls::SetRadaltOut(RadaltExtDataIfc* port)
{
    m_radaltOut = port;
}
