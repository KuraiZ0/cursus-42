# 📞 Call Me Maybe

[![42 Project](https://img.shields.io/badge/42-Call_Me_Maybe-00babc?style=flat-square&logo=42)](https://github.com/KuraiZ0/cursus-42/tree/main/Circle_3/Call_Me_Maybe)
[![Circle](https://img.shields.io/badge/Circle-3-orange?style=flat-square)]()
[![Language](https://img.shields.io/badge/Language-C-blue?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Locked-lightgrey?style=flat-square)]()
[![Signals](https://img.shields.io/badge/UNIX-Signals-red?style=flat-square)]()

> Client-server communication using only UNIX signals.

## 📋 Table of Contents

- [Description](#-description)
- [How It Works](#-how-it-works)
- [Signals Used](#-signals-used)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)

## 🎯 Description

**Call Me Maybe** is a 42 Brussels project that implements a **client-server communication system** using exclusively UNIX signals. The server receives messages sent bit-by-bit by the client via `SIGUSR1` and `SIGUSR2`, reconstructs them, and prints them to stdout.

Key constraints:
- No sockets, no pipes, no shared memory
- Communication via `SIGUSR1` / `SIGUSR2` only
- Server must handle multiple clients without restart
- Bonus: Unicode support & server acknowledgement

## ⚙️ How It Works

```
Client                          Server
  |                               |
  | -- SIGUSR1 (bit = 0) -------> |
  | -- SIGUSR2 (bit = 1) -------> |
  |  (repeat for each bit of     |
  |   each character)            |
  |                               |
  | <-- SIGUSR1 (ACK) ----------- |  (bonus)
```

1. The **server** starts and prints its PID.
2. The **client** takes the server PID and a string as arguments.
3. Each character is encoded bit-by-bit: `SIGUSR1` = 0, `SIGUSR2` = 1.
4. The server reconstructs each character and prints the full message.

## 🔔 Signals Used

| Signal | Meaning |
|--------|---------|
| `SIGUSR1` | Bit 0 (or ACK from server) |
| `SIGUSR2` | Bit 1 |

## 📂 Project Structure

```
Call_Me_Maybe/
├── en.subject.pdf             # Project subject
└── attachments_project_ai.zip # AI-related assets
```

> Source code will be added once the project is unlocked.

## 🚀 Installation & Usage

```bash
# Terminal 1 — start the server
./server
# Output: Server PID: 12345

# Terminal 2 — send a message
./client 12345 "Hello 42!"
# Server prints: Hello 42!
```

### Compile

```bash
make        # Build server and client
make clean  # Remove object files
make fclean # Remove all binaries
make re     # Recompile
```

**Status**: Locked 🔒 | **Author**: [ialmani](https://profile.intra.42.fr/users/ialmani)
