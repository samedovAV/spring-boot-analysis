#!/usr/bin/env python3
"""
Script to add @Prove annotations to all methods in Java files.
This script identifies method declarations and adds @Prove annotations.
"""

import re
import os
import sys

def annotate_file(filepath):
    """Add @Prove annotations to all methods in a Java file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        result = []
        i = 0
        in_multiline_comment = False

        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Track comment state
            if '/*' in line and '*/' not in line:
                in_multiline_comment = True
            elif '*/' in line:
                in_multiline_comment = False

            # Skip if in comment or empty
            if in_multiline_comment or stripped.startswith('//') or stripped.startswith('*') or stripped == '':
                result.append(line)
                i += 1
                continue

            # Skip lines that already have @Prove above them
            has_prove = False
            if i > 0:
                for j in range(max(0, i-5), i):
                    if '@Prove' in lines[j]:
                        has_prove = True
                        break

            if has_prove:
                result.append(line)
                i += 1
                continue

            # Check if this line starts a method/constructor declaration
            # Look for lines with opening parenthesis that look like method declarations
            is_method = False

            # Check for method patterns
            if '(' in line and '{' in line:
                # Single-line method
                method_patterns = [
                    r'^\s*(public|private|protected|static|final|abstract|synchronized|native|strictfp|\s)+([\w<>\[\]@,\s\?\.\*]+\s+)?\w+\s*\([^)]*\)\s*(throws\s+[\w,\s\.]+)?\s*\{',
                ]
                for pattern in method_patterns:
                    if re.match(pattern, line):
                        if not stripped.startswith('@') and 'class ' not in line and 'interface ' not in line and 'enum ' not in line:
                            if not stripped.startswith('if') and not stripped.startswith('while') and not stripped.startswith('for') and not stripped.startswith('switch') and not stripped.startswith('catch'):
                                is_method = True
                                break
            elif '(' in line and not '{' in line:
                # Could be multi-line method - check if it's a declaration
                # Look ahead to find the closing paren or opening brace
                if stripped and not stripped.startswith('@') and 'class ' not in line and 'interface ' not in line and 'enum ' not in line:
                    if not stripped.startswith('if') and not stripped.startswith('while') and not stripped.startswith('for') and not stripped.startswith('switch') and not stripped.startswith('catch') and not stripped.startswith('return'):
                        # Check if this looks like a method signature start
                        if re.match(r'^\s*(public|private|protected|static|final|abstract|synchronized|default)', line):
                            is_method = True
                        elif re.match(r'^\s*\w+\s*\([^)]*$', line):  # Constructor-like
                            is_method = True

            if is_method:
                # Find the indentation of the method
                indent = len(line) - len(line.lstrip())

                # Check if previous line is javadoc end, annotation, or empty
                add_annotation = False
                if i > 0:
                    prev_stripped = lines[i-1].strip()
                    if prev_stripped.endswith('*/'):
                        add_annotation = True
                    elif prev_stripped == '':
                        add_annotation = True
                    elif prev_stripped.startswith('@') and '@Prove' not in prev_stripped:
                        add_annotation = True
                else:
                    add_annotation = True

                if add_annotation:
                    # Add @Prove annotation with proper indentation
                    annotation = '\t' * (indent // 4) + '@Prove(complexity = Complexity.O_1, n = "", count = {})'
                    result.append(annotation)

            result.append(line)
            i += 1

        # Write back
        new_content = '\n'.join(result)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True

    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def main():
    config_dir = '/home/samedov/coding/spring-boot-analysis/core/spring-boot/src/main/java/org/springframework/boot/context/config'

    if not os.path.isdir(config_dir):
        print(f"Directory not found: {config_dir}")
        return 1

    java_files = []
    for filename in os.listdir(config_dir):
        if filename.endswith('.java') and filename != 'package-info.java':
            filepath = os.path.join(config_dir, filename)
            java_files.append(filepath)

    java_files.sort()

    print(f"Processing {len(java_files)} Java files...")

    success = 0
    for filepath in java_files:
        basename = os.path.basename(filepath)
        if annotate_file(filepath):
            print(f"✓ {basename}")
            success += 1
        else:
            print(f"✗ {basename}")

    print(f"\nCompleted: {success}/{len(java_files)} files")
    return 0

if __name__ == '__main__':
    sys.exit(main())

