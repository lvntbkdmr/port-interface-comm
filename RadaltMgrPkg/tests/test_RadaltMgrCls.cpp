#include <gtest/gtest.h>
#include <RadaltMgrCls.h>
#include <EgiExtDataIfc.h>

class RadaltMgrClsTest : public ::testing::Test {
protected:
    RadaltMgrCls radaltMgr;
};

TEST_F(RadaltMgrClsTest, Construction) {
    RadaltMgrCls mgr;
    SUCCEED();
}

TEST_F(RadaltMgrClsTest, Initialize) {
    radaltMgr.Initialize();
    SUCCEED();
}

TEST_F(RadaltMgrClsTest, PeriodicRun) {
    radaltMgr.PeriodicRun();
    SUCCEED();
}

TEST_F(RadaltMgrClsTest, ImplicitUpcastViaLruMgr) {
    // C++ implicitly upcasts to base class pointers
    RadaltMgrCls mgr;
    EgiExtDataIfc* ifc = &mgr.GetRadaltLruMgr();
    EXPECT_NE(ifc, nullptr);
}

TEST_F(RadaltMgrClsTest, ImplicitUpcast) {
    EgiExtDataIfc* ifc = &radaltMgr.GetRadaltLruMgr();
    EXPECT_NE(ifc, nullptr);
}

TEST_F(RadaltMgrClsTest, FullLifecycle) {
    RadaltMgrCls mgr;
    mgr.Initialize();
    mgr.PeriodicRun();
    mgr.PeriodicRun();
    SUCCEED();
}
