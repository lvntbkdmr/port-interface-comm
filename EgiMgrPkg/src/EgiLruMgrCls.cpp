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

void EgiLruMgrCls::SetEgiOut(EgiExtDataIfc* port)
{
    m_egiOut = port;
}

void EgiLruMgrCls::SetCommandOut(EgiCommandIfc* port)
{
    m_commandOut = port;
}

void EgiLruMgrCls::PeriodicRun()
{
    if (m_egiOut != nullptr) {
        EgiExtDataType EgiExtData;
        EgiExtData.exampleField = 42; // Example data assignment

        m_egiOut->SetEgiExtData(EgiExtData);
    }

    if (m_commandOut != nullptr) {
        EgiCommandType cmd;
        cmd.commandId = 1;
        cmd.commandValue = 100.0f;

        m_commandOut->SetEgiCommand(cmd);
    }
}
