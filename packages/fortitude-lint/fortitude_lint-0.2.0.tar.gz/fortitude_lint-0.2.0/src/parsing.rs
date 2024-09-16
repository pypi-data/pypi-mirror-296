use tree_sitter::Node;
/// Utilities to simplify parsing tree-sitter structures.

/// Get the first child with a given name. Returns None if not found.
pub fn child_with_name<'a>(node: &'a Node, name: &'a str) -> Option<Node<'a>> {
    let mut cursor = node.walk();
    let result = node.named_children(&mut cursor).find(|x| x.kind() == name);
    result
}

// Convert a node to text, collapsing any raised errors to None.
pub fn to_text<'a>(node: &'a Node<'a>, src: &'a str) -> Option<&'a str> {
    let result = node.utf8_text(src.as_bytes()).ok()?;
    Some(result)
}

/// Strip line breaks from a string of Fortran code.
pub fn strip_line_breaks(src: &str) -> String {
    src.replace("&", "").replace("\n", " ")
}

/// Given a variable declaration or function statement, return its type if it's an intrinsic type,
/// or None otherwise.
pub fn intrinsic_type(node: &Node) -> Option<String> {
    if let Some(child) = child_with_name(node, "intrinsic_type") {
        let grandchild = child.child(0)?;
        return Some(grandchild.kind().to_string());
    }
    None
}

/// Returns true if the type passed to it is number-like.
/// Deliberately does not include 'double precision' or 'double complex'.
pub fn dtype_is_number(dtype: &str) -> bool {
    matches!(
        dtype.to_lowercase().as_str(),
        "integer" | "real" | "logical" | "complex"
    )
}
