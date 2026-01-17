#ifndef EGICOMMANDIFC_H
#define EGICOMMANDIFC_H

#include <EgiCommandType.h>

class EgiCommandIfc {
public:
    virtual void SetEgiCommand(const EgiCommandType& cmd) = 0;
};

#endif
