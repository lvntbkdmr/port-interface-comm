#include <EgiCmpCls.h>

EgiCmpCls::EgiCmpCls()
{
}

EgiCmpCls::~EgiCmpCls()
{
}

void EgiCmpCls::Initialize()
{
}

void EgiCmpCls::PeriodicRun()
{
}

void EgiCmpCls::SetRadaltExtData(const RadaltExtDataType& data)
{
    m_lastReceivedData = data;
    m_receivedDataCount++;
}

const RadaltExtDataType& EgiCmpCls::GetLastReceivedData() const
{
    return m_lastReceivedData;
}

int EgiCmpCls::GetReceivedDataCount() const
{
    return m_receivedDataCount;
}
