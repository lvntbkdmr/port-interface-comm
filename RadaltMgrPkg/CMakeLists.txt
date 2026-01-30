add_library(RadaltMgrPkg STATIC
    src/RadaltMgrCls.cpp
    src/RadaltLruMgrCls.cpp
)

target_include_directories(RadaltMgrPkg PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/inc
    ${CMAKE_SOURCE_DIR}/PartitionPkg/inc
)

target_link_libraries(RadaltMgrPkg PUBLIC
    EgiMgrExtPkg
    RadaltMgrExtPkg
)
