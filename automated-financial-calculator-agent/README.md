# Automated Financial Calculator Agent

A **Streamlit-based agentic financial calculator** that converts natural-language financial questions into structured tool calls and executes the calculations using deterministic Python functions.

The application follows a simple **agent/router architecture**:

> **Natural-language query → Router → Calculator Tool → Validated Result**

The LLM, when configured, is responsible only for **selecting the appropriate tool and extracting its arguments**. It does **not** perform the financial arithmetic. All calculations are executed by deterministic Python functions with input sanitization and validation.

This separation makes the system easier to test, audit, and reason about.

---

## Live Demo

**Try the deployed application:**

[Automated Financial Calculator Agent](https://automated-financial-calculator-agent.streamlit.app/)

---

## Features

- **Loan EMI Calculator**
  - Calculates monthly loan payments from principal, interest rate, and tenure.

- **SIP / Recurring Investment Calculator**
  - Estimates the future value of periodic investments.

- **Simple Interest**
  - Calculates interest and maturity value using the simple-interest formula.

- **Compound Interest**
  - Calculates accumulated value with periodic compounding.

- **CAGR Calculator**
  - Calculates the compound annual growth rate between two values.

- **NPV Calculator**
  - Calculates Net Present Value for a series of cash flows.

- **IRR Calculator**
  - Calculates the Internal Rate of Return for a series of cash flows.

- **ROI Calculator**
  - Calculates return on investment from initial and final values.

- **Safe Arithmetic Evaluation**
  - Supports controlled mathematical expressions without using unsafe arbitrary code execution.

- **Input Sanitization & Validation**
  - Validates and sanitizes user inputs before calculations are executed.

- **Dual Routing Modes**
  - **Rule-based routing** works without an LLM or API key.
  - **Gemini-powered routing** can optionally be enabled for natural-language tool selection.

- **Audit-Friendly Architecture**
  - The application keeps routing, validation, and calculation responsibilities separate.

---

## Example Queries

The application supports natural-language financial queries such as:

```text
EMI for 500000 at 8.5% for 20 years
```

```text
SIP 10000 at 12% for 15 years
```

```text
CAGR from 100000 to 250000 in 6 years
```

```text
IRR of -1000, 300, 400, 500
```

```text
1200 * 1.08^3
```

The router identifies the appropriate calculator and extracts the required parameters before execution.

---

## Architecture

```text
                    User Query
                        │
                        ▼
              ┌───────────────────┐
              │   Streamlit UI    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │      Router       │
              │                   │
              │ Rule-based / LLM  │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Input Sanitizer   │
              │ & Validator       │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Calculator Tools  │
              │                   │
              │ EMI / SIP / CAGR  │
              │ NPV / IRR / ROI   │
              │ Interest / Math   │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Validated Result  │
              │ + Audit Details   │
              └───────────────────┘
```

### LLM Responsibility

When Gemini is enabled, the LLM acts as a **tool router**, not as the calculator.

For example:

```text
User:
"Calculate EMI for a 500000 loan at 8.5% for 20 years"

        ↓

LLM / Router:
tool = calculate_emi
principal = 500000
rate = 8.5
years = 20

        ↓

Python Calculator:
calculate_emi(500000, 8.5, 20)

        ↓

Validated Financial Result
```

This architecture prevents the language model from being responsible for numerical computation.

---

## Why This Architecture?

Financial calculations require predictable and reproducible results.

Instead of asking an LLM to calculate:

```text
LLM → Understand → Calculate → Return Answer
```

this project separates reasoning from execution:

```text
LLM → Select Tool + Arguments
                  ↓
           Python Tool
                  ↓
        Deterministic Result
```

### Benefits

- **Deterministic calculations**
- **Reduced arithmetic errors**
- **Easier unit testing**
- **Clear separation of concerns**
- **Improved input validation**
- **More explainable execution**
- **Offline functionality without an LLM**
- **Easier extension with additional financial tools**

---

## Project Structure

```text
automated-financial-calculator-agent/
│
├── app.py
├── router.py
├── tools.py
├── sanitizer.py
├── test.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### Core Files

| File               | Responsibility                                         |
| ------------------ | ------------------------------------------------------ |
| `app.py`           | Streamlit application and user interface               |
| `router.py`        | Query routing, tool selection, and validation pipeline |
| `tools.py`         | Deterministic financial calculators and tool registry  |
| `sanitizer.py`     | Input sanitization and safe arithmetic evaluation      |
| `test.py`          | Tests for routing, calculations, and invalid inputs    |
| `requirements.txt` | Python dependencies                                    |

---

## Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini API** — optional LLM-based routing
- **Pydantic / validation utilities** — input validation where applicable
- **Pytest** — automated testing
- **dotenv** — environment variable management

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd automated-financial-calculator-agent
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini — Optional

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

The Gemini integration is optional.

If `GOOGLE_API_KEY` is not configured, the application automatically falls back to the deterministic rule-based router.

**Never commit your `.env` file or API keys to Git.**

---

## Run Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, typically:

```text
http://localhost:8501
```

Open the URL in your browser to use the application.

---

## Testing

Run the test suite with:

```bash
pytest -q
```

The tests cover areas such as:

- Calculator correctness
- Query routing
- Tool selection
- Arithmetic evaluation
- Input validation
- Invalid-input handling
- Safety-related edge cases

---

## Design Principles

### 1. LLM as a Router, Not a Calculator

The LLM should determine **what needs to be calculated**, while deterministic Python code determines **the numerical result**.

### 2. Deterministic Tool Execution

Each financial operation is implemented as a dedicated Python function.

This makes individual calculations independently testable.

### 3. Input Validation

User-provided values are sanitized and validated before being passed to calculator functions.

### 4. Safe Expression Evaluation

Arithmetic expressions are evaluated through a controlled mechanism rather than arbitrary Python execution.

### 5. Graceful Degradation

The application does not depend entirely on an external LLM.

Without a Gemini API key:

```text
User Query
    ↓
Rule-Based Router
    ↓
Calculator
    ↓
Result
```

With Gemini configured:

```text
User Query
    ↓
Gemini Router
    ↓
Calculator
    ↓
Result
```

---

## Example Execution Flow

For a query such as:

```text
Calculate CAGR from 100000 to 250000 over 6 years
```

the application follows this flow:

```text
1. Receive natural-language query
            ↓
2. Identify CAGR calculation
            ↓
3. Extract:
   - Initial value = 100000
   - Final value = 250000
   - Period = 6 years
            ↓
4. Validate inputs
            ↓
5. Execute deterministic CAGR function
            ↓
6. Return calculated result
            ↓
7. Display result and validated inputs
```

---

## Security Considerations

This project intentionally separates **language-model reasoning** from **code execution**.

Important safeguards include:

- API keys are loaded through environment variables.
- User inputs are sanitized before processing.
- Financial calculators operate on validated values.
- Arithmetic expressions use controlled evaluation.
- The LLM does not directly execute Python code.
- The LLM does not determine the final numerical result.

For production financial applications, additional controls such as authentication, authorization, rate limiting, logging, monitoring, and comprehensive financial-domain validation would be required.

---

## Limitations

This project is intended as an **agentic AI engineering demonstration**, not as a financial advisory system.

Results should not be treated as personalized financial advice.

The accuracy of a calculation depends on the assumptions and inputs supplied by the user. Real-world financial products may also involve taxes, fees, compounding conventions, payment schedules, and other factors that are not represented by simplified calculator formulas.

---

## Future Improvements

Potential extensions include:

- Add more financial calculators
- Introduce structured tool schemas
- Add conversational context and multi-turn queries
- Add calculation history
- Add downloadable calculation reports
- Add comprehensive unit and integration test coverage
- Add observability and execution tracing
- Add LangGraph-based workflow orchestration
- Add RAG for financial terminology and documentation
- Add authentication and user-specific calculation history
- Add configurable financial assumptions
- Add automated evaluation of router accuracy

---

## Learning Objectives

This project demonstrates several practical **agentic AI engineering patterns**:

- Tool calling
- Agent/router architecture
- Function-based tool execution
- LLM-to-tool parameter extraction
- Deterministic computation
- Input validation and sanitization
- Safe expression evaluation
- LLM fallback strategies
- Streamlit application development
- Automated testing

---

## Disclaimer

This application is an educational and engineering project.

It provides mathematical calculations based on user-provided inputs and should **not be considered financial, investment, tax, or legal advice**.

Always verify financial calculations and assumptions against appropriate professional or official sources before making financial decisions.

---

## License

This project is available for educational and demonstration purposes. Add the appropriate license here if the repository is distributed under a specific open-source license.

---

## Author

**Sheefa Naaz**

Frontend / Software Engineer | Agentic AI | LLM Integration | Multi-Agent Workflows

- GitHub: [github.com/sheefanaaz123](https://github.com/sheefanaaz123)
- LinkedIn: [linkedin.com/in/sheefa-naaz](https://linkedin.com/in/sheefa-naaz/)
- Portfolio: [sheefa-naaz.vercel.app](https://sheefa-naaz.vercel.app/)
