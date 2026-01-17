#include <gtest/gtest.h>
#include <PartitionCls.h>

class IntegrationTest : public ::testing::Test {
protected:
    PartitionCls partition;
};

TEST_F(IntegrationTest, PartitionConstruction) {
    // Partition constructs successfully with all port wiring done
    SUCCEED();
}

TEST_F(IntegrationTest, PartitionInitialize) {
    partition.Initialize();
    SUCCEED();
}

TEST_F(IntegrationTest, PartitionPeriodicRun) {
    partition.Initialize();
    partition.PeriodicRun();
    SUCCEED();
}

TEST_F(IntegrationTest, MultiplePeriodicRuns) {
    partition.Initialize();

    for (int i = 0; i < 10; i++) {
        partition.PeriodicRun();
    }

    SUCCEED();
}

TEST_F(IntegrationTest, PeriodicRunBeforeInitialize) {
    // Port wiring is done in constructor, so PeriodicRun should work
    partition.PeriodicRun();
    SUCCEED();
}
