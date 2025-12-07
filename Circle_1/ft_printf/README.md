# 📝 ft_printf

[![42 Project](https://img.shields.io/badge/42-ft__printf-00babc?style=flat-square&logo=42)](https://github.com/yourusername/ft_printf)
![Grade](https://img.shields.io/badge/Grade-100%2F100-success?style=flat-square)
![Language](https://img.shields.io/badge/Language-C-blue?style=flat-square)

## 📋 Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Conversions](#supported-conversions)

## 🎯 Description

**ft_printf** is a recreation of the standard C library function printf(). This project teaches variadic functions and formatted output.

## 🚀 Installation

```bash
git clone https://github.com/KuraiZ0/ft_printf.git
cd ft_printf
make
```

## 💻 Usage

```c
#include "ft_printf.h"

int main(void)
{
    ft_printf("Hello, %s!\n", "world");
    ft_printf("Number: %d\n", 42);
    return (0);
}
```

### Compilation
```bash
gcc main.c libftprintf.a -o program
```

## 🔧 Supported Conversions

| Conversion | Description | Example |
|------------|-------------|---------|
| %c | Character | A |
| %s | String | Hello |
| %d | Decimal | 42 |
| %x | Hex lowercase | ff |
| %X | Hex uppercase | FF |
| %p | Pointer | 0x7ffd |

---
**Grade**: 100/100 | **Status**: Validated
