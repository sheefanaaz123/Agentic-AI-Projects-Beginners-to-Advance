"""Deterministic financial calculators. The LLM never performs arithmetic: it only
selects a tool and arguments. All numbers come from these pure functions."""
from __future__ import annotations

import math
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, Callable

from pydantic import BaseModel, Field

from sanitizer import safe_eval


def _r(x: float, nd: int = 2) -> float:
    if not math.isfinite(x):
        raise ValueError("Result is not finite.")
    return float(Decimal(repr(x)).quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


# ---------- Schemas (strict bounds = validation layer) ----------
class SimpleInterestIn(BaseModel):
    principal: float = Field(gt=0, le=1e12, description="Principal amount")
    annual_rate_pct: float = Field(ge=0, le=100, description="Annual interest rate in percent")
    years: float = Field(gt=0, le=100, description="Duration in years")


class CompoundInterestIn(SimpleInterestIn):
    compounds_per_year: int = Field(default=12, ge=1, le=365, description="Compounding frequency per year")


class LoanEmiIn(BaseModel):
    principal: float = Field(gt=0, le=1e12, description="Loan amount")
    annual_rate_pct: float = Field(ge=0, le=100, description="Annual interest rate in percent")
    years: float = Field(gt=0, le=60, description="Loan tenure in years")


class SipIn(BaseModel):
    monthly_investment: float = Field(gt=0, le=1e9, description="Monthly SIP amount")
    annual_return_pct: float = Field(ge=0, le=100, description="Expected annual return in percent")
    years: float = Field(gt=0, le=80, description="Investment horizon in years")


class CagrIn(BaseModel):
    initial_value: float = Field(gt=0, le=1e15)
    final_value: float = Field(gt=0, le=1e15)
    years: float = Field(gt=0, le=200)


class NpvIn(BaseModel):
    discount_rate_pct: float = Field(gt=-100, le=1000, description="Discount rate in percent")
    cash_flows: list[float] = Field(min_length=2, max_length=100, description="Cash flows; index 0 is time 0")


class IrrIn(BaseModel):
    cash_flows: list[float] = Field(min_length=2, max_length=100, description="Cash flows; index 0 is time 0")


class RoiIn(BaseModel):
    cost: float = Field(gt=0, le=1e15)
    final_value: float = Field(ge=0, le=1e15)


class MathIn(BaseModel):
    expression: str = Field(min_length=1, max_length=200, description="Numeric expression using + - * / ** % //")


# ---------- Calculators ----------
def simple_interest(principal, annual_rate_pct, years):
    interest = principal * annual_rate_pct / 100 * years
    return {"interest": _r(interest), "total": _r(principal + interest),
            "formula": "I = P × r × t"}


def compound_interest(principal, annual_rate_pct, years, compounds_per_year=12):
    total = principal * (1 + annual_rate_pct / 100 / compounds_per_year) ** (compounds_per_year * years)
    return {"total": _r(total), "interest": _r(total - principal),
            "formula": "A = P(1 + r/n)^(nt)"}


def loan_emi(principal, annual_rate_pct, years):
    n = round(years * 12)
    if n < 1:
        raise ValueError("Tenure must be at least one month.")
    r = annual_rate_pct / 12 / 100
    emi = principal / n if r == 0 else principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    total = emi * n
    return {"emi": _r(emi), "months": n, "total_payment": _r(total),
            "total_interest": _r(total - principal),
            "formula": "EMI = P·r·(1+r)^n / ((1+r)^n − 1), r = annual rate / 12"}


def sip_future_value(monthly_investment, annual_return_pct, years):
    n = round(years * 12)
    i = annual_return_pct / 12 / 100
    fv = monthly_investment * n if i == 0 else monthly_investment * (((1 + i) ** n - 1) / i) * (1 + i)
    invested = monthly_investment * n
    return {"future_value": _r(fv), "total_invested": _r(invested), "estimated_gain": _r(fv - invested),
            "formula": "FV = P·[((1+i)^n − 1)/i]·(1+i), payments at start of month"}


def cagr(initial_value, final_value, years):
    rate = (final_value / initial_value) ** (1 / years) - 1
    return {"cagr_pct": _r(rate * 100, 4), "formula": "CAGR = (Final/Initial)^(1/years) − 1"}


def _npv(rate: float, flows: list[float]) -> float:
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))


def npv(discount_rate_pct, cash_flows):
    return {"npv": _r(_npv(discount_rate_pct / 100, cash_flows)),
            "formula": "NPV = Σ CF_t / (1 + r)^t"}


def irr(cash_flows):
    if not (any(c < 0 for c in cash_flows) and any(c > 0 for c in cash_flows)):
        raise ValueError("Cash flows need at least one negative and one positive value.")
    lo, hi = -0.999, 10.0
    f_lo, f_hi = _npv(lo, cash_flows), _npv(hi, cash_flows)
    if f_lo * f_hi > 0:
        raise ValueError("No IRR found in the range -99.9% to 1000%.")
    for _ in range(200):  # bisection: deterministic, no random starts
        mid = (lo + hi) / 2
        f_mid = _npv(mid, cash_flows)
        if abs(f_mid) < 1e-10:
            break
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return {"irr_pct": _r(mid * 100, 4), "formula": "Rate r where NPV(r) = 0 (bisection)"}


def roi(cost, final_value):
    return {"roi_pct": _r((final_value - cost) / cost * 100), "profit": _r(final_value - cost),
            "formula": "ROI = (Final − Cost) / Cost × 100"}


def safe_math(expression):
    return {"value": _r(safe_eval(expression), 6), "formula": "Arithmetic (AST-whitelisted)"}


# ---------- Registry ----------
@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    schema: type[BaseModel]
    func: Callable[..., dict]


REGISTRY: dict[str, ToolSpec] = {t.name: t for t in [
    ToolSpec("simple_interest", "Simple interest on a principal.", SimpleInterestIn, simple_interest),
    ToolSpec("compound_interest", "Compound interest / future value of a lump sum.", CompoundInterestIn, compound_interest),
    ToolSpec("loan_emi", "Monthly EMI, total payment and interest for a loan.", LoanEmiIn, loan_emi),
    ToolSpec("sip_future_value", "Future value of a monthly SIP / recurring investment.", SipIn, sip_future_value),
    ToolSpec("cagr", "Compound annual growth rate between two values.", CagrIn, cagr),
    ToolSpec("npv", "Net present value of cash flows at a discount rate.", NpvIn, npv),
    ToolSpec("irr", "Internal rate of return of cash flows.", IrrIn, irr),
    ToolSpec("roi", "Return on investment from cost and final value.", RoiIn, roi),
    ToolSpec("safe_math", "Plain arithmetic expression evaluation.", MathIn, safe_math),
]}


def run_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    """Validate arguments against the schema, then execute deterministically."""
    if name not in REGISTRY:
        raise KeyError(f"Unknown tool: {name}")
    spec = REGISTRY[name]
    validated = spec.schema(**args)  # raises pydantic.ValidationError on bad input
    result = spec.func(**validated.model_dump())
    return {"tool": name, "inputs": validated.model_dump(), "result": result}