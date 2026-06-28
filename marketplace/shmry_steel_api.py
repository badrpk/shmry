def get_steel_prices():
    return {
        "Rebar": 650.00,
        "Hot Rolled Coil": 720.50,
        "Cold Rolled Sheet": 850.00,
    }

def get_rfq_response(query):
    q = (query or "").lower()
    prices = get_steel_prices()

    if any(x in q for x in ["steel", "price", "rate", "rebar", "coil", "sheet"]):
        lines = []
        for name, usd in prices.items():
            pkr = usd * 280
            lines.append(f"- {name}: PKR {pkr:,.0f}/ton approx")
        return "Current Steel Market Rates:\n" + "\n".join(lines)

    return "Steel RFQ received. Please share product, quantity, city, and delivery date."
