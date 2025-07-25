# Wallet Risk Scoring - Compound V2

## 🧾 Data Collection
We used the Expand.Network API to query Compound V2 user positions. For each wallet, we fetched:
- Supplied amount (USD)
- Borrowed amount (USD)
- Health Factor

## 🧪 Feature Selection
We engineered the following risk features:
- `net_worth`: Supplied - Borrowed
- `borrow_to_supply_ratio`: Higher values imply higher risk
- `health_factor`: Lower than 1 means liquidation risk

## 📊 Scoring Method
Each wallet was scored using a weighted average of normalized features:

```
score = 1000 * (
    0.4 * health_factor_score +
    0.3 * net_worth_score +
    0.3 * (1 - borrow_to_supply_ratio)
)
```

Scores range from 0 (high risk) to 1000 (low risk).

## 📁 Files
- `wallet_scorer.py`: Python script for scoring
- `wallet_scores.csv`: Output CSV with scores