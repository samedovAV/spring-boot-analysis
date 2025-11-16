#!/usr/bin/env python3
"""
Script to fix indentation of @Prove annotations in Java files.
"""

import re
import os

def fix_prove_indentation(filepath):
    """Fix indentation of @Prove annotations."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        result = []

        for i, line in enumerate(lines):
            # Check if line contains @Prove annotation with incorrect indentation
            if '@Prove(complexity' in line:
                # Find the next non-empty line to match its indentation
                next_indent = 0
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j]
                    if next_line.strip() and not next_line.strip().startswith('@'):
                        next_indent = len(next_line) - len(next_line.lstrip())
                        break

                # Recreate the @Prove line with correct indentation
                stripped_prove = line.strip()
                fixed_line = '\t' * (next_indent // 4) + ' ' * (next_indent % 4) + stripped_prove
                result.append(fixed_line)
            else:
                result.append(line)

        # Write back
        new_content = '\n'.join(result)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    config_dir = '/home/samedov/coding/spring-boot-analysis/core/spring-boot/src/main/java/org/springframework/boot/context/config'

    java_files = []
    for filename in os.listdir(config_dir):
        if filename.endswith('.java') and filename != 'package-info.java':
            filepath = os.path.join(config_dir, filename)
            java_files.append(filepath)

    java_files.sort()

    print(f"Fixing indentation in {len(java_files)} files...")

    for filepath in java_files:
        basename = os.path.basename(filepath)
        if fix_prove_indentation(filepath):
            print(f"✓ {basename}")
        else:
            print(f"✗ {basename}")

if __name__ == '__main__':
    main()

