find_package(GTest REQUIRED)

add_executable(EgiCmpPkg_tests
    test_EgiCmpCls.cpp
)

target_link_libraries(EgiCmpPkg_tests
    PRIVATE
        EgiCmpPkg
        GTest::gtest
        GTest::gtest_main
)

include(GoogleTest)
gtest_discover_tests(EgiCmpPkg_tests DISCOVERY_MODE PRE_TEST)
