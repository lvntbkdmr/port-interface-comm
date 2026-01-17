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

void EgiCmpCls::SetVorIlsOut(EgiVorExtDataIfc* port)
{
    m_vorIlsOut = port;
}

void EgiCmpCls::PeriodicRun()
{
    if (m_vorIlsOut != nullptr) {
        EgiVorExtDataType data;
        data.latitude = 37.7749;
        data.longitude = -122.4194;

        m_vorIlsOut->SetEgiVorExtData(data);
    }
}

void EgiCmpCls::SetRadaltExtData(const RadaltExtDataType& data)
{
    (void)data;
}

void EgiCmpCls::SetEgiCommand(const EgiCommandType& cmd)
{
    (void)cmd;
}
