# Simple Compile Commands Generator

A lightweight solution for generating `compile_commands.json` for C projects without the overhead of complex build systems.

## Why This Exists

**The Problem**: Modern editors and LSP servers need a `compile_commands.json` file to provide proper C language support (syntax highlighting, error checking, code completion, go-to-definition, etc.). However, generating this file typically requires:

- Setting up CMake (overkill for simple projects)
- Learning complex build system syntax
- Installing heavy tooling like `bear` or `compiledb`
- Dealing with build system quirks and edge cases

**The Solution**: For simple C projects, you shouldn't need a complex build system just to get basic editor support. This tool lets you describe your project structure in a simple YAML file and generates the JSON that LSP servers require.

## When to Use This

✅ **Perfect for:**
- Small to medium C projects
- Personal/hobby projects
- Learning projects and tutorials
- Prototypes and experiments
- Projects with straightforward compilation needs

❌ **Not ideal for:**
- Large, complex codebases with intricate build requirements
- Projects that already use CMake/Meson/Autotools effectively
- Cross-compilation or embedded development
- Projects with complex conditional compilation

## Quick Start

1. **Install dependency:**
   ```bash
   pip install pyyaml
   ```

2. **Create `project.yaml`:**
   ```yaml
   project:
     name: my-project
     language: c
     standard: c99

   compiler:
     flags: ["-Wall", "-Wextra", "-g"]
     defines: ["_GNU_SOURCE"]

   source_groups:
     - name: main
       source_dirs: ["src/"]
       include_dirs: ["include/"]
   ```

3. **Generate compile commands:**
   ```bash
   python generate_compile_commands.py
   ```


## Configuration

### Basic Structure

The `project.yaml` file has four main sections:

- **`project`**: Basic project metadata
- **`compiler`**: Global compiler settings
- **`source_groups`**: Map source directories to their include paths
- **`dependencies`**: External include directories

### Source Groups

The key feature is **source groups** - they let you specify different include paths for different parts of your project:

```yaml
source_groups:
  # Main code only needs project headers
  - name: main
    source_dirs: ["src/"]
    include_dirs: ["include/"]
    
  # Tests need both project headers and test utilities
  - name: tests
    source_dirs: ["tests/"]
    include_dirs: ["include/", "tests/"]
    flags: ["-DTESTING"]
```

### External Dependencies

Add system or library include paths as needed:

```yaml
dependencies:
  external_includes:
    - "/usr/include"
    - "/usr/local/include"
    - "/usr/include/openssl"  # For specific libraries
```

## Examples

See `example_project.yaml` for a complete example of an HTTP server project with multiple source groups.

## How It Works

1. **Scans** your source directories for `.c` files
2. **Maps** each source file to its appropriate include paths based on source groups
3. **Generates** a `compile_commands.json` with the exact compilation commands LSP servers expect
4. **No actual compilation** - just generates the metadata for language servers

## Philosophy

Sometimes the simplest solution is the best solution. Not every C project needs a full build system - sometimes you just want your editor to understand your code structure without jumping through hoops.

This tool embraces the Unix philosophy: do one thing well. It generates compile commands, nothing more, nothing less.

## Limitations

- **No linking**: Only generates compilation commands, not linking
- **No dependency tracking**: Won't rebuild when headers change  
- **No conditional compilation**: All files get the same treatment within a source group
- **Basic file discovery**: Simple recursive search, no complex filtering

For projects that outgrow these limitations, graduate to a proper build system like CMake or Meson.
