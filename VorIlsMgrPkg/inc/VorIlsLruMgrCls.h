#ifndef VORILSLRUMGR_H
#define VORILSLRUMGR_H

#include <EgiVorExtDataIfc.h>

class VorIlsLruMgrCls:
    public EgiVorExtDataIfc
{
public:
    VorIlsLruMgrCls();
    ~VorIlsLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void SetEgiVorExtData(const EgiVorExtDataType& data) override;
};
#endif
