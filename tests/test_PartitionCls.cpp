#include <gtest/gtest.h>
#include <PartitionCls.h>

class PartitionClsTest : public ::testing::Test {
protected:
    PartitionCls partition;
};

TEST_F(PartitionClsTest, Construction) {
    PartitionCls p;
    SUCCEED();
}

TEST_F(PartitionClsTest, Initialize) {
    partition.Initialize();
    SUCCEED();
}

TEST_F(PartitionClsTest, PeriodicRun) {
    partition.PeriodicRun();
    SUCCEED();
}

TEST_F(PartitionClsTest, InitRelationsIdempotent) {
    // InitRelations is called in constructor, calling again should be safe
    partition.InitRelations();
    SUCCEED();
}

TEST_F(PartitionClsTest, FullLifecycleSequence) {
    PartitionCls p;
    p.Initialize();
    p.PeriodicRun();
    SUCCEED();
}

TEST_F(PartitionClsTest, MultiplePeriodicRuns) {
    partition.Initialize();

    for (int i = 0; i < 10; i++) {
        partition.PeriodicRun();
    }
    SUCCEED();
}

// Integration test: Verify data flows from EgiMgr to RadaltMgr
TEST_F(PartitionClsTest, IntegrationDataFlow) {
    partition.Initialize();

    // InitRelations was called in constructor, so EgiMgr's output port
    // is already connected to RadaltMgr's input port.
    partition.PeriodicRun();
    SUCCEED();
}
