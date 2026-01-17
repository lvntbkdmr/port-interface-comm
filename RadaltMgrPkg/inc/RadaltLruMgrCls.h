#ifndef RADALTLRUMGR_H
#define RADALTLRUMGR_H

#include <EgiExtDataIfc.h>

class RadaltLruMgrCls:
    public EgiExtDataIfc
{
public:
    RadaltLruMgrCls();
    ~RadaltLruMgrCls();

    void Initialize();
    void PeriodicRun(); 

    void SetEgiExtData(const EgiExtDataType& data) override;

    EgiExtDataIfc * GetItsRadaltEgiInPortEgiExtDataIfc();

private:
protected:
};
#endif
