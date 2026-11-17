# Nand to Tetris (NTT) — Computer Systems Architecture

**Author:** Kumari Pratibha  
**ID:** `2501010123`  
**Repository:** [K-Pratzz/NTT](https://github.com/K-Pratzz/NTT)

---

## Overview

This repository contains project implementations, hardware descriptions, and software modules built for the **Nand to Tetris** (*From Nand to Tetris: Building a Modern Computer From First Principles*) coursework and capstone project[cite: 1]. Starting from basic Boolean logic gates, the projects progressively construct a complete general-purpose computer system.

---

## Project Structure

| Module / Project | Topic | Key Components / Files |
| :--- | :--- | :--- |
| **Project 01** | Boolean Logic | `Not`, `And`, `Or`, `Xor`, `Mux`, `DMux`, multi-bit & multi-way variants (`.hdl`) |
| **Project 02** | Boolean Arithmetic | `HalfAdder`, `FullAdder`, `Add16`, `Inc16`, `ALU` (`.hdl`) |
| **Project 03** | Sequential Logic | `Bit`, `Register`, `RAM8`, `RAM64`, `RAM512`, `RAM4K`, `RAM16K`, `PC` (`.hdl`) |
| **Project 04** | Machine Language | Low-level Hack assembly programs (`Mult.asm`, `Fill.asm`) |
| **Project 05** | Computer Architecture | `Memory`, `CPU`, `Computer` (`.hdl`) |
| **Project 06+** | System Software / Capstone | Assembler, VM Translator, Compiler, or Capstone Implementation[cite: 1] |

*(Note: Adjust or remove rows above depending on which specific project folders are included in your submission.)*

---

## Tools & Requirements

To test and simulate the files in this repository, download the official **Nand to Tetris Software Suite**:
* **Hardware Simulator** — for running and verifying `.hdl` chips alongside `.tst` and `.cmp` scripts.
* **CPU Emulator** — for executing and testing `.asm` and `.hack` machine language programs.
* **VM Emulator** — for running intermediate virtual machine code (`.vm`).

---

## How to Run & Verify

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/K-Pratzz/NTT.git](https://github.com/K-Pratzz/NTT.git)
   cd NTT
