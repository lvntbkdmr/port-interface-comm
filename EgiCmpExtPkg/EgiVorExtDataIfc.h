#ifndef EGIVOREXTDATAIFC_H
#define EGIVOREXTDATAIFC_H

#include <EgiExtDataType.h>

class EgiVorExtDataIfc
{
public:
    virtual void SetEgiVorExtData(const EgiVorExtDataType& data) = 0;
};

#endif
