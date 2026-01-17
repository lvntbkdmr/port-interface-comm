#include <gtest/gtest.h>
#include <RadaltLruMgrCls.h>
#include <EgiExtDataIfc.h>
#include <EgiExtDataType.h>

class RadaltLruMgrClsTest : public ::testing::Test {
protected:
    RadaltLruMgrCls radaltLruMgr;
};

TEST_F(RadaltLruMgrClsTest, Construction) {
    RadaltLruMgrCls mgr;
    SUCCEED();
}

TEST_F(RadaltLruMgrClsTest, Initialize) {
    radaltLruMgr.Initialize();
    SUCCEED();
}

TEST_F(RadaltLruMgrClsTest, PeriodicRun) {
    radaltLruMgr.PeriodicRun();
    SUCCEED();
}

TEST_F(RadaltLruMgrClsTest, ImplementsEgiExtDataIfc) {
    // RadaltLruMgrCls implements EgiExtDataIfc
    EgiExtDataIfc* ifc = &radaltLruMgr;
    EXPECT_NE(ifc, nullptr);
}

TEST_F(RadaltLruMgrClsTest, SetEgiExtData) {
    EgiExtDataType data;
    data.exampleField = 100;
    radaltLruMgr.SetEgiExtData(data);
    SUCCEED();
}

TEST_F(RadaltLruMgrClsTest, ImplicitUpcastToInterface) {
    // C++ implicitly upcasts to base class pointers
    EgiExtDataIfc* ifc = &radaltLruMgr;
    EXPECT_EQ(ifc, &radaltLruMgr);
}

TEST_F(RadaltLruMgrClsTest, ReceiveMultipleData) {
    EgiExtDataType data1, data2, data3;
    data1.exampleField = 10;
    data2.exampleField = 20;
    data3.exampleField = 30;

    radaltLruMgr.SetEgiExtData(data1);
    radaltLruMgr.SetEgiExtData(data2);
    radaltLruMgr.SetEgiExtData(data3);
    SUCCEED();
}
