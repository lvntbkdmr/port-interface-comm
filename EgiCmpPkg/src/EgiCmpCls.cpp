#include <EgiCmpCls.h>
#include <EgiExtDataType.h>

EgiCmpCls::EgiCmpCls()
{
}

EgiCmpCls::~EgiCmpCls()
{
}

void EgiCmpCls::Initialize()
{
}

// Set output port for VOR/ILS data (connects to VorIlsLruMgr)
void EgiCmpCls::SetVorIlsOut(EgiVorExtDataIfc* port)
{
    m_vorIlsOut = port;
}

void EgiCmpCls::PeriodicRun()
{
    // Send VOR/ILS navigation data to VorIlsLruMgr
    if (m_vorIlsOut != nullptr) {
        EgiVorExtDataType data;
        data.latitude = 37.7749;
        data.longitude = -122.4194;

        m_vorIlsOut->SetEgiVorExtData(data);
    }
}

// Receive radar altimeter data from RadaltLruMgr
void EgiCmpCls::SetRadaltExtData(const RadaltExtDataType& data)
{
    (void)data;
}

// Receive command from EgiLruMgr
void EgiCmpCls::SetEgiCommand(const EgiCommandType& cmd)
{
    (void)cmd;
}
