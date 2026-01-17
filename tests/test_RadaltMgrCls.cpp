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

TEST_F(RadaltMgrClsTest, InitRelationsIdempotent) {
    // InitRelations is called in constructor, calling again should be safe
    radaltMgr.InitRelations();
    SUCCEED();
}

TEST_F(RadaltMgrClsTest, GetPortInterfaceViaLruMgr) {
    // Access port via LRU manager
    RadaltMgrCls mgr;
    EgiExtDataIfc* ifc = mgr.GetRadaltLruMgr().GetItsRadaltEgiInPortEgiExtDataIfc();
    EXPECT_NE(ifc, nullptr);
}

TEST_F(RadaltMgrClsTest, GetPortInterface) {
    EgiExtDataIfc* ifc = radaltMgr.GetRadaltLruMgr().GetItsRadaltEgiInPortEgiExtDataIfc();
    EXPECT_NE(ifc, nullptr);
}

TEST_F(RadaltMgrClsTest, FullLifecycle) {
    RadaltMgrCls mgr;
    mgr.Initialize();
    mgr.PeriodicRun();
    mgr.PeriodicRun();
    SUCCEED();
}
