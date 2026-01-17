#include <EgiLruMgrCls.h>
#include <EgiCommandType.h>

EgiLruMgrCls::EgiLruMgrCls()
{
}

EgiLruMgrCls::~EgiLruMgrCls()
{
}

void EgiLruMgrCls::Initialize()
{
}

// Set output port for EGI external data (connects to RadaltLruMgr)
void EgiLruMgrCls::SetEgiOut(EgiExtDataIfc* port)
{
    m_egiOut = port;
}

// Set output port for command messages (connects to EgiCmp)
void EgiLruMgrCls::SetCommandOut(EgiCommandIfc* port)
{
    m_commandOut = port;
}

void EgiLruMgrCls::PeriodicRun()
{
    // Send EGI external data to RadaltLruMgr
    if (m_egiOut != nullptr) {
        EgiExtDataType EgiExtData;
        EgiExtData.exampleField = 42;

        m_egiOut->SetEgiExtData(EgiExtData);
    }

    // Send command to EgiCmp
    if (m_commandOut != nullptr) {
        EgiCommandType cmd;
        cmd.commandId = 1;
        cmd.commandValue = 100.0f;

        m_commandOut->SetEgiCommand(cmd);
    }
}
