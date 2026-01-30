add_library(EgiMgrPkg STATIC
    src/EgiMgrCls.cpp
    src/EgiLruMgrCls.cpp
    src/EgiModControllerCls.cpp
)

target_include_directories(EgiMgrPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
    ${CMAKE_SOURCE_DIR}/PartitionPkg/inc
)

target_link_libraries(EgiMgrPkg PUBLIC
    EgiCmpPkg
    EgiMgrExtPkg
    EgiCmpExtPkg
    RadaltMgrExtPkg
)
