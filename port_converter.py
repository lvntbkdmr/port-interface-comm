#!/usr/bin/env python3
"""
Port Converter - Convert OUT_PORT macro-based port connections to flat mechanism.

This script reads the JSON export from port_analyzer.py and directly edits
the C++ header and source files to add:
1. Port member declarations (private section)
2. Port setter declarations (public section)
3. Component accessor declarations (public section)
4. Port setter implementations (source file)
5. Component accessor implementations (source file)
6. InitRelations wiring code

Usage:
    python port_analyzer.py PartitionCls --export-json connections.json
    python port_converter.py connections.json --dry-run     # Preview changes
    python port_converter.py connections.json --apply       # Apply changes
"""

import json
import re
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
            parent_class = data["component_tree"]["class_name"]
        else:
            parent_path = ".".join(from_parts[:common_len])
            parent_class = _find_class_at_path(data["component_tree"], parent_path)

        if not parent_class:
            continue

        from_rel = from_parts[common_len:] if common_len < len(from_parts) else from_parts
        to_rel = to_parts[common_len:] if common_len < len(to_parts) else to_parts

        # Build accessor chains
        from_chain = _build_accessor_chain(from_rel, data["component_tree"], from_parts[:common_len])
        to_chain = _build_accessor_chain(to_rel, data["component_tree"], to_parts[:common_len])

        setter_name = f"Set{derive_port_name(interface).capitalize()}Out"

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
                    chain_parts.append(part)
                else:
                    accessor = derive_accessor_name(part)
                    chain_parts.append(f"{accessor}()")
                current = child
                break

    return ".".join(chain_parts)


# ============================================================================
# Header file editing
# ============================================================================

def edit_header_file(header_path: str, info: ClassGenInfo) -> tuple[str, str]:
    """
    Edit a header file to add port members, setters, and accessors.

    Returns (original_content, modified_content)
    """
    with open(header_path) as f:
        content = f.read()

    original = content

    # Find the class definition
    class_pattern = rf'class\s+{re.escape(info.class_name)}\s*[^{{]*\{{'
    class_match = re.search(class_pattern, content)
    if not class_match:
        print(f"  Warning: Could not find class {info.class_name} in {header_path}")
        return original, original

    # Find sections in the class
    class_start = class_match.end()

    # Find the closing brace of the class (matching braces)
    brace_count = 1
    class_end = class_start
    for i in range(class_start, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                class_end = i
                break

    class_body = content[class_start:class_end]

    # Check what already exists to avoid duplicates
    existing_content = class_body

    # Generate new declarations
    new_public_decls = []
    new_private_decls = []

    # Port setters (public)
    for port in info.ports:
        setter_decl = f"void {port.setter_name}({port.interface}* port);"
        if setter_decl not in existing_content and port.setter_name not in existing_content:
            new_public_decls.append(f"    {setter_decl}")

    # Component accessors (public)
    for acc in info.accessors:
        accessor_decl = f"{acc.return_type}& {acc.method_name}();"
        if accessor_decl not in existing_content and f"{acc.method_name}()" not in existing_content:
            new_public_decls.append(f"    {accessor_decl}")

    # Port members (private)
    for port in info.ports:
        member_decl = f"{port.interface}* {port.member_name}{{nullptr}};"
        if port.member_name not in existing_content:
            new_private_decls.append(f"    {member_decl}")

    if not new_public_decls and not new_private_decls:
        return original, original  # Nothing to add

    # Find insertion points
    # Look for existing public/private sections
    public_match = re.search(r'\bpublic\s*:', class_body)
    private_match = re.search(r'\bprivate\s*:', class_body)
    protected_match = re.search(r'\bprotected\s*:', class_body)

    insertions = []  # List of (position, text) to insert

    # Insert public declarations after "public:" line
    if new_public_decls and public_match:
        # Find end of the public: line
        public_pos = class_start + public_match.end()
        # Find the next newline
        next_newline = content.find('\n', public_pos)
        if next_newline != -1:
            insert_text = "\n" + "\n".join(new_public_decls)
            insertions.append((next_newline, insert_text))

    # Insert private declarations
    if new_private_decls:
        if private_match:
            # Add after private: line
            private_pos = class_start + private_match.end()
            next_newline = content.find('\n', private_pos)
            if next_newline != -1:
                insert_text = "\n" + "\n".join(new_private_decls)
                insertions.append((next_newline, insert_text))
        else:
            # No private section exists, add one before class closing brace
            insert_text = "\nprivate:\n" + "\n".join(new_private_decls) + "\n"
            insertions.append((class_end, insert_text))

    # Apply insertions in reverse order (so positions stay valid)
    insertions.sort(key=lambda x: x[0], reverse=True)
    modified = content
    for pos, text in insertions:
        modified = modified[:pos] + text + modified[pos:]

    return original, modified


# ============================================================================
# Source file editing
# ============================================================================

def edit_source_file(impl_path: str, info: ClassGenInfo, statements: list[WiringStatement]) -> tuple[str, str]:
    """
    Edit a source file to add port setters, accessors, and InitRelations.

    Returns (original_content, modified_content)
    """
    with open(impl_path) as f:
        content = f.read()

    original = content
    additions = []

    # Check what already exists
    existing = content

    # Add port setter implementations
    for port in info.ports:
        func_sig = f"{info.class_name}::{port.setter_name}"
        if func_sig not in existing:
            impl = f"""
void {info.class_name}::{port.setter_name}({port.interface}* port)
{{
    {port.member_name} = port;
}}
"""
            additions.append(impl)

    # Add accessor implementations
    for acc in info.accessors:
        func_sig = f"{info.class_name}::{acc.method_name}"
        if func_sig not in existing:
            impl = f"""
{acc.return_type}& {info.class_name}::{acc.method_name}()
{{
    return {acc.member_name};
}}
"""
            additions.append(impl)

    # Handle InitRelations
    class_statements = [s for s in statements if s.parent_class == info.class_name]
    if class_statements:
        init_relations_pattern = rf'void\s+{re.escape(info.class_name)}::InitRelations\s*\([^)]*\)\s*\{{'
        init_match = re.search(init_relations_pattern, content)

        if init_match:
            # InitRelations exists - add new wiring statements
            # Find the closing brace of the function
            func_start = init_match.end()
            brace_count = 1
            func_end = func_start
            for i in range(func_start, len(content)):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        func_end = i
                        break

            # Check which statements are missing
            func_body = content[func_start:func_end]
            new_stmts = []
            for stmt in class_statements:
                # Check if this wiring already exists (simplified check)
                if stmt.statement not in func_body:
                    new_stmts.append(f"    // {stmt.comment}")
                    new_stmts.append(f"    {stmt.statement}")
                    new_stmts.append("")

            if new_stmts:
                # Insert before the closing brace
                insert_text = "\n    // === Generated flat port wiring ===\n" + "\n".join(new_stmts)
                content = content[:func_end] + insert_text + content[func_end:]
        else:
            # InitRelations doesn't exist - create it
            lines = []
            lines.append(f"\nvoid {info.class_name}::InitRelations()")
            lines.append("{")
            for stmt in class_statements:
                lines.append(f"    // {stmt.comment}")
                lines.append(f"    {stmt.statement}")
                lines.append("")
            lines.append("}")
            additions.append("\n".join(lines))

    # Append additions to end of file
    if additions:
        # Ensure file ends with newline
        if content and not content.endswith('\n'):
            content += '\n'
        content += "\n// === Generated flat port mechanism ===\n"
        content += "\n".join(additions)

    return original, content


# ============================================================================
# Main entry point
# ============================================================================

def generate_preview(info: ClassGenInfo, statements: list[WiringStatement]) -> str:
    """Generate a preview of changes for dry-run mode."""
    lines = []

    lines.append(f"\n{'='*60}")
    lines.append(f"CLASS: {info.class_name}")
    lines.append(f"{'='*60}")

    if info.ports:
        lines.append(f"\n--- Port members (private) ---")
        for port in info.ports:
            lines.append(f"    {port.interface}* {port.member_name}{{nullptr}};")

    if info.ports:
        lines.append(f"\n--- Port setters (public) ---")
        for port in info.ports:
            lines.append(f"    void {port.setter_name}({port.interface}* port);")

    if info.accessors:
        lines.append(f"\n--- Component accessors (public) ---")
        for acc in info.accessors:
            lines.append(f"    {acc.return_type}& {acc.method_name}();")

    if info.ports:
        lines.append(f"\n--- Setter implementations ---")
        for port in info.ports:
            lines.append(f"void {info.class_name}::{port.setter_name}({port.interface}* port)")
            lines.append("{")
            lines.append(f"    {port.member_name} = port;")
            lines.append("}")
            lines.append("")

    if info.accessors:
        lines.append(f"\n--- Accessor implementations ---")
        for acc in info.accessors:
            lines.append(f"{acc.return_type}& {info.class_name}::{acc.method_name}()")
            lines.append("{")
            lines.append(f"    return {acc.member_name};")
            lines.append("}")
            lines.append("")

    class_statements = [s for s in statements if s.parent_class == info.class_name]
    if class_statements:
        lines.append(f"\n--- InitRelations wiring ---")
        for stmt in class_statements:
            lines.append(f"    // {stmt.comment}")
            lines.append(f"    {stmt.statement}")

    return "\n".join(lines)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert OUT_PORT macro-based ports to flat mechanism"
    )
    parser.add_argument("json_file", help="JSON file exported from port_analyzer.py")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes directly to C++ files"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Create .bak backup files before modifying (default: True)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_false",
        dest="backup",
        help="Don't create backup files"
    )

    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        print("Error: Must specify --dry-run or --apply", file=sys.stderr)
        return 1

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

    if args.dry_run:
        print("=" * 60)
        print("DRY RUN - Preview of changes")
        print("=" * 60)

        for class_name, info in gen_info.items():
            if not info.ports and not info.accessors:
                continue
            print(generate_preview(info, statements))

        print("\n" + "=" * 60)
        print("Run with --apply to modify files")
        print("=" * 60)
        return 0

    # Apply mode - edit files directly
    modified_files = []

    for class_name, info in gen_info.items():
        if not info.ports and not info.accessors:
            continue

        print(f"\nProcessing {class_name}...")

        # Edit header file
        if info.header_path and Path(info.header_path).exists():
            original, modified = edit_header_file(info.header_path, info)
            if original != modified:
                if args.backup:
                    backup_path = info.header_path + ".bak"
                    Path(backup_path).write_text(original)
                    print(f"  Backup: {backup_path}")
                Path(info.header_path).write_text(modified)
                print(f"  Modified: {info.header_path}")
                modified_files.append(info.header_path)
            else:
                print(f"  Skipped: {info.header_path} (no changes needed)")

        # Edit source file
        if info.impl_path and Path(info.impl_path).exists():
            original, modified = edit_source_file(info.impl_path, info, statements)
            if original != modified:
                if args.backup:
                    backup_path = info.impl_path + ".bak"
                    Path(backup_path).write_text(original)
                    print(f"  Backup: {backup_path}")
                Path(info.impl_path).write_text(modified)
                print(f"  Modified: {info.impl_path}")
                modified_files.append(info.impl_path)
            else:
                print(f"  Skipped: {info.impl_path} (no changes needed)")

    print(f"\n{'='*60}")
    print(f"Modified {len(modified_files)} files")
    if args.backup:
        print("Backup files created with .bak extension")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
