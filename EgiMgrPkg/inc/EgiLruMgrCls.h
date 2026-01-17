#ifndef EGILRUMGR_H
#define EGILRUMGR_H

#include <EgiExtDataIfc.h>
#include <EgiCommandIfc.h>

class EgiLruMgrCls
{
public:
    EgiLruMgrCls();
    ~EgiLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void SetEgiOut(EgiExtDataIfc* port);
    void SetCommandOut(EgiCommandIfc* port);

private:
    EgiExtDataIfc* m_egiOut{nullptr};
    EgiCommandIfc* m_commandOut{nullptr};
};
#endif