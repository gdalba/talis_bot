# Memory Pointer Finding Tutorial

This tutorial explains how to find memory pointers for a game using the built-in scanner in `pointers.py`. This is useful when you have a different game version and the existing pointers don't work.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Understanding Memory Pointers](#understanding-memory-pointers)
3. [Getting Started](#getting-started)
4. [Finding Known Values](#finding-known-values)
5. [Narrowing Down Results](#narrowing-down-results)
6. [Exploring Memory Structure](#exploring-memory-structure)
7. [Finding Static Pointer Chains](#finding-static-pointer-chains)
8. [Verifying Pointer Chains](#verifying-pointer-chains)
9. [Updating the Code](#updating-the-code)

---

## Prerequisites

- Python with `pymem` installed (`pip install pymem`)
- The game running
- Administrator privileges (required for memory reading)
- Knowledge of some in-game values (HP, Mana, Gold, Character Name, etc.)

---

## Understanding Memory Pointers

### Dynamic vs Static Addresses

When a game runs, data like your character's HP is stored in memory. However, the **address changes every time you restart the game**. These are called **dynamic addresses**.

To reliably read values, we need to find a **static address** (one that doesn't change) and follow a chain of **offsets** to reach the dynamic data.

### Pointer Chain Example

```
[0x0045BFB4] -> +0xAD4 -> +0xFEC -> +0xC88 -> +0x48 -> +0x320 = Character Data
```

This means:
1. Read the value at static address `0x0045BFB4`
2. Add offset `0xAD4` to that value, read again
3. Continue until you reach the final data

Static addresses are typically in the range `0x00400000 - 0x02000000` (the game's code/data section).

---

## Getting Started

### 1. Find the Game's Process ID (PID)

Open Task Manager, go to Details tab, find your game, and note the PID.

### 2. Start the Scanner

```bash
python pointers.py <PID> --scan
```

You'll see:
```
============================================================
  Pointers Test - PID: 12345
============================================================

[+] Successfully attached to process!

============================================================
  Interactive Memory Scanner
============================================================

Commands:
  si <value>       - Search for integer value
  sf <value>       - Search for float value  
  ss <text>        - Search for string
  d <address>      - Dump memory at address (hex)
  r <address>      - Read int at address (hex)
  rf <address>     - Read float at address (hex)
  rs <address>     - Read string at address (hex)
  n <value>        - Narrow down previous search (enter new value)
  p                - Probe around known pointers
  pc <address>     - Pointer chain scan (find static pointer to address)
  vc               - Verify a pointer chain
  q                - Quit scanner

scanner>
```

---

## Finding Known Values

### Search for Your Character Name

If your character is named "CJSpace":

```
scanner> ss CJSpace
[*] Searching for string: 'CJSpace'
[*] Scanning 2182 memory regions...
[+] Found 3 matches
  0x2DEA242C
  0x1A3B5678
  0x0F123456
```

### Search for Your HP

If your current HP is 5000:

```
scanner> si 5000
[*] Searching for integer: 5000 (0x1388)
[*] Scanning 2182 memory regions...
[+] Found 47 matches
  0x2DEA23C8
  0x2DEA2728
  ... (more results)
```

---

## Narrowing Down Results

When you get many results, use the **narrow** command:

### Step 1: Search for current value
```
scanner> si 5000
[+] Found 47 matches
```

### Step 2: Change the value in-game
Use a health potion, take damage, etc. Let's say HP is now 4850.

### Step 3: Narrow the results
```
scanner> n 4850
[*] Narrowing 47 addresses to new value: 4850
[+] 2 addresses remaining
  0x2DEA23C8
  0x2DEA2728
```

### Step 4: Repeat if needed
Keep changing the value and narrowing until you have 1-3 results.

---

## Exploring Memory Structure

Once you find an address, explore the surrounding memory to find related values.

### Dump Memory

```
scanner> d 2DEA23C8
[*] Memory dump at 0x2DEA23C8 (256 bytes):

  2DEA23C8  F3 13 00 00 88 31 00 00 00 00 00 00 47 00 56 40   .....1......G.V@
  2DEA23D8  F6 12 2C 00 E4 18 27 00 00 00 00 00 00 00 00 00   ..,...'.........
  ...
  2DEA2420  CD AE 62 00 78 80 07 00 A5 84 3C 3F 43 4A 53 70   ..b.x.....<?CJSp
  2DEA2430  61 63 65 00 17 35 53 40 12 2C 07 42 07 00 00 00   ace..5S@.,.B....
```

Look for:
- **Readable text** (like "CJSpace" above)
- **Reasonable numbers** in hex (HP, Mana, Level)
- **Patterns** (related values are often near each other)

### Read Specific Offsets

```
scanner> r 2DEA23C8      # Max HP?
  0x2DEA23C8 = 5107

scanner> r 2DEA23CC      # Max Mana?
  0x2DEA23CC = 12680

scanner> rs 2DEA242C     # Character Name?
  0x2DEA242C = 'CJSpace'
```

---

## Finding Static Pointer Chains

Once you have a dynamic address with your data, find the static pointer chain.

### Use Pointer Chain Scanner

```
scanner> pc 2DEA23C8
============================================================
  Pointer Chain Scanner
============================================================
  Target: 0x2DEA23C8
  Max depth: 4, Max offset: 0x1000
============================================================

[*] Loaded 2182 memory regions
[*] Building pointer map (this may take a moment)...
[*] Found 1234567 unique pointer values

[*] Searching for pointer chains to 0x2DEA23C8...

  [FOUND] 0x0045BFB4 -> [+0xAD4] -> [+0xFEC] -> [+0xC88] -> [+0x48] -> [+0x320] = 0x2DEA23C8
  [FOUND] 0x01A9C0D0 -> [+0x3E0] -> [+0xFEC] -> [+0xC88] -> [+0x48] -> [+0x320] = 0x2DEA23C8
  ...
```

### Choose the Best Chain

Look for:
1. **Shortest chains** (fewer arrows = more reliable)
2. **Base address starting with 0x004 or 0x01** (closer to game code)
3. **Small offsets** (0x0, 0x4, 0x8, etc.)

---

## Verifying Pointer Chains

Before using a chain, verify it works:

```
scanner> vc 0045BFB4 AD4 FEC C88 48 320

[*] Verifying pointer chain from 0x0045BFB4
    Offsets: +0xAD4 -> +0xFEC -> +0xC88 -> +0x48 -> +0x320

  Step 0: [0x0045BFB4] = 0x17B0B950
  Step 1: [0x17B0B950 + 0xAD4] = [0x17B0C424] = 0x1727CD38
  Step 2: [0x1727CD38 + 0xFEC] = [0x1727DD24] = 0x180CD4B0
  Step 3: [0x180CD4B0 + 0xC88] = [0x180CE138] = 0x175A0EC4
  Step 4: [0x175A0EC4 + 0x48] = [0x175A0F0C] = 0x2DEA20A8
  Step 5: 0x2DEA20A8 + 0x320 = 0x2DEA23C8 (final data address)

  Final address: 0x2DEA23C8

  Reading values at final address:
    +0x000 (Max HP?):    5975
    +0x004 (Max Mana?):  12995
    +0x360 (Cur HP?):    5975
    +0x364 (Cur Mana?):  12995
    +0x064 (Name?):      'CJSpace'
```

**Success!** The chain works and shows your character's data.

---

## Updating the Code

### Add to `pointers.py`

In the `Pointers` class `__init__` method:

```python
# Static base -> Character structure
self.CHAR_BASE_STATIC = 0x0045BFB4
self.CHAR_BASE_OFFSETS = [0xAD4, 0xFEC, 0xC88, 0x48, 0x320]

# Calculate character base address
self.CHAR_BASE = self.get_pointer(self.CHAR_BASE_STATIC, offsets=self.CHAR_BASE_OFFSETS)

# Character structure offsets
self.MAX_HP_POINTER = self.CHAR_BASE + 0x000 if self.CHAR_BASE else None
self.MAX_MANA_POINTER = self.CHAR_BASE + 0x004 if self.CHAR_BASE else None
self.CHAR_NAME_POINTER_NEW = self.CHAR_BASE + 0x064 if self.CHAR_BASE else None
self.HP_POINTER = self.CHAR_BASE + 0x360 if self.CHAR_BASE else None
self.MANA_POINTER = self.CHAR_BASE + 0x364 if self.CHAR_BASE else None
```

---

## Tips & Tricks

### Common Data Types

| Type | Size | Use For |
|------|------|---------|
| Byte | 1 byte | Flags, Level, Small counters |
| Int | 4 bytes | HP, Mana, Gold, IDs |
| Float | 4 bytes | Coordinates (X, Y, Z) |
| String | Variable | Names, Locations |

### Common Structure Patterns

Games often store related data together:
- HP and Max HP near each other (often +0x04 apart)
- Character name within the character structure
- Coordinates (X, Y, Z) in sequence

### If Pointer Chain Fails

1. The game may have been updated - repeat the process
2. Try searching for a different value
3. Try `pc` with a nearby address (±0x100)
4. The structure might be accessed differently

### Memory Regions

- `0x00400000 - 0x01FFFFFF` = Static (game code/data) ✓
- `0x10000000+` = Dynamic (heap/allocated) - needs pointer chain

---

## Quick Reference

| Command | Description |
|---------|-------------|
| `si <int>` | Search for integer |
| `sf <float>` | Search for float |
| `ss <text>` | Search for string |
| `d <addr>` | Dump memory (hex) |
| `r <addr>` | Read integer |
| `rf <addr>` | Read float |
| `rs <addr>` | Read string |
| `n <value>` | Narrow previous search |
| `pc <addr>` | Find pointer chain to address |
| `vc <base> <off1> <off2>...` | Verify pointer chain |
| `p` | Probe around known pointers |
| `q` | Quit |

---

## Example Workflow Summary

1. **Start scanner**: `python pointers.py <PID> --scan`
2. **Search for known value**: `si 5000` (your HP)
3. **Change value in-game** (take damage/heal)
4. **Narrow results**: `n 4850` (new HP)
5. **Repeat until 1-3 results**
6. **Dump memory**: `d <address>` to explore structure
7. **Find pointer chain**: `pc <address>`
8. **Verify chain**: `vc <base> <offsets...>`
9. **Update code** with new pointers

Happy hunting! 🎮
