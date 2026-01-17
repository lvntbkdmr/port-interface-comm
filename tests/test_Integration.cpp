#include <gtest/gtest.h>
#include <PartitionCls.h>
#include <EgiExtDataType.h>
#include <RadaltExtDataType.h>

class IntegrationTest : public ::testing::Test {
protected:
    PartitionCls partition;
};

// Test that EgiLruMgr sends data to RadaltLruMgr and it successfully receives it
TEST_F(IntegrationTest, EgiLruMgrSendsDataToRadaltLruMgr) {
    partition.Initialize();

    // Before PeriodicRun, no data should have been received
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 0);

    // Run one periodic cycle - EgiLruMgr should send data to RadaltLruMgr
    partition.PeriodicRun();

    // Verify data was received
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 1);

    // Verify the data value (EgiLruMgrCls sends exampleField = 42)
    const EgiExtDataType& receivedData = partition.GetLastReceivedEgiData();
    EXPECT_EQ(receivedData.exampleField, 42);
}

TEST_F(IntegrationTest, MultiplePeriodicRunsAccumulateData) {
    partition.Initialize();

    // Run multiple periodic cycles
    partition.PeriodicRun();
    partition.PeriodicRun();
    partition.PeriodicRun();

    // Verify all data transmissions were received
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 3);

    // Last received data should still have the expected value
    const EgiExtDataType& receivedData = partition.GetLastReceivedEgiData();
    EXPECT_EQ(receivedData.exampleField, 42);
}

TEST_F(IntegrationTest, DataFlowBeforeInitialize) {
    // Even without calling Initialize(), the port wiring is done in constructor
    // so data should still flow
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 0);

    partition.PeriodicRun();

    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 1);
    EXPECT_EQ(partition.GetLastReceivedEgiData().exampleField, 42);
}

TEST_F(IntegrationTest, EndToEndDataIntegrity) {
    partition.Initialize();

    // Run 10 periodic cycles
    for (int i = 0; i < 10; i++) {
        partition.PeriodicRun();
    }

    // Verify all 10 data transmissions were received
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 10);

    // Data integrity - value should be consistent
    EXPECT_EQ(partition.GetLastReceivedEgiData().exampleField, 42);
}

// Test bidirectional data flow: RadaltLruMgr sends data to EgiCmpCls
TEST_F(IntegrationTest, RadaltLruMgrSendsDataToEgiCmp) {
    partition.Initialize();

    // Before PeriodicRun, no radalt data should have been received
    EXPECT_EQ(partition.GetReceivedRadaltDataCount(), 0);

    // Run one periodic cycle - RadaltLruMgr should send data to EgiCmpCls
    partition.PeriodicRun();

    // Verify data was received
    EXPECT_EQ(partition.GetReceivedRadaltDataCount(), 1);

    // Verify the data value (RadaltLruMgrCls sends altitudeField = 100)
    const RadaltExtDataType& receivedData = partition.GetLastReceivedRadaltData();
    EXPECT_EQ(receivedData.altitudeField, 100);
}

TEST_F(IntegrationTest, BidirectionalDataFlow) {
    partition.Initialize();

    // Before PeriodicRun, no data should have been received in either direction
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 0);
    EXPECT_EQ(partition.GetReceivedRadaltDataCount(), 0);

    // Run one periodic cycle - data should flow in both directions
    partition.PeriodicRun();

    // Verify forward flow: EgiLruMgr -> RadaltLruMgr
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 1);
    EXPECT_EQ(partition.GetLastReceivedEgiData().exampleField, 42);

    // Verify reverse flow: RadaltLruMgr -> EgiCmpCls
    EXPECT_EQ(partition.GetReceivedRadaltDataCount(), 1);
    EXPECT_EQ(partition.GetLastReceivedRadaltData().altitudeField, 100);
}

TEST_F(IntegrationTest, MultipleBidirectionalCycles) {
    partition.Initialize();

    // Run multiple periodic cycles
    for (int i = 0; i < 5; i++) {
        partition.PeriodicRun();
    }

    // Verify all data transmissions were received in both directions
    EXPECT_EQ(partition.GetReceivedEgiDataCount(), 5);
    EXPECT_EQ(partition.GetReceivedRadaltDataCount(), 5);

    // Data integrity
    EXPECT_EQ(partition.GetLastReceivedEgiData().exampleField, 42);
    EXPECT_EQ(partition.GetLastReceivedRadaltData().altitudeField, 100);
}
