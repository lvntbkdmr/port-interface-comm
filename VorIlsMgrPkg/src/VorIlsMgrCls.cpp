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

VorIlsLruMgrCls& VorIlsMgrCls::GetVorIlsLruMgr()
{
    return VorIlsLruMgr;
}
