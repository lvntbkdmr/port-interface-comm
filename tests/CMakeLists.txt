find_package(GTest REQUIRED)

# Integration tests only
# Unit tests are in each package's tests/ directory
add_executable(integration_tests
    test_Integration.cpp
)

target_link_libraries(integration_tests
    PRIVATE
        PartitionPkg
        GTest::gtest
        GTest::gtest_main
)

# Register tests with CTest
include(GoogleTest)
gtest_discover_tests(integration_tests DISCOVERY_MODE PRE_TEST)
