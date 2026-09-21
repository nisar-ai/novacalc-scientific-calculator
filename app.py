import ast
import csv
import io
import math
import operator
import re
from datetime import datetime

import numpy as np
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Nisar's NovaCalc",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# HIGH-CONTRAST UI
# ============================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    :root {
        --bg-dark: #07111f;
        --panel: #0d1b2e;
        --panel-light: #132742;
        --line: #294565;
        --cyan: #22d3ee;
        --blue: #38bdf8;
        --green: #34d399;
        --yellow: #facc15;
        --orange: #fb923c;
        --pink: #fb7185;
        --white: #f8fafc;
        --muted: #a9bad0;
    }

    * {
        font-family: "Inter", sans-serif;
    }

    .stApp {
        min-height: 100vh;
        color: var(--white);
        background:
            radial-gradient(circle at 10% 0%, rgba(34, 211, 238, 0.16), transparent 30%),
            radial-gradient(circle at 90% 100%, rgba(56, 189, 248, 0.15), transparent 34%),
            linear-gradient(135deg, #050b14 0%, #0b1830 50%, #07111f 100%);
    }

    .block-container {
        max-width: 1280px;
        padding: 1.3rem 1rem 2.8rem;
    }

    .app-shell {
        background: rgba(9, 22, 40, 0.95);
        border: 1px solid #25405f;
        border-radius: 28px;
        padding: 1.15rem;
        box-shadow:
            0 25px 80px rgba(0, 0, 0, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 1.5rem 1rem;
        text-align: center;
        border: 1px solid rgba(34, 211, 238, 0.40);
        border-radius: 22px;
        background:
            linear-gradient(135deg, rgba(14, 116, 144, 0.95), rgba(30, 64, 175, 0.96)),
            #0e7490;
        box-shadow: 0 18px 35px rgba(8, 145, 178, 0.22);
    }

    .hero::after {
        content: "∑  √  π  ∫  Δ";
        position: absolute;
        right: 1rem;
        bottom: 0.4rem;
        color: rgba(255, 255, 255, 0.12);
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: 0.45rem;
    }

    .hero h1 {
        position: relative;
        z-index: 1;
        margin: 0;
        color: white;
        font-size: clamp(2rem, 5vw, 3.25rem);
        font-weight: 800;
        letter-spacing: -0.06em;
    }

    .hero p {
        position: relative;
        z-index: 1;
        margin: 0.55rem 0 0;
        color: rgba(255, 255, 255, 0.90);
        font-size: 0.98rem;
    }

    .card {
        height: 100%;
        margin-top: 1rem;
        padding: 1.15rem;
        border: 1px solid var(--line);
        border-radius: 20px;
        background: linear-gradient(145deg, #0d1b2e, #0a1728);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
    }

    .card-title {
        margin-bottom: 0.85rem;
        padding-bottom: 0.55rem;
        border-bottom: 2px solid rgba(34, 211, 238, 0.55);
        color: var(--white);
        font-size: 1rem;
        font-weight: 800;
        letter-spacing: 0.02em;
    }

    .status-pill {
        display: inline-block;
        padding: 0.35rem 0.65rem;
        border: 1px solid rgba(52, 211, 153, 0.35);
        border-radius: 999px;
        background: rgba(52, 211, 153, 0.10);
        color: #86efac;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .shift-active {
        display: inline-block;
        margin-left: 0.45rem;
        padding: 0.35rem 0.65rem;
        border: 1px solid rgba(250, 204, 21, 0.60);
        border-radius: 999px;
        background: rgba(250, 204, 21, 0.14);
        color: #fde68a;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.03em;
    }

    .shift-inactive {
        display: inline-block;
        margin-left: 0.45rem;
        padding: 0.35rem 0.65rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
        border-radius: 999px;
        background: rgba(148, 163, 184, 0.08);
        color: #cbd5e1;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.03em;
    }

    .shift-map {
        margin-top: 0.8rem;
        padding: 0.8rem;
        border: 1px solid rgba(250, 204, 21, 0.28);
        border-radius: 12px;
        background: rgba(250, 204, 21, 0.08);
        color: #fef3c7;
        font-size: 0.84rem;
        line-height: 1.55;
    }

    .display-card {
        min-height: 166px;
        padding: 1.15rem;
        border: 1px solid rgba(34, 211, 238, 0.36);
        border-radius: 18px;
        background:
            linear-gradient(145deg, rgba(6, 22, 39, 0.98), rgba(10, 31, 53, 0.98));
        box-shadow: inset 0 0 25px rgba(34, 211, 238, 0.05);
    }

    .display-label {
        color: var(--muted);
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .display-expression {
        min-height: 28px;
        margin-top: 0.55rem;
        color: #bae6fd;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.95rem;
        overflow-wrap: anywhere;
    }

    .display-result {
        margin-top: 0.35rem;
        color: #67e8f9;
        font-family: "JetBrains Mono", monospace;
        font-size: clamp(1.8rem, 4vw, 2.65rem);
        font-weight: 700;
        overflow-wrap: anywhere;
    }

    .metric-box {
        padding: 0.75rem;
        border: 1px solid #294565;
        border-radius: 13px;
        background: rgba(19, 39, 66, 0.72);
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
    }

    .metric-value {
        margin-top: 0.25rem;
        color: var(--white);
        font-family: "JetBrains Mono", monospace;
        font-size: 1rem;
        font-weight: 700;
        overflow-wrap: anywhere;
    }

    .history-row {
        margin: 0.42rem 0;
        padding: 0.65rem 0.8rem;
        border-left: 3px solid var(--cyan);
        border-radius: 8px;
        background: #10243d;
        color: #dbeafe;
        font-family: "JetBrains Mono", monospace;
        font-size: 0.84rem;
        overflow-wrap: anywhere;
    }

    .help-box {
        margin: 0.65rem 0;
        padding: 0.95rem;
        border: 1px solid #294565;
        border-radius: 12px;
        background: rgba(19, 39, 66, 0.68);
        color: #dbeafe;
        line-height: 1.65;
    }

    .help-box strong {
        color: #67e8f9;
    }

    /* ========================================================
       NEW: HIGH-CONTRAST DEVELOPER PROFILE AT PAGE BOTTOM
       ======================================================== */
    .developer-spotlight {
        position: relative;
        overflow: hidden;
        margin-top: 1.35rem;
        padding: 2rem 1.5rem;
        border: 2px solid rgba(34, 211, 238, 0.72);
        border-radius: 22px;
        background:
            radial-gradient(circle at 12% 15%, rgba(34, 211, 238, 0.30), transparent 34%),
            radial-gradient(circle at 88% 80%, rgba(168, 85, 247, 0.34), transparent 35%),
            linear-gradient(135deg, #0f172a 0%, #172554 52%, #0e7490 100%);
        box-shadow:
            0 20px 48px rgba(0, 0, 0, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.14);
        text-align: center;
    }

    .developer-spotlight::before {
        content: "N";
        position: absolute;
        left: 3%;
        top: -1.6rem;
        color: rgba(255, 255, 255, 0.07);
        font-size: 12rem;
        font-weight: 800;
        line-height: 1;
        pointer-events: none;
    }

    .developer-badge {
        position: relative;
        z-index: 1;
        display: inline-block;
        margin-bottom: 0.75rem;
        padding: 0.38rem 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.30);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.12);
        color: #cffafe;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
    }

    .developer-name {
        position: relative;
        z-index: 1;
        margin: 0;
        color: #ffffff;
        font-size: clamp(2rem, 5vw, 3.6rem);
        font-weight: 800;
        letter-spacing: -0.05em;
        line-height: 1.08;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.32);
    }

    .developer-role {
        position: relative;
        z-index: 1;
        margin: 0.65rem 0 0;
        color: #a5f3fc;
        font-size: clamp(1rem, 2vw, 1.2rem);
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    .cui-campus {
        position: relative;
        z-index: 1;
        display: inline-block;
        margin-top: 1rem;
        padding: 0.8rem 1.15rem;
        border: 1px solid rgba(250, 204, 21, 0.60);
        border-radius: 13px;
        background: rgba(250, 204, 21, 0.15);
        color: #fef3c7;
        font-size: clamp(1rem, 2vw, 1.22rem);
        font-weight: 800;
        line-height: 1.45;
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.18);
    }

    .developer-note {
        position: relative;
        z-index: 1;
        max-width: 780px;
        margin: 1rem auto 0;
        color: rgba(255, 255, 255, 0.90);
        font-size: 0.92rem;
        line-height: 1.65;
    }

    .developer-spotlight:hover {
        transform: translateY(-2px);
        border-color: #67e8f9;
        box-shadow:
            0 25px 56px rgba(0, 0, 0, 0.42),
            0 0 28px rgba(34, 211, 238, 0.18);
        transition: all 0.25s ease;
    }

    .footer {
        margin-top: 1rem;
        color: #94a3b8;
        font-size: 0.78rem;
        text-align: center;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stRadio label,
    .stCheckbox label {
        color: #dbeafe !important;
        font-weight: 700 !important;
    }

    .stTextInput input,
    .stNumberInput input {
        color: #f8fafc !important;
        background: #081525 !important;
        border: 1px solid #3b5b7f !important;
        border-radius: 10px !important;
        font-family: "JetBrains Mono", monospace !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.18) !important;
    }

    .stSelectbox > div[data-baseweb="select"] > div {
        min-height: 43px !important;
        background: #081525 !important;
        border: 1px solid #3b5b7f !important;
        border-radius: 10px !important;
    }

    .stSelectbox div[data-baseweb="select"] * {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background: #0d1b2e !important;
        color: #f8fafc !important;
    }

    div[data-baseweb="popover"] li:hover {
        background: #153454 !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        min-height: 43px;
        border: 1px solid #3b6b8e !important;
        border-radius: 11px !important;
        background: #122943 !important;
        color: #eff6ff !important;
        font-weight: 800 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: var(--cyan) !important;
        background: #164567 !important;
        color: white !important;
    }

    .primary-button .stButton > button {
        border: none !important;
        background: linear-gradient(135deg, #06b6d4, #2563eb) !important;
        box-shadow: 0 8px 22px rgba(37, 99, 235, 0.28);
    }

    .shift-button .stButton > button {
        border: 1px solid rgba(250, 204, 21, 0.75) !important;
        background: linear-gradient(135deg, #b45309, #f59e0b) !important;
        color: #fffbeb !important;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.22);
    }

    .danger-button .stButton > button {
        border-color: rgba(251, 113, 133, 0.55) !important;
        color: #fecdd3 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.3rem;
        background: #081525;
        border-radius: 12px;
        padding: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        color: #9fb4cc !important;
        font-weight: 700 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #67e8f9 !important;
        background: #153454 !important;
        border-radius: 9px;
    }

    .stAlert {
        border-radius: 11px !important;
    }

    .stCaption {
        color: #9fb4cc !important;
    }

    @media (max-width: 760px) {
        .block-container {
            padding: 0.75rem 0.55rem 2rem;
        }

        .app-shell {
            padding: 0.75rem;
            border-radius: 20px;
        }

        .hero {
            padding: 1.2rem 0.8rem;
        }

        .developer-spotlight {
            padding: 1.5rem 0.9rem;
        }

        .cui-campus {
            width: 100%;
            box-sizing: border-box;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================
DEFAULT_STATE = {
    "history": [],
    "result": None,
    "expression": "",
    "memory": 0.0,
    "angle_mode": "Degrees",
    "last_operation": "Addition (+)",
    "shift_mode": False,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# OPERATION LISTS AND SHIFT MAPPING
# ============================================================
NORMAL_OPERATIONS = [
    "Addition (+)",
    "Subtraction (-)",
    "Multiplication (×)",
    "Division (÷)",
    "Modulus (%)",
    "Power (xʸ)",
    "Square (x²)",
    "Cube (x³)",
    "Square Root (√x)",
    "Cube Root (∛x)",
    "Inverse (1/x)",
    "Absolute Value |x|",
    "Factorial (x!)",
    "Percentage (%)",
    "Natural Log (ln)",
    "Log Base 10 (log₁₀)",
    "Log Base 2 (log₂)",
    "Exponential (eˣ)",
    "Sine (sin)",
    "Cosine (cos)",
    "Tangent (tan)",
    "Cosecant (csc)",
    "Secant (sec)",
    "Cotangent (cot)",
    "Ceiling ⌈x⌉",
    "Floor ⌊x⌋",
    "Round",
]

SHIFT_OPERATION_MAP = {
    "Square (x²)": "Cube (x³)",
    "Cube (x³)": "Square (x²)",
    "Square Root (√x)": "Cube Root (∛x)",
    "Cube Root (∛x)": "Square Root (√x)",
    "Natural Log (ln)": "Log Base 10 (log₁₀)",
    "Log Base 10 (log₁₀)": "Log Base 2 (log₂)",
    "Log Base 2 (log₂)": "Natural Log (ln)",
    "Sine (sin)": "Cosine (cos)",
    "Cosine (cos)": "Tangent (tan)",
    "Tangent (tan)": "Cotangent (cot)",
    "Cosecant (csc)": "Sine (sin)",
    "Secant (sec)": "Cosine (cos)",
    "Cotangent (cot)": "Sine (sin)",
    "Ceiling ⌈x⌉": "Floor ⌊x⌋",
    "Floor ⌊x⌋": "Ceiling ⌈x⌉",
}


# ============================================================
# SAFE EXPRESSION EVALUATION
# ============================================================
BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_eval_expression(expression):
    expression = expression.strip().replace("^", "**")

    if not expression:
        raise ValueError("Enter an expression first.")

    if len(expression) > 160:
        raise ValueError("Expression is too long.")

    allowed_characters = re.compile(r"^[0-9eE+\-*/%().\s]+$")

    if not allowed_characters.match(expression):
        raise ValueError(
            "Use only numbers, parentheses, +, -, *, /, %, or ^."
        )

    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return float(node.value)
            raise ValueError("Only numeric values are allowed.")

        if isinstance(node, ast.BinOp):
            operation = BINARY_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported arithmetic operation.")

            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)) and right == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")

            value = operation(left, right)

            if not math.isfinite(value) or abs(value) > 1e308:
                raise OverflowError("The result is too large.")

            return float(value)

        if isinstance(node, ast.UnaryOp):
            operation = UNARY_OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported unary operation.")

            return float(operation(evaluate(node.operand)))

        raise ValueError("Unsupported expression.")

    result = evaluate(tree)

    if not math.isfinite(result):
        raise ValueError("The result is not a finite number.")

    return result


# ============================================================
# CALCULATOR HELPERS
# ============================================================
def format_number(value, decimals=10):
    if value is None:
        return "—"

    value = float(value)

    if not math.isfinite(value):
        return "Undefined"

    if abs(value) >= 1e12 or (0 < abs(value) < 1e-8):
        return f"{value:.{decimals}e}"

    return f"{value:,.{decimals}f}".rstrip("0").rstrip(".")


def angle_value(value, angle_mode):
    if angle_mode == "Degrees":
        return math.radians(value)
    return value


def format_angle(value, angle_mode):
    if angle_mode == "Degrees":
        return f"{value}°"
    return f"{value} rad"


def get_effective_operation(selected_operation, shift_mode):
    if shift_mode:
        return SHIFT_OPERATION_MAP.get(selected_operation, selected_operation)
    return selected_operation


def calculate_operation(num1, num2, operation, angle_mode):
    angle = angle_value(num1, angle_mode)
    angle_text = format_angle(num1, angle_mode)

    if operation == "Addition (+)":
        return num1 + num2, f"{num1} + {num2}"

    if operation == "Subtraction (-)":
        return num1 - num2, f"{num1} − {num2}"

    if operation == "Multiplication (×)":
        return num1 * num2, f"{num1} × {num2}"

    if operation == "Division (÷)":
        if num2 == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return num1 / num2, f"{num1} ÷ {num2}"

    if operation == "Modulus (%)":
        if num2 == 0:
            raise ZeroDivisionError("Modulus by zero is not allowed.")
        return num1 % num2, f"{num1} % {num2}"

    if operation == "Power (xʸ)":
        return num1 ** num2, f"{num1}^{num2}"

    if operation == "Square (x²)":
        return num1 ** 2, f"{num1}²"

    if operation == "Cube (x³)":
        return num1 ** 3, f"{num1}³"

    if operation == "Square Root (√x)":
        if num1 < 0:
            raise ValueError("Square root requires a non-negative number.")
        return math.sqrt(num1), f"√{num1}"

    if operation == "Cube Root (∛x)":
        return float(np.cbrt(num1)), f"∛{num1}"

    if operation == "Inverse (1/x)":
        if num1 == 0:
            raise ZeroDivisionError("Zero has no multiplicative inverse.")
        return 1 / num1, f"1/{num1}"

    if operation == "Absolute Value |x|":
        return abs(num1), f"|{num1}|"

    if operation == "Factorial (x!)":
        if num1 < 0 or not float(num1).is_integer():
            raise ValueError("Factorial requires a non-negative integer.")
        if num1 > 170:
            raise ValueError("Factorial input must be 170 or less.")
        return math.factorial(int(num1)), f"{int(num1)}!"

    if operation == "Percentage (%)":
        return num1 / 100, f"{num1}%"

    if operation == "Natural Log (ln)":
        if num1 <= 0:
            raise ValueError("Natural logarithm requires a positive number.")
        return math.log(num1), f"ln({num1})"

    if operation == "Log Base 10 (log₁₀)":
        if num1 <= 0:
            raise ValueError("Logarithm requires a positive number.")
        return math.log10(num1), f"log₁₀({num1})"

    if operation == "Log Base 2 (log₂)":
        if num1 <= 0:
            raise ValueError("Logarithm requires a positive number.")
        return math.log2(num1), f"log₂({num1})"

    if operation == "Exponential (eˣ)":
        return math.exp(num1), f"e^{num1}"

    if operation == "Sine (sin)":
        return math.sin(angle), f"sin({angle_text})"

    if operation == "Cosine (cos)":
        return math.cos(angle), f"cos({angle_text})"

    if operation == "Tangent (tan)":
        cosine = math.cos(angle)

        if abs(cosine) < 1e-12:
            raise ValueError("Tangent is undefined at this angle.")

        return math.tan(angle), f"tan({angle_text})"

    if operation == "Cosecant (csc)":
        sine = math.sin(angle)

        if abs(sine) < 1e-12:
            raise ValueError("Cosecant is undefined when sine is zero.")

        return 1 / sine, f"csc({angle_text})"

    if operation == "Secant (sec)":
        cosine = math.cos(angle)

        if abs(cosine) < 1e-12:
            raise ValueError("Secant is undefined when cosine is zero.")

        return 1 / cosine, f"sec({angle_text})"

    if operation == "Cotangent (cot)":
        sine = math.sin(angle)

        if abs(sine) < 1e-12:
            raise ValueError("Cotangent is undefined when sine is zero.")

        return math.cos(angle) / sine, f"cot({angle_text})"

    if operation == "Ceiling ⌈x⌉":
        return math.ceil(num1), f"ceil({num1})"

    if operation == "Floor ⌊x⌋":
        return math.floor(num1), f"floor({num1})"

    if operation == "Round":
        return round(num1), f"round({num1})"

    raise ValueError("Please select a valid operation.")


def add_history(expression, result):
    timestamp = datetime.now().strftime("%H:%M:%S")

    st.session_state.history.append(
        {
            "time": timestamp,
            "expression": expression,
            "result": float(result),
        }
    )

    st.session_state.history = st.session_state.history[-50:]


def history_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Time", "Expression", "Result"])

    for item in st.session_state.history:
        writer.writerow(
            [
                item["time"],
                item["expression"],
                format_number(item["result"], 12),
            ]
        )

    return output.getvalue()


def clear_history_and_display():
    st.session_state.history = []
    st.session_state.result = None
    st.session_state.expression = ""


# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="app-shell">', unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <h1>🧮 NovaCalc</h1>
        <p>Scientific calculations with Shift Mode, memory, history, and built-in guidance</p>
    </div>
    """,
    unsafe_allow_html=True,
)

header_left, header_right = st.columns([4, 1])

with header_left:
    st.markdown(
        '<span class="status-pill">● Calculator ready</span>',
        unsafe_allow_html=True,
    )

    if st.session_state.shift_mode:
        st.markdown(
            '<span class="shift-active">⇧ SHIFT MODE ON</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="shift-inactive">⇧ Shift Mode OFF</span>',
            unsafe_allow_html=True,
        )

with header_right:
    if st.button("↻ Reset all", use_container_width=True):
        clear_history_and_display()
        st.session_state.memory = 0.0
        st.session_state.shift_mode = False
        st.session_state.last_operation = "Addition (+)"
        st.rerun()


# ============================================================
# MAIN LAYOUT
# ============================================================
left_column, right_column = st.columns([1.18, 0.82], gap="large")


# ============================================================
# LEFT SIDE: INPUTS AND OPERATIONS
# ============================================================
with left_column:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-title">⌨️ Quick expression</div>',
        unsafe_allow_html=True,
    )

    expression_input = st.text_input(
        "Type an arithmetic expression",
        placeholder="Examples: (25 + 5) * 3   |   2^8   |   100 / 4 + 7.5",
        help="Supported: numbers, parentheses, +, -, *, /, %, //, and ^ for power.",
        key="expression_input",
    )

    expression_col1, expression_col2 = st.columns([1.5, 1])

    with expression_col1:
        if st.button("⚡ Evaluate expression", use_container_width=True):
            try:
                expression_result = safe_eval_expression(expression_input)
                expression_display = expression_input.replace("**", "^")

                st.session_state.result = expression_result
                st.session_state.expression = expression_display
                add_history(expression_display, expression_result)

                st.success("Expression evaluated successfully.")

            except Exception as error:
                st.error(f"❌ {error}")

    with expression_col2:
        if st.button("Use memory value", use_container_width=True):
            st.session_state.expression_input = f"{st.session_state.memory:g}"
            st.rerun()

    st.markdown(
        '<div class="card-title" style="margin-top:1.3rem;">'
        '🎛️ Scientific operations</div>',
        unsafe_allow_html=True,
    )

    shift_col1, shift_col2 = st.columns([1, 2])

    with shift_col1:
        st.markdown('<div class="shift-button">', unsafe_allow_html=True)

        shift_button_text = (
            "⇧ SHIFT: ON"
            if st.session_state.shift_mode
            else "⇧ SHIFT: OFF"
        )

        if st.button(shift_button_text, use_container_width=True):
            st.session_state.shift_mode = not st.session_state.shift_mode
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with shift_col2:
        if st.session_state.shift_mode:
            selected_for_shift = st.session_state.last_operation
            shifted_operation = SHIFT_OPERATION_MAP.get(
                selected_for_shift,
                selected_for_shift,
            )

            st.markdown(
                f"""
                <div class="shift-map">
                    <strong>Shift is active.</strong><br>
                    Selected operation: <strong>{selected_for_shift}</strong><br>
                    Calculator will perform: <strong>{shifted_operation}</strong>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="shift-map">
                    <strong>How Shift works:</strong><br>
                    Turn it on to activate an alternate function. For example,
                    <strong>sin → cos</strong>, <strong>tan → cot</strong>,
                    <strong>x² → x³</strong>, and <strong>√x → ∛x</strong>.
                </div>
                """,
                unsafe_allow_html=True,
            )

    settings_col1, settings_col2 = st.columns(2)

    with settings_col1:
        angle_mode = st.radio(
            "Angle mode for sin, cos, tan, csc, sec, and cot",
            ["Degrees", "Radians"],
            horizontal=True,
            key="angle_mode_widget",
        )
        st.session_state.angle_mode = angle_mode

    with settings_col2:
        operation_index = 0

        if st.session_state.last_operation in NORMAL_OPERATIONS:
            operation_index = NORMAL_OPERATIONS.index(
                st.session_state.last_operation
            )

        selected_operation = st.selectbox(
            "Choose operation",
            NORMAL_OPERATIONS,
            index=operation_index,
            key="operation_widget",
        )

        st.session_state.last_operation = selected_operation

    effective_operation = get_effective_operation(
        selected_operation,
        st.session_state.shift_mode,
    )

    if st.session_state.shift_mode and effective_operation != selected_operation:
        st.info(
            f"⇧ Shift Mode changes **{selected_operation}** into "
            f"**{effective_operation}**."
        )

    number_col1, number_col2 = st.columns(2)

    with number_col1:
        num1 = st.number_input(
            "First number",
            value=0.0,
            step=0.1,
            format="%.8f",
            key="first_number",
        )

    with number_col2:
        num2 = st.number_input(
            "Second number",
            value=0.0,
            step=0.1,
            format="%.8f",
            key="second_number",
        )

    st.caption(
        "For one-number functions such as sin, √x, factorial, or log, "
        "only the first number is used."
    )

    st.markdown('<div class="primary-button">', unsafe_allow_html=True)

    if st.button("🚀 Calculate", use_container_width=True):
        try:
            result, expression = calculate_operation(
                num1=num1,
                num2=num2,
                operation=effective_operation,
                angle_mode=angle_mode,
            )

            if not math.isfinite(float(result)):
                raise ValueError("The result is not a finite number.")

            display_expression = expression

            if st.session_state.shift_mode and effective_operation != selected_operation:
                display_expression = (
                    f"SHIFT [{selected_operation} → {effective_operation}] : "
                    f"{expression}"
                )

            st.session_state.result = float(result)
            st.session_state.expression = display_expression
            add_history(display_expression, float(result))

            st.success("Calculation completed successfully.")

        except Exception as error:
            st.error(f"❌ {error}")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # MEMORY CARD
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">🧠 Calculator memory</div>',
        unsafe_allow_html=True,
    )

    memory_col1, memory_col2, memory_col3, memory_col4 = st.columns(4)

    with memory_col1:
        if st.button("MC", help="Memory Clear", use_container_width=True):
            st.session_state.memory = 0.0
            st.toast("Memory cleared.")

    with memory_col2:
        if st.button("MR", help="Memory Recall", use_container_width=True):
            st.session_state.result = st.session_state.memory
            st.session_state.expression = "Memory recall (MR)"
            st.toast("Memory recalled to display.")

    with memory_col3:
        if st.button("M+", help="Add current result to memory", use_container_width=True):
            if st.session_state.result is None:
                st.warning("Calculate a result first.")
            else:
                st.session_state.memory += st.session_state.result
                st.toast("Current result added to memory.")

    with memory_col4:
        if st.button("M−", help="Subtract current result from memory", use_container_width=True):
            if st.session_state.result is None:
                st.warning("Calculate a result first.")
            else:
                st.session_state.memory -= st.session_state.result
                st.toast("Current result subtracted from memory.")

    st.markdown(
        f"""
        <div class="metric-box" style="margin-top:0.8rem;">
            <div class="metric-label">Stored memory value</div>
            <div class="metric-value">{format_number(st.session_state.memory)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# RIGHT SIDE: DISPLAY AND QUICK TOOLS
# ============================================================
with right_column:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">📟 Calculator display</div>',
        unsafe_allow_html=True,
    )

    current_expression = st.session_state.expression or "No calculation yet"
    current_result = st.session_state.result

    st.markdown(
        f"""
        <div class="display-card">
            <div class="display-label">Expression</div>
            <div class="display-expression">{current_expression}</div>
            <div class="display-label" style="margin-top:1rem;">Result</div>
            <div class="display-result">{format_number(current_result, 12)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.markdown(
            f"""
            <div class="metric-box" style="margin-top:0.8rem;">
                <div class="metric-label">Angle mode</div>
                <div class="metric-value">{angle_mode}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_col2:
        shift_label = "ON" if st.session_state.shift_mode else "OFF"

        st.markdown(
            f"""
            <div class="metric-box" style="margin-top:0.8rem;">
                <div class="metric-label">Shift mode</div>
                <div class="metric-value">{shift_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="card-title">📚 Constants and tools</div>',
        unsafe_allow_html=True,
    )

    constant_col1, constant_col2 = st.columns(2)

    with constant_col1:
        if st.button("π Insert Pi", use_container_width=True):
            st.session_state.expression_input = "3.141592653589793"
            st.rerun()

        if st.button("e Insert Euler number", use_container_width=True):
            st.session_state.expression_input = "2.718281828459045"
            st.rerun()

    with constant_col2:
        if st.button("φ Insert golden ratio", use_container_width=True):
            st.session_state.expression_input = "1.618033988749895"
            st.rerun()

        if st.button("Clear display", use_container_width=True):
            st.session_state.result = None
            st.session_state.expression = ""
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# CALCULATION HISTORY
# ============================================================
st.markdown('<div class="card">', unsafe_allow_html=True)

history_title_col, history_action_col = st.columns([3, 1])

with history_title_col:
    st.markdown(
        '<div class="card-title">🕘 Calculation history</div>',
        unsafe_allow_html=True,
    )

with history_action_col:
    if st.session_state.history:
        st.download_button(
            "⬇️ Download CSV",
            data=history_csv(),
            file_name="novacalc_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

if not st.session_state.history:
    st.caption(
        "No calculations yet. Your latest calculations will appear here."
    )
else:
    for item in reversed(st.session_state.history[-15:]):
        st.markdown(
            f"""
            <div class="history-row">
                <span style="color:#7dd3fc;">{item["time"]}</span>
                &nbsp;|&nbsp; {item["expression"]}
                &nbsp;=&nbsp; <strong>{format_number(item["result"], 12)}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="danger-button">', unsafe_allow_html=True)

    if st.button("🗑️ Clear calculation history", use_container_width=True):
        clear_history_and_display()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# HELP CENTER
# ============================================================
help_tab, shift_tab = st.tabs(
    ["📘 Complete Help", "⇧ Shift Mode Guide"]
)

with help_tab:
    st.markdown("## How to use NovaCalc")

    st.markdown(
        """
        <div class="help-box">
            <strong>1. Quick Expression</strong><br>
            Type a complete expression using numbers, parentheses, and operators:
            <strong>+</strong>, <strong>-</strong>, <strong>*</strong>,
            <strong>/</strong>, <strong>%</strong>, and <strong>^</strong>.<br><br>
            Examples: <code>(25 + 5) * 3</code>,
            <code>2^8</code>, <code>(100 / 4) + 7.5</code>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="help-box">
            <strong>2. Scientific Operations</strong><br>
            Choose an operation, enter the first number, and click
            <strong>Calculate</strong>. Two-number operations include addition,
            subtraction, multiplication, division, modulus, and power. One-number
            operations include roots, factorial, trigonometry, and logarithms.
        </div>
        """,
        unsafe_allow_html=True,
    )

    help_col1, help_col2 = st.columns(2)

    with help_col1:
        st.markdown(
            """
            <div class="help-box">
                <strong>3. Basic operations</strong><br>
                • Addition: <code>5 + 3 = 8</code><br>
                • Subtraction: <code>5 - 3 = 2</code><br>
                • Multiplication: <code>5 × 3 = 15</code><br>
                • Division: <code>10 ÷ 2 = 5</code><br>
                • Modulus: <code>10 % 3 = 1</code><br>
                • Power: <code>2^5 = 32</code>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="help-box">
                <strong>4. Roots, powers, and logs</strong><br>
                • Square: <code>5² = 25</code><br>
                • Cube: <code>3³ = 27</code><br>
                • Square root: <code>√81 = 9</code><br>
                • Cube root: <code>∛27 = 3</code><br>
                • Inverse: <code>1/4 = 0.25</code><br>
                • ln, log₁₀, and log₂ require positive numbers.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with help_col2:
        st.markdown(
            """
            <div class="help-box">
                <strong>5. Angle mode</strong><br>
                Angle mode applies to sin, cos, tan, csc, sec, and cot.<br><br>
                Use <strong>Degrees</strong> for normal geometry:
                <code>sin(30°) = 0.5</code>.<br><br>
                Use <strong>Radians</strong> for calculus, physics, and programming:
                <code>sin(1.570796...) = 1</code>.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="help-box">
                <strong>6. Memory buttons</strong><br>
                • <strong>MC</strong>: Clear memory<br>
                • <strong>MR</strong>: Recall memory<br>
                • <strong>M+</strong>: Add result to memory<br>
                • <strong>M−</strong>: Subtract result from memory<br><br>
                Example: calculate <code>10 + 5</code>, then click M+ to store 15.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="help-box">
            <strong>7. Constants and history</strong><br>
            Use π, e, or φ to insert standard mathematical constants into the
            expression input. Every successful calculation is saved in History.
            Download your session history as CSV when needed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="help-box">
            <strong>8. Safety checks</strong><br>
            The calculator prevents division by zero, invalid logarithms, negative
            square roots, invalid factorials, and undefined trig values.
        </div>
        """,
        unsafe_allow_html=True,
    )

with shift_tab:
    st.markdown("## ⇧ How Shift Mode works")

    st.markdown(
        """
        <div class="help-box">
            <strong>Shift Mode activates alternate functions.</strong><br>
            Select a normal function first. Turn on Shift Mode, confirm the
            alternate operation shown by the calculator, then click Calculate.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="help-box">
            <strong>Trigonometric Shift functions</strong><br>
            • sin → cos<br>
            • cos → tan<br>
            • tan → cot<br><br>
            Reciprocal trig functions:<br>
            • <code>csc(x) = 1 / sin(x)</code><br>
            • <code>sec(x) = 1 / cos(x)</code><br>
            • <code>cot(x) = 1 / tan(x)</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="help-box">
            <strong>Other Shift mappings</strong><br>
            • x² → x³ &nbsp; • √x → ∛x<br>
            • ln → log₁₀ &nbsp; • log₁₀ → log₂<br>
            • ceil → floor &nbsp; • floor → ceil
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Example: choose Sine (sin), enter 30, use Degrees, enable Shift, "
        "then click Calculate. NovaCalc will calculate cos(30°)."
    )


# ============================================================
# NEW: PROMINENT DEVELOPER SECTION AT END OF FIRST PAGE
# ============================================================
st.markdown(
    """
    <div class="developer-spotlight">
        <div class="developer-badge">Developed By</div>
        <h2 class="developer-name">Nisar Ahmad</h2>
        <div class="developer-role">AI/ML Developer • BS Computer Science Student</div>
        <div class="cui-campus">
            🎓 COMSATS University Islamabad<br>
            Sahiwal Campus
        </div>
        <p class="developer-note">
            Building practical AI-powered applications, modern web tools,
            and interactive software solutions with Python and Streamlit.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        Built with Python and Streamlit • NovaCalc by Nisar Ahmad
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
