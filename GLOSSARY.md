# Glossary of Forensic Monetization Terms

This document defines the technical and behavioral metrics used in the F2P Forensic Toolset.

## Distributional Metrics

### Conditional Tail Expectation (CTE₉₅)
The average cost for the unluckiest 5% of players. While the "Median" tells you what happens to the average person, CTE₉₅ tells you the severity of the financial "crash" for those who hit the tail end of the probability curve.

### Whale Revenue Ratio (WRR)
Calculated as `CTE₉₅ / Median`. This metric quantifies a system's reliance on extreme outliers for revenue. A high WRR (e.g., > 4.0) indicates a "predatory tail" where a small percentage of players pay significantly more than the average.

### Safety Net Tax (SNT)
The premium players pay for the existence of "Pity" systems. Pity systems reduce variance (making the cost more predictable) but often raise the median cost for all players. SNT quantifies this tradeoff.

### Confidence Budget (95%)
The amount of currency a player must have to be 95% certain of acquiring an item. This is the "true" sticker price of an item, as opposed to the misleading "average cost" often cited by developers.

## Behavioral & Friction Metrics

### Loss Aversion Index (LAI)
Quantifies the psychological pressure of "Sunk Cost." As a player collects shards (e.g., 8 out of 10), the perceived value of the next pull increases non-linearly because stopping would mean forfeiting all previous progress.

### Top-Up Pressure Index
Measures the "Residual Utility" trap. It calculates the minimum additional spend required to bring a currency balance to zero when the leftover amount is slightly less than the cheapest available item.

### Currency Obfuscation Multiplier (COM)
The number of exchange steps between real-world currency (USD) and the final item. Each step (USD -> Gems -> Tokens -> Shards) increases cognitive load and makes it harder for the human brain to track actual spending.

### Utility Decay (Power Creep)
The rate at which an item loses its meta-relevance. If an item costs $500 but is only relevant for 100 days before a stronger item is released, its "Cost Per Day of Relevance" is $5.00.

## Integrity Metrics

### Chi-Squared Goodness-of-Fit
A statistical test used to compare observed community data (e.g., 10,000 pulls from YouTube) against the game's published rates. A significant discrepancy suggests a "Silent Nerf" or misleading odds.

### Purchasing Power Parity (PPP) Adjustment
Adjusts labor-cost metrics to reflect local economic realities. $10 USD represents significantly more "economic pain" in India than in the USA, even if the digital price is identical.
