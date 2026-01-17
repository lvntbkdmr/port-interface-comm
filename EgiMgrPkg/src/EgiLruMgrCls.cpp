#include <EgiLruMgrCls.h>

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

void EgiLruMgrCls::SetEgiOut(EgiExtDataIfc* port)
{
    m_egiOut = port;
}

void EgiLruMgrCls::PeriodicRun()
{
    m_EgiCmpCls.PeriodicRun();

    EgiExtDataType EgiExtData;
    EgiExtData.exampleField = 42; // Example data assignment

    m_egiOut->SetEgiExtData(EgiExtData);
}

EgiCmpCls& EgiLruMgrCls::GetEgiCmp()
{
    return m_EgiCmpCls;
}
