import requests
import pandas as pd

API_KEY = "mP3Hn71jql2qu1Dmzrhhr2nXAoq5fqgL4vfYnVFJ"
WALLETS = [
    "0xfaa0768bde629806739c3a4620656c5d26f44ef2",
    "0x742d35cc6634c0532925a3b844bc454e4438f44e",
    "0xfe9e8709d3215310075d67e3ed32a380ccf451c8",
    "0x281055afc982d96fab65b3a49cac8b878184cb16",
    "0x53d284357ec70ce289d6d64134dfac8e511c8a3d"
]

def fetch_compound_data(wallet):
    url = f"https://api.expand.network/v1/defi/compound/user-positions?protocol=compound_v2&wallet_address={wallet}&chain_id=1"
    headers = {"x-api-key": API_KEY}
    r = requests.get(url, headers=headers)
    data = r.json().get("data", {})
    return {
        "wallet_id": wallet,
        "total_supplied": float(data.get("totalSuppliedUSD", 0)),
        "total_borrowed": float(data.get("totalBorrowedUSD", 0)),
        "health_factor": float(data.get("healthFactor", 1))
    }

def min_max(col):
    return (col - col.min()) / (col.max() - col.min())

records = [fetch_compound_data(wallet) for wallet in WALLETS]
df = pd.DataFrame(records)
df["net_worth"] = df["total_supplied"] - df["total_borrowed"]
df["borrow_to_supply_ratio"] = df["total_borrowed"] / df["total_supplied"].replace(0, 1)

df["score_health"] = min_max(df["health_factor"])
df["score_net_worth"] = min_max(df["net_worth"])
df["score_ratio"] = 1 - min_max(df["borrow_to_supply_ratio"])

df["score"] = 1000 * (
    0.4 * df["score_health"] +
    0.3 * df["score_net_worth"] +
    0.3 * df["score_ratio"]
)
df["score"] = df["score"].round(0).astype(int)
df[["wallet_id", "score"]].to_csv("wallet_scores.csv", index=False)