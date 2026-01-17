#ifndef EGICMP_H
#define EGICMP_H

#include <RadaltExtDataIfc.h>

class EgiCmpCls:
    public RadaltExtDataIfc
{
public:
    EgiCmpCls();
    ~EgiCmpCls();

    void Initialize();
    void PeriodicRun();

    void SetRadaltExtData(const RadaltExtDataType& data) override;

    const RadaltExtDataType& GetLastReceivedData() const;
    int GetReceivedDataCount() const;

private:
    RadaltExtDataType m_lastReceivedData{};
    int m_receivedDataCount{0};
protected:
};
#endif