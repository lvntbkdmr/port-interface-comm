find_package(GTest REQUIRED)

# Collect all test source files
set(TEST_SOURCES
    test_EgiCmpCls.cpp
    test_EgiExtDataType.cpp
    test_EgiLruMgrCls.cpp
    test_EgiMgrCls.cpp
    test_Integration.cpp
    test_PartitionCls.cpp
    test_RadaltLruMgrCls.cpp
    test_RadaltMgrCls.cpp
)

# Create test executable
add_executable(run_tests ${TEST_SOURCES})

target_link_libraries(run_tests
    PRIVATE
        PartitionPkg
        GTest::gtest
        GTest::gtest_main
)

# Register tests with CTest
include(GoogleTest)
gtest_discover_tests(run_tests)
