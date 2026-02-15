# Compile Commands & Simple Build

A lightweight solution for C/C++ projects that does two things well:

1. Generate `compile_commands.json` for LSP/editor support
2. Actually build your project

No makefiles. No CMake. No build system sprawl. Just one YAML config.

## The Problem

Modern editors need `compile_commands.json` for C/C++ language support. Building requires compilation and linking. The industry's answer? CMake, Ninja, Meson, Bazel, Make, and countless other complex tools.

For most projects, this is massive overkill.

## The Solution

Describe your project once in `project.yaml`. Then:

- Generate compile commands for your editor
- Build debug or release binaries
- Watch for changes and regenerate automatically
- Use terminal scripts for everything else

## Installation

```bash
git clone https://github.com/qa3-tech/compile-commands.git
cd compile-commands
pip install pyyaml
```

## Quick Start

**1. Create `project.yaml`:**

```yaml
project:
  name: my-project
  language: c
  standard: c11

compiler:
  compiler_path: gcc
  flags: ["-Wall", "-Wextra", "-g"]
  defines: ["_GNU_SOURCE"]

source_groups:
  - name: main
    source_dirs: ["src/"]
    include_dirs: ["include/"]
    flags: []
    defines: []

  - name: tests
    source_dirs: ["tests/"]
    include_dirs: ["include/", "tests/"]
    flags: []
    defines: ["UNIT_TESTING"]

dependencies:
  external_includes: []

build:
  output: "myapp"

  linker:
    flags: ["-lm"]

  modes:
    debug:
      output_dir: "build/debug"
      output_name: "myapp_debug"
      source_groups: ["main", "tests"]
      extra_flags: []
      linker_flags: []

    release:
      output_dir: "build/release"
      source_groups: ["main"]
      extra_flags: ["-O3", "-DNDEBUG"]
      linker_flags: ["-s"]
```

See `EXAMPLES.md` for more configurations (Clang, ARM, MinGW, RISC-V, etc).

**2. Generate compile commands for LSP:**

```bash
python compile_commands_generate.py
```

**3. Build your project:**

```bash
python compile_commands_build.py --mode debug
python compile_commands_build.py --mode release
```

**4. Watch for changes (optional):**

```bash
python compile_commands_watch.py
```

## Scripts

### Generate (`compile_commands_generate.py`)

Generates `compile_commands.json` for LSP servers (clangd, ccls, etc).

```bash
python compile_commands_generate.py
python compile_commands_generate.py --verbose
python compile_commands_generate.py --config my_project.yaml --output build/compile_commands.json
```

### Build (`compile_commands_build.py`)

Compiles and links your project.

```bash
# Basic usage
python compile_commands_build.py --mode debug
python compile_commands_build.py --mode release

# Parallel compilation (default: all CPU cores)
python compile_commands_build.py --mode debug -j4
python compile_commands_build.py --mode release --jobs 8

# Clean build artifacts
python compile_commands_build.py --clean
python compile_commands_build.py --clean --mode debug

# Verbose output
python compile_commands_build.py --mode debug --verbose
```

### Watch (`compile_commands_watch.py`)

Watches source/include directories and regenerates `compile_commands.json` on changes.

```bash
python compile_commands_watch.py
python compile_commands_watch.py --interval 5
python compile_commands_watch.py --config my_project.yaml
```

Press `Ctrl+C` to stop.

## Configuration Reference

### Project Section

```yaml
project:
  name: my-project
  language: c # or c++
  standard: c11 # c99, c11, c17, c++11, c++17, c++20, etc.
```

### Compiler Section

```yaml
compiler:
  compiler_path: gcc # optional, defaults to gcc/g++
  flags: ["-Wall", "-Wextra", "-g"]
  defines: ["_GNU_SOURCE", "DEBUG"]
```

### Source Groups

```yaml
source_groups:
  - name: main
    source_dirs: ["src/"]
    include_dirs: ["include/"]
    flags: []
    defines: []

  - name: tests
    source_dirs: ["tests/"]
    include_dirs: ["include/", "tests/"]
    flags: []
    defines: ["TESTING"]
```

### Build Section

```yaml
build:
  output: "myapp"

  linker:
    flags: ["-lm", "-lpthread"]

  modes:
    debug:
      output_dir: "build/debug"
      output_name: "myapp_debug" # optional
      source_groups: ["main", "tests"] # REQUIRED
      extra_flags: []
      linker_flags: []

    release:
      output_dir: "build/release"
      source_groups: ["main"] # REQUIRED
      extra_flags: ["-O3", "-DNDEBUG", "-flto"]
      linker_flags: ["-s", "-flto"]
```

**Important:** `source_groups` is required for each mode — explicitly control what gets compiled.

## Environment Variables

Both scripts respect standard C/C++ environment variables:

| YAML Config              | Environment Variable  | Purpose              |
| ------------------------ | --------------------- | -------------------- |
| `compiler.compiler_path` | `CC` / `CXX`          | Compiler executable  |
| `compiler.flags`         | `CFLAGS` / `CXXFLAGS` | Compilation flags    |
| `compiler.defines`       | `CPPFLAGS`            | Preprocessor defines |
| `build.linker.flags`     | `LDFLAGS`             | Linker flags         |

Environment variables override config:

```bash
CC=clang python compile_commands_generate.py
CC=clang python compile_commands_build.py --mode debug
```

## Cross-Compilation

```bash
# ARM
CC=arm-linux-gnueabihf-gcc python compile_commands_generate.py
CC=arm-linux-gnueabihf-gcc python compile_commands_build.py --mode release

# Windows (MinGW)
CC=x86_64-w64-mingw32-gcc python compile_commands_generate.py
CC=x86_64-w64-mingw32-gcc python compile_commands_build.py --mode release

# RISC-V
CC=riscv64-unknown-elf-gcc python compile_commands_generate.py
CC=riscv64-unknown-elf-gcc python compile_commands_build.py --mode release
```

Or set in YAML:

```yaml
compiler:
  compiler_path: "arm-linux-gnueabihf-gcc"
  flags: ["-march=armv7-a", "-mfpu=neon"]
```

## What This Does Well

✅ **Perfect for:**

- Small to medium C/C++ projects
- Learning projects and tutorials
- Prototypes and experiments
- Embedded development
- Projects where you want explicit control

✅ **Benefits:**

- One config file for everything
- Simple and transparent
- No hidden magic — just runs gcc/clang
- Standard environment variables
- Easy cross-compilation
- Parallel compilation
- Explicit control over build composition

## Limitations

❌ **Not ideal for:**

- Large codebases with complex dependencies
- Projects needing incremental builds
- Projects already using CMake/Meson effectively

For projects that outgrow these limitations, graduate to CMake or Meson.

## Philosophy

Not every C project needs a complex build system. Most just need to compile source files, link them together, and let the editor understand the code structure.

This tool embraces the Unix philosophy: do one thing well. Three simple scripts, one config file, standard environment variables, zero complexity.
