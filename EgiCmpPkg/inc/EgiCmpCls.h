#ifndef EGICMP_H
#define EGICMP_H

#include <RadaltExtDataIfc.h>
#include <EgiCommandIfc.h>
#include <EgiVorExtDataIfc.h>

class EgiCmpCls:
    public RadaltExtDataIfc,
    public EgiCommandIfc
{
public:
    EgiCmpCls();
    ~EgiCmpCls();

    void Initialize();
    void PeriodicRun();

    void SetVorIlsOut(EgiVorExtDataIfc* port);

    void SetRadaltExtData(const RadaltExtDataType& data) override;
    void SetEgiCommand(const EgiCommandType& cmd) override;

private:
    EgiVorExtDataIfc* m_vorIlsOut{nullptr};
protected:
};
#endif