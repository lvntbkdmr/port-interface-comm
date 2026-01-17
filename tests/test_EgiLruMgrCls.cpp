#include <gtest/gtest.h>
#include <EgiLruMgrCls.h>
#include <EgiExtDataIfc.h>
#include <EgiExtDataType.h>

// Mock implementation of EgiExtDataIfc for testing
class MockEgiExtDataIfc : public EgiExtDataIfc {
public:
    MockEgiExtDataIfc() : callCount(0), lastData{0} {}

    void SetEgiExtData(const EgiExtDataType& data) override {
        lastData = data;
        callCount++;
    }

    int callCount;
    EgiExtDataType lastData;
};

class EgiLruMgrClsTest : public ::testing::Test {
protected:
    EgiLruMgrCls egiLruMgr;
    MockEgiExtDataIfc mockIfc;

    void SetUp() override {
        egiLruMgr.SetItsDataOutPortEgiExtDataIfc(&mockIfc);
    }
};

TEST_F(EgiLruMgrClsTest, Construction) {
    EgiLruMgrCls mgr;
    SUCCEED();
}

TEST_F(EgiLruMgrClsTest, Initialize) {
    egiLruMgr.Initialize();
    SUCCEED();
}

TEST_F(EgiLruMgrClsTest, SetPortInterface) {
    EgiLruMgrCls mgr;
    MockEgiExtDataIfc ifc;
    mgr.SetItsDataOutPortEgiExtDataIfc(&ifc);
    SUCCEED();
}

TEST_F(EgiLruMgrClsTest, PeriodicRunSendsData) {
    egiLruMgr.Initialize();
    egiLruMgr.PeriodicRun();

    EXPECT_EQ(mockIfc.callCount, 1);
    EXPECT_EQ(mockIfc.lastData.exampleField, 42);
}

TEST_F(EgiLruMgrClsTest, MultiplePeriodicRuns) {
    egiLruMgr.Initialize();

    egiLruMgr.PeriodicRun();
    egiLruMgr.PeriodicRun();
    egiLruMgr.PeriodicRun();

    EXPECT_EQ(mockIfc.callCount, 3);
}
