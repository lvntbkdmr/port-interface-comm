#include <EgiCmpCls.h>

EgiCmpCls::EgiCmpCls()
{
    InitRelations();
}

EgiCmpCls::~EgiCmpCls()
{
}

void EgiCmpCls::Initialize()
{
    m_EgiFormatterCls.Initialize();
}

void EgiCmpCls::PeriodicRun()
{
    m_EgiFormatterCls.PeriodicRun();
}

void EgiCmpCls::SetRadaltExtData(const RadaltExtDataType& data)
{
    
}

void EgiCmpCls::InitRelations()
{
    ItsItsAns611ControlInPortAns611ControlIfc = m_EgiFormatterCls.GetItsAns611ControlInPortAns611ControlIfc();
}

RadaltExtDataIfc* EgiCmpCls::GetItsRadaltInPortRadaltExtDataIfc()
{
    return this;
}

Ans611ControlIfc* EgiCmpCls::GetItsAns611ControlInPortAns611ControlIfc()
{
    return ItsItsAns611ControlInPortAns611ControlIfc;
}