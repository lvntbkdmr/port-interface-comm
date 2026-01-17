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
    // Send radar altimeter data to EgiCmp
    if (m_radaltOut != nullptr) {
        RadaltExtDataType RadaltExtData;
        RadaltExtData.altitudeField = 100;

        m_radaltOut->SetRadaltExtData(RadaltExtData);
    }
}

// Receive EGI external data from EgiLruMgr
void RadaltLruMgrCls::SetEgiExtData(const EgiExtDataType& data)
{
    (void)data;
}

// Set output port for radar altimeter data (connects to EgiCmp)
void RadaltLruMgrCls::SetRadaltOut(RadaltExtDataIfc* port)
{
    m_radaltOut = port;
}
