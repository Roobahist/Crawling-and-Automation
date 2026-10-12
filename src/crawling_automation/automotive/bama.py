"""Read-only Bama price-list extraction with separately testable parsing."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from typing import Mapping, TextIO

from bs4 import BeautifulSoup


@dataclass(frozen=True)
class VehiclePrice:
    english_brand: str
    persian_brand: str
    car_name: str
    year: str
    company: str
    price_toman: int
    change: str = ""
    dealership: bool = False


class PriceListFormatError(ValueError):
    """The fetched page does not contain the expected price-list structure."""


def parse_bama_prices(html: str, brands: Mapping[str, str] | None = None) -> list[VehiclePrice]:
    """Parse the historic Bama HTML structure without changing scraped values."""
    soup = BeautifulSoup(html, "html.parser")
    container = soup.select_one(".sefr-price-list")
    if container is None:
        raise PriceListFormatError("No .sefr-price-list element; the site layout may have changed")
    translations = brands or {}
    records = []
    for section in container.select("section"):
        brand_element = section.select_one(".price-list-brand-name a")
        if brand_element is None:
            raise PriceListFormatError("Brand header missing from a price section")
        persian_brand = brand_element.get_text(" ", strip=True).removeprefix("قیمت خودرو ").strip()
        for item in section.select("li"):
            name = item.select_one("span")
            year = item.select_one("small")
            price = item.select_one(".sefr-price")
            if name is None or year is None or price is None:
                raise PriceListFormatError(f"Missing car fields for {persian_brand}")
            price_text = price.get_text(" ", strip=True).replace(",", "").replace("٬", "")
            try:
                amount = int(price_text.split()[0])
            except (ValueError, IndexError) as exc:
                raise PriceListFormatError(f"Invalid listed price for {persian_brand}") from exc
            if amount < 0:
                raise PriceListFormatError("Listed prices cannot be negative")
            up = item.select_one(".sefr-updown.price-up")
            down = item.select_one(".sefr-updown.price-down")
            steady = item.select_one(".sefr-updown.zero")
            change = (
                "-" + down.get_text(" ", strip=True) if down else
                up.get_text(" ", strip=True) if up else
                steady.get_text(" ", strip=True) if steady else ""
            )
            company = item.select_one(".sefr-company")
            bazaar = item.select_one(".sefr-bazaar")
            records.append(VehiclePrice(
                english_brand=translations.get(persian_brand, ""),
                persian_brand=persian_brand,
                car_name=name.get_text(" ", strip=True),
                year=year.get_text(" ", strip=True),
                company=company.get_text(" ", strip=True).replace("،", "") if company else "",
                price_toman=amount,
                change=change,
                dealership=bool(bazaar and "نمایندگی" in bazaar.get_text()),
            ))
    return records


def collect_bama_prices(session, url: str, timeout: float, brands=None) -> list[VehiclePrice]:
    """Fetch a listing using an injected HTTP session, then parse it."""
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    return parse_bama_prices(response.text, brands=brands)


def write_prices(records: list[VehiclePrice], stream: TextIO) -> None:
    """Write records using the original dollar-delimited column contract."""
    writer = csv.writer(stream, delimiter="$", lineterminator="\n")
    writer.writerow(["Eng_Brand", "Per_Brand", "CarName", "Year", "Company",
                     "Updown", "Namayandegi", "Price"])
    for row in records:
        writer.writerow([
            row.english_brand, row.persian_brand, row.car_name, row.year,
            row.company, row.change, str(int(row.dealership)),
            f"{row.price_toman:,} تومان",
        ])
