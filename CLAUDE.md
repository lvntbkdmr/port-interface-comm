# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

### Host Build (Development & Testing)

```bash
# Configure and build with tests
cmake -B build -DBUILD_TESTS=ON
cmake --build build

# Run all tests
cd build && ctest --output-on-failure

# Run specific test suite
ctest -R EgiCmpClsTest

# Run integration tests only
ctest -R IntegrationTest

# List all available tests
ctest -N
```

### Cross-Compilation (Target Deployment)

```bash
# Copy and customize toolchain file
cp cmake/toolchain-target.cmake.example cmake/toolchain-target.cmake
# Edit with your cross-compiler paths

# Build for target (tests disabled automatically)
cmake -B build-target -DCMAKE_TOOLCHAIN_FILE=cmake/toolchain-target.cmake
cmake --build build-target
```

### Build Options

| Option | Default | Description |
|--------|---------|-------------|
| `BUILD_TESTS` | ON | Build unit and integration tests |
| `USE_VENDORED_GTEST` | ON | Use GoogleTest from third_party/ |

```bash
# Use system GoogleTest instead of vendored
cmake -B build -DBUILD_TESTS=ON -DUSE_VENDORED_GTEST=OFF
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
- Output ports: `m_egiOut`, `m_radaltOut`, `m_commandOut` (member variables)
- Setters: `SetEgiOut()`, `SetRadaltOut()`, `SetCommandOut()`
- Input ports: C++ implicitly upcasts to interface pointers (e.g., `&radaltLruMgr` → `EgiExtDataIfc*`)

### Lifecycle Methods

All manager classes follow a consistent lifecycle:
1. Constructor calls `InitRelations()` to wire up port connections
2. `Initialize()` initializes sub-components
3. `PeriodicRun()` executes the periodic processing cycle

### Key Interfaces

| Interface | Location | Description |
|-----------|----------|-------------|
| EgiExtDataIfc | EgiMgrExtPkg/ | Receiving EGI external data |
| EgiCommandIfc | EgiMgrExtPkg/ | Receiving EGI commands |
| RadaltExtDataIfc | RadaltMgrExtPkg/ | Receiving radar altimeter data |
| EgiVorExtDataIfc | EgiCmpExtPkg/ | Receiving VOR/ILS navigation data |

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

### Test Structure

Unit tests are located in each package's `tests/` directory:

| Package | Test Executable | Test Suites |
|---------|-----------------|-------------|
| EgiCmpPkg/tests | EgiCmpPkg_tests | EgiCmpClsTest |
| EgiMgrPkg/tests | EgiMgrPkg_tests | EgiLruMgrClsTest, EgiMgrClsTest |
| EgiMgrExtPkg/tests | EgiMgrExtPkg_tests | EgiExtDataTypeTest |
| RadaltMgrPkg/tests | RadaltMgrPkg_tests | RadaltLruMgrClsTest, RadaltMgrClsTest |
| PartitionPkg/tests | PartitionPkg_tests | PartitionClsTest |
| tests/ | integration_tests | IntegrationTest |

### Dependencies

- GoogleTest is vendored in `third_party/googletest/` for offline builds
- No external dependencies required for intranet development
