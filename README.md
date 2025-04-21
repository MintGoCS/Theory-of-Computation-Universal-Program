# Theory of Computation - Programming Assignment #2

**Author:** Zhongyu Xie  
**Course:** Theory of Computation  
**Date:** April 10, 2025

---

## File Structure

### `decoding.py`
- Adapted from Programming_Assignment_1, basically the same.
- Contains functions for decoding the `#(P)` into lines of the corresponding program.

### `universal.py`
- Simulates execution of any encoded program given its input.

### `config.py`
- Stores key configuration parameters.
    - `PRIME_LIST`: List of the first 30 prime numbers.
    - `MAX_STEP`: Upper bound for steps to detect potential infinite loops.
    - `Min_STEP` and `MAX_STEP`: Limit the range of the user's input.

---

## How to Run the Script

To execute the program, run:

```bash
python main.py
```

This will prompt for:
1. An input value `x_1`
2. A program number `#(P)`

The program will:
- Decode and display the original program.
- Print the snapshots
- Return `Error` message if input is invalid or program is infinite.

---

## Notes
- Make sure all `.py` files (`main.py`, `decoding.py`, `universal.py`, `config.py`) are in the same directory.

