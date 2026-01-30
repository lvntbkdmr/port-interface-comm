add_library(EgiCmpPkg STATIC
    src/EgiCmpCls.cpp
    src/EgiFormatterCls.cpp
)

target_include_directories(EgiCmpPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
)

target_link_libraries(EgiCmpPkg PUBLIC
    EgiCmpExtPkg
    RadaltMgrExtPkg
)
