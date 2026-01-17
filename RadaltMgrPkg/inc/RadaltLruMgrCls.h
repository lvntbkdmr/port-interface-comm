#ifndef RADALTLRUMGR_H
#define RADALTLRUMGR_H

#include <EgiExtDataIfc.h>
#include <RadaltExtDataIfc.h>

class RadaltLruMgrCls:
    public EgiExtDataIfc
{
public:
    RadaltLruMgrCls();
    ~RadaltLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void SetEgiExtData(const EgiExtDataType& data) override;

    void SetRadaltOut(RadaltExtDataIfc* port);

private:
    RadaltExtDataIfc* m_radaltOut;
};
#endif
