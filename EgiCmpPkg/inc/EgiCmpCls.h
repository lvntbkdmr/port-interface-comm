#ifndef EGICMP_H
#define EGICMP_H

#include <RadaltExtDataIfc.h>
#include <Ans611ControlIfc.h>
#include <EgiFormatterCls.h>

class EgiCmpCls:
    public RadaltExtDataIfc
{
public:
    EgiCmpCls();
    ~EgiCmpCls();

    void Initialize();
    void PeriodicRun();

    void InitRelations();

    void SetRadaltExtData(const RadaltExtDataType& data) override;

    RadaltExtDataIfc* GetItsRadaltInPortRadaltExtDataIfc();

    Ans611ControlIfc* GetItsAns611ControlInPortAns611ControlIfc();

private:
    Ans611ControlIfc* ItsItsAns611ControlInPortAns611ControlIfc;

protected:
    EgiFormatterCls m_EgiFormatterCls;
};
#endif