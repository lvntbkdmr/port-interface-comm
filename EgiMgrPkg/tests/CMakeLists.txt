add_executable(EgiMgrPkg_tests
    test_EgiLruMgrCls.cpp
    test_EgiMgrCls.cpp
)

target_link_libraries(EgiMgrPkg_tests
    PRIVATE
        EgiMgrPkg
        GTest::gtest
        GTest::gtest_main
)

gtest_discover_tests(EgiMgrPkg_tests DISCOVERY_MODE PRE_TEST)
