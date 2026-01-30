#ifndef EGIFORMATTERCLS_H
#define EGIFORMATTERCLS_H

#include <Ans611ControlIfc.h>

class EgiFormatterCls:
    public Ans611ControlIfc
{
public:
    EgiFormatterCls();
    ~EgiFormatterCls();

    void Initialize();
    void PeriodicRun();

    void SetEgiMode(const Ans611ControlEgiModeType& data) override;
    void SetAns611ControlData(const Ans611ControlEgiModeType& data) override;

    Ans611ControlIfc* GetItsAns611ControlInPortAns611ControlIfc();

private:

protected:
};
#endif