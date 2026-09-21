---
title: NovaCalc — Scientific Calculator
emoji: 🧮
colorFrom: blue
colorTo: cyan
sdk: streamlit
sdk_version: 1.39.0
app_file: app.py
pinned: false
license: mit
short_description: A scientific calculator with Shift functions, memory, history, and CSV export.
---

# 🧮 NovaCalc — Scientific Calculator

NovaCalc is a modern, high-contrast scientific calculator built with Python and Streamlit. It supports everyday arithmetic, scientific calculations, trigonometry, memory functions, Shift-mode alternate operations, calculation history, and CSV export.

## Live features

- Basic arithmetic: addition, subtraction, multiplication, division, modulus, and powers
- Scientific functions: square, cube, square root, cube root, inverse, absolute value, factorial, percentage, rounding, ceiling, and floor
- Logarithmic and exponential functions: `ln`, `log₁₀`, `log₂`, and `eˣ`
- Trigonometry: sine, cosine, tangent, cosecant, secant, and cotangent
- Degree and radian modes for trigonometric calculations
- Quick expression evaluation using `+`, `-`, `*`, `/`, `%`, `^`, and parentheses
- Shift mode for alternate calculator functions
- Memory operations: `MC`, `MR`, `M+`, and `M−`
- Mathematical constants: π, Euler’s number `e`, and the golden ratio `φ`
- Session-based calculation history
- Download calculation history as a CSV file
- Built-in help center explaining each feature

## Shift mode

Shift Mode activates alternate functions for selected operations.

| Normal operation | Shift operation |
|---|---|
| `sin(x)` | `cos(x)` |
| `cos(x)` | `tan(x)` |
| `tan(x)` | `cot(x)` |
| `x²` | `x³` |
| `x³` | `x²` |
| `√x` | `∛x` |
| `∛x` | `√x` |
| `ln(x)` | `log₁₀(x)` |
| `log₁₀(x)` | `log₂(x)` |
| `log₂(x)` | `ln(x)` |
| `ceil(x)` | `floor(x)` |
| `floor(x)` | `ceil(x)` |

## How to use

1. Use **Quick Expression** to calculate expressions such as `(25 + 5) * 3` or `2^8`.
2. Or select a scientific operation from the dropdown.
3. Enter the first number and, when needed, the second number.
4. Select **Degrees** or **Radians** before using trigonometric functions.
5. Turn on **Shift Mode** to activate an alternate function.
6. Click **Calculate** to view the result.
7. Use the memory controls and calculation history as needed.

## Example calculations

```text
(25 + 5) * 3 = 90
2^8 = 256
sin(30°) = 0.5
cos(60°) = 0.5
tan(45°) = 1
√81 = 9
5! = 120
log₁₀(1000) = 3
```

## Technology stack

- Python
- Streamlit
- NumPy
- Python `math` module
- Python `ast` module for safe expression processing

## Safety and limitations

NovaCalc validates common mathematical errors, including division by zero, negative square roots, invalid logarithms, invalid factorial inputs, and undefined trigonometric values.

The Quick Expression feature safely supports only arithmetic values, parentheses, and approved arithmetic operators. It does not execute arbitrary Python code.

Calculation history and memory are stored only for the active browser session. They are cleared when the user session ends or when the history is reset.
Live Demo: https://huggingface.co/spaces/nisar-ai/novacalc-scientific-calculator

## Developer

**Nisar Ahmad**  
AI/ML Developer and BS Computer Science Student  
COMSATS University Islamabad, Sahiwal Campus

This project demonstrates practical Python programming, Streamlit application development, input validation, mathematical computing, session-state management, and CSV export.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
