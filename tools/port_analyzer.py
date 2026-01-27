#!/usr/bin/env python3
"""
Port Analyzer - Static analysis tool for detecting port connections
in C++ component-based systems.

Usage: python tools/port_analyzer.py <PartitionClassName>
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field

import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser


@dataclass
class ScannedFiles:
    """Results of scanning project directory."""
    headers: list[Path] = field(default_factory=list)
    implementations: list[Path] = field(default_factory=list)


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


def create_parser() -> Parser:
    """Create and configure tree-sitter C++ parser."""
    parser = Parser(Language(tscpp.language()))
    return parser


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


if __name__ == "__main__":
    sys.exit(main())
