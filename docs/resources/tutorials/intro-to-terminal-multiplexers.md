---
title: "[Tutorial] Intro to terminal multiplexers (screen, tmux, byobu)"
description: "A beginner's guide to terminal multiplexers: keeping sessions alive, running multiple shells in one window, and the basics of screen, tmux, and byobu."
authors:
    - Gregg Thomas
---

# Intro to terminal multiplexers

{{ author_row(page) }}

If you work on a remote server or cluster over SSH, you have probably had this
happen: you start a long process, your laptop goes to sleep or your Wi-Fi drops,
and when you reconnect the process is gone. Or you find yourself opening five
separate SSH connections just to watch a log in one, edit a file in another, and
run a command in a third.

A **terminal multiplexer** solves both problems. It lets you:

- **Keep sessions alive** even after you disconnect. You can start something,
  close your laptop, go home, reconnect from a different computer, and pick up
  exactly where you left off.
- **Run many shells in one window**, split into panes or organized as tabs, all
  inside a single SSH connection.

The two classic tools are **`screen`** and **`tmux`**. **`byobu`** is a friendly
wrapper that sits on top of either one. This tutorial covers the core concepts
and the handful of commands you need to get productive with each.

!!! note "Where this matters on the cluster"
    On the FAS cluster, a multiplexer running on a **login node** is perfect for
    keeping an interactive workflow open — monitoring jobs, editing files, or
    holding a long `salloc`/`srun` interactive session so it survives a dropped
    connection. It is **not** a tool for running heavy computation directly:
    login nodes are shared, so real work still belongs in a Slurm job. Think of a
    multiplexer as a durable, organized workspace, not a way around the scheduler.

---

## What is a terminal multiplexer?

A multiplexer wraps your shell in a layer that keeps running independently of
your connection. There are three concepts to understand, from biggest to
smallest:

- **Session** — a whole workspace that keeps running on the server. You *detach*
  from it (leave it running in the background) and later *reattach* to it. This
  is the piece that survives a disconnect.
- **Window** — like a tab inside a session. Each window is a full-screen shell.
  A session can hold many windows.
- **Pane** — a split *within* a window, so you can see several shells side by
  side at once.

```text
Session  "analysis"
├── Window 0: editing
├── Window 1: monitoring   ┌───────────┬───────────┐
│                          │  pane 0   │  pane 1   │   <- one window,
│                          │  (htop)   │  (tail)   │      split into panes
│                          └───────────┴───────────┘
└── Window 2: git
```

### The prefix key

Almost every multiplexer command is triggered by a **prefix key**: you press the
prefix, release it, then press a command key. This keeps the tools from
intercepting normal keystrokes.

- **`screen`** prefix: `Ctrl-a` (written `C-a`)
- **`tmux`** prefix: `Ctrl-b` (written `C-b`)

So "press the prefix, then `c`" means press `Ctrl-a` (or `Ctrl-b` in tmux),
let go, then press `c`. Throughout this tutorial, `C-a c` means exactly that.

!!! tip "Detach vs. exit"
    **Detaching** leaves the session running on the server — this is what you
    want when you log off. **Exiting** the shell (typing `exit` in every window)
    closes the session for good. If you want your work to survive, detach; don't
    exit.

---

## screen basics

`screen` is the older of the two and is installed almost everywhere by default,
which makes it a safe fallback on any server.

### Starting and naming a session

```bash
screen                  # start an unnamed session
screen -S analysis      # start a session named "analysis" (recommended)
```

Naming your sessions makes them much easier to find later.

### Detaching and reattaching

```bash
# From inside a session, detach with the keystroke:
#   C-a d          (Ctrl-a, then d)

screen -ls              # list running sessions
screen -r analysis      # reattach to the "analysis" session
screen -r               # reattach if there is only one
```

You can now disconnect entirely, SSH back in later, run `screen -r`, and your
session is exactly as you left it.

### Working with windows

| Keys      | Action                          |
|-----------|---------------------------------|
| `C-a c`   | **c**reate a new window         |
| `C-a n`   | **n**ext window                 |
| `C-a p`   | **p**revious window             |
| `C-a "`   | list windows to pick from       |
| `C-a A`   | rename the current window       |
| `C-a 0`–`9` | jump to window by number      |

### Splitting into panes

| Keys        | Action                                  |
|-------------|-----------------------------------------|
| `C-a S`     | split horizontally (top/bottom)         |
| `C-a \|`    | split vertically (left/right)           |
| `C-a <Tab>` | move focus to the next pane             |
| `C-a X`     | close the current pane                  |

!!! note "A newly split pane is empty"
    In `screen`, a fresh pane has no shell in it yet — move into it with
    `C-a <Tab>` and press `C-a c` to start one.

### Scrolling back

Your mouse wheel often won't scroll inside `screen`. Enter **copy mode** to
scroll through history:

- Press `C-a <Esc>`, then use the arrow keys / PageUp to scroll.
- Press `<Esc>` again to leave copy mode.

---

## tmux basics

`tmux` is the modern successor to `screen`. It has cleaner defaults, a scriptable
config file, and mouse support, so it's the tool most people reach for today. The
concepts are identical — only the keybindings differ (prefix is `C-b`).

### Starting and naming a session

```bash
tmux                    # start an unnamed session
tmux new -s analysis    # start a session named "analysis"
```

### Detaching and reattaching

```bash
# From inside a session, detach with:
#   C-b d

tmux ls                     # list sessions
tmux attach -t analysis     # reattach to "analysis"
tmux attach                 # reattach to the most recent session
```

### Working with windows

| Keys      | Action                              |
|-----------|-------------------------------------|
| `C-b c`   | **c**reate a new window             |
| `C-b n`   | **n**ext window                     |
| `C-b p`   | **p**revious window                 |
| `C-b w`   | list windows to pick from           |
| `C-b ,`   | rename the current window           |
| `C-b 0`–`9` | jump to window by number          |

### Splitting into panes

Unlike `screen`, a new `tmux` pane immediately opens a shell.

| Keys              | Action                                    |
|-------------------|-------------------------------------------|
| `C-b %`           | split vertically (left/right)             |
| `C-b "`           | split horizontally (top/bottom)           |
| `C-b <arrow>`     | move focus between panes                   |
| `C-b z`           | zoom the current pane to full screen (toggle) |
| `C-b x`           | close the current pane                    |
| `C-b <space>`     | cycle through pane layouts                |

### Scrolling back

Press `C-b [` to enter copy mode, then scroll with the arrow keys / PageUp.
Press `q` to exit.

### A minimal config file

`tmux` reads `~/.tmux.conf` on startup. A couple of quality-of-life settings
that beginners tend to want:

```bash
# ~/.tmux.conf
set -g mouse on            # click panes/windows, drag to resize, wheel to scroll
set -g history-limit 50000 # keep a much longer scrollback buffer
```

With `mouse on`, you can click to select panes, drag borders to resize, and
scroll with the wheel — a big usability jump.

!!! tip "Reloading the config"
    After editing `~/.tmux.conf`, apply it without restarting: from inside tmux
    press `C-b :`, type `source-file ~/.tmux.conf`, and hit `Enter`.

---

## screen vs. tmux at a glance

| Task                | screen        | tmux              |
|---------------------|---------------|-------------------|
| Prefix key          | `C-a`         | `C-b`             |
| New named session   | `screen -S x` | `tmux new -s x`   |
| Detach              | `C-a d`       | `C-b d`           |
| List sessions       | `screen -ls`  | `tmux ls`         |
| Reattach            | `screen -r x` | `tmux attach -t x`|
| New window          | `C-a c`       | `C-b c`           |
| Next / prev window  | `C-a n` / `p` | `C-b n` / `p`     |
| Split vertical      | `C-a \|`      | `C-b %`           |
| Split horizontal    | `C-a S`       | `C-b "`           |
| Switch pane         | `C-a <Tab>`   | `C-b <arrow>`     |
| Scrollback / copy   | `C-a <Esc>`   | `C-b [`           |

**Which should you use?** If you're starting fresh, learn **tmux** — better
defaults, mouse support, and a config you can carry between machines. Keep
**screen** in your back pocket for servers where tmux isn't installed.

---

## byobu: a friendlier front-end

If the prefix-key gymnastics feel like a lot, **`byobu`** is a wrapper around
tmux (or screen) that adds a helpful status bar and maps the most common actions
to plain **function keys** — no prefix required.

```bash
byobu                   # start (or reattach to) a byobu session
```

Common byobu keys:

| Key         | Action                          |
|-------------|---------------------------------|
| `F2`        | new window                      |
| `F3` / `F4` | previous / next window          |
| `F6`        | detach (leave it running)       |
| `F8`        | rename the current window       |
| `Shift-F2`  | split horizontally              |
| `Ctrl-F2`   | split vertically                |
| `F9`        | open the byobu config menu      |

The status bar along the bottom shows things like the time, load, and memory,
and the config menu (`F9`) lets you toggle features and change the backend
without editing files by hand.

!!! note "byobu is still tmux/screen underneath"
    Because byobu just drives tmux or screen, everything you learned above still
    applies — you can mix function keys with the normal prefix commands. Check
    which backend is active with `byobu-status` or in the `F9` menu.

??? tip "Making byobu (or tmux) auto-start on login"
    Some people like their multiplexer to launch automatically every time they
    log in. You can enable that with `byobu-enable` (and undo it with
    `byobu-disable`). This is optional and a matter of taste — many users prefer
    to start it manually so they control when a session is created.

---

## A few gotchas

!!! warning "Clusters with multiple login nodes"
    Your session lives on the **specific machine** where you started it. On a
    cluster with several login nodes (e.g. `holylogin01`, `holylogin02`, …), if
    you reconnect to a *different* login node your session won't be there. Note
    which node you're on (it's in your prompt) and SSH back to that same one to
    reattach.

!!! warning "Don't do heavy compute on a login node"
    A multiplexer is great for editing, monitoring, and holding interactive
    sessions open, but it does **not** exempt you from the scheduler. Launch real
    computation through Slurm (`sbatch`, `salloc`, `srun`).

!!! tip "Nesting"
    Running tmux inside tmux (for example, a local tmux and another on the
    server) means the prefix goes to the outer one. Send a command to the *inner*
    session by pressing the prefix **twice**: `C-b C-b c`.

---

## Further reading

- tmux manual: `man tmux`, and the official [tmux wiki :octicons-link-external-24:](https://github.com/tmux/tmux/wiki){:target="_blank"}
- [GNU screen manual :octicons-link-external-24:](https://www.gnu.org/software/screen/manual/){:target="_blank"}
- [byobu documentation :octicons-link-external-24:](https://www.byobu.org/){:target="_blank"}
