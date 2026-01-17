#include <VorIlsMgrCls.h>

VorIlsMgrCls::VorIlsMgrCls()
{
}

VorIlsMgrCls::~VorIlsMgrCls()
{
}

void VorIlsMgrCls::Initialize()
{
}

void VorIlsMgrCls::PeriodicRun()
{
    VorIlsLruMgr.PeriodicRun();
}

// Accessor for external port wiring
VorIlsLruMgrCls& VorIlsMgrCls::GetVorIlsLruMgr()
{
    return VorIlsLruMgr;
}
