"""Deterministic vehicle price calculations adapted from the historical exercises."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Mapping, TextIO


# The source exercises use 100,000-toman increments and round ties downward.
PRICE_INCREMENT = 100_000
PRICE_TIERS = (
    (25_000_000, 1_000_000),
    (50_000_000, 2_000_000),
    (75_000_000, 3_000_000),
    (100_000_000, 4_000_000),
    (200_000_000, 5_000_000),
    (300_000_000, 7_000_000),
    (400_000_000, 10_000_000),
    (500_000_000, 15_000_000),
    (600_000_000, 20_000_000),
    (700_000_000, 25_000_000),
    (800_000_000, 30_000_000),
    (900_000_000, 35_000_000),
    (1_000_000_000, 40_000_000),
    (2_000_000_000, 50_000_000),
    (3_600_000_000, 100_000_000),
    (4_000_000_000, 150_000_000),
    (float("inf"), 200_000_000),
)


def round_price(value: float, increment: int = PRICE_INCREMENT) -> int:
    """Round nonnegative prices to the closest increment, resolving ties down."""
    if value < 0 or increment <= 0:
        raise ValueError("Price must be nonnegative and increment positive")
    quotient, remainder = divmod(int(value), increment)
    return (quotient + int(remainder > increment / 2)) * increment


def format_price(value: int) -> str:
    """Return a price with conventional thousands separators."""
    return f"{value:,}"


def price_bounds(base_price: int, listed_price: int, tiers=PRICE_TIERS) -> tuple[int, int]:
    """Return inclusive upper and lower offsets for a reference vehicle price."""
    if base_price <= 0 or listed_price < 0:
        raise ValueError("Base price must be positive and listed price nonnegative")
    for threshold, delta in tiers:
        if base_price <= threshold:
            return listed_price + delta, listed_price - delta
    raise ValueError("Price tiers must cover the requested base price")


def load_damage_coefficients(stream: TextIO) -> dict[int, float]:
    """Read the original two-row, dollar-delimited coefficient file."""
    rows = list(csv.reader(stream, delimiter="$"))
    if len(rows) != 2 or len(rows[0]) != len(rows[1]):
        raise ValueError("Coefficient file must have two equally sized rows")
    coefficients = {int(code): float(value) for code, value in zip(*rows)}
    if not coefficients or any(not 0 < factor <= 1 for factor in coefficients.values()):
        raise ValueError("Damage coefficients must be in (0, 1]")
    if len(coefficients) != len(rows[0]):
        raise ValueError("Duplicate damage codes are not allowed")
    return coefficients


def damage_adjusted_price(
    base_price: int,
    damage_codes: list[int],
    coefficients: Mapping[int, float],
) -> int:
    """Apply damage factors in order, preserving historic per-step rounding."""
    if base_price < 0:
        raise ValueError("Base price must be nonnegative")
    result = base_price
    for code in damage_codes:
        factor = coefficients[code]
        if not 0 < factor <= 1:
            raise ValueError(f"Invalid coefficient for damage code {code}")
        result = round_price(result * factor)
    return result


@dataclass(frozen=True)
class MileageRule:
    """Mileage-based adjustment parameters for a single vehicle model year."""

    low_multiplier: float
    minimum_km: int
    reference_km: int
    maximum_km: int
    high_multiplier: float

    def __post_init__(self) -> None:
        if not (0 <= self.minimum_km < self.reference_km < self.maximum_km):
            raise ValueError("Mileage limits must be strictly ordered")
        if self.low_multiplier < 1 or not 0 <= self.high_multiplier <= 1:
            raise ValueError("Mileage multipliers are outside their expected ranges")


def mileage_adjusted_price(
    year: int,
    base_price: int,
    kilometres: int,
    rules: Mapping[int, MileageRule],
) -> int:
    """Apply historic linear mileage adjustment rules supplied by the caller."""
    if base_price < 0 or kilometres < 0:
        raise ValueError("Price and kilometres must be nonnegative")
    rule = rules[year]
    if kilometres > rule.reference_km:
        available_loss = (1 - rule.high_multiplier) * base_price
        loss = (kilometres - rule.reference_km) * available_loss / (
            rule.maximum_km - rule.reference_km
        )
        adjusted = base_price - loss
    elif kilometres < rule.reference_km:
        available_bonus = (rule.low_multiplier - 1) * base_price
        bonus = (rule.reference_km - kilometres) * available_bonus / (
            rule.reference_km - rule.minimum_km
        )
        adjusted = base_price + bonus
    else:
        adjusted = base_price
    if adjusted < 0:
        raise ValueError("Mileage extrapolation produced a negative price")
    return round_price(int(adjusted))
