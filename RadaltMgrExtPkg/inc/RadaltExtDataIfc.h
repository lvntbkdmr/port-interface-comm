#ifndef RADALTEXTDATAIFC_H
#define RADALTEXTDATAIFC_H

#include <RadaltExtDataType.h>

class RadaltExtDataIfc
{
public:
    virtual void SetRadaltExtData(const RadaltExtDataType& data) = 0;

};
#endif