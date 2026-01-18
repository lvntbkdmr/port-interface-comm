# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

### CMake Build (Recommended)

```bash
# Configure and build all libraries and tests
mkdir build && cd build
cmake ..
cmake --build .

# Run all tests
ctest --output-on-failure

# Run a single test suite
./tests/run_tests --gtest_filter=IntegrationTest.*

# Run a single test
./tests/run_tests --gtest_filter=IntegrationTest.PartitionConstruction

# Build without tests
cmake -DBUILD_TESTS=OFF ..
cmake --build .
```

### Manual Build (Legacy)

```bash
# Compile and run all tests
clang++ -std=c++17 \
  -I /opt/homebrew/include \
  -I EgiMgrPkg/inc \
  -I EgiMgrExtPkg \
  -I EgiCmpPkg/inc \
  -I EgiCmpExtPkg \
  -I PartitionPkg/inc \
  -I RadaltMgrPkg/inc \
  -I RadaltMgrExtPkg \
  -I VorIlsMgrPkg/inc \
  -L /opt/homebrew/lib \
  -lgtest -lgtest_main -pthread \
  tests/test_*.cpp \
  EgiMgrPkg/src/*.cpp \
  EgiCmpPkg/src/*.cpp \
  PartitionPkg/src/*.cpp \
  RadaltMgrPkg/src/*.cpp \
  VorIlsMgrPkg/src/*.cpp \
  -o out/run_tests && ./out/run_tests
```

## Architecture

This is a component-based C++ project implementing port-based inter-component communication, following patterns typical of avionics/real-time systems.

### Component Hierarchy

```
PartitionCls (top-level container)
├── EgiMgrCls (EGI manager)
│   ├── EgiLruMgrCls (LRU manager)
│   └── EgiCmpCls (component)
├── RadaltMgrCls (Radar Altimeter manager)
│   └── RadaltLruMgrCls (LRU manager)
└── VorIlsMgrCls (VOR/ILS manager)
    └── VorIlsLruMgrCls (LRU manager)
```

### Port Interface Pattern

Components communicate through typed port interfaces using a simple naming convention:
- Output ports: `m_egiOut`, `m_radaltOut` (member variables)
- Setters: `SetEgiOut()`, `SetRadaltOut()`
- Input ports: C++ implicitly upcasts to interface pointers (e.g., `&radaltLruMgr` → `EgiExtDataIfc*`)

### Lifecycle Methods

All manager classes follow a consistent lifecycle:
1. Constructor calls `InitRelations()` to wire up port connections
2. `Initialize()` initializes sub-components
3. `PeriodicRun()` executes the periodic processing cycle

### Key Interfaces

- `EgiExtDataIfc` - Abstract interface for receiving EGI external data
- `EgiCommandIfc` - Abstract interface for receiving EGI commands
- `RadaltExtDataIfc` - Abstract interface for receiving radar altimeter data
- `EgiVorExtDataIfc` - Abstract interface for receiving VOR/ILS navigation data

### Package Structure

Each package is a separate CMake library project:

| Package | Type | Description |
|---------|------|-------------|
| EgiMgrExtPkg | Interface (header-only) | EGI external interfaces and types |
| RadaltMgrExtPkg | Interface (header-only) | Radar altimeter external interfaces |
| EgiCmpExtPkg | Interface (header-only) | EGI component external interfaces |
| EgiCmpPkg | Library | EGI component implementation |
| EgiMgrPkg | Library | EGI manager implementation |
| RadaltMgrPkg | Library | Radar altimeter manager implementation |
| VorIlsMgrPkg | Library | VOR/ILS manager implementation |
| PartitionPkg | Library | Top-level partition container |
