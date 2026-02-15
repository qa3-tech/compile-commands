# YAML Configuration Examples

## Example 1: Basic GCC C Project

```yaml
project:
  name: simple-server
  language: c
  standard: c11

compiler:
  compiler_path: gcc
  flags: ["-Wall", "-Wextra", "-Wpedantic", "-g"]
  defines: ["_GNU_SOURCE", "DEBUG"]

source_groups:
  - name: main
    source_dirs: ["src/"]
    include_dirs: ["include/"]
    flags: []
    defines: []

dependencies:
  external_includes: []

build:
  output: "server"

  linker:
    flags: ["-lpthread", "-lm"]

  modes:
    debug:
      output_dir: "build/debug"
      output_name: "server_debug" # Debug binary with suffix
      source_groups: ["main"] # Mandatory: specify which groups to build
      extra_flags: []
      linker_flags: []

    release:
      output_dir: "build/release"
      source_groups: ["main"] # Must explicitly list groups
      extra_flags: ["-O3", "-DNDEBUG", "-flto"]
      linker_flags: ["-s"]
```

## Example 2: Clang with Sanitizers (C++)

```yaml
project:
  name: fast-parser
  language: c++
  standard: c++20

compiler:
  compiler_path: clang++
  flags: ["-Wall", "-Wextra", "-Werror", "-fcolor-diagnostics"]
  defines: ["_FORTIFY_SOURCE=2"]

source_groups:
  - name: core
    source_dirs: ["src/core/"]
    include_dirs: ["include/", "src/core/internal/"]
    flags: ["-ffast-math"]
    defines: []

  - name: tests
    source_dirs: ["tests/"]
    include_dirs: ["include/", "tests/lib/"]
    flags: ["-fno-omit-frame-pointer"]
    defines: ["TESTING", "VERBOSE_ERRORS"]

dependencies:
  external_includes: ["/usr/include/catch2"]

build:
  output: "parser"

  linker:
    flags: ["-lstdc++", "-lm"]

  modes:
    debug:
      output_dir: "build/debug"
      output_name: "parser_test" # Different name for debug with tests
      source_groups: ["core", "tests"] # Include tests in debug build
      extra_flags: ["-O0", "-g3", "-fsanitize=address", "-fsanitize=undefined"]
      linker_flags: ["-fsanitize=address", "-fsanitize=undefined"]

    release:
      output_dir: "build/release"
      source_groups: ["core"] # Exclude tests from release build
      extra_flags: ["-O3", "-DNDEBUG", "-march=native", "-flto"]
      linker_flags: ["-s", "-flto"]
```

## Example 3: ARM Cross-Compilation

```yaml
project:
  name: embedded-app
  language: c
  standard: c99

compiler:
  compiler_path: arm-linux-gnueabihf-gcc
  flags: ["-Wall", "-Wextra", "-march=armv7-a", "-mfpu=neon", "-mfloat-abi=hard"]
  defines: ["ARM_TARGET", "EMBEDDED"]

source_groups:
  - name: main
    source_dirs: ["src/"]
    include_dirs: ["include/", "platform/arm/"]
    flags: []
    defines: []

  - name: drivers
    source_dirs: ["drivers/"]
    include_dirs: ["include/", "drivers/include/"]
    flags: ["-fno-strict-aliasing"]
    defines: ["DRIVER_VERSION=2"]

dependencies:
  external_includes: ["/opt/arm-sdk/include"]

build:
  output: "embedded-app.elf"

  linker:
    flags: ["-lpthread", "-lrt"]

  modes:
    debug:
      output_dir: "build/arm-debug"
      output_name: "embedded-app-debug.elf"
      source_groups: ["main", "drivers"] # Both groups for debugging
      extra_flags: ["-O1", "-g3"]
      linker_flags: []

    release:
      output_dir: "build/arm-release"
      source_groups: ["main", "drivers"] # Same groups for production
      extra_flags: ["-O2", "-DNDEBUG", "-ffunction-sections", "-fdata-sections"]
      linker_flags: ["-Wl,--gc-sections", "-s"]
```

## Example 4: Windows MinGW Cross-Compilation

```yaml
project:
  name: win-tool
  language: c
  standard: c11

compiler:
  compiler_path: x86_64-w64-mingw32-gcc
  flags: ["-Wall", "-Wextra", "-municode"]
  defines: ["UNICODE", "_UNICODE", "WINVER=0x0601"]

source_groups:
  - name: main
    source_dirs: ["src/"]
    include_dirs: ["include/"]
    flags: []
    defines: []

  - name: win32
    source_dirs: ["src/platform/windows/"]
    include_dirs: ["include/", "src/platform/windows/"]
    flags: ["-mwindows"]
    defines: ["WIN32_LEAN_AND_MEAN"]

dependencies:
  external_includes: []

build:
  output: "tool.exe"

  linker:
    flags: ["-lws2_32", "-lkernel32", "-luser32"]

  modes:
    debug:
      output_dir: "build/win-debug"
      output_name: "tool_debug.exe"
      source_groups: ["main", "win32"] # Include all platform code
      extra_flags: ["-O0", "-g", "-gcodeview"]
      linker_flags: ["-Wl,--subsystem,console"]

    release:
      output_dir: "build/win-release"
      source_groups: ["main", "win32"] # Same groups for release
      extra_flags: ["-O3", "-DNDEBUG"]
      linker_flags: ["-s", "-Wl,--subsystem,windows"]
```

## Example 5: Multi-Library Project with External Dependencies

```yaml
project:
  name: http-server
  language: c
  standard: c17

compiler:
  compiler_path: gcc
  flags: ["-Wall", "-Wextra", "-Wshadow", "-Wformat=2", "-g"]
  defines: ["_POSIX_C_SOURCE=200809L", "_DEFAULT_SOURCE"]

source_groups:
  - name: server
    source_dirs: ["src/server/"]
    include_dirs: ["include/", "src/server/internal/"]
    flags: []
    defines: []

  - name: protocol
    source_dirs: ["src/protocol/"]
    include_dirs: ["include/", "src/protocol/"]
    flags: ["-Wno-unused-parameter"]
    defines: ["HTTP_VERSION=11"]

  - name: crypto
    source_dirs: ["src/crypto/"]
    include_dirs: ["include/"]
    flags: ["-fstack-protector-strong"]
    defines: ["USE_OPENSSL"]

  - name: tests
    source_dirs: ["tests/"]
    include_dirs: ["include/", "tests/"]
    flags: []
    defines: ["UNIT_TESTING"]

dependencies:
  external_includes:
    ["/usr/include/openssl", "/usr/local/include", "/opt/libevent/include"]

build:
  output: "httpd"

  linker:
    flags: ["-lpthread", "-lssl", "-lcrypto", "-levent", "-ldl"]

  modes:
    debug:
      output_dir: "build/debug"
      output_name: "httpd_debug"
      source_groups: ["server", "protocol", "crypto", "tests"] # Include tests
      extra_flags: ["-O0", "-DDEBUG_LOGGING"]
      linker_flags: []

    release:
      output_dir: "build/release"
      source_groups: ["server", "protocol", "crypto"] # No tests in production
      extra_flags: ["-O3", "-DNDEBUG", "-flto", "-fstack-protector-strong"]
      linker_flags: ["-s", "-flto", "-Wl,-z,relro,-z,now"]
```

## Example 6: RISC-V Bare Metal

```yaml
project:
  name: riscv-firmware
  language: c
  standard: c11

compiler:
  compiler_path: riscv64-unknown-elf-gcc
  flags:
    [
      "-Wall",
      "-Wextra",
      "-march=rv64imac",
      "-mabi=lp64",
      "-mcmodel=medany",
      "-fno-common",
      "-ffunction-sections",
      "-fdata-sections",
    ]
  defines: ["BARE_METAL", "RISCV64"]

source_groups:
  - name: boot
    source_dirs: ["src/boot/"]
    include_dirs: ["include/"]
    flags: ["-nostdlib", "-nostartfiles"]
    defines: ["BOOT_STAGE"]

  - name: kernel
    source_dirs: ["src/kernel/"]
    include_dirs: ["include/", "src/kernel/arch/riscv/"]
    flags: ["-ffreestanding"]
    defines: ["KERNEL_MODE"]

  - name: drivers
    source_dirs: ["src/drivers/"]
    include_dirs: ["include/", "src/drivers/"]
    flags: ["-ffreestanding"]
    defines: ["DRIVER_MODE"]

dependencies:
  external_includes: []

build:
  output: "firmware.elf"

  linker:
    flags: ["-nostdlib", "-nostartfiles", "-T", "linker.ld"]

  modes:
    debug:
      output_dir: "build/riscv-debug"
      source_groups: ["boot", "kernel", "drivers"] # All components
      extra_flags: ["-O1", "-g3"]
      linker_flags: []

    release:
      output_dir: "build/riscv-release"
      source_groups: ["boot", "kernel"] # Minimal firmware without drivers
      extra_flags: ["-Os", "-DNDEBUG"]
      linker_flags: ["-Wl,--gc-sections"]
```

## Key Points

### Mode-Specific Source Groups

- **MANDATORY**: Each mode MUST specify `source_groups` array
- Build will fail if `source_groups` is missing or empty
- Allows different combinations for debug vs release:
  - Include test code only in debug builds
  - Exclude optional modules from release
  - Build minimal configurations for embedded systems

### Mode-Specific Output Names

- Optional `output_name` field in each mode
- Overrides the global `output` field
- Useful for distinguishing debug/release binaries:
  ```yaml
  modes:
    debug:
      output_name: "myapp_debug"
      source_groups: ["main", "tests"]
    release:
      output_name: "myapp"
      source_groups: ["main"]
  ```

### Clean Operation

- `./compile_commands_build.py --clean` - Clean all build modes
- `./compile_commands_build.py --clean --mode debug` - Clean specific mode only
- Removes .o files and executables from build directories

### Explicit Arrays

- Always use `[]` for empty arrays (not implicit/null)
- Write `flags: []` not `flags:` or omit it
- Makes config clear and prevents parsing issues

### Compiler Selection

- `gcc` - Standard GNU Compiler
- `g++` - GNU C++ Compiler
- `clang` / `clang++` - LLVM compiler with better diagnostics
- `arm-linux-gnueabihf-gcc` - ARM hard-float cross-compiler
- `x86_64-w64-mingw32-gcc` - Windows cross-compiler (MinGW)
- `riscv64-unknown-elf-gcc` - RISC-V bare metal

### Common Flag Patterns

**Debug builds:**

- `-O0` - No optimization
- `-g3` - Full debug info
- `-fsanitize=address` - Memory error detection
- `-fsanitize=undefined` - Undefined behavior detection

**Release builds:**

- `-O3` - Maximum optimization
- `-DNDEBUG` - Disable assertions
- `-flto` - Link-time optimization
- `-march=native` - CPU-specific optimizations
- `-s` - Strip symbols (smaller binary)

**Embedded/Bare metal:**

- `-Os` - Optimize for size
- `-ffunction-sections` - Separate functions
- `-fdata-sections` - Separate data
- `-Wl,--gc-sections` - Remove unused sections
- `-nostdlib` - Don't link standard library
- `-ffreestanding` - Freestanding environment

**Security hardening:**

- `-fstack-protector-strong` - Stack canaries
- `-D_FORTIFY_SOURCE=2` - Buffer overflow detection
- `-Wl,-z,relro` - Read-only relocations
- `-Wl,-z,now` - Immediate binding

### Language Standards

- C: `c89`, `c99`, `c11`, `c17`, `c23`
- C++: `c++11`, `c++14`, `c++17`, `c++20`, `c++23`

### Common Libraries

- `-lm` - Math library
- `-lpthread` - POSIX threads
- `-lrt` - Real-time extensions
- `-ldl` - Dynamic linking
- `-lssl`, `-lcrypto` - OpenSSL
- `-lstdc++` - C++ standard library

## Usage Tips

1. **Source groups are mandatory** - Each mode MUST specify which source groups to build
2. **Start simple** - Begin with Example 1 and add complexity as needed
3. **Test both modes** - Always test debug and release builds
4. **Use verbose mode** - `--verbose` flag shows all commands and environment
5. **Clean regularly** - Use `--clean` to ensure fresh builds
6. **Explicit arrays** - Never omit `[]` for empty arrays
7. **Cross-compilation** - Set compiler in YAML or use `CC` environment variable

## Common Build Patterns

### Testing Strategy

```yaml
modes:
  debug:
    source_groups: ["core", "tests", "benchmarks"]
  release:
    source_groups: ["core"]
```

### Platform-Specific Builds

```yaml
source_groups:
  - name: core
  - name: platform_linux
  - name: platform_windows

modes:
  linux_release:
    source_groups: ["core", "platform_linux"]
  windows_release:
    source_groups: ["core", "platform_windows"]
```

### Minimal vs Full Builds

```yaml
modes:
  minimal:
    source_groups: ["core"]
    output_name: "app_lite"
  full:
    source_groups: ["core", "extras", "plugins"]
    output_name: "app_full"
```
