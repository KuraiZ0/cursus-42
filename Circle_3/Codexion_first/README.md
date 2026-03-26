# 💻 Codexion

> *Master the race for resources before the deadline masters you.*

*This project has been created as part of the 42 curriculum by **ialmani**.*

## 📖 Description

Codexion is a concurrency simulation inspired by the classic Dining Philosophers problem. Multiple coders share a circular co-working hub equipped with a Quantum Compiler. 

To compile their quantum code, each coder needs to simultaneously hold two USB dongles — one on their left, one on their right. Coders alternate between three phases: **compiling**, **debugging**, and **refactoring**. A coder who fails to start compiling within `time_to_burnout` milliseconds burns out, ending the simulation.

The challenge is to prevent deadlock, starvation, and race conditions using POSIX threads and mutexes, while implementing a priority-based scheduler (FIFO or EDF) backed by a min-heap to ensure fair dongle arbitration.

---

## 🚀 Instructions

### 🛠️ Compilation

```bash
make        # build the project
make clean  # remove object files
make fclean # remove object files and binary
make re     # full recompile
```

### ⚙️ Execution

```bash
./codexion number_of_coders time_to_burnout time_to_compile time_to_debug time_to_refactor number_of_compiles_required dongle_cooldown scheduler
```

*All 8 arguments are mandatory. Invalid inputs (negative numbers, non-integers, unknown scheduler) are rejected.*

| Argument | Type | Description |
| :--- | :---: | :--- |
| `number_of_coders` | `int` | Number of coders (and dongles). |
| `time_to_burnout` | `ms` | Max time without compiling before burnout. |
| `time_to_compile` | `ms` | Duration of the compile phase (requires 2 dongles). |
| `time_to_debug` | `ms` | Duration of the debug phase. |
| `time_to_refactor` | `ms` | Duration of the refactor phase. |
| `number_of_compiles_required` | `int` | Simulation ends when all coders reach this count. |
| `dongle_cooldown` | `ms` | Cooldown before a released dongle can be re-acquired. |
| `scheduler` | `string` | `fifo` (arrival order) or `edf` (earliest deadline first). |

---

## 💡 Examples

```bash
# 5 coders, 800ms burnout limit, 200ms compile/debug/refactor, no compile limit, 50ms cooldown, FIFO
./codexion 5 800 200 200 200 0 50 fifo

# 4 coders, each must compile 5 times, EDF scheduler
./codexion 4 410 200 200 200 5 0 edf

# Edge case: single coder (can never compile — no second dongle available)
./codexion 1 800 200 200 200 0 0 fifo
```

---

## 📋 Expected Log Format

The simulation logs state changes in the following format:
* `timestamp_in_ms X has taken a dongle`
* `timestamp_in_ms X is compiling`
* `timestamp_in_ms X is debugging`
* `timestamp_in_ms X is refactoring`
* `timestamp_in_ms X burned out`

**Example output:**
```text
0 1 has taken a dongle
2 1 has taken a dongle
2 1 is compiling
202 1 is debugging
402 1 is refactoring
405 2 has taken a dongle
406 2 has taken a dongle
406 2 is compiling
606 2 is debugging
806 2 is refactoring
1505 4 burned out
```

---

## 🛡️ Blocking Cases Handled

### Deadlock Prevention
A circular wait is the classic deadlock scenario in the Dining Philosophers problem. Coffman's four conditions for deadlock are: mutual exclusion, hold-and-wait, no preemption, and circular wait. This implementation breaks the circular wait condition by assigning an asymmetric acquisition order based on each coder's ID:
* **Even ID:** Take left dongle first, then right.
* **Odd ID:** Take right dongle first, then left.

This ensures that not all coders attempt to acquire resources in the same rotational direction, making a full circular wait impossible.

### Starvation Prevention
Starvation is prevented through the fair arbitration mechanism required by the subject. Each dongle maintains a min-heap priority queue of pending requests. When a coder requests a dongle, it is enqueued with a priority computed by the active scheduler:
* **FIFO:** `priority = get_time_ms()` at request time → requests served in arrival order.
* **EDF:** `priority = last_compile + time_to_burnout` → the coder with the earliest deadline (closest to burnout) is served first.

A coder can only acquire a dongle when it sits at the head of the queue, preventing any coder from being indefinitely bypassed.

### Dongle Cooldown
After a coder releases a dongle, the dongle records `available_at = get_time_ms() + dongle_cd`. Any waiting coder is woken via `pthread_cond_broadcast`, but the acquisition condition inside `take_dongle` also checks `get_time_ms() >= dongle->available_at`. If the cooldown has not elapsed, the thread yields (`usleep(1000)`) and retries, ensuring the cooldown is strictly respected before any coder can re-acquire the dongle.

### Precise Burnout Detection
A dedicated monitor thread runs in parallel with all coder threads. It polls every 1ms and reads each coder's `last_compile` timestamp (under `state_mutex`). If `now - last_compile > time_to_burnout`, the monitor logs the burnout event and calls `set_stop`, guaranteeing detection within the 10ms window required by the subject.

### Log Serialization
All `printf` calls pass through `log_event`, which holds `log_mutex` for the entire duration of the print. Before printing, the function re-checks the stop flag under the lock, preventing any post-burnout messages from appearing. This guarantees that log lines are never interleaved and that the burnout message is always the last line printed.

---

## 🔄 Thread Synchronization Mechanisms

### Primitives Used

| Primitive | Instance | Purpose |
| :--- | :--- | :--- |
| `pthread_mutex_t log_mutex` | `t_params` | Serializes all log output. |
| `pthread_mutex_t stop_mutex` | `t_params` | Protects the shared stop flag. |
| `pthread_mutex_t state_mutex` | `t_coder` | Protects `last_compile` and `compile_count` per coder. |
| `pthread_mutex_t t_mutex` | `t_dongle` | Protects dongle state and its heap queue. |
| `pthread_cond_t t_cond` | `t_dongle` | Wakes waiting coders when a dongle is released. |

### Dongle Access Coordination
When a coder wants to acquire a dongle (`take_dongle`), it:
1. Locks `dongle->t_mutex`.
2. Pushes itself into `dongle->queue` with its scheduler-computed priority.
3. Enters a wait loop: if the dongle is unavailable, it blocks on `pthread_cond_wait`; if available but not first in queue or cooldown not elapsed, it releases the lock briefly (`usleep(1000)`) and retries.
4. Once all conditions are met, sets `dongle->available = 0`, pops itself from the queue, and unlocks.

On release (`release_dongle`), the coder sets `available_at`, marks the dongle available, and calls `pthread_cond_broadcast` to wake all waiting coders.

### Monitor–Coder Communication
The monitor thread reads `coder->last_compile` under `state_mutex` to avoid a data race with the coder thread that updates it after each successful compile. The stop flag is always read and written under `stop_mutex`, both by coder threads (which set it when `number_of_compiles_required` is reached) and by the monitor (which sets it on burnout).

### Race Condition Prevention Example
Without `state_mutex`, the monitor could read a partially-written `last_compile` value while a coder is in the middle of updating it, producing a false burnout detection. The lock guarantees a consistent snapshot:

```c
// Coder thread — after compiling:
pthread_mutex_lock(&coder->state_mutex);
coder->last_compile = get_time_ms();
coder->compile_count++;
pthread_mutex_unlock(&coder->state_mutex);

// Monitor thread — burnout check:
pthread_mutex_lock(&sim->coders[i].state_mutex);
last_co = sim->coders[i].last_compile;
pthread_mutex_unlock(&sim->coders[i].state_mutex);

if (now - last_co > sim->params.time_to_burnout)
    // burnout detected
```

---

## 📚 Resources

* [POSIX Threads Programming](https://computing.llnl.gov/tutorials/pthreads/) — Lawrence Livermore National Laboratory
* [The Dining Philosophers Problem](https://en.wikipedia.org/wiki/Dining_philosophers_problem) — Wikipedia
* [Coffman Conditions for Deadlock](https://en.wikipedia.org/wiki/Deadlock#Necessary_conditions) — Wikipedia
* [Earliest Deadline First Scheduling](https://en.wikipedia.org/wiki/Earliest_deadline_first_scheduling) — Wikipedia
* [Priority Queue / Binary Heap](https://en.wikipedia.org/wiki/Binary_heap) — Wikipedia
* Manuals: `man pthread_create`, `man pthread_mutex_init`, `man pthread_cond_wait`, `man gettimeofday`

---

## 🤖 AI Usage

AI assistance was kept to a strict minimum during this project and was exclusively used for:
* **Conceptual explanations:** Clarifying new concepts, such as the semantic differences between FIFO and EDF scheduling semantics.
* **Debugging assistance:** Helping to pinpoint minor logic errors or oversights during the testing phase (e.g., identifying a missing file in the Makefile or a flaw in the compile count stop condition).

No core logic or project structure was generated by AI. All implementations and solutions are entirely my own work.