#include <gtest/gtest.h>
#include <EgiCmpCls.h>

class EgiCmpClsTest : public ::testing::Test {
protected:
    EgiCmpCls egiCmp;
};

TEST_F(EgiCmpClsTest, Construction) {
    EgiCmpCls cmp;
    SUCCEED();
}

TEST_F(EgiCmpClsTest, Initialize) {
    egiCmp.Initialize();
    SUCCEED();
}

TEST_F(EgiCmpClsTest, PeriodicRun) {
    egiCmp.PeriodicRun();
    SUCCEED();
}

TEST_F(EgiCmpClsTest, LifecycleSequence) {
    EgiCmpCls cmp;
    cmp.Initialize();
    cmp.PeriodicRun();
    cmp.PeriodicRun();
    cmp.PeriodicRun();
    SUCCEED();
}
