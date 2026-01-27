# Port Analyzer Tool Design

A Python tool that statically analyzes C++ code to detect port connections between classes in a partition-based component system.

## Overview

- **Input**: Partition class name (e.g., `PartitionCls`)
- **Output**: ASCII diagram showing component hierarchy and port connections
- **Technology**: Tree-sitter with tree-sitter-cpp for AST parsing
- **Source**: Working directory files (run from project root)

## Target Code Pattern

Analyzes the old port pattern with naming conventions:
- Output ports: `ItsDataOutPortEgiExtDataIfc` member + `SetItsDataOutPortEgiExtDataIfc()` setter
- Input ports: `GetItsRadaltEgiInPortEgiExtDataIfc()` getter
- Wiring: Assignments in `InitRelations()` methods

## Data Model

```python
ClassInfo:
    name: str                    # "EgiMgrCls"
    header_path: str             # "EgiMgrPkg/inc/EgiMgrCls.h"
    impl_path: str               # "EgiMgrPkg/src/EgiMgrCls.cpp"
    base_classes: list[str]      # ["EgiExtDataIfc"] (interfaces implemented)
    members: list[MemberInfo]    # Component instances owned by this class

MemberInfo:
    name: str                    # "EgiLruMgr"
    type_name: str               # "EgiLruMgrCls"

PortConnection:
    from_path: str               # "EgiMgr.EgiLruMgr" (member path from partition root)
    to_path: str                 # "RadaltMgr.RadaltLruMgr"
    interface: str               # "EgiExtDataIfc"
    setter_method: str           # "SetItsDataOutPortEgiExtDataIfc"
```

## Workflow

1. **Scan phase**: Find all `*Pkg/inc/*.h` and `*Pkg/src/*.cpp` files
2. **Parse phase**: Build `ClassInfo` for each class (members, inheritance)
3. **Traverse phase**: Starting from partition class, recursively collect all components
4. **Connect phase**: Parse `InitRelations()` in each class, detect `SetIts*`/`GetIts*` calls
5. **Output phase**: Render connections as ASCII diagram

## Tree-sitter Parsing Strategy

### Header Parsing

Extract class structure from `.h` files:

```cpp
// 1. Class declaration with inheritance
class RadaltLruMgrCls : public EgiExtDataIfc { ... }
//    ^^^^^^^^^^^^^^^^         ^^^^^^^^^^^^^^
//    class_name               base_class (interface)

// 2. Member variable declarations (in private/protected sections)
EgiLruMgrCls EgiLruMgr;
//^^^^^^^^^^  ^^^^^^^^
// type_name  member_name

// 3. Port member patterns (old style)
EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
//             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
//             matches Its*Port* pattern -> output port
```

### Implementation Parsing

Extract connections from `.cpp` `InitRelations()`:

```cpp
// 1. Output port setter calls
SetItsDataOutPortEgiExtDataIfc(something)
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
// setter name -> extract interface type

// 2. Input port getter calls
RadaltLruMgr.GetItsRadaltEgiInPortEgiExtDataIfc()
//           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
// getter name -> extract interface type

// 3. Assignment wiring
ItsX = Y.GetIts...();
// Left side = output port, Right side = input port source
```

### Interface Extraction

From port names, extract interface by taking everything after the last `Port`:
- `ItsDataOutPortEgiExtDataIfc` -> `EgiExtDataIfc`
- `GetItsRadaltEgiInPortEgiExtDataIfc` -> `EgiExtDataIfc`

## Hierarchy Traversal

Recursively build component tree from partition root:

```
PartitionCls (root)
├── EgiMgr: EgiMgrCls
│   ├── EgiLruMgr: EgiLruMgrCls
│   └── EgiCmp: EgiCmpCls
├── RadaltMgr: RadaltMgrCls
│   └── RadaltLruMgr: RadaltLruMgrCls
└── VorIlsMgr: VorIlsMgrCls
    └── VorIlsLruMgr: VorIlsLruMgrCls
```

Each component gets a dotted path from root (e.g., `EgiMgr.EgiLruMgr`).

## Output Format

```
$ python tools/port_analyzer.py PartitionCls

Partition: PartitionCls
=======================

Component Hierarchy:
  PartitionCls
  ├── EgiMgr: EgiMgrCls
  │   └── EgiLruMgr: EgiLruMgrCls
  ├── RadaltMgr: RadaltMgrCls
  │   └── RadaltLruMgr: RadaltLruMgrCls
  └── VorIlsMgr: VorIlsMgrCls
      └── VorIlsLruMgr: VorIlsLruMgrCls

Port Connections:
  EgiMgr.EgiLruMgr --[EgiExtDataIfc]--> RadaltMgr.RadaltLruMgr

Legend:
  A --[Interface]--> B  means A sends data to B via Interface
```

Unresolved connections shown as:
```
  EgiMgr.EgiLruMgr --[EgiExtDataIfc]--> ??? (unresolved: SomeUnknownMgr)
```

## Project Structure

```
tools/
└── port_analyzer.py    # Single-file script
```

## Dependencies

```
tree-sitter>=0.20.0
tree-sitter-cpp>=0.20.0
```

## CLI Interface

```bash
python tools/port_analyzer.py PartitionCls
```

## Error Handling

- Class not found: `Error: Class 'FooCls' not found in *Pkg/inc/*.h`
- Parse failure: `Error: Failed to parse EgiMgrCls.h: <tree-sitter error>`
- No InitRelations: `Warning: EgiMgrCls has no InitRelations() method`

## Exit Codes

- `0`: Success
- `1`: Class not found or argument error
- `2`: Parse error
