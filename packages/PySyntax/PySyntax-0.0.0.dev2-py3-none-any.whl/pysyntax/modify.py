import re as _re

import pysyntax as _pysyntax


def rename_imports(module_content: str, mapping: dict[str, str]) -> str:
    """
    Rename imports in a module.

    Parameters
    ----------
    module_content : str
        The content of the Python module as a string.
    mapping : dict[str, str]
        A dictionary mapping the old import names to the new import names.

    Returns
    -------
    new_module_content : str
        The updated module content as a string with the old names replaced by the new names.
    """
    updated_module_content = module_content
    for old_name, new_name in mapping.items():
        # Regular expression patterns to match the old name in import statements
        patterns = [
            rf"^\s*from\s+{_re.escape(old_name)}(?:.[a-zA-Z0-9_]+)*\s+import",
            rf"^\s*import\s+{_re.escape(old_name)}(?:.[a-zA-Z0-9_]+)*",
        ]
        for pattern in patterns:
            # Compile the pattern into a regular expression object
            regex = _re.compile(pattern, flags=_re.MULTILINE)
            # Replace the old name with the new name wherever it matches
            updated_module_content = regex.sub(
                lambda match: match.group(0).replace(old_name, new_name, 1), updated_module_content
            )
    return updated_module_content


def update_docstring(file_content, new_docstring, quotes: str = '"""'):
    """
    Replaces the existing module docstring with new_docstring, or adds it if none exists.

    Parameters:
        file_content (str): The content of the Python file as a string.
        new_docstring (str): The new docstring to replace or add.

    Returns:
        str: The modified file content.
    """
    existing_docstring = _pysyntax.parse.docstring(file_content)
    if existing_docstring is not None:
        # Replace the existing docstring with the new one
        return file_content.replace(existing_docstring, new_docstring, 1)

    lines = file_content.splitlines()
    insert_pos = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('#') or stripped == '':
            insert_pos = i + 1
        else:
            break
    whitespace_before = "\n" if insert_pos != 0 and lines[insert_pos - 1].strip() else ""
    whitespace_after = "\n" if insert_pos != len(lines) and lines[insert_pos].strip() else "\n"
    lines.insert(insert_pos, f'{whitespace_before}{quotes}{new_docstring}{quotes}{whitespace_after}')
    return '\n'.join(lines)
