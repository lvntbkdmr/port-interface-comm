#include <EgiFormatterCls.h>

EgiFormatterCls::EgiFormatterCls()
{
}

EgiFormatterCls::~EgiFormatterCls()
{
}

void EgiFormatterCls::Initialize()
{
}

void EgiFormatterCls::PeriodicRun()
{
}

void EgiFormatterCls::SetEgiMode(const Ans611ControlEgiModeType& data)
{
}

void EgiFormatterCls::SetAns611ControlData(const Ans611ControlEgiModeType& data)
{
    SetEgiMode(data);
}

Ans611ControlIfc* EgiFormatterCls::GetItsAns611ControlInPortAns611ControlIfc()
{
    return this;
}