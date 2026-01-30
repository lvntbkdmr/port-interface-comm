#ifndef EGIMGR_H
#define EGIMGR_H

#include <EgiLruMgrCls.h>
#include <EgiCmpCls.h>
#include <EgiExtDataIfc.h>
#include <Ans611ControlIfc.h>
#include <RadaltExtDataIfc.h>

class EgiMgrCls:
    public RadaltExtDataIfc
{
private:
    /* data */
public:
    EgiMgrCls(/* args */);
    ~EgiMgrCls();

    void Initialize();
    void PeriodicRun();

    void InitRelations();

    void SetRadaltExtData(const RadaltExtDataType& data) override;

    void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);

    RadaltExtDataIfc* GetItsRadaltInPortRadaltExtDataIfc();

private:
    EgiLruMgrCls EgiLruMgr;
    EgiCmpCls Egi1Cmp;
    EgiCmpCls Egi2Cmp;

protected:
    RadaltExtDataIfc* ItsEgi1RadaltInPortRadaltExtDataIfc;
    RadaltExtDataIfc* ItsEgi2RadaltInPortRadaltExtDataIfc;

};

#endif