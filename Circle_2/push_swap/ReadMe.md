# 🔄 push_swap

[![42 Project](https://img.shields.io/badge/42-push__swap-00babc?style=flat-square&logo=42)](https://github.com/yourusername/push_swap)
![Grade](https://img.shields.io/badge/Grade-84%2F100-success?style=flat-square)
![Language](https://img.shields.io/badge/Language-C-blue?style=flat-square)

## 📋 Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Operations](#operations)
- [Algorithm Strategy](#algorithm-strategy)
- [Performance](#performance)

## 🎯 Description

**push_swap** is a 42 school project that implements an efficient sorting algorithm using two stacks and a limited set of operations. The goal is to sort numbers in ascending order using the minimum number of moves.

## 🚀 Installation

```bash
git clone https://github.com/KuraiZ0/push_swap.git
cd push_swap
make
```

## 💻 Usage

```bash
./push_swap 3 2 1 5 4
```

## 🔧 Operations

| Operation | Description |
|-----------|-------------|
| sa | Swap first 2 elements of stack A |
| pb | Push first element of A to B |
| ra | Rotate stack A |
| rra | Reverse rotate A |

## 📊 Performance

| Stack Size | Operations | Status |
|------------|------------|--------|
| 3 numbers  | ≤ 3        | ✅ |
| 5 numbers  | ≤ 12       | ✅ |
| 100 numbers| < 700      | ⭐ |
| 500 numbers| < 5500     | ⭐ |

---
**Grade**: 84/100 | **Status**: Validated
