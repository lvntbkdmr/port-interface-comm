#include <gtest/gtest.h>
#include <EgiMgrCls.h>
#include <EgiExtDataIfc.h>
#include <EgiExtDataType.h>

// Mock implementation of EgiExtDataIfc for testing
class MockEgiExtDataIfcForMgr : public EgiExtDataIfc {
public:
    MockEgiExtDataIfcForMgr() : callCount(0), lastData{0} {}

    void SetEgiExtData(const EgiExtDataType& data) override {
        lastData = data;
        callCount++;
    }

    int callCount;
    EgiExtDataType lastData;
};

class EgiMgrClsTest : public ::testing::Test {
protected:
    EgiMgrCls egiMgr;
    MockEgiExtDataIfcForMgr mockIfc;

    void SetUp() override {
        egiMgr.GetEgiLruMgr().SetEgiOut(&mockIfc);
    }
};

TEST_F(EgiMgrClsTest, Construction) {
    EgiMgrCls mgr;
    SUCCEED();
}

TEST_F(EgiMgrClsTest, Initialize) {
    egiMgr.Initialize();
    SUCCEED();
}

TEST_F(EgiMgrClsTest, SetPortInterfaceViaLruMgr) {
    EgiMgrCls mgr;
    MockEgiExtDataIfcForMgr ifc;
    mgr.GetEgiLruMgr().SetEgiOut(&ifc);
    SUCCEED();
}

TEST_F(EgiMgrClsTest, PeriodicRunDelegates) {
    egiMgr.Initialize();
    egiMgr.PeriodicRun();

    EXPECT_EQ(mockIfc.callCount, 1);
    EXPECT_EQ(mockIfc.lastData.exampleField, 42);
}

TEST_F(EgiMgrClsTest, FullLifecycle) {
    EgiMgrCls mgr;
    MockEgiExtDataIfcForMgr ifc;

    mgr.GetEgiLruMgr().SetEgiOut(&ifc);
    mgr.Initialize();
    mgr.PeriodicRun();
    mgr.PeriodicRun();

    EXPECT_EQ(ifc.callCount, 2);
}
