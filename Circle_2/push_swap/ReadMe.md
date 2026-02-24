# 🔄 push_swap

[![42 Project](https://img.shields.io/badge/42-push__swap-00babc?style=flat-square&logo=42)](https://github.com/KuraiZ0/cursus-42/tree/main/Circle_2/push_swap)
[![Grade](https://img.shields.io/badge/Grade-84%2F100-success?style=flat-square)]()
[![Language](https://img.shields.io/badge/Language-C-blue?style=flat-square)]()
[![Circle](https://img.shields.io/badge/Circle-2-orange?style=flat-square)]()

> Sort a stack of integers using two stacks and a limited set of operations, with the fewest moves possible.

## 📋 Table of Contents

- [Description](#-description)
- [How It Works](#-how-it-works)
- [Operations](#-operations)
- [Algorithm Strategy](#-algorithm-strategy)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Performance](#-performance)

## 🎯 Description

**push_swap** is a 42 school project that implements an efficient sorting algorithm using two stacks (`a` and `b`) and a limited set of stack operations. The goal is to sort a list of integers in ascending order using the **minimum number of moves**.

This project focuses on:
- Algorithm design and optimization
- Time and space complexity analysis
- Working with linked lists and stack data structures in C

## ⚙️ How It Works

The program receives a list of integers as arguments, then outputs the sequence of operations needed to sort stack `a` in ascending order. Stack `b` is used as a temporary buffer.

```
Stack A: [3, 2, 1, 5, 4]      Stack B: []
          ↓
   push_swap magic
          ↓
Stack A: [1, 2, 3, 4, 5]      Stack B: []
```

## 🔧 Operations

| Operation | Description |
|-----------|-------------|
| `sa` | Swap the first 2 elements of stack A |
| `sb` | Swap the first 2 elements of stack B |
| `ss` | `sa` and `sb` simultaneously |
| `pa` | Push the top of B onto stack A |
| `pb` | Push the top of A onto stack B |
| `ra` | Rotate stack A upward (first becomes last) |
| `rb` | Rotate stack B upward |
| `rr` | `ra` and `rb` simultaneously |
| `rra` | Reverse rotate stack A (last becomes first) |
| `rrb` | Reverse rotate stack B |
| `rrr` | `rra` and `rrb` simultaneously |

## 🧠 Algorithm Strategy

### Small sets (2-5 elements)
- **2 numbers**: one `sa` if needed
- **3 numbers**: hardcoded optimal sequence (≤3 moves)
- **5 numbers**: push 2 to B, sort 3, then re-insert optimally

### Large sets (100+ elements)
The algorithm uses a **chunk-based Turk sort** approach:
1. Divide the values into chunks based on sorted rank
2. Push each chunk to B in the right order
3. Rotate to find optimal push position
4. Re-insert from B back to A in sorted order

This achieves near-optimal move counts for 100 and 500 element sorts.

## 📂 Project Structure

```
push_swap/
├── Makefile
├── index.c          # Entry point, argument parsing dispatch
├── parsing.c        # Input validation and stack initialization
├── parsing_utils.c  # Helper functions for parsing
├── push.c           # pa / pb operations
├── push_swap.c      # Core sorting logic
├── error_handle.c   # Error management and cleanup
├── libft/           # Custom C library
└── ft_printf/       # Custom printf implementation
```

## 🚀 Installation & Usage

```bash
# Clone the repository
git clone https://github.com/KuraiZ0/cursus-42.git
cd cursus-42/Circle_2/push_swap

# Compile
make

# Run
./push_swap 3 2 1 5 4

# Count operations
./push_swap 3 2 1 5 4 | wc -l

# Validate sort (using a checker)
./push_swap 3 2 1 5 4 | ./checker 3 2 1 5 4
```

### Error handling

```bash
./push_swap        # Error: no arguments
./push_swap a b c  # Error: non-integer input
./push_swap 1 1 2  # Error: duplicates
```

### Compile flags

```bash
make        # Standard build
make clean  # Remove object files
make fclean # Remove all generated files
make re     # Recompile from scratch
```

## 📊 Performance

| Stack Size | Target | Result | Grade |
|------------|--------|--------|-------|
| 3 numbers  | ≤ 3 ops | ≤ 3 ops | ✅ |
| 5 numbers  | ≤ 12 ops | ≤ 12 ops | ✅ |
| 100 numbers | < 700 ops | ~600 ops | ⭐ |
| 500 numbers | < 5500 ops | ~4800 ops | ⭐ |

**Grade**: 84/100 | **Status**: Validated 🔵

> *Note: The grade reflects that bonus (checker) was not submitted.*

## 📚 Resources

- [Push_swap visualizer](https://github.com/o-reo/push_swap_visualizer) — visualize your sort in real time
- [LeoFu9487's tester](https://github.com/LeoFu9487/push_swap_tester) — automated performance testing
- [Turk sort algorithm explained](https://medium.com/@ayogun/push-swap-c1f5d2d41e97)
