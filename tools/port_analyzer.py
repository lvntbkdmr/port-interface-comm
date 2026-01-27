#!/usr/bin/env python3
"""
Port Analyzer - Static analysis tool for detecting port connections
in C++ component-based systems.

Usage: python tools/port_analyzer.py <PartitionClassName>
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field


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
    print(f"Found {len(scanned.headers)} headers, {len(scanned.implementations)} implementations")

    for h in sorted(scanned.headers):
        print(f"  Header: {h.relative_to(project_root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
