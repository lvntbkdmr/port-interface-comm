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

    EgiExtDataIfc * GetItsRadaltEgiInPortEgiExtDataIfc();

    void SetItsDataOutPortRadaltExtDataIfc(RadaltExtDataIfc* ifc);

private:
protected:
    RadaltExtDataIfc* ItsDataOutPortRadaltExtDataIfc;
};
#endif
