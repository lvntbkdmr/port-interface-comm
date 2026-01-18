add_executable(EgiMgrExtPkg_tests
    test_EgiExtDataType.cpp
)

target_link_libraries(EgiMgrExtPkg_tests
    PRIVATE
        EgiMgrExtPkg
        GTest::gtest
        GTest::gtest_main
)

gtest_discover_tests(EgiMgrExtPkg_tests DISCOVERY_MODE PRE_TEST)
