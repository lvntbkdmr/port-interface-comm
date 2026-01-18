find_package(GTest REQUIRED)

add_executable(PartitionPkg_tests
    test_PartitionCls.cpp
)

target_link_libraries(PartitionPkg_tests
    PRIVATE
        PartitionPkg
        GTest::gtest
        GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(PartitionPkg_tests DISCOVERY_MODE PRE_TEST)
