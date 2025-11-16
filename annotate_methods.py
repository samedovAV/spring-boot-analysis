#!/usr/bin/env python3
"""
Script to add @Prove annotations to all methods in Java files.
"""

import re
import sys
import os

def has_prove_import(content):
    """Check if file already has Prove imports."""
    return 'import com.samedov.annotation.Prove;' in content

def add_imports(content):
    """Add Prove annotation imports after package declaration and existing imports."""
    if has_prove_import(content):
        return content

    # Find the last import statement
    import_pattern = r'^import\s+[\w.]+;'
    lines = content.split('\n')
    last_import_idx = -1

    for i, line in enumerate(lines):
        if re.match(import_pattern, line):
            last_import_idx = i

    if last_import_idx >= 0:
        # Insert after the last import
        lines.insert(last_import_idx + 1, '')
        lines.insert(last_import_idx + 2, 'import com.samedov.annotation.Complexity;')
        lines.insert(last_import_idx + 3, 'import com.samedov.annotation.Prove;')
        return '\n'.join(lines)

    return content

def add_prove_annotations(content):
    """Add @Prove annotations to methods that don't have them."""
    lines = content.split('\n')
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a method/constructor declaration line
        # Look for: visibility modifiers + return type/void/constructor + method name + (
        method_pattern = r'^\s*(public|private|protected|static|final|abstract|synchronized|native|strictfp|\s)+([\w<>\[\]@,\s\?\.]+\s+)?(\w+)\s*\([^)]*\)\s*(\{|throws)?'

        # Skip lines that already have @Prove, @Override, or are inside comments
        is_override = i > 0 and '@Override' in lines[i-1]
        has_prove_above = i > 0 and '@Prove' in lines[i-1]

        # Check if this line looks like a method declaration
        if re.match(method_pattern, line) and not is_override and not has_prove_above:
            # Check if previous line is part of javadoc or annotation
            if i > 0:
                prev_line = lines[i-1].strip()
                # If previous line ends with */, it's end of javadoc
                if prev_line.endswith('*/'):
                    # Add annotation before method
                    indent = len(line) - len(line.lstrip())
                    result.append(' ' * indent + '@Prove(complexity = Complexity.O_1, n = "", count = {})')
                elif prev_line.startswith('@'):
                    # Already has an annotation, skip this one
                    pass
                elif prev_line == '':
                    # Empty line before method
                    indent = len(line) - len(line.lstrip())
                    result.append(' ' * indent + '@Prove(complexity = Complexity.O_1, n = "", count = {})')
            else:
                # First line, add annotation
                indent = len(line) - len(line.lstrip())
                result.append(' ' * indent + '@Prove(complexity = Complexity.O_1, n = "", count = {})')

        result.append(line)
        i += 1

    return '\n'.join(result)

def process_file(filepath):
    """Process a single Java file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add imports first
        content = add_imports(content)

        # Add annotations
        # content = add_prove_annotations(content)

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Processed: {filepath}")
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    # Directory containing the config files
    config_dir = '/home/samedov/coding/spring-boot-analysis/core/spring-boot/src/main/java/org/springframework/boot/context/config'

    # Get all Java files except package-info
    java_files = []
    for filename in os.listdir(config_dir):
        if filename.endswith('.java') and filename != 'package-info.java':
            filepath = os.path.join(config_dir, filename)
            java_files.append(filepath)

    java_files.sort()

    print(f"Found {len(java_files)} files to process")

    success_count = 0
    for filepath in java_files:
        if process_file(filepath):
            success_count += 1

    print(f"\nProcessed {success_count}/{len(java_files)} files successfully")

if __name__ == '__main__':
    main()

