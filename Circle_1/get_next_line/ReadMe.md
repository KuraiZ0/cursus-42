# 📖 get_next_line

[![42 Project](https://img.shields.io/badge/42-get__next__line-00babc?style=flat-square&logo=42)](https://github.com/yourusername/get_next_line)
![Grade](https://img.shields.io/badge/Grade-105%2F100-success?style=flat-square)
![Language](https://img.shields.io/badge/Language-C-blue?style=flat-square)

## 📋 Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Buffer Size](#buffer-size)

## 🎯 Description

**get_next_line** is a function that reads a line from a file descriptor. This project introduces static variables in C.

## 🚀 Installation

```bash
git clone https://github.com/KuraiZ0/cursus-42/tree/main/Circle_1/get_next_line.git
cd get_next_line
```

## 💻 Usage

```c
#include "get_next_line.h"
#include <fcntl.h>

int main(void)
{
    int fd = open("test.txt", O_RDONLY);
    char *line;
    
    while ((line = get_next_line(fd)) != NULL)
    {
        printf("%s", line);
        free(line);
    }
    close(fd);
    return (0);
}
```

### Compilation
```bash
gcc -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c main.c
```

## ⚙️ Buffer Size

```bash
# Small buffer
gcc -D BUFFER_SIZE=1 ...

# Large buffer
gcc -D BUFFER_SIZE=1024 ...
```

---
**Grade**: 105/100 | **Status**: Validated
