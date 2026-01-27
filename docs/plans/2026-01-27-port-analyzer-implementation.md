# Port Analyzer Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python tool that statically analyzes C++ code to detect and report port connections between classes in a partition-based component system.

**Architecture:** Single-file Python script using Tree-sitter for AST parsing. Scans `*Pkg/` directories, builds a class graph from headers, traverses component hierarchy from partition root, detects port patterns in `InitRelations()`, and outputs ASCII diagram.

**Tech Stack:** Python 3.10+, tree-sitter, tree-sitter-cpp

---

## Task 1: Project Setup and Dependencies

**Files:**
- Create: `tools/port_analyzer.py`
- Create: `tools/requirements.txt`
- Create: `tools/test_fixtures/` (directory for test C++ files)

**Step 1: Create tools directory and requirements file**

```bash
mkdir -p tools
```

**Step 2: Create requirements.txt**

Create `tools/requirements.txt`:
```
tree-sitter>=0.23.0
tree-sitter-cpp>=0.23.0
```

**Step 3: Create minimal port_analyzer.py skeleton**

Create `tools/port_analyzer.py`:
```python
#!/usr/bin/env python3
"""
Port Analyzer - Static analysis tool for detecting port connections
in C++ component-based systems.

Usage: python tools/port_analyzer.py <PartitionClassName>
"""

import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/port_analyzer.py <PartitionClassName>", file=sys.stderr)
        return 1

    partition_class = sys.argv[1]
    print(f"Analyzing partition: {partition_class}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Step 4: Verify script runs**

Run: `python tools/port_analyzer.py TestPartition`
Expected: `Analyzing partition: TestPartition`

**Step 5: Commit**

```bash
git add tools/port_analyzer.py tools/requirements.txt
git commit -m "feat: add port_analyzer skeleton and dependencies"
```

---

## Task 2: Create Test Fixtures

**Files:**
- Create: `tools/test_fixtures/EgiMgrExtPkg/EgiExtDataIfc.h`
- Create: `tools/test_fixtures/EgiMgrExtPkg/EgiExtDataType.h`
- Create: `tools/test_fixtures/EgiMgrPkg/inc/EgiMgrCls.h`
- Create: `tools/test_fixtures/EgiMgrPkg/inc/EgiLruMgrCls.h`
- Create: `tools/test_fixtures/EgiMgrPkg/src/EgiMgrCls.cpp`
- Create: `tools/test_fixtures/RadaltMgrPkg/inc/RadaltMgrCls.h`
- Create: `tools/test_fixtures/RadaltMgrPkg/inc/RadaltLruMgrCls.h`
- Create: `tools/test_fixtures/RadaltMgrPkg/src/RadaltMgrCls.cpp`
- Create: `tools/test_fixtures/PartitionPkg/inc/PartitionCls.h`
- Create: `tools/test_fixtures/PartitionPkg/src/PartitionCls.cpp`

**Step 1: Create fixture directory structure**

```bash
mkdir -p tools/test_fixtures/EgiMgrExtPkg
mkdir -p tools/test_fixtures/EgiMgrPkg/inc tools/test_fixtures/EgiMgrPkg/src
mkdir -p tools/test_fixtures/RadaltMgrPkg/inc tools/test_fixtures/RadaltMgrPkg/src
mkdir -p tools/test_fixtures/PartitionPkg/inc tools/test_fixtures/PartitionPkg/src
```

**Step 2: Create interface files**

Create `tools/test_fixtures/EgiMgrExtPkg/EgiExtDataType.h`:
```cpp
#ifndef EGIEXTDATATYPE_H
#define EGIEXTDATATYPE_H

struct EgiExtDataType
{
    int exampleField;
};

#endif
```

Create `tools/test_fixtures/EgiMgrExtPkg/EgiExtDataIfc.h`:
```cpp
#ifndef EGIEXTDATAIFC_H
#define EGIEXTDATAIFC_H

#include <EgiExtDataType.h>

class EgiExtDataIfc
{
public:
    virtual void SetEgiExtData(const EgiExtDataType& data) = 0;
};

#endif
```

**Step 3: Create EgiMgrPkg headers**

Create `tools/test_fixtures/EgiMgrPkg/inc/EgiLruMgrCls.h`:
```cpp
#ifndef EGILRUMGR_H
#define EGILRUMGR_H

#include <EgiExtDataIfc.h>

class EgiLruMgrCls
{
public:
    EgiLruMgrCls();
    ~EgiLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);

private:
protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
};

#endif
```

Create `tools/test_fixtures/EgiMgrPkg/inc/EgiMgrCls.h`:
```cpp
#ifndef EGIMGR_H
#define EGIMGR_H

#include <EgiLruMgrCls.h>
#include <EgiExtDataIfc.h>

class EgiMgrCls
{
public:
    EgiMgrCls();
    ~EgiMgrCls();

    void Initialize();
    void PeriodicRun();
    void InitRelations();

    void SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc);

private:
    EgiLruMgrCls EgiLruMgr;

protected:
    EgiExtDataIfc* ItsDataOutPortEgiExtDataIfc;
};

#endif
```

**Step 4: Create EgiMgrPkg implementation**

Create `tools/test_fixtures/EgiMgrPkg/src/EgiMgrCls.cpp`:
```cpp
#include <EgiMgrCls.h>

EgiMgrCls::EgiMgrCls()
{
    InitRelations();
}

EgiMgrCls::~EgiMgrCls()
{
}

void EgiMgrCls::Initialize()
{
    EgiLruMgr.Initialize();
}

void EgiMgrCls::PeriodicRun()
{
    EgiLruMgr.PeriodicRun();
}

void EgiMgrCls::InitRelations()
{
    ItsDataOutPortEgiExtDataIfc = nullptr;
}

void EgiMgrCls::SetItsDataOutPortEgiExtDataIfc(EgiExtDataIfc* ifc)
{
    ItsDataOutPortEgiExtDataIfc = ifc;
}
```

**Step 5: Create RadaltMgrPkg headers**

Create `tools/test_fixtures/RadaltMgrPkg/inc/RadaltLruMgrCls.h`:
```cpp
#ifndef RADALTLRUMGR_H
#define RADALTLRUMGR_H

#include <EgiExtDataIfc.h>

class RadaltLruMgrCls : public EgiExtDataIfc
{
public:
    RadaltLruMgrCls();
    ~RadaltLruMgrCls();

    void Initialize();
    void PeriodicRun();

    void SetEgiExtData(const EgiExtDataType& data) override;

    EgiExtDataIfc* GetItsRadaltEgiInPortEgiExtDataIfc();

private:
protected:
};

#endif
```

Create `tools/test_fixtures/RadaltMgrPkg/inc/RadaltMgrCls.h`:
```cpp
#ifndef RADALTMGR_H
#define RADALTMGR_H

#include <RadaltLruMgrCls.h>

class RadaltMgrCls
{
public:
    RadaltMgrCls();
    ~RadaltMgrCls();

    void Initialize();
    void PeriodicRun();
    void InitRelations();

    EgiExtDataIfc* GetItsRadaltEgiInPortEgiExtDataIfc();

private:
    RadaltLruMgrCls RadaltLruMgr;

protected:
    EgiExtDataIfc* ItsRadaltEgiInPortEgiExtDataIfc;
};

#endif
```

**Step 6: Create RadaltMgrPkg implementation**

Create `tools/test_fixtures/RadaltMgrPkg/src/RadaltMgrCls.cpp`:
```cpp
#include <RadaltMgrCls.h>

RadaltMgrCls::RadaltMgrCls()
{
}

RadaltMgrCls::~RadaltMgrCls()
{
}

void RadaltMgrCls::Initialize()
{
}

void RadaltMgrCls::PeriodicRun()
{
}

EgiExtDataIfc* RadaltMgrCls::GetItsRadaltEgiInPortEgiExtDataIfc()
{
    return ItsRadaltEgiInPortEgiExtDataIfc;
}

void RadaltMgrCls::InitRelations()
{
    ItsRadaltEgiInPortEgiExtDataIfc = RadaltLruMgr.GetItsRadaltEgiInPortEgiExtDataIfc();
}
```

**Step 7: Create PartitionPkg files**

Create `tools/test_fixtures/PartitionPkg/inc/PartitionCls.h`:
```cpp
#ifndef PARTITIONCLS_H
#define PARTITIONCLS_H

#include <EgiMgrCls.h>
#include <RadaltMgrCls.h>

class PartitionCls
{
public:
    PartitionCls();
    ~PartitionCls();

    void Initialize();
    void PeriodicRun();
    void InitRelations();

private:
    EgiMgrCls EgiMgr;
    RadaltMgrCls RadaltMgr;

protected:
};

#endif
```

Create `tools/test_fixtures/PartitionPkg/src/PartitionCls.cpp`:
```cpp
#include <PartitionCls.h>

PartitionCls::PartitionCls()
{
    InitRelations();
}

PartitionCls::~PartitionCls()
{
}

void PartitionCls::Initialize()
{
    EgiMgr.Initialize();
    RadaltMgr.Initialize();
}

void PartitionCls::PeriodicRun()
{
    EgiMgr.PeriodicRun();
    RadaltMgr.PeriodicRun();
}

void PartitionCls::InitRelations()
{
    EgiMgr.SetItsDataOutPortEgiExtDataIfc(RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc());
}
```

**Step 8: Commit test fixtures**

```bash
git add tools/test_fixtures/
git commit -m "test: add C++ test fixtures for port analyzer"
```

---

## Task 3: File Scanner Module

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Write failing test inline (manual verification)**

We'll verify manually. Expected behavior: find all `*Pkg/inc/*.h` and `*Pkg/src/*.cpp` files.

**Step 2: Implement file scanner**

Add to `tools/port_analyzer.py` after imports:
```python
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ScannedFiles:
    """Results of scanning project directory."""
    headers: list[Path] = field(default_factory=list)
    implementations: list[Path] = field(default_factory=list)


def scan_project(project_root: Path) -> ScannedFiles:
    """
    Scan project for C++ header and implementation files.

    Searches for:
    - *Pkg/inc/*.h (headers)
    - *Pkg/src/*.cpp (implementations)
    """
    result = ScannedFiles()

    for pkg_dir in project_root.glob("*Pkg"):
        if not pkg_dir.is_dir():
            continue

        # Scan headers
        inc_dir = pkg_dir / "inc"
        if inc_dir.is_dir():
            result.headers.extend(inc_dir.glob("*.h"))

        # Also scan ExtPkg root for headers (interface packages)
        if pkg_dir.name.endswith("ExtPkg"):
            result.headers.extend(pkg_dir.glob("*.h"))

        # Scan implementations
        src_dir = pkg_dir / "src"
        if src_dir.is_dir():
            result.implementations.extend(src_dir.glob("*.cpp"))

    return result
```

**Step 3: Update main() to test scanner**

Replace main() function:
```python
def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/port_analyzer.py <PartitionClassName>", file=sys.stderr)
        return 1

    partition_class = sys.argv[1]
    project_root = Path.cwd()

    # Scan for files
    scanned = scan_project(project_root)
    print(f"Found {len(scanned.headers)} headers, {len(scanned.implementations)} implementations")

    for h in sorted(scanned.headers):
        print(f"  Header: {h.relative_to(project_root)}")

    return 0
```

**Step 4: Verify scanner works**

Run from test_fixtures:
```bash
cd tools/test_fixtures && python ../port_analyzer.py PartitionCls
```

Expected output:
```
Found 6 headers, 3 implementations
  Header: EgiMgrExtPkg/EgiExtDataIfc.h
  Header: EgiMgrExtPkg/EgiExtDataType.h
  Header: EgiMgrPkg/inc/EgiLruMgrCls.h
  Header: EgiMgrPkg/inc/EgiMgrCls.h
  Header: PartitionPkg/inc/PartitionCls.h
  Header: RadaltMgrPkg/inc/RadaltLruMgrCls.h
  Header: RadaltMgrPkg/inc/RadaltMgrCls.h
```

**Step 5: Commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add file scanner for *Pkg directories"
```

---

## Task 4: Data Model Classes

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add data model classes**

Add after ScannedFiles class:
```python
@dataclass
class MemberInfo:
    """A member variable in a class."""
    name: str           # "EgiLruMgr"
    type_name: str      # "EgiLruMgrCls"


@dataclass
class ClassInfo:
    """Information about a C++ class."""
    name: str                           # "EgiMgrCls"
    header_path: Path | None = None     # Path to .h file
    impl_path: Path | None = None       # Path to .cpp file
    base_classes: list[str] = field(default_factory=list)   # Inherited interfaces
    members: list[MemberInfo] = field(default_factory=list) # Component members
    port_members: list[str] = field(default_factory=list)   # Its*Port* members


@dataclass
class PortConnection:
    """A port connection between components."""
    from_path: str      # "EgiMgr" (dotted path from partition root)
    to_path: str        # "RadaltMgr.RadaltLruMgr"
    interface: str      # "EgiExtDataIfc"


@dataclass
class ComponentNode:
    """A node in the component hierarchy tree."""
    name: str                   # "EgiMgr" (member name) or "root"
    class_name: str             # "EgiMgrCls"
    children: list['ComponentNode'] = field(default_factory=list)

    def get_path(self, parent_path: str = "") -> str:
        """Get dotted path from root."""
        if parent_path:
            return f"{parent_path}.{self.name}" if self.name != "root" else parent_path
        return self.name if self.name != "root" else ""
```

**Step 2: Commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add data model classes for port analyzer"
```

---

## Task 5: Tree-sitter Parser Setup

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add tree-sitter imports and parser initialization**

Add at top of file after existing imports:
```python
import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser
```

Add after data model classes:
```python
def create_parser() -> Parser:
    """Create and configure tree-sitter C++ parser."""
    parser = Parser(Language(tscpp.language()))
    return parser
```

**Step 2: Verify tree-sitter loads**

Add temporary test in main():
```python
    # Test parser creation
    parser = create_parser()
    print(f"Parser created: {parser}")
```

Run: `cd tools/test_fixtures && python ../port_analyzer.py PartitionCls`
Expected: No errors, parser created message

**Step 3: Remove test code and commit**

Remove the temporary test lines, then:
```bash
git add tools/port_analyzer.py
git commit -m "feat: add tree-sitter parser initialization"
```

---

## Task 6: Header Parser - Class Declaration

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add header parsing function**

Add after create_parser():
```python
def parse_header(parser: Parser, file_path: Path) -> ClassInfo | None:
    """
    Parse a C++ header file and extract class information.

    Returns ClassInfo or None if no class found.
    """
    content = file_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    # Find class_specifier node
    class_node = None
    for node in root.children:
        if node.type == "class_specifier":
            class_node = node
            break
        # Handle case where class is inside other constructs
        for child in node.children:
            if child.type == "class_specifier":
                class_node = child
                break

    if class_node is None:
        return None

    # Extract class name
    class_name = None
    base_classes = []
    members = []
    port_members = []

    for child in class_node.children:
        if child.type == "type_identifier":
            class_name = content[child.start_byte:child.end_byte].decode()

        elif child.type == "base_class_clause":
            # Extract base classes
            for base_child in child.children:
                if base_child.type == "type_identifier":
                    base_name = content[base_child.start_byte:base_child.end_byte].decode()
                    base_classes.append(base_name)

        elif child.type == "field_declaration_list":
            # Parse class body for members
            _parse_class_body(content, child, members, port_members)

    if class_name is None:
        return None

    return ClassInfo(
        name=class_name,
        header_path=file_path,
        base_classes=base_classes,
        members=members,
        port_members=port_members,
    )


def _parse_class_body(
    content: bytes,
    body_node,
    members: list[MemberInfo],
    port_members: list[str],
) -> None:
    """Parse class body for member declarations."""
    for node in body_node.children:
        if node.type == "field_declaration":
            _parse_field_declaration(content, node, members, port_members)
        elif node.type == "access_specifier":
            continue  # Skip public/private/protected


def _parse_field_declaration(
    content: bytes,
    field_node,
    members: list[MemberInfo],
    port_members: list[str],
) -> None:
    """Parse a field declaration to extract member info."""
    type_name = None
    member_name = None
    is_pointer = False

    for child in field_node.children:
        if child.type == "type_identifier":
            type_name = content[child.start_byte:child.end_byte].decode()
        elif child.type == "field_identifier":
            member_name = content[child.start_byte:child.end_byte].decode()
        elif child.type == "pointer_declarator":
            is_pointer = True
            # Get the identifier from pointer declarator
            for pc in child.children:
                if pc.type == "field_identifier":
                    member_name = content[pc.start_byte:pc.end_byte].decode()

    if type_name and member_name:
        # Check if it's a port member (Its*Port* pattern)
        if member_name.startswith("Its") and "Port" in member_name:
            port_members.append(member_name)
        # Check if it's a component member (ends with Cls, not a pointer)
        elif type_name.endswith("Cls") and not is_pointer:
            members.append(MemberInfo(name=member_name, type_name=type_name))
```

**Step 2: Test header parsing**

Update main() to test:
```python
def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/port_analyzer.py <PartitionClassName>", file=sys.stderr)
        return 1

    partition_class = sys.argv[1]
    project_root = Path.cwd()

    # Scan for files
    scanned = scan_project(project_root)
    parser = create_parser()

    # Parse all headers
    for h in sorted(scanned.headers):
        info = parse_header(parser, h)
        if info:
            print(f"{info.name}:")
            print(f"  bases: {info.base_classes}")
            print(f"  members: {[(m.name, m.type_name) for m in info.members]}")
            print(f"  ports: {info.port_members}")

    return 0
```

Run: `cd tools/test_fixtures && python ../port_analyzer.py PartitionCls`

Expected output includes:
```
EgiMgrCls:
  bases: []
  members: [('EgiLruMgr', 'EgiLruMgrCls')]
  ports: ['ItsDataOutPortEgiExtDataIfc']
PartitionCls:
  bases: []
  members: [('EgiMgr', 'EgiMgrCls'), ('RadaltMgr', 'RadaltMgrCls')]
  ports: []
RadaltLruMgrCls:
  bases: ['EgiExtDataIfc']
  members: []
  ports: []
```

**Step 3: Commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add header parser for class declarations"
```

---

## Task 7: Build Class Registry

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add class registry builder**

Add after parse_header:
```python
def build_class_registry(
    parser: Parser,
    scanned: ScannedFiles,
) -> dict[str, ClassInfo]:
    """
    Build a registry mapping class names to ClassInfo.

    Also associates implementation files with their classes.
    """
    registry: dict[str, ClassInfo] = {}

    # Parse all headers
    for header in scanned.headers:
        info = parse_header(parser, header)
        if info:
            registry[info.name] = info

    # Associate implementation files
    for impl in scanned.implementations:
        # Implementation file name should match class name
        # e.g., EgiMgrCls.cpp -> EgiMgrCls
        stem = impl.stem
        if stem in registry:
            registry[stem].impl_path = impl

    return registry
```

**Step 2: Update main() to use registry**

```python
def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/port_analyzer.py <PartitionClassName>", file=sys.stderr)
        return 1

    partition_class = sys.argv[1]
    project_root = Path.cwd()

    # Scan and build registry
    scanned = scan_project(project_root)
    parser = create_parser()
    registry = build_class_registry(parser, scanned)

    print(f"Registered {len(registry)} classes:")
    for name, info in sorted(registry.items()):
        impl = info.impl_path.name if info.impl_path else "none"
        print(f"  {name} (impl: {impl})")

    # Verify partition class exists
    if partition_class not in registry:
        print(f"Error: Class '{partition_class}' not found in *Pkg/inc/*.h", file=sys.stderr)
        return 1

    return 0
```

**Step 3: Test registry**

Run: `cd tools/test_fixtures && python ../port_analyzer.py PartitionCls`

Expected:
```
Registered 5 classes:
  EgiLruMgrCls (impl: none)
  EgiMgrCls (impl: EgiMgrCls.cpp)
  PartitionCls (impl: PartitionCls.cpp)
  RadaltLruMgrCls (impl: none)
  RadaltMgrCls (impl: RadaltMgrCls.cpp)
```

**Step 4: Commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add class registry builder"
```

---

## Task 8: Component Hierarchy Traversal

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add hierarchy builder**

Add after build_class_registry:
```python
def build_component_tree(
    class_name: str,
    registry: dict[str, ClassInfo],
    member_name: str = "root",
) -> ComponentNode:
    """
    Recursively build component hierarchy tree.

    Args:
        class_name: The class to start from
        registry: Class registry
        member_name: Name of this node in parent (or "root")

    Returns:
        ComponentNode tree
    """
    node = ComponentNode(name=member_name, class_name=class_name)

    info = registry.get(class_name)
    if info is None:
        return node

    # Recurse into component members
    for member in info.members:
        if member.type_name in registry:
            child = build_component_tree(member.type_name, registry, member.name)
            node.children.append(child)

    return node


def print_component_tree(node: ComponentNode, indent: str = "", is_last: bool = True) -> None:
    """Print component tree as ASCII art."""
    # Determine prefix
    if node.name == "root":
        print(f"  {node.class_name}")
    else:
        connector = "└── " if is_last else "├── "
        print(f"  {indent}{connector}{node.name}: {node.class_name}")

    # Print children
    child_indent = indent + ("    " if is_last else "│   ")
    for i, child in enumerate(node.children):
        print_component_tree(child, child_indent, i == len(node.children) - 1)
```

**Step 2: Update main() to show tree**

```python
def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/port_analyzer.py <PartitionClassName>", file=sys.stderr)
        return 1

    partition_class = sys.argv[1]
    project_root = Path.cwd()

    # Scan and build registry
    scanned = scan_project(project_root)
    parser = create_parser()
    registry = build_class_registry(parser, scanned)

    # Verify partition class exists
    if partition_class not in registry:
        print(f"Error: Class '{partition_class}' not found in *Pkg/inc/*.h", file=sys.stderr)
        return 1

    # Build and display hierarchy
    tree = build_component_tree(partition_class, registry)

    print(f"Partition: {partition_class}")
    print("=" * (len(partition_class) + 11))
    print()
    print("Component Hierarchy:")
    print_component_tree(tree)

    return 0
```

**Step 3: Test hierarchy**

Run: `cd tools/test_fixtures && python ../port_analyzer.py PartitionCls`

Expected:
```
Partition: PartitionCls
=======================

Component Hierarchy:
  PartitionCls
  ├── EgiMgr: EgiMgrCls
  │   └── EgiLruMgr: EgiLruMgrCls
  └── RadaltMgr: RadaltMgrCls
      └── RadaltLruMgr: RadaltLruMgrCls
```

**Step 4: Commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add component hierarchy traversal and display"
```

---

## Task 9: InitRelations Parser

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add InitRelations parser**

Add after print_component_tree:
```python
def parse_init_relations(
    parser: Parser,
    impl_path: Path,
) -> list[tuple[str, str]]:
    """
    Parse InitRelations() method to find port wirings.

    Returns list of (setter_call, getter_call) tuples.
    E.g., ("EgiMgr.SetItsDataOutPortEgiExtDataIfc", "RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc()")
    """
    content = impl_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    wirings = []

    # Find InitRelations function
    for node in root.children:
        if node.type == "function_definition":
            # Check if this is InitRelations
            func_name = _get_function_name(content, node)
            if func_name and "InitRelations" in func_name:
                # Parse the function body
                wirings.extend(_parse_init_relations_body(content, node))

    return wirings


def _get_function_name(content: bytes, func_node) -> str | None:
    """Extract function name from function_definition node."""
    for child in func_node.children:
        if child.type == "function_declarator":
            for fc in child.children:
                if fc.type == "qualified_identifier":
                    return content[fc.start_byte:fc.end_byte].decode()
                elif fc.type == "field_identifier":
                    return content[fc.start_byte:fc.end_byte].decode()
    return None


def _parse_init_relations_body(content: bytes, func_node) -> list[tuple[str, str]]:
    """Parse function body for port wirings."""
    wirings = []

    for child in func_node.children:
        if child.type == "compound_statement":
            for stmt in child.children:
                wiring = _parse_statement_for_wiring(content, stmt)
                if wiring:
                    wirings.append(wiring)

    return wirings


def _parse_statement_for_wiring(content: bytes, stmt_node) -> tuple[str, str] | None:
    """
    Parse a statement to find port wiring patterns.

    Patterns:
    1. X.SetIts*Port*(Y.GetIts*Port*())
    2. ItsX = Y.GetIts*Port*()
    """
    if stmt_node.type == "expression_statement":
        for child in stmt_node.children:
            return _parse_expression_for_wiring(content, child)
    return None


def _parse_expression_for_wiring(content: bytes, expr_node) -> tuple[str, str] | None:
    """Parse expression for wiring pattern."""
    expr_text = content[expr_node.start_byte:expr_node.end_byte].decode().strip()

    # Pattern 1: Call expression with SetIts*Port*
    if expr_node.type == "call_expression" and "SetIts" in expr_text and "Port" in expr_text:
        # Extract the full call: Obj.SetIts*Port*(arg)
        return _extract_setter_getter(expr_text)

    # Pattern 2: Assignment with GetIts*Port*
    if expr_node.type == "assignment_expression" and "GetIts" in expr_text and "Port" in expr_text:
        return _extract_assignment_wiring(expr_text)

    return None


def _extract_setter_getter(expr_text: str) -> tuple[str, str] | None:
    """
    Extract setter and getter from: Obj.SetIts*Port*(Arg.GetIts*Port*())
    """
    import re

    # Match: something.SetIts...Port...(...GetIts...Port...())
    # Capture the object calling Set and the argument with Get
    match = re.match(
        r'([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\.(SetIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*)\(([^)]+)\)',
        expr_text.replace('\n', ' ').replace(' ', '')
    )

    if match:
        setter_obj = match.group(1)
        setter_method = match.group(2)
        getter_expr = match.group(3)
        return (f"{setter_obj}.{setter_method}", getter_expr)

    return None


def _extract_assignment_wiring(expr_text: str) -> tuple[str, str] | None:
    """
    Extract from: ItsX = Y.GetIts*Port*()
    """
    import re

    match = re.match(
        r'(Its[A-Za-z0-9_]*Port[A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_()]*)+)',
        expr_text.replace('\n', ' ')
    )

    if match:
        port_member = match.group(1)
        getter_expr = match.group(2)
        return (port_member, getter_expr)

    return None
```

**Step 2: Test InitRelations parsing**

Add temporary test to main():
```python
    # Test InitRelations parsing
    for name, info in registry.items():
        if info.impl_path:
            wirings = parse_init_relations(parser, info.impl_path)
            if wirings:
                print(f"\n{name} wirings:")
                for setter, getter in wirings:
                    print(f"  {setter} <- {getter}")
```

Run: `cd tools/test_fixtures && python ../port_analyzer.py PartitionCls`

Expected to include:
```
PartitionCls wirings:
  EgiMgr.SetItsDataOutPortEgiExtDataIfc <- RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc()
```

**Step 3: Remove test code and commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add InitRelations parser for port wirings"
```

---

## Task 10: Connection Resolution

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add connection resolver**

Add after InitRelations parser:
```python
def extract_interface_from_port(port_name: str) -> str:
    """
    Extract interface name from port naming pattern.

    ItsDataOutPortEgiExtDataIfc -> EgiExtDataIfc
    GetItsRadaltEgiInPortEgiExtDataIfc -> EgiExtDataIfc
    """
    # Find "Port" and take everything after it
    if "Port" in port_name:
        idx = port_name.rfind("Port")
        interface = port_name[idx + 4:]  # Skip "Port"
        # Remove trailing () if present
        interface = interface.rstrip("()")
        return interface
    return "Unknown"


def resolve_member_path(expr: str) -> str:
    """
    Convert getter expression to member path.

    RadaltMgr.GetItsRadaltEgiInPortEgiExtDataIfc() -> RadaltMgr
    EgiMgr.GetEgiLruMgr().SetIts... -> EgiMgr.EgiLruMgr
    """
    # Remove method calls, keep only member access
    parts = []
    current = ""

    for char in expr:
        if char == '.':
            if current and not current.startswith("Get") and not current.startswith("Set"):
                parts.append(current)
            elif current.startswith("Get") and current.endswith("()"):
                # Convert GetXxx() to Xxx (member accessor)
                member = current[3:-2]  # Remove "Get" and "()"
                parts.append(member)
            current = ""
        elif char == '(':
            # End of identifier
            if current and not current.startswith("Get") and not current.startswith("Set"):
                parts.append(current)
            current = current + char
        elif char == ')':
            current = current + char
        else:
            current = current + char

    # Handle remaining
    if current and not current.startswith("Get") and not current.startswith("Set"):
        if not current.endswith(")"):
            parts.append(current)

    return ".".join(parts) if parts else expr


def collect_connections(
    tree: ComponentNode,
    registry: dict[str, ClassInfo],
    parser: Parser,
    parent_path: str = "",
) -> list[PortConnection]:
    """
    Recursively collect all port connections from component tree.
    """
    connections = []
    current_path = tree.get_path(parent_path)

    info = registry.get(tree.class_name)
    if info and info.impl_path:
        wirings = parse_init_relations(parser, info.impl_path)

        for setter, getter in wirings:
            # Extract interface from setter/port name
            interface = extract_interface_from_port(setter)

            # Resolve from_path (who is calling the setter)
            if "." in setter:
                setter_parts = setter.split(".")
                from_member = setter_parts[0]
                from_path = f"{current_path}.{from_member}" if current_path else from_member
            else:
                from_path = current_path

            # Resolve to_path (who is being connected)
            to_member = resolve_member_path(getter)
            to_path = f"{current_path}.{to_member}" if current_path else to_member

            connections.append(PortConnection(
                from_path=from_path,
                to_path=to_path,
                interface=interface,
            ))

    # Recurse into children
    for child in tree.children:
        child_path = tree.get_path(parent_path)
        connections.extend(collect_connections(child, registry, parser, child_path))

    return connections
```

**Step 2: Update main() for full output**

Replace main():
```python
def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/port_analyzer.py <PartitionClassName>", file=sys.stderr)
        return 1

    partition_class = sys.argv[1]
    project_root = Path.cwd()

    # Scan and build registry
    scanned = scan_project(project_root)
    if not scanned.headers:
        print("Error: No *Pkg directories found. Run from project root.", file=sys.stderr)
        return 1

    parser = create_parser()
    registry = build_class_registry(parser, scanned)

    # Verify partition class exists
    if partition_class not in registry:
        print(f"Error: Class '{partition_class}' not found in *Pkg/inc/*.h", file=sys.stderr)
        return 1

    # Build hierarchy
    tree = build_component_tree(partition_class, registry)

    # Collect connections
    connections = collect_connections(tree, registry, parser)

    # Output
    print(f"Partition: {partition_class}")
    print("=" * (len(partition_class) + 11))
    print()
    print("Component Hierarchy:")
    print_component_tree(tree)
    print()
    print("Port Connections:")
    if connections:
        for conn in connections:
            print(f"  {conn.from_path} --[{conn.interface}]--> {conn.to_path}")
    else:
        print("  (none)")
    print()
    print("Legend:")
    print("  A --[Interface]--> B  means A sends data to B via Interface")

    return 0
```

**Step 3: Test full output**

Run: `cd tools/test_fixtures && python ../port_analyzer.py PartitionCls`

Expected:
```
Partition: PartitionCls
=======================

Component Hierarchy:
  PartitionCls
  ├── EgiMgr: EgiMgrCls
  │   └── EgiLruMgr: EgiLruMgrCls
  └── RadaltMgr: RadaltMgrCls
      └── RadaltLruMgr: RadaltLruMgrCls

Port Connections:
  EgiMgr --[EgiExtDataIfc]--> RadaltMgr

Legend:
  A --[Interface]--> B  means A sends data to B via Interface
```

**Step 4: Commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add connection resolution and final output"
```

---

## Task 11: Error Handling and Polish

**Files:**
- Modify: `tools/port_analyzer.py`

**Step 1: Add warning for unresolved connections**

Update PortConnection class:
```python
@dataclass
class PortConnection:
    """A port connection between components."""
    from_path: str      # "EgiMgr" (dotted path from partition root)
    to_path: str        # "RadaltMgr.RadaltLruMgr"
    interface: str      # "EgiExtDataIfc"
    unresolved: bool = False  # True if target couldn't be resolved
```

Update collect_connections to detect unresolved:
```python
            # Check if to_path is valid (exists in tree)
            unresolved = not _path_exists_in_tree(tree, to_member)

            connections.append(PortConnection(
                from_path=from_path,
                to_path=to_path,
                interface=interface,
                unresolved=unresolved,
            ))
```

Add helper:
```python
def _path_exists_in_tree(tree: ComponentNode, path: str) -> bool:
    """Check if a member path exists in the component tree."""
    parts = path.split(".")
    current = tree

    for part in parts:
        found = False
        for child in current.children:
            if child.name == part:
                current = child
                found = True
                break
        if not found:
            return False

    return True
```

Update output:
```python
    for conn in connections:
        if conn.unresolved:
            print(f"  {conn.from_path} --[{conn.interface}]--> ??? (unresolved: {conn.to_path})")
        else:
            print(f"  {conn.from_path} --[{conn.interface}]--> {conn.to_path}")
```

**Step 2: Add parse error handling**

Wrap parse calls with try/except:
```python
def parse_header(parser: Parser, file_path: Path) -> ClassInfo | None:
    """..."""
    try:
        content = file_path.read_bytes()
        tree = parser.parse(content)
        # ... rest of function
    except Exception as e:
        print(f"Warning: Failed to parse {file_path}: {e}", file=sys.stderr)
        return None
```

**Step 3: Add shebang and make executable**

Ensure first line is:
```python
#!/usr/bin/env python3
```

**Step 4: Test error cases**

```bash
# Test missing class
cd tools/test_fixtures && python ../port_analyzer.py NonExistent
# Expected: Error: Class 'NonExistent' not found in *Pkg/inc/*.h

# Test wrong directory
cd /tmp && python /path/to/port_analyzer.py PartitionCls
# Expected: Error: No *Pkg directories found. Run from project root.
```

**Step 5: Final commit**

```bash
git add tools/port_analyzer.py
git commit -m "feat: add error handling and polish"
```

---

## Task 12: Final Integration Test

**Files:**
- No changes, verification only

**Step 1: Run full test**

```bash
cd tools/test_fixtures && python ../port_analyzer.py PartitionCls
```

**Step 2: Verify output matches expected**

Expected output:
```
Partition: PartitionCls
=======================

Component Hierarchy:
  PartitionCls
  ├── EgiMgr: EgiMgrCls
  │   └── EgiLruMgr: EgiLruMgrCls
  └── RadaltMgr: RadaltMgrCls
      └── RadaltLruMgr: RadaltLruMgrCls

Port Connections:
  EgiMgr --[EgiExtDataIfc]--> RadaltMgr

Legend:
  A --[Interface]--> B  means A sends data to B via Interface
```

**Step 3: Create final commit with test verification**

```bash
git add -A
git commit -m "test: verify port_analyzer works with test fixtures"
```

---

## Summary

12 tasks implementing:
1. Project setup
2. Test fixtures
3. File scanner
4. Data model
5. Tree-sitter setup
6. Header parser
7. Class registry
8. Hierarchy traversal
9. InitRelations parser
10. Connection resolution
11. Error handling
12. Integration test

Each task follows TDD: verify behavior, implement, commit.
