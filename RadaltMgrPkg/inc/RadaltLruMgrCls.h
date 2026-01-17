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

    EgiExtDataIfc* GetEgiIn();

    void SetRadaltOut(RadaltExtDataIfc* port);

    const EgiExtDataType& GetLastReceivedData() const;
    int GetReceivedDataCount() const;

private:
    EgiExtDataType m_lastReceivedData{};
    int m_receivedDataCount{0};
    RadaltExtDataIfc* m_radaltOut;
};
#endif
