from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import json
import urllib.request
import csv


ROOT = Path(__file__).resolve().parent
API = "https://wmsc.lcsc.com/ftps/wm/product/detail?productCode={}"


def tier_price(tiers, quantity):
    valid = [t for t in tiers if int(t.get("ladder", 0)) <= quantity]
    if not valid:
        return None
    tier = max(valid, key=lambda t: int(t["ladder"]))
    return float(tier.get("usdPrice") or tier.get("productPrice"))


def fetch(lcsc):
    request = urllib.request.Request(
        API.format(lcsc),
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response).get("result") or {}
    tiers = result.get("productPriceList") or []
    return lcsc, {
        "mpn": result.get("productModel"),
        "currency": "$",
        "qty_1_unit_usd": tier_price(tiers, 1),
        "qty_500_unit_usd": tier_price(tiers, 500),
        "price_tiers": tiers,
    }


def main():
    with (ROOT / "Piezo_Demo_7x7_BOM.csv").open(newline="", encoding="utf-8") as handle:
        lcsc_ids = [row["LCSC"] for row in csv.DictReader(handle)]
    prices = {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(fetch, lcsc): lcsc for lcsc in lcsc_ids}
        for future in as_completed(futures):
            lcsc = futures[future]
            try:
                _, data = future.result()
                prices[lcsc] = data
                print(lcsc, data["qty_1_unit_usd"], data["qty_500_unit_usd"])
            except Exception as exc:
                prices[lcsc] = {"error": str(exc)}
                print(lcsc, "ERROR", exc)

    payload = {
        "source": "LCSC live product detail API",
        "retrieved_utc": datetime.now(timezone.utc).isoformat(),
        "prices": dict(sorted(prices.items())),
    }
    (ROOT / "lcsc_prices.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
