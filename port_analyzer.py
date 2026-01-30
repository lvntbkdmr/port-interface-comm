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
    unresolved: bool = False  # True if target couldn't be resolved


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
    try:
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
    except Exception as e:
        print(f"Warning: Failed to parse {file_path}: {e}", file=sys.stderr)
        return None


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
        child_indent = ""
    else:
        connector = "└── " if is_last else "├── "
        print(f"  {indent}{connector}{node.name}: {node.class_name}")
        child_indent = indent + ("    " if is_last else "│   ")

    # Print children
    for i, child in enumerate(node.children):
        print_component_tree(child, child_indent, i == len(node.children) - 1)


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
                # Parse the function body with variable tracking
                wirings.extend(_parse_init_relations_body_with_vars(content, node))

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
        # Handle pointer return types: EgiExtDataIfc * Class::Method()
        elif child.type == "pointer_declarator":
            for pc in child.children:
                if pc.type == "function_declarator":
                    for fc in pc.children:
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


def _parse_init_relations_body_with_vars(content: bytes, func_node) -> list[tuple[str, str]]:
    """Parse function body for port wirings with variable tracking."""
    wirings = []
    var_map: dict[str, str] = {}  # var_name -> getter_expression

    for child in func_node.children:
        if child.type == "compound_statement":
            for stmt in child.children:
                # First, check for variable declarations with getter assignments
                var_decl = _parse_var_declaration(content, stmt)
                if var_decl:
                    var_name, getter_expr = var_decl
                    var_map[var_name] = getter_expr
                    continue

                # Then check for wirings (setter calls or port assignments)
                wiring = _parse_statement_for_wiring_with_vars(content, stmt, var_map)
                if wiring:
                    wirings.append(wiring)

    return wirings


def _parse_var_declaration(content: bytes, stmt_node) -> tuple[str, str] | None:
    """
    Parse variable declaration with getter assignment.

    Pattern: Type* VarName = Obj.GetIts*Port*();
    Returns: (var_name, getter_expression) or None
    """
    if stmt_node.type != "declaration":
        return None

    stmt_text = content[stmt_node.start_byte:stmt_node.end_byte].decode().strip()

    # Check if this is a port-related getter assignment
    if "GetIts" not in stmt_text or "Port" not in stmt_text:
        return None

    import re
    # Match: Type* VarName = Obj.GetIts...Port...();
    match = re.search(
        r'[A-Za-z_][A-Za-z0-9_]*\s*\*?\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([A-Za-z_][A-Za-z0-9_]*\.GetIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*\(\))',
        stmt_text
    )
    if match:
        return (match.group(1), match.group(2))

    return None


def _parse_statement_for_wiring_with_vars(
    content: bytes,
    stmt_node,
    var_map: dict[str, str],
) -> tuple[str, str] | None:
    """
    Parse a statement to find port wiring patterns, resolving variables.
    """
    if stmt_node.type == "expression_statement":
        for child in stmt_node.children:
            return _parse_expression_for_wiring_with_vars(content, child, var_map)
    return None


def _parse_expression_for_wiring_with_vars(
    content: bytes,
    expr_node,
    var_map: dict[str, str],
) -> tuple[str, str] | None:
    """Parse expression for wiring pattern, resolving variables."""
    expr_text = content[expr_node.start_byte:expr_node.end_byte].decode().strip()

    import re

    # Pattern 1: Obj.SetIts*Port*(arg) - where arg might be a variable
    if expr_node.type == "call_expression" and "SetIts" in expr_text and "Port" in expr_text:
        match = re.match(
            r'([A-Za-z_][A-Za-z0-9_]*)\.([Ss]etIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*)\(([^)]+)\)',
            expr_text.replace('\n', ' ').replace(' ', '')
        )
        if match:
            setter_obj = match.group(1)
            setter_method = match.group(2)
            arg = match.group(3)

            # Resolve the argument if it's a variable
            if arg in var_map:
                getter_expr = var_map[arg]
            elif "GetIts" in arg and "Port" in arg:
                getter_expr = arg
            else:
                # Unresolved variable - return as-is for debugging
                getter_expr = arg

            return (f"{setter_obj}.{setter_method}", getter_expr)

    # Note: We intentionally skip Pattern 2 (ItsX = Y.GetIts*Port*())
    # Port member assignments are for delegation/exposure, not actual data flows.
    # Actual data flows are established through setter calls from external components.

    return None


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

    # Note: We skip port member assignments (ItsX = Y.GetIts*Port*())
    # These are delegation/exposure, not actual data flows.

    return None


def _extract_setter_getter(expr_text: str) -> tuple[str, str] | None:
    """
    Extract setter and getter from: Obj.SetIts*Port*(Arg.GetIts*Port*())
    """
    import re

    # Match: something.SetIts...Port...(...GetIts...Port...())
    # Capture the object calling Set and the argument with Get
    # Use .+ with greedy matching and anchor to end to handle nested parens
    match = re.match(
        r'([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*)\.(SetIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*)\((.+)\)$',
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


def trace_getter_to_source(
    getter_expr: str,
    current_path: str,
    registry: dict[str, ClassInfo],
    parser: Parser,
    tree: 'ComponentNode',
    depth: int = 0,
) -> str:
    """
    Trace a getter expression to find the ultimate source component.

    E.g., Egi1Cmp.GetItsAns611ControlInPortAns611ControlIfc() traces through
    EgiCmpCls to find it returns m_EgiFormatterCls.

    Returns the full path to the source component.
    """
    if depth > 5:  # Prevent infinite recursion
        return resolve_member_path(getter_expr)

    import re

    # Parse the getter expression: Obj.GetIts*Port*()
    match = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\.GetIts([A-Za-z0-9_]*)Port([A-Za-z0-9_]*)\(\)', getter_expr)
    if not match:
        return resolve_member_path(getter_expr)

    obj_name = match.group(1)
    port_name = f"Its{match.group(2)}Port{match.group(3)}"

    # Find the object's class in the component tree
    obj_class = _find_class_at_path(tree, obj_name)
    if not obj_class:
        return f"{current_path}.{obj_name}" if current_path else obj_name

    # Look up the class info
    class_info = registry.get(obj_class)
    if not class_info or not class_info.impl_path:
        return f"{current_path}.{obj_name}" if current_path else obj_name

    # Parse the class's InitRelations to see where port_name is assigned from
    source = _find_port_source(parser, class_info.impl_path, port_name)
    if source:
        # source is something like "m_EgiFormatterCls.GetIts...Port...()"
        # Recursively trace it
        obj_path = f"{current_path}.{obj_name}" if current_path else obj_name

        # Build a subtree for the object
        subtree = _find_subtree(tree, obj_name)
        if subtree:
            traced = trace_getter_to_source(source, obj_path, registry, parser, subtree, depth + 1)
            return traced

    # Default: just return the object path
    return f"{current_path}.{obj_name}" if current_path else obj_name


def _find_class_at_path(tree: 'ComponentNode', member_name: str) -> str | None:
    """Find the class name of a direct child member in the tree."""
    for child in tree.children:
        if child.name == member_name:
            return child.class_name
    return None


def _find_subtree(tree: 'ComponentNode', member_name: str) -> 'ComponentNode | None':
    """Find the subtree for a direct child member."""
    for child in tree.children:
        if child.name == member_name:
            return child
    return None


def _find_port_source(parser: Parser, impl_path: Path, port_name: str) -> str | None:
    """
    Find what a port member is assigned from in InitRelations.

    Looks for pattern: ItsXxxPortYyy = something.GetIts*Port*();
    or: port_name = something.GetIts*Port*();
    """
    content = impl_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    for node in root.children:
        if node.type == "function_definition":
            func_name = _get_function_name(content, node)
            if func_name and "InitRelations" in func_name:
                return _find_assignment_source(content, node, port_name)

    return None


def _find_assignment_source(content: bytes, func_node, target_pattern: str) -> str | None:
    """Find the source of an assignment to a port member."""
    import re

    for child in func_node.children:
        if child.type == "compound_statement":
            for stmt in child.children:
                if stmt.type == "expression_statement":
                    stmt_text = content[stmt.start_byte:stmt.end_byte].decode().strip()

                    # Look for assignment to the target pattern
                    # Pattern: ItsXxxPortYyy = something.GetIts*Port*()
                    match = re.match(
                        rf'(Its[A-Za-z0-9_]*{re.escape(target_pattern[3:])}|{re.escape(target_pattern)})\s*=\s*([A-Za-z_][A-Za-z0-9_]*\.GetIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*\(\))',
                        stmt_text
                    )
                    if match:
                        return match.group(2)

    return None


def parse_data_forwardings(
    parser: Parser,
    impl_path: Path,
) -> list[tuple[str, str, str]]:
    """
    Parse interface method implementations for OUT_PORT data forwarding.

    Looks for pattern in Set*() methods:
        OUT_PORT(PortName, Interface)->SetXxx(data);

    Returns list of (method_name, port_member, interface) tuples.
    E.g., ("SetRadaltExtData", "ItsEgi1RadaltInPortRadaltExtDataIfc", "RadaltExtDataIfc")
    """
    import re

    content = impl_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    forwardings = []

    for node in root.children:
        if node.type == "function_definition":
            func_name = _get_function_name(content, node)
            # Look for Set* methods (interface implementations)
            if func_name and "::Set" in func_name:
                method_name = func_name.split("::")[-1] if "::" in func_name else func_name

                # Parse body for OUT_PORT calls
                for child in node.children:
                    if child.type == "compound_statement":
                        body_text = content[child.start_byte:child.end_byte].decode()

                        # Find OUT_PORT(PortName, Interface)->Set...(...)
                        for match in re.finditer(
                            r'OUT_PORT\(([A-Za-z0-9_]+),\s*([A-Za-z0-9_]+)\)->([A-Za-z0-9_]+)\(',
                            body_text
                        ):
                            port_name = match.group(1)
                            interface = match.group(2)
                            # Construct the full port member name: Its{PortName}{Interface}
                            port_member = f"Its{port_name}{interface}"
                            forwardings.append((method_name, port_member, interface))

    return forwardings


def parse_setter_forwardings(
    parser: Parser,
    impl_path: Path,
) -> list[tuple[str, str, str]]:
    """
    Parse setter methods to find forwarded port connections.

    Looks for pattern in SetIts*Port* methods:
        ChildComponent.SetIts*Port*(ifc);

    Returns list of (setter_method, child_component, child_setter) tuples.
    E.g., ("SetItsEgi1ControlOutPortAns611ControlIfc", "Egi1ModController", "SetItsControlOutPortAns611ControlIfc")
    """
    content = impl_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    forwardings = []

    for node in root.children:
        if node.type == "function_definition":
            func_name = _get_function_name(content, node)
            if func_name and ("SetIts" in func_name or "setIts" in func_name) and ("Port" in func_name or "port" in func_name):
                # Extract just the method name (after ::)
                if "::" in func_name:
                    method_name = func_name.split("::")[-1]
                else:
                    method_name = func_name

                # Look for child setter calls in the body
                forwards = _parse_setter_body_for_forwards(content, node)
                for child_comp, child_setter in forwards:
                    forwardings.append((method_name, child_comp, child_setter))

    return forwardings


def _parse_setter_body_for_forwards(content: bytes, func_node) -> list[tuple[str, str]]:
    """
    Parse setter method body for forwarded calls.

    Returns list of (child_component, child_setter_method) tuples.
    """
    import re
    forwards = []

    for child in func_node.children:
        if child.type == "compound_statement":
            for stmt in child.children:
                if stmt.type == "expression_statement":
                    stmt_text = content[stmt.start_byte:stmt.end_byte].decode().strip()

                    # Look for: ChildComponent.SetIts*Port*(ifc); or setIts*Port*
                    match = re.match(
                        r'([A-Za-z_][A-Za-z0-9_]*)\.([sS]et[Ii]ts[A-Za-z0-9_]*[Pp]ort[A-Za-z0-9_]*)\(([A-Za-z_][A-Za-z0-9_]*)\)',
                        stmt_text
                    )
                    if match:
                        child_comp = match.group(1)
                        child_setter = match.group(2)
                        forwards.append((child_comp, child_setter))

    return forwards


def _path_exists_in_tree(tree: ComponentNode, path: str) -> bool:
    """Check if a member path exists in the component tree."""
    if not path:
        return True

    parts = [p for p in path.split(".") if p]
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


def collect_connections(
    tree: ComponentNode,
    registry: dict[str, ClassInfo],
    parser: Parser,
    parent_path: str = "",
    root_tree: 'ComponentNode | None' = None,
) -> list[PortConnection]:
    """
    Recursively collect all port connections from component tree.
    """
    connections = []
    current_path = tree.get_path(parent_path)

    # Keep reference to root tree for path resolution
    if root_tree is None:
        root_tree = tree

    info = registry.get(tree.class_name)
    if info and info.impl_path:
        wirings = parse_init_relations(parser, info.impl_path)

        for setter, getter in wirings:
            # Extract interface from setter/port name
            interface = extract_interface_from_port(setter)

            # Resolve from_path by tracing through setter forwarding chain
            if "." in setter:
                setter_parts = setter.split(".")
                setter_obj = setter_parts[0]
                setter_method = setter_parts[1] if len(setter_parts) > 1 else setter
                base_from_path = f"{current_path}.{setter_obj}" if current_path else setter_obj

                # Trace through setter forwarding to find the leaf component
                from_path = trace_setter_to_leaf(
                    base_from_path, setter_method, tree, registry, parser
                )
            else:
                from_path = current_path
                setter_method = setter

            # Trace getter to find the receiver component
            to_path = trace_getter_to_receiver(getter, current_path, registry, parser, tree)

            # Check if to_path is valid
            unresolved = not _path_exists_in_tree(root_tree, to_path.lstrip("."))

            connections.append(PortConnection(
                from_path=from_path,
                to_path=to_path,
                interface=interface,
                unresolved=unresolved,
            ))

            # Also add connections for any forwarded ports (deeper child components)
            # Start from the original setter object path, not the traced leaf
            if "." in setter:
                original_setter_path = f"{current_path}.{setter_parts[0]}" if current_path else setter_parts[0]
                _add_forwarded_connections(
                    connections, setter_parts[0], setter_method, original_setter_path, to_path,
                    interface, tree, registry, parser, unresolved,
                    already_added_path=from_path  # Skip duplicates with the main connection
                )

    # Also check for data forwarding via OUT_PORT in interface method implementations
    if info and info.impl_path:
        data_forwardings = parse_data_forwardings(parser, info.impl_path)
        for method_name, port_member, interface in data_forwardings:
            # Find where this port points to by checking InitRelations
            # The port was assigned from some child's getter
            target = _resolve_port_member_target(port_member, tree, registry, parser)
            if target:
                to_path = f"{current_path}.{target}" if current_path else target
                unresolved = not _path_exists_in_tree(root_tree, to_path.lstrip("."))

                connections.append(PortConnection(
                    from_path=current_path if current_path else tree.class_name,
                    to_path=to_path,
                    interface=interface,
                    unresolved=unresolved,
                ))

    # Recurse into children
    for child in tree.children:
        child_path = tree.get_path(parent_path)
        connections.extend(collect_connections(child, registry, parser, child_path, root_tree))

    return connections


def _resolve_port_member_target(
    port_member: str,
    tree: ComponentNode,
    registry: dict[str, ClassInfo],
    parser: Parser,
) -> str | None:
    """
    Resolve where a port member (Its*Port*) points to.

    Looks in InitRelations for the assignment:
        ItsXxxPortYyy = Child.GetIts*Port*();

    Returns the child component path (e.g., "Egi1Cmp") or None if not found.
    """
    class_info = registry.get(tree.class_name)
    if not class_info or not class_info.impl_path:
        return None

    source = _find_port_member_source(parser, class_info.impl_path, port_member)
    if source:
        # source is like "Egi1Cmp.GetItsRadaltInPortRadaltExtDataIfc()"
        # Extract the object name and trace to final target
        import re
        match = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\.GetIts', source)
        if match:
            child_name = match.group(1)
            # Check if this child's getter returns 'this' or traces deeper
            child_class = _find_class_at_path(tree, child_name)
            if child_class:
                child_info = registry.get(child_class)
                if child_info and child_info.impl_path:
                    getter_return = _analyze_getter_return(parser, child_info.impl_path, source)
                    if getter_return == "this":
                        return child_name
                    elif getter_return and getter_return.startswith("Its") and "Port" in getter_return:
                        # Trace deeper through port member
                        subtree = _find_subtree(tree, child_name)
                        if subtree:
                            deeper = _resolve_port_member_target(getter_return, subtree, registry, parser)
                            if deeper:
                                return f"{child_name}.{deeper}"
            return child_name

    return None


def _add_forwarded_connections(
    connections: list[PortConnection],
    setter_obj: str,
    setter_method: str,
    base_from_path: str,
    to_path: str,
    interface: str,
    tree: ComponentNode,
    registry: dict[str, ClassInfo],
    parser: Parser,
    unresolved: bool,
    already_added_path: str = "",
) -> None:
    """
    Recursively add connections for forwarded ports.

    When a setter forwards to child components, add those as separate connections.
    already_added_path is the main connection's from_path to avoid duplicates.
    """
    # Find the class of the setter object
    setter_class = _find_class_at_path(tree, setter_obj)
    if not setter_class:
        return

    setter_info = registry.get(setter_class)
    if not setter_info or not setter_info.impl_path:
        return

    # Find forwardings in the setter method
    forwardings = parse_setter_forwardings(parser, setter_info.impl_path)
    for fwd_setter, child_comp, child_setter in forwardings:
        if fwd_setter.lower() == setter_method.lower():
            # Found a forwarding - add the connection
            fwd_from_path = f"{base_from_path}.{child_comp}"
            fwd_interface = extract_interface_from_port(child_setter)

            # Skip if this is the same as the already added main connection
            if fwd_from_path != already_added_path:
                connections.append(PortConnection(
                    from_path=fwd_from_path,
                    to_path=to_path,
                    interface=fwd_interface,
                    unresolved=unresolved,
                ))

            # Recursively check for deeper forwardings
            subtree = _find_subtree(tree, setter_obj)
            if subtree:
                _add_forwarded_connections(
                    connections, child_comp, child_setter, fwd_from_path, to_path,
                    fwd_interface, subtree, registry, parser, unresolved,
                    already_added_path
                )


def trace_setter_to_leaf(
    base_path: str,
    setter_method: str,
    tree: ComponentNode,
    registry: dict[str, ClassInfo],
    parser: Parser,
    depth: int = 0,
) -> str:
    """
    Trace through setter forwarding chain to find the leaf component.

    When a setter like SetItsDataOutPortXxx forwards to a child component,
    follow the chain to find who actually has the OUT_PORT.
    """
    if depth > 5:
        return base_path

    # Find the class at base_path
    path_parts = [p for p in base_path.split(".") if p]
    current = tree
    for part in path_parts:
        found = None
        for child in current.children:
            if child.name == part:
                found = child
                break
        if found:
            current = found
        else:
            return base_path

    class_name = current.class_name
    class_info = registry.get(class_name)
    if not class_info or not class_info.impl_path:
        return base_path

    # Check if this setter forwards to a child
    forwardings = parse_setter_forwardings(parser, class_info.impl_path)
    for fwd_setter, child_comp, child_setter in forwardings:
        # Case-insensitive comparison for setter method names
        if fwd_setter.lower() == setter_method.lower():
            # Found forwarding - recurse
            child_path = f"{base_path}.{child_comp}"
            return trace_setter_to_leaf(
                child_path, child_setter, tree, registry, parser, depth + 1
            )

    return base_path


def trace_getter_to_receiver(
    getter_expr: str,
    current_path: str,
    registry: dict[str, ClassInfo],
    parser: Parser,
    tree: ComponentNode,
    depth: int = 0,
) -> str:
    """
    Trace a getter expression to find the component that receives data.

    When a getter like GetItsRadaltInPortXxx() returns 'this', the component
    itself is the receiver. When it returns a member's getter, trace further.
    """
    if depth > 5:
        return resolve_member_path(getter_expr)

    import re

    # Parse the getter expression: Obj.GetIts*Port*()
    match = re.match(r'([A-Za-z_][A-Za-z0-9_]*)\.GetIts([A-Za-z0-9_]*)Port([A-Za-z0-9_]*)\(\)', getter_expr)
    if not match:
        return resolve_member_path(getter_expr)

    obj_name = match.group(1)
    obj_path = f"{current_path}.{obj_name}" if current_path else obj_name

    # Find the object's class
    obj_class = _find_class_at_path(tree, obj_name)
    if not obj_class:
        return obj_path

    class_info = registry.get(obj_class)
    if not class_info or not class_info.impl_path:
        return obj_path

    # Check if the getter returns 'this' or a member
    getter_return = _analyze_getter_return(parser, class_info.impl_path, getter_expr)

    if getter_return == "this":
        # The component itself receives the data
        return obj_path
    elif getter_return:
        # Check if it returns a port member (Its*Port*)
        if getter_return.startswith("Its") and "Port" in getter_return:
            # Trace through port member assignment
            subtree = _find_subtree(tree, obj_name)
            if subtree:
                return trace_port_member_to_source(getter_return, obj_path, registry, parser, subtree, depth + 1)
        # It returns something else (like another getter) - trace further
        subtree = _find_subtree(tree, obj_name)
        if subtree:
            return trace_getter_to_receiver(getter_return, obj_path, registry, parser, subtree, depth + 1)

    return obj_path


def _analyze_getter_return(parser: Parser, impl_path: Path, getter_expr: str) -> str | None:
    """
    Analyze what a getter method returns.

    Returns:
    - "this" if it returns this
    - A getter expression if it returns a member's port
    - None if can't determine
    """
    import re

    # Extract method name from getter_expr
    match = re.match(r'[A-Za-z_][A-Za-z0-9_]*\.(GetIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*)\(\)', getter_expr)
    if not match:
        return None

    method_name = match.group(1)

    content = impl_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    for node in root.children:
        if node.type == "function_definition":
            func_name = _get_function_name(content, node)
            if func_name and method_name in func_name:
                # Found the getter - analyze its return statement
                return _find_return_value(content, node)

    return None


def _find_return_value(content: bytes, func_node) -> str | None:
    """Find what a function returns."""
    for child in func_node.children:
        if child.type == "compound_statement":
            for stmt in child.children:
                if stmt.type == "return_statement":
                    stmt_text = content[stmt.start_byte:stmt.end_byte].decode().strip()
                    # Remove "return " prefix and ";" suffix
                    ret_val = stmt_text.replace("return", "").strip().rstrip(";").strip()
                    return ret_val
    return None


def trace_port_member_to_source(
    port_member: str,
    obj_path: str,
    registry: dict[str, ClassInfo],
    parser: Parser,
    subtree: ComponentNode,
    depth: int = 0,
) -> str:
    """
    Trace a port member (Its*Port*) back to its source through InitRelations.

    When a getter returns a port member, trace where that member was assigned.
    subtree is the ComponentNode for the object at obj_path.
    """
    if depth > 5:
        return obj_path

    class_name = subtree.class_name
    class_info = registry.get(class_name)
    if not class_info or not class_info.impl_path:
        return obj_path

    # Look for assignment to this port member in InitRelations
    source = _find_port_member_source(parser, class_info.impl_path, port_member)
    if source:
        # source is something like "RadaltLruMgr.GetIts...Port...()"
        # Continue tracing from this component's subtree
        return trace_getter_to_receiver(source, obj_path, registry, parser, subtree, depth + 1)

    return obj_path


def _find_port_member_source(parser: Parser, impl_path: Path, port_member: str) -> str | None:
    """
    Find what a port member is assigned from in InitRelations.

    Looks for pattern: Its*Port* = something.GetIts*Port*();
    """
    import re

    content = impl_path.read_bytes()
    tree = parser.parse(content)
    root = tree.root_node

    for node in root.children:
        if node.type == "function_definition":
            func_name = _get_function_name(content, node)
            if func_name and "InitRelations" in func_name:
                for child in node.children:
                    if child.type == "compound_statement":
                        for stmt in child.children:
                            if stmt.type == "expression_statement":
                                stmt_text = content[stmt.start_byte:stmt.end_byte].decode().strip()

                                # Look for: port_member = something.GetIts*Port*()
                                # Handle both exact match and partial match (Its prefix variations)
                                pattern = rf'{re.escape(port_member)}\s*=\s*([A-Za-z_][A-Za-z0-9_]*\.GetIts[A-Za-z0-9_]*Port[A-Za-z0-9_]*\(\))'
                                match = re.search(pattern, stmt_text)
                                if match:
                                    return match.group(1)

    return None


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
    print("Port Connections (grouped by interface):")
    if connections:
        # Group connections by interface
        from collections import defaultdict
        by_interface: dict[str, list[PortConnection]] = defaultdict(list)
        for conn in connections:
            by_interface[conn.interface].append(conn)

        # Print grouped by interface
        for interface in sorted(by_interface.keys()):
            print(f"\n  [{interface}]")
            for conn in by_interface[interface]:
                if conn.unresolved:
                    print(f"    {conn.from_path} --> ??? (unresolved: {conn.to_path})")
                else:
                    print(f"    {conn.from_path} --> {conn.to_path}")
    else:
        print("  (none)")
    print()
    print("Legend:")
    print("  A --> B  means A sends data to B via the interface in brackets")

    return 0


if __name__ == "__main__":
    sys.exit(main())
