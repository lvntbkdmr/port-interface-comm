#ifndef EGIEXTDATAIFC_H
#define EGIEXTDATAIFC_H

#include <EgiExtDataType.h>

class EgiExtDataIfc
{
public:
    virtual void SetEgiExtData(const EgiExtDataType& data) = 0;

};
#endif