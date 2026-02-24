# 💻 Codexion

![42](https://img.shields.io/badge/42-cursus-blue?style=flat-square&logo=42)
![Circle](https://img.shields.io/badge/Circle-3-blueviolet?style=flat-square)
![Language](https://img.shields.io/badge/Language-C-blue?style=flat-square&logo=c)
![Threads](https://img.shields.io/badge/POSIX-Threads-orange?style=flat-square)
![Status](https://img.shields.io/badge/Status-Locked-red?style=flat-square)

> Master the race for resources before the deadline masters you.

---

## 📝 Table of Contents

- [Description](#-description)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Rules & Constraints](#-rules--constraints)
- [Status](#-status)

---

## 📌 Description

**Codexion** is a concurrency challenge inspired by the classic Dining Philosophers problem.
Multiple coders in a shared development space compete for a limited number of USB dongles
(hardware licenses). Each coder must alternately **code**, **sleep**, and **think**, and needs
two dongles to code. The challenge: prevent deadlock, starvation, and race conditions using
**POSIX threads** and **mutexes**.

---

## ⚙️ How It Works

- Each **coder** runs in its own thread
- Each **USB dongle** is protected by a mutex
- Coders must pick up the **left and right dongles** before coding
- A coder dies if they don’t start coding within a set time limit
- The simulation stops when a coder dies or all coders have coded enough times

### Lifecycle of a coder:

```
[Think] → [Pick up left dongle] → [Pick up right dongle] → [Code] → [Put down dongles] → [Sleep] → [Think] → ...
```

---

## 📁 Project Structure

```
Codexion/
├── en.subject (1).pdf   # Project subject
```

> Source code will be added once the project is unlocked.

---

## 🚀 Installation & Usage

```bash
# Compile
make

# Run
./codexion number_of_coders time_to_die time_to_code time_to_sleep [number_of_times_each_coder_must_code]
```

### Example:

```bash
./codexion 5 800 200 200
# 5 coders, die if no coding starts within 800ms, coding takes 200ms, sleeping takes 200ms

./codexion 4 410 200 200 5
# 4 coders, each must code 5 times before simulation ends
```

---

## 📜 Rules & Constraints

| Rule | Detail |
|------|--------|
| No global variables | All data via struct |
| No data races | Mutexes protect all shared state |
| No deadlock | Proper dongle acquisition order |
| No memory leaks | All allocations freed |
| Threads | One thread per coder |
| Mutexes | One mutex per dongle + one for logging |

---

## 📊 Status

| Field | Info |
|-------|------|
| **Project** | Codexion |
| **Circle** | 3 |
| **Language** | C |
| **Concurrency** | POSIX Threads + Mutexes |
| **Status** | 🔒 Locked |
| **Author** | ialmani |
