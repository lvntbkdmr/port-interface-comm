#ifndef ANS611CONTROLIFC_H
#define ANS611CONTROLIFC_H

#include <Ans611ControlDataType.h>

class Ans611ControlIfc
{
public:
    virtual void SetEgiMode(const Ans611ControlEgiModeType& data) = 0;
    virtual void SetAns611ControlData(const Ans611ControlEgiModeType& data) = 0;
};

#endif
