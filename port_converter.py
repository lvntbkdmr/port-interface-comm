#!/usr/bin/env python3
"""
Port Converter - Convert OUT_PORT macro-based port connections to flat mechanism.

This script reads the JSON export from port_analyzer.py and generates:
1. New header declarations (port members, setters, component accessors)
2. New source implementations
3. Updated InitRelations wiring code

Usage:
    python port_analyzer.py PartitionCls --export-json connections.json
    python port_converter.py connections.json --output-dir generated/
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class PortInfo:
    """Information about a port to generate."""
    member_name: str       # m_radaltOut
    setter_name: str       # SetRadaltOut
    interface: str         # RadaltExtDataIfc
    target_path: str       # Component path this port sends to


@dataclass
class ComponentAccessor:
    """Information about a component accessor to generate."""
    method_name: str       # GetEgiLruMgr
    member_name: str       # EgiLruMgr
    return_type: str       # EgiLruMgrCls


@dataclass
class ClassGenInfo:
    """Generated code info for a class."""
    class_name: str
    header_path: str | None
    impl_path: str | None
    ports: list[PortInfo] = field(default_factory=list)
    accessors: list[ComponentAccessor] = field(default_factory=list)
    base_classes: list[str] = field(default_factory=list)


@dataclass
class WiringStatement:
    """A wiring statement for InitRelations."""
    parent_class: str      # PartitionCls
    statement: str         # EgiMgr.GetEgiLruMgr().SetRadaltOut(&RadaltMgr.GetRadaltLruMgr());
    comment: str           # EgiLruMgr sends RadaltExtDataIfc to RadaltLruMgr


def load_connections(json_path: Path) -> dict:
    """Load exported connections from JSON file."""
    with open(json_path) as f:
        return json.load(f)


def derive_port_name(interface: str) -> str:
    """
    Derive a simple port name from interface name.

    EgiExtDataIfc -> egi
    RadaltExtDataIfc -> radalt
    Ans611ControlIfc -> command (special case)
    """
    # Remove 'Ifc' suffix
    name = interface.replace("Ifc", "").replace("ExtData", "").replace("Control", "")

    # Special mappings
    if "Ans611" in interface:
        return "command"

    # Convert to camelCase
    return name[0].lower() + name[1:] if name else "port"


def derive_accessor_name(member_name: str) -> str:
    """
    Derive accessor method name from member name.

    EgiLruMgr -> GetEgiLruMgr
    m_EgiFormatterCls -> GetEgiFormatter
    """
    name = member_name
    if name.startswith("m_"):
        name = name[2:]
    # Remove 'Cls' suffix if present
    if name.endswith("Cls"):
        name = name[:-3]
    return f"Get{name}"


def build_class_gen_info(data: dict) -> dict[str, ClassGenInfo]:
    """
    Build generation info for each class from the exported data.

    Returns dict mapping class_name -> ClassGenInfo
    """
    gen_info: dict[str, ClassGenInfo] = {}
    connections = data["connections"]

    def process_node(node: dict) -> None:
        class_name = node["class_name"]

        if class_name not in gen_info:
            gen_info[class_name] = ClassGenInfo(
                class_name=class_name,
                header_path=node.get("header_path"),
                impl_path=node.get("impl_path"),
                base_classes=node.get("base_classes", []),
            )

        info = gen_info[class_name]

        # Add component accessors for children
        for child in node.get("children", []):
            child_class = child["class_name"]
            child_member = child["name"]

            accessor = ComponentAccessor(
                method_name=derive_accessor_name(child_member),
                member_name=child_member,
                return_type=child_class,
            )

            # Avoid duplicates
            if not any(a.member_name == accessor.member_name for a in info.accessors):
                info.accessors.append(accessor)

            # Recurse
            process_node(child)

    process_node(data["component_tree"])

    # Add ports based on connections (from_path determines which class needs the port)
    for conn in connections:
        from_path = conn["from_path"]
        to_path = conn["to_path"]
        interface = conn["interface"]

        # Find the class that sends data (from_path)
        # The from_path is like "EgiMgr.EgiLruMgr" - we need the last component's class
        from_parts = from_path.split(".")
        from_class = _find_class_at_path(data["component_tree"], from_path)

        if from_class and from_class in gen_info:
            port_name = derive_port_name(interface)

            # Create unique port name if needed (e.g., radaltOut1, radaltOut2)
            existing_ports = [p.member_name for p in gen_info[from_class].ports]
            base_member = f"m_{port_name}Out"
            member_name = base_member
            counter = 1
            while member_name in existing_ports:
                counter += 1
                member_name = f"m_{port_name}Out{counter}"

            port = PortInfo(
                member_name=member_name,
                setter_name=f"Set{port_name[0].upper()}{port_name[1:]}Out" + (str(counter) if counter > 1 else ""),
                interface=interface,
                target_path=to_path,
            )

            gen_info[from_class].ports.append(port)

    return gen_info


def _find_class_at_path(tree: dict, path: str) -> str | None:
    """Find the class name at a given path in the component tree."""
    if not path:
        return tree.get("class_name")

    parts = path.split(".")
    current = tree

    for part in parts:
        found = None
        for child in current.get("children", []):
            if child["name"] == part:
                found = child
                break
        if found:
            current = found
        else:
            return None

    return current.get("class_name")


def generate_wiring_statements(data: dict, gen_info: dict[str, ClassGenInfo]) -> list[WiringStatement]:
    """
    Generate InitRelations wiring statements.

    Converts connections to flat wiring syntax like:
    EgiMgr.GetEgiLruMgr().SetRadaltOut(&RadaltMgr.GetRadaltLruMgr());
    """
    statements = []
    connections = data["connections"]

    # Group connections by the parent that should wire them
    # The parent is the common ancestor of from_path and to_path
    for conn in connections:
        from_path = conn["from_path"]
        to_path = conn["to_path"]
        interface = conn["interface"]

        from_parts = from_path.split(".")
        to_parts = to_path.split(".")

        # Find common prefix (the parent that should do the wiring)
        common_len = 0
        for i in range(min(len(from_parts), len(to_parts))):
            if from_parts[i] == to_parts[i]:
                common_len = i + 1
            else:
                break

        # Determine the parent class that should wire this
        if common_len == 0:
            # Root level wiring (PartitionCls)
            parent_class = data["component_tree"]["class_name"]
            parent_prefix = ""
        else:
            parent_path = ".".join(from_parts[:common_len])
            parent_class = _find_class_at_path(data["component_tree"], parent_path)
            parent_prefix = ""

        if not parent_class:
            continue

        # Build the wiring statement
        # from_path relative to parent -> accessor chain
        # to_path relative to parent -> accessor chain with &

        from_rel = from_parts[common_len:] if common_len < len(from_parts) else from_parts
        to_rel = to_parts[common_len:] if common_len < len(to_parts) else to_parts

        # Build accessor chains
        from_chain = _build_accessor_chain(from_rel, data["component_tree"], from_parts[:common_len])
        to_chain = _build_accessor_chain(to_rel, data["component_tree"], to_parts[:common_len])

        # Find the setter name for this port
        from_class = _find_class_at_path(data["component_tree"], from_path)
        setter_name = f"Set{derive_port_name(interface).capitalize()}Out"

        # Build statement
        if from_chain:
            statement = f"{from_chain}.{setter_name}(&{to_chain});"
        else:
            statement = f"{setter_name}(&{to_chain});"

        comment = f"{from_parts[-1]} sends {interface} to {to_parts[-1]}"

        statements.append(WiringStatement(
            parent_class=parent_class,
            statement=statement,
            comment=comment,
        ))

    return statements


def _build_accessor_chain(path_parts: list[str], tree: dict, prefix_parts: list[str]) -> str:
    """
    Build accessor chain for a path.

    ["EgiMgr", "EgiLruMgr"] -> "EgiMgr.GetEgiLruMgr()"
    """
    if not path_parts:
        return ""

    chain_parts = []
    current = tree

    # Navigate to prefix first
    for part in prefix_parts:
        for child in current.get("children", []):
            if child["name"] == part:
                current = child
                break

    # Build chain for remaining parts
    for i, part in enumerate(path_parts):
        for child in current.get("children", []):
            if child["name"] == part:
                if i == 0:
                    # First part is direct member access
                    chain_parts.append(part)
                else:
                    # Subsequent parts use accessor
                    accessor = derive_accessor_name(part)
                    chain_parts.append(f"{accessor}()")
                current = child
                break

    return ".".join(chain_parts)


def generate_header_additions(info: ClassGenInfo) -> str:
    """Generate header code additions for a class."""
    lines = []

    lines.append(f"// === Generated flat port mechanism for {info.class_name} ===")
    lines.append("")

    # Port members
    if info.ports:
        lines.append("// Output ports")
        for port in info.ports:
            lines.append(f"    {port.interface}* {port.member_name}{{nullptr}};")
        lines.append("")

    # Port setters
    if info.ports:
        lines.append("// Port setters")
        for port in info.ports:
            lines.append(f"    void {port.setter_name}({port.interface}* port);")
        lines.append("")

    # Component accessors
    if info.accessors:
        lines.append("// Component accessors for external wiring")
        for acc in info.accessors:
            lines.append(f"    {acc.return_type}& {acc.method_name}();")
        lines.append("")

    return "\n".join(lines)


def generate_source_additions(info: ClassGenInfo) -> str:
    """Generate source code additions for a class."""
    lines = []

    lines.append(f"// === Generated flat port mechanism for {info.class_name} ===")
    lines.append("")

    # Port setters
    for port in info.ports:
        lines.append(f"void {info.class_name}::{port.setter_name}({port.interface}* port)")
        lines.append("{")
        lines.append(f"    {port.member_name} = port;")
        lines.append("}")
        lines.append("")

    # Component accessors
    for acc in info.accessors:
        lines.append(f"{acc.return_type}& {info.class_name}::{acc.method_name}()")
        lines.append("{")
        lines.append(f"    return {acc.member_name};")
        lines.append("}")
        lines.append("")

    return "\n".join(lines)


def generate_init_relations(class_name: str, statements: list[WiringStatement]) -> str:
    """Generate InitRelations method for a class."""
    class_statements = [s for s in statements if s.parent_class == class_name]

    if not class_statements:
        return ""

    lines = []
    lines.append(f"void {class_name}::InitRelations()")
    lines.append("{")

    for stmt in class_statements:
        lines.append(f"    // {stmt.comment}")
        lines.append(f"    {stmt.statement}")
        lines.append("")

    lines.append("}")

    return "\n".join(lines)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert OUT_PORT macro-based ports to flat mechanism"
    )
    parser.add_argument("json_file", help="JSON file exported from port_analyzer.py")
    parser.add_argument(
        "--output-dir",
        default="generated",
        help="Output directory for generated code (default: generated/)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated code instead of writing files"
    )

    args = parser.parse_args()

    # Load data
    json_path = Path(args.json_file)
    if not json_path.exists():
        print(f"Error: File not found: {json_path}", file=sys.stderr)
        return 1

    data = load_connections(json_path)

    # Build generation info
    gen_info = build_class_gen_info(data)

    # Generate wiring statements
    statements = generate_wiring_statements(data, gen_info)

    # Output directory
    output_dir = Path(args.output_dir)
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Generate code for each class
    for class_name, info in gen_info.items():
        if not info.ports and not info.accessors:
            continue

        header_code = generate_header_additions(info)
        source_code = generate_source_additions(info)
        init_relations = generate_init_relations(class_name, statements)

        if args.dry_run:
            print(f"\n{'='*60}")
            print(f"CLASS: {class_name}")
            print(f"{'='*60}")

            if header_code.strip():
                print(f"\n--- Header additions ({info.header_path}) ---")
                print(header_code)

            if source_code.strip():
                print(f"\n--- Source additions ({info.impl_path}) ---")
                print(source_code)

            if init_relations:
                print(f"\n--- InitRelations ---")
                print(init_relations)
        else:
            # Write to files
            if header_code.strip():
                header_file = output_dir / f"{class_name}_header.txt"
                header_file.write_text(header_code)
                print(f"Generated: {header_file}")

            if source_code.strip():
                source_file = output_dir / f"{class_name}_source.txt"
                source_file.write_text(source_code)
                print(f"Generated: {source_file}")

            if init_relations:
                init_file = output_dir / f"{class_name}_init_relations.txt"
                init_file.write_text(init_relations)
                print(f"Generated: {init_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
