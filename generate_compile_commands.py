#!/usr/bin/env python3
"""
Simple compile_commands.json generator for C projects

Reads project.yaml and generates compile_commands.json for LSP servers.
Much simpler than dealing with complex build systems for basic projects.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def load_config(config_file: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_path = Path(config_file)
    
    if not config_path.exists():
        print(f"Error: Configuration file '{config_file}' not found")
        sys.exit(1)
    
    try:
        import yaml
    except ImportError:
        print("Error: Need 'pip install pyyaml' for YAML support")
        sys.exit(1)
    
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def find_source_files(source_dirs: List[str], extensions: List[str] = ['.c']) -> List[Path]:
    """Find all source files in the given directories."""
    source_files = []
    
    for source_dir in source_dirs:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"Warning: Source directory '{source_dir}' does not exist")
            continue
            
        for ext in extensions:
            # Find all files with the given extension
            source_files.extend(source_path.rglob(f'*{ext}'))
    
    return sorted(source_files)

def build_compile_command(file_path: Path, config: Dict[str, Any], group_config: Dict[str, Any]) -> Dict[str, str]:
    """Build a compile command entry for a single file."""
    
    # Start with the compiler
    compiler = config.get('compiler', {}).get('compiler_path', 'gcc')
    
    # Build the command parts
    cmd_parts = [compiler]
    
    # Add language standard
    if 'standard' in config.get('project', {}):
        cmd_parts.append(f"-std={config['project']['standard']}")
    
    # Add global compiler flags
    global_flags = config.get('compiler', {}).get('flags', [])
    cmd_parts.extend(global_flags)
    
    # Add group-specific flags
    group_flags = group_config.get('flags', [])
    cmd_parts.extend(group_flags)
    
    # Add include directories
    include_dirs = group_config.get('include_dirs', [])
    for include_dir in include_dirs:
        cmd_parts.append(f"-I{include_dir}")
    
    # Add external includes
    external_includes = config.get('dependencies', {}).get('external_includes', [])
    for ext_include in external_includes:
        cmd_parts.append(f"-I{ext_include}")
    
    # Add global defines
    global_defines = config.get('compiler', {}).get('defines', [])
    for define in global_defines:
        cmd_parts.append(f"-D{define}")
    
    # Add group-specific defines
    group_defines = group_config.get('defines', [])
    for define in group_defines:
        cmd_parts.append(f"-D{define}")
    
    # Add compilation flags (compile only, don't link)
    cmd_parts.extend(['-c', '-o'])
    
    # Generate output path
    build_dir = config.get('build', {}).get('output_dir', 'build/')
    output_file = Path(build_dir) / f"{file_path.stem}.o"
    cmd_parts.append(str(output_file))
    
    # Add the source file
    cmd_parts.append(str(file_path))
    
    return {
        "directory": str(Path.cwd()),
        "command": " ".join(cmd_parts),
        "file": str(file_path)
    }

def generate_compile_commands(config_file: str) -> List[Dict[str, str]]:
    """Generate compile commands from project configuration."""
    
    # Load configuration (supports both TOML and YAML)
    config = load_config(config_file)
    
    compile_commands = []
    
    # Process each source group
    for group in config.get('source_groups', []):
        group_name = group.get('name', 'unnamed')
        print(f"Processing source group: {group_name}")
        
        # Find source files for this group
        source_dirs = group.get('source_dirs', [])
        source_files = find_source_files(source_dirs)
        
        print(f"  Found {len(source_files)} source files")
        
        # Generate compile commands for each file
        for source_file in source_files:
            cmd = build_compile_command(source_file, config, group)
            compile_commands.append(cmd)
            print(f"    {source_file}")
    
    return compile_commands

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate compile_commands.json from project.yaml")
    parser.add_argument('--config', '-c', default='project.yaml',
                       help='Configuration file (default: project.yaml)')
    parser.add_argument('--output', '-o', default='compile_commands.json',
                       help='Output file (default: compile_commands.json)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.verbose:
        # Reduce output for non-verbose mode
        global print
        original_print = print
        print = lambda *a, **k: None if not args.verbose else original_print(*a, **k)
    
    print(f"Reading configuration from: {args.config}")
    
    # Generate compile commands
    compile_commands = generate_compile_commands(args.config)
    
    if not compile_commands:
        print("Warning: No source files found!")
        return
    
    # Write to output file
    with open(args.output, 'w') as f:
        json.dump(compile_commands, f, indent=2)
    
    original_print = globals().get('original_print', print)
    original_print(f"Generated {args.output} with {len(compile_commands)} entries")
    
    # Verify the file exists and is valid JSON
    try:
        with open(args.output, 'r') as f:
            json.load(f)
        original_print("✓ Generated file is valid JSON")
    except json.JSONDecodeError as e:
        original_print(f"✗ Error: Generated file is not valid JSON: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()