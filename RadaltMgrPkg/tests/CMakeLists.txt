find_package(GTest REQUIRED)

add_executable(RadaltMgrPkg_tests
    test_RadaltLruMgrCls.cpp
    test_RadaltMgrCls.cpp
)

target_link_libraries(RadaltMgrPkg_tests
    PRIVATE
        RadaltMgrPkg
        GTest::gtest
        GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(RadaltMgrPkg_tests DISCOVERY_MODE PRE_TEST)
