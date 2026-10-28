# AAPL — WAIT @ 0% — 2026-09-15  |  目标价: 259 USD (5-year mean PE 29.73x)

> Excellent business, poor price: 38.2x earnings against a 4.78% risk-free rate. Wait for the multiple, not the business.

**Ticker:** AAPL (Apple Inc., Nasdaq) · **Price:** $333.08 (close 2026-09-14) · **Market cap:** $4.86T · **Currency:** USD
**Layer totals:** L0 🟢 UNDERSTOOD · M 🔴 RED (valuation) · L1 🟡 YELLOW · L2b 🟡 YELLOW · L2a 🔴 RED (margin of safety) · L3 → **WAIT, confidence low (0.35), position 0%**

---

## 1. Investment Thesis

**Apple is not in dispute. The price is.**

All four master lenses — Buffett, Duan Yongping, Munger and Li Lu — independently graded the *business* GREEN and the *margin of safety* RED, and all four returned **WAIT at 0%**. The convergence was not on a vague "it looks expensive" but on arithmetic all four derived separately: a buyer at $333.08 receives a 2.81% free-cash-flow yield while the 10-year Treasury pays 4.784% — a spread of **−197 basis points** (source: L2a定性/四大师共识; computed with `financial_rigor.py calc`).

**What the current price already reflects.** PE TTM is 38.21x, *above* the five-year fiscal-year-end maximum of 37.19x and 28.5% above the five-year mean of 29.73x (source: M层/valuation_history, 02-market.json). Price sits at the 96.9th percentile of its five-year range, 1.97% below the 52-week high (source: M层/price_data). The market has already priced in continued low-teens Services growth, a sustained ~50% gross margin, and no adverse antitrust remedy.

**Where this analysis is non-consensus.** Not about growth: 9M FY2026 revenue grew **+16.2%** and consolidated gross margin expanded 3.57 points to **50.06%** (source: M层/SEC 10-Q FY26Q3). The non-consensus point is the *durability of the profit pool*. The most profitable part of Services — the App Store commission plus the Google default-search payment — is under simultaneous legal attack from the US DOJ, the EU DMA, the UK CMA, Japan and Korea, and its size is **disclosed nowhere in Apple's filings** (source: L2a定性/芒格, 李录; L0 01-capability.md Q3). Nothing in any valuation figure in this report models that loss, which means **every number below is optimistic by an unknown amount**.

**Catalyst timing.** There is no catalyst that closes a gap *upward*, because there is no gap — the price is above its own historical range. The identified catalysts are all on the downside: FOMC decisions against a 10-year already at 4.784%, and antitrust remedy rulings.

**Verdict:** **WAIT @ 0%**, engine confidence **low (0.35)**, with four master-defined re-entry levels clustering at **$210–$262**. The decision is a real wait, not an evasion: the framework's own test — "would you add on a 30% drawdown?" — was answered **yes, conditionally**, and the condition was written down (see §9).

---

## 2. Business Overview

| Dimension | Content |
|:----------|:--------|
| **Revenue structure** | Two engines. Products **$307.003B** (73.8% of FY2025) — iPhone, Mac, iPad, Wearables/Home; Services **$109.158B** (26.2%) — App Store, iCloud, Music, AppleCare, Ads, Payments. 9M FY2026 Services ran **$91.728B vs $80.408B** (+14.1%). (来源: M层/SEC 10-K FY2025, 10-Q FY26Q3) |
| **Business model** | Sell premium hardware at a hardware gross margin, then monetize the resulting installed base at a software gross margin. Products segment cost of sales implies a ~36.8% product margin; Services cost of sales implies a ~75.4% services margin (source: 10-K FY2025 gross margin $195.201B on $416.161B; segment cost lines). Customers are primarily consumer, SMB, education, enterprise and government (来源: L0/SEC 10-K Item 1, "Markets and Distribution") |
| **Competitive position** | Not priced as a hardware maker. The comparable set that matters is the mega-cap platform group (Alphabet, Microsoft, Meta, Amazon), and Apple trades at the **top** of that band — PE 39.69x vs a peer median of 23.70x on the same snapshot date (来源: L2b量化/engine_raw.factor_analysis) |
| **Management** | **YELLOW** (2 GREEN / 2 YELLOW, split → conservative colour). Operating capital allocation is genuinely good — no empire-building M&A, share count down 14.77B → 14.59B, shareholders' equity rebuilding from $73.733B toward $107.520B, R&D +32.5%. The YELLOW is a *price* judgment, not a character judgment: FY2025 repurchases of $90.711B (123% of year-end book equity) show no visible price condition in the disclosed record, and the same dollars would have bought roughly 58% more shares at the five-year low multiple. (来源: L2a定性/管理层; 05-qualitative_lights.json) |

**Segment map (FY2025, geographic).** Americas $178.353B (+6.8%) · Europe $111.032B (+9.6%) · **Greater China $64.377B (−3.8%)** · Japan $28.703B (+14.6%) · Rest of Asia Pacific $33.696B (+9.9%). Greater China is the only shrinking region, at 15.5% of revenue. (来源: L0/SEC 10-K FY2025 segment note)

---

## 3. Industry & Competition

**Industry.** Consumer electronics plus digital services. Apple does not publish TAM/SAM/SOM, and no first-hand source for those figures was obtainable in this run (live search tooling failed — see the disclosure at the end of §11), so **no TAM number is asserted here**. What is asserted is the observable structure: a mature hardware market with lengthening upgrade cycles (source: 10-K Item 1A) monetized through a services layer whose growth comes from attaching more paid services to an installed base, not from unit volume.

**Competitive landscape.**

| Competitor | Advantage | Disadvantage | Threat level to AAPL |
|:-----------|:----------|:-------------|:---------------------|
| **Alphabet (Google)** | Android/Chrome distribution; pays Apple for default search | Depends on the same default-search arrangement it is being sued over | **Medium as a competitor, High as a counterparty** — the DOJ remedy that hurts Google also removes a rent stream from Apple (来源: L2a定性/芒格) |
| **Microsoft** | Enterprise/cloud; Copilot as an assistant-layer beachhead | No consumer handset position | **Medium** — the assistant-interface shift is the vector |
| **Samsung** | Handset scale and component vertical integration | Low-teens multiple; no comparable services attach | **Low** — not the binding constraint; the risk is an interface shift, not a handset (来源: L0/01-capability.md Q2) |
| **Meta** | Social graph, advertising scale, on-device AI ambitions | Hardware attempts have repeatedly failed | **Low-Medium** — competes for the same consumer attention, not the same OS position |
| **OpenAI / assistant-layer entrants** | Own the user's primary surface if the assistant replaces the OS | No hardware distribution at Apple's scale | **High, and unresolved** — this is the structural threat Apple names itself in the 10-K (来源: L0/01-capability.md Q3) |

**The structural point that shapes the whole risk matrix.** The two biggest threats — antitrust remedies on App Store/default-search economics and AI-assistant disintermediation of the interface layer — attack **the same profit pool**. They are correlated, not independent. That correlation is what makes the margin-of-safety question binding rather than academic.

---

## 4. Financial Analysis

| Metric | FY2023 | FY2024 | FY2025 | YoY (FY25) |
|:-------|-------:|-------:|-------:|-----------:|
| Revenue ($M) | 383,285 | 391,035 | 416,161 | **+6.4%** |
| Gross margin % | 44.13% | 46.21% | **46.91%** | +0.70pp |
| Operating margin % | 29.82% | 31.51% | **31.97%** | +0.46pp |
| Net income ($M) | 96,995 | 93,736 | **112,010** | **+19.5%** |
| Net margin % | 25.31% | 23.97% | 26.92% | +2.95pp |
| Diluted EPS ($) | 6.13 | 6.08 | **7.46** | +22.7% |
| ROE (net income ÷ year-end equity) | n/a | 164.6% | **151.9%** | — |
| Operating cash flow ($M) | 110,543 | 118,254 | 111,482 | −5.7% |
| Capex ($M) | 10,959 | 9,447 | 12,715 | +34.6% |
| Free cash flow ($M) | 99,584 | 108,807 | **98,767** | −9.2% |
| Revenue growth % | — | +2.02% | **+6.43%** | — |

*(来源: M层/SEC 10-K FY2025 accession 0000320193-25-000079, income statement and cash flow statement; all ratios computed by `financial_rigor.py calc`, not by hand.)*

**Reading the FY2024 net-income dip.** FY2024 net income ($93.736B) was *lower* than FY2023 ($96.995B) despite higher revenue, because the FY2024 tax provision was $29.749B versus $16.741B in FY2023 — the European Commission State Aid decision. The underlying operating trend never broke: operating income rose every year (114.301 → 123.216 → 133.050). (来源: M层/SEC 10-K income statement, "Provision for income taxes")

**Cash-flow quality.** TTM free cash flow / net income = **106.0%** — earnings are cash-backed. On a fiscal-year basis FY2025 FCF/NI = 88.2%, the gap being the working-capital swing and the step-up in cash taxes paid to **$43.369B** from $26.102B a year earlier, which is consistent with reported earnings rather than contradicting them. (来源: L2a定性/会计质量; M层/SEC 10-K cash flow statement)

**Balance sheet.** Total assets $359.241B; total liabilities $285.508B; shareholders' equity **$73.733B** at FY2025 year-end, rebuilding toward **$107.520B** by 2026-06-27 (10-Q FY26Q3). Term debt $78.328B non-current plus $12.350B current; commercial paper $7.979B. Equity is small **by construction** — $90.711B of FY2025 buybacks against $73.733B of closing equity — which is why every ROE figure for this company must be read as a capital-structure artifact, not a quality signal. (来源: M层/SEC 10-K balance sheet; L2b量化/ai_review)

**Dividends and buybacks.** FY2025: $15.421B dividends + $90.711B repurchases = **$106.132B returned, 94.75% of net income**. Dividend yield 0.32%; payout ratio 12.39%. (来源: M层/SEC 10-K cash flow statement; computed by `financial_rigor.py calc`)

**Recent-quarter acceleration.** Q3 FY2026 revenue $109.417B (+16.4% YoY), gross margin **50.06%** versus 46.49% a year earlier, 9M net income +20.0% ($101.460B vs $84.540B), R&D $34.035B for 9M (+32.5%). (来源: M层/SEC 10-Q FY26Q3)

---

## 5. Valuation

### 5.1 Tool verification (§ mandatory — no mental arithmetic)

| Check | Command | Result |
|:------|:--------|:-------|
| Market cap | `verify-market-cap --price 333.08 --shares 14.59e9 --reported 4.86e12` | computed 4.86T vs reported 4.86T, **deviation 0.01% — PASS** |
| Multiples | `verify-valuation --price 333.08 --eps 8.72 --bvps 7.37` | PE **38.20x**, earnings yield 2.62%, PB **45.19x** (BVPS $7.37 = equity $107.520B ÷ 14.59B shares; the M-layer's 45.26x uses a slightly different BVPS vintage — the two agree to 0.15%) |
| Cross-source | `cross-validate --field revenue --values {"SEC 10-K FY2025": 4161.61, "M-layer filings-derived": 4161.61} --unit 亿` | 0.00% deviation, **consistent** |
| Three scenarios | `three-scenario --price 333.08 --eps 8.72 --shares 145.9 --growth 0.10 0.07 0.04 --pe 36 29.73 24.17 --years 5` | see table below |

### 5.2 Relative valuation

| Metric | AAPL | Peer median (META/GOOGL/MSFT/AMZN/NFLX) | 5-year history | Percentile |
|:-------|-----:|----------------------------------------:|:---------------|:-----------|
| PE (TTM) | **38.21x** | 23.70x | 24.17x–37.19x (FY-end), mean 29.73x | **above the 5-year maximum** |
| Forward PE | **36.18x** | 20.14x | — | — |
| PB | **45.26x** | — | — | not meaningful (equity crushed by buybacks) |
| PS (TTM) | **10.41x** | — | — | — |
| EV/EBITDA | **28.57x** | — | — | — |
| PEG | **3.25** | — | — | — |
| FCF yield | **2.81%** | — | vs 10Y Treasury 4.784% | **−197bp spread** |

*(来源: M层/SEC filings + stockanalysis.com fetched 2026-09-15; peer medians from L2b量化/engine_raw factor_analysis; FCF yield and spread computed by `financial_rigor.py calc`.)*

**PE history, two independent computations agreeing within 1%.**

| Fiscal year end | Local DB price × FY EPS | stockanalysis.com |
|:----------------|------------------------:|------------------:|
| 2021-09-25 | 25.57x | 25.65x |
| 2022-09-24 | 24.17x | 24.22x |
| 2023-09-30 | 27.58x | 27.60x |
| 2024-09-28 | 37.19x | 36.95x |
| 2025-09-27 | 34.15x | 33.85x |

*(来源: M层/sources/aapl_pe_fy.json; https://stockanalysis.com/stocks/AAPL/financials/ratios/)*

### 5.3 Absolute valuation — three-scenario model (tool output, verbatim)

| Scenario | EPS growth | Exit PE | Target EPS | **Target price** | vs $333.08 |
|:---------|-----------:|--------:|-----------:|-----------------:|-----------:|
| Bull | 10% | 36x | $14.04 | **$505.60** | **+51.8%** |
| Base | 7% | 30x | $12.23 | **$363.60** | **+9.2%** |
| Bear | 4% | 24x | $10.61 | **$256.40** | **−23.0%** |

*(来源: `financial_rigor.py three-scenario`, 5-year horizon; exit PEs anchored on the historical band — 36x near the current forward multiple, 29.73x the 5-year mean, 24.17x the 5-year minimum.)*

**How to read that table — and why the base case is not a buy signal.** The base case (+9.2% over five years) is roughly **1.8% annualized**, below the 4.784% risk-free rate, for taking equity risk in a company facing unresolved antitrust and interface-shift threats. The model is also **structurally optimistic**: it assumes no antitrust remedy removes any commission revenue, because that revenue has never been separately disclosed and therefore cannot be subtracted. An unknown negative is not the same as zero.

**Independent corroboration from the panel.** Li Lu ran his own DCF and got **$212 conservative / $259 base / $344 optimistic** against a $333.08 price — his *optimistic* case is roughly break-even with today. Munger ran the arithmetic differently: hold a 9% required return, let FCF compound at 6.1%/yr for ten years, and the total return is about **6.4%**; let the multiple merely revert to its own five-year average and it is about **5.7%**. Three independent methods, one conclusion: the price is full. (来源: L2a定性/李录, 芒格; 05-qualitative_lights.json)

### 5.4 SOTP

Not applicable. Apple does not disclose the profit pools that would make a sum-of-the-parts possible (the default-search payment is the clearest example), and its segments share one product line and one cost base. Any SOTP built here would be fabrication.

### 5.5 Target price and margin of safety

- **Target price: $259** — the five-year mean multiple (29.73x) applied to TTM EPS of $8.72 ($259.25, computed by `financial_rigor.py calc`). This is Duan Yongping's re-entry band.
- **Downside anchor: $240.50** — the five-year *median* multiple (27.58x) on the same EPS, which is Munger's 10–15% position trigger.
- **Master re-entry levels, derived independently:** Buffett **$230** (26.4x, 4.07% FCF yield); Munger **$262** first tranche / **$241** second / **$196** fat pitch; Li Lu **$215** first tranche / **$210** full; Duan Yongping the **29.73x mean band (~$259)**. Spread: **$196–$262**.
- **Upside to target: −22.2%.** The target is *below* the current price. **Current price provides no margin of safety** — the 安全边际 lamp is RED 4/4 unanimous (来源: L2a定性/安全边际).

---

## 6. Quantitative Factor Signals

| Factor | z-score | Signal | Interpretation |
|:-------|--------:|:-------|:---------------|
| Value (Trailing PE) | **−1.28** | **BEAR** | 39.69x vs peer median 23.70x — most expensive in the group |
| Value (Forward PE) | **−1.28** | **BEAR** | 33.81x vs peer median 20.14x — most expensive in the group |
| Profit margin | **−1.28** | **BEAR** | 27.2% vs peer median 32.8% — only above AMZN |
| Revenue growth | **−0.52** | **BEAR** | 16.6% vs peer median 18.3% — mildly weak |
| Leverage (D/E) | **−1.28** | **BEAR** | 79.55 vs peer max 55.24 — most levered in the group |
| Quality (ROE) | **+1.28** | **BULL** | 141.5% vs peer median 34.0% — **but see the artifact note** |
| Momentum (6m) | n/a (absolute rule) | **BULL** | +31.87% over six months, > 10% threshold |

**Consensus: 5 BEAR : 2 BULL : 0 NEUTRAL : 0 abstain** (来源: L2b量化/04-quantitative.json, engine `fengquant.py`).

- **Strongest BULL:** quality_roe at z = +1.28. **Strongest BEAR:** value_pe / value_fwd_pe / profit_margin / leverage_de, all tied at the z-floor of −1.28.
- **Extreme-signal warning:** none. But the warning threshold (|z| > 2.5) is **structurally unreachable** at n = 5 peers — the continuity-corrected z-score `(rank−0.5)/n → norm.ppf` caps at |z| = 1.28. The real information is that **five factors simultaneously hit that cap**, meaning Apple is the *worst* in its peer group on five dimensions, not merely below average.
- **The ROE BULL is an artifact, not a quality signal.** ROE = 141.5% has a denominator crushed by buybacks: FY2025 shareholders' equity of $73.733B is 1.5% of a $4.86T market cap. The numerator did not change; the denominator was repurchased. The same company computed four ways gives 119.9% (TTM NI ÷ latest equity $107.520B), 141.5% (local-DB snapshot), 148.75% (stockanalysis FY basis) and 151.9% (FY2025 NI ÷ FY2025 equity) — a range wide enough to prove the point. This BULL should be compiled as **neutral**. (来源: L2b量化/ai_review; all four figures computed by `financial_rigor.py calc`)
- **Shape of the disagreement.** Both BULLs sit on the *outcome* side (ROE, momentum); all five BEARs sit on the *price and balance-sheet* side (PE, FwdPE, margin, D/E, growth). That is the classic signature of **a good company at a bad price** — not a mixed picture.

**Data provenance.** yfinance was rate-limited across the board (`YFRateLimitError`) and no Clash node was available. The engine was driven instead through `tools/fengquant_local.py`, a data-source adapter that substitutes the local `market_data.db` for `yf.Ticker` and calls the **unmodified** `fengquant.py` factor logic. Fundamentals are a **2026-07-23 snapshot, identical for all six companies** (cross-sectional comparability intact); prices run through 2026-09-14. `degraded: false`. Apple's own PE snapshot (39.69x) is *higher* than the real-time value (38.21x), so using the snapshot cannot have flattered the conclusion. (来源: L2b量化/data_source)

---

## 7. Risk Matrix

| Risk | Probability | Impact | Mitigating factors |
|:-----|:-----------:|:------:|:-------------------|
| **Valuation / multiple compression** | **High** | **High** | None at this price. PE is above the 5-year maximum; a reversion to the median multiple alone implies ~$240 (−28%) with earnings untouched (来源: M层/valuation_history; L3 adversarial_check) |
| **Regulatory / antitrust** | **High** | **High** | Apple has absorbed fines before and kept the business; the moat is wide enough that a partial remedy is survivable. **But the loss cannot be sized** — the default-search payment is undisclosed, so no valuation figure in this report nets it out (来源: L0/10-K Item 1A; L2a定性/芒格,李录) |
| **AI disintermediation of the interface** | Medium | High | R&D +32.5% YoY ($34.035B 9M FY26) is a real defensive spend; Apple controls the OS and the silicon. Unresolved, not refuted (来源: L0/01-capability.md Q2-Q3) |
| **Greater China decline** | Medium-High | Medium | 15.5% of revenue, −3.8% in FY2025, the only shrinking region. Li Lu's hypothesis: structural re-fragmentation rather than a cyclical dip — declared as a hypothesis, not asserted (来源: L0/SEC 10-K segments; L2a定性/李录) |
| **Business / consumer cycle** | Medium | Medium | Upgrade-cycle length is the swing factor; Services revenue is recurring and less cyclical than hardware (来源: L0/10-K Item 1A) |
| **Macro / discount rate** | Medium | Medium | Fed easing (target 3.50–3.75%, EFFR 3.63%) helps at the short end, but the 10-year at 4.784% is **above** its MA50 (4.633%) and MA200 (4.360%), up 14.56% YoY — a 38x multiple is a long-duration asset and the discount rate is moving against it (来源: M层/macro_context) |
| **Margin reversal from a record high** | Medium | High | Q3 FY2026 gross margin 50.06% is a record, achieved while R&D rose 32.5%. If price increases stop sticking or the R&D step-up fails to produce a defensible product, margin **and** multiple compress together — the two variables are positively correlated, not independent (来源: L3/adversarial_check Q1) |

### Counter-case summary

- **Weakest quantitative signal:** value_pe at z = −1.28 (39.69x vs peer median 23.70x), corroborated by value_fwd_pe, profit_margin and leverage_de at the same floor.
- **Most pessimistic master:** Munger. *"A rent stream a regulator can legally cut is a licence as much as a moat."* He graded 护城河, 管理层 and 需求稳定 all YELLOW and priced the fat pitch at ~$196.
- **Panel dissent against the headline:** none on direction — all four returned WAIT @ 0%. The dissent is inside the lamps: 护城河, 管理层 and 需求稳定 are all split 2–2, and both YELLOW graders on 管理层 explicitly **diverge from the prior run's GREEN**, on the grounds that $90.711B of buybacks at 38x earnings with no visible price condition is a price-insensitivity observation.
- **Most lethal dissenting signal:** the **5 BEAR : 2 BULL** factor split. It is not one bad number; it is the peer group saying the price paid for a good company is the worst in the cohort.

---

## 7.5 DK Four Principles Audit (坐标 / 家国 / 息价 / 取舍)

| Principle | Finding | Impact on decision |
|:----------|:--------|:-------------------|
| **坐标原则 (coordinate)** | **🟡 YELLOW.** The comparable anchor is clear (mega-cap platform group + own history) and the coordinate *type* is correctly identified as Buffett (good business at a fair price), not Graham liquidation — book value is $7.37/share (equity $107.520B ÷ 14.59B shares) against a $333.08 price, so no asset backstop exists. But the price gap is **negative**: PE 38.21x is *above* the 5-year FY-end maximum, and the convergence path is broken — there is no catalyst that closes a gap upward because there is no gap. (来源: L0 01-capability.md 坐标原则; knowledge/principles/坐标原则.md) | Confidence penalty applied by the engine; recorded as a conflict item |
| **家国原则 (nation/state)** | **🟡 NEUTRAL-TO-CAUTIOUS.** Read as the US policy stance plus China exposure, since Apple is a US issuer. **Against:** US and EU antitrust actions target the highest-margin line; the regulatory direction is adversarial. **For:** no state policy seeks to suppress consumer-electronics demand, and tariff policy is a cost item rather than an existential threat. **Not RED** — Apple is not a state's direct trading counterparty in the sense the principle targets. Scored against the principle's five dimensions (政策方向 🟡 / 政策级别 🟡 / 时间维度 🟡 / 风险对冲 🟡 / **国际关系 🔴**): the international-relations row matches that criterion's red pole on the filings' own terms — a majority of net sales and of supplier facilities sit outside the US, and Greater China revenue fell 3.8% in FY2025. That row is a **geographic-exposure** red, not a state-*direction* red, so the principle-level reading stays 🟡. A reader who mechanically took the worst row as the principle light would make 家国 🔴 and flip this verdict to **PASS @ 0%** — under Rule 12 directly, or via Rule 10's upstream interception. (来源: M层/dk_policy.家国五维度; `02-market.md` §"家国原则 — the five dimensions"; SEC 10-K FY2025) | Not a blocker; informs the risk matrix. **The aggregation rule for the five dimensions is undefined in `knowledge/principles/家国原则.md`** — recorded as an open item |
| **息价原则 (cash-flow vs price)** | **🔴 RED — this is the binding constraint.** Scored against the principle's own five-row checklist (`knowledge/principles/息价原则.md`): **dividend yield 0.32%** is *not* above the 4.784% risk-free rate (🔴); **价差空间** is negative — PE 38.21x is above the five-year maximum, so there is no discount to converge to (🔴); **安全边际 −22.2%**, i.e. far under the 30% floor (🔴); **回购回报** is GREEN ($90.711B in FY2025) — the one favourable row; **兑现路径** "不知道价值何时回归" (🔴) — there is no catalyst that closes a gap *upward* because there is no gap. Four rows RED, one GREEN. Corroborated independently: FCF yield **2.81%** against a 10-year Treasury of **4.784%** = **−197bp**, which all four masters named as the crux. (来源: knowledge/principles/息价原则.md; L2a定性/安全边际 unanimous 4/4; computed by `financial_rigor.py calc`) | **Drives the RED layer light and the WAIT decision** |
| **取舍原则 (trade-off / opportunity cost)** | **🟢 / NOT TESTED — no order generated.** No capital is being committed, so no opportunity cost is actually incurred. Portfolio-level opportunity cost is assessed at the P layer. (来源: L3/06-collision.json) | None at 0% position |

**DK discipline-rule check (from L1 03-discipline.json).** The table below is L1's six discipline rules. L3's DK rule family (rules 10–14) did **not** run this pass — the engine received no DK inputs — so these lights feed the hand ruling in §7.5, not the machine verdict.

| Rule | Light | Note |
|:-----|:-----:|:-----|
| 2638法則 (index above year line) | 🟢 | S&P 500 at 7,619.98 vs MA250 7,076 — above. The 2638 line itself is an A-share reference; the rule requires a per-market anchor and the US anchor passes |
| 年线法则 (year-line, anti-chasing) | 🟡 | Price $333.08 is **19.0% above** the MA250 of $279.93 (computed by `financial_rigor.py calc`: +18.99%). The rule maps >15% to *caution / not suitable for heavy position building*; >30% would be a hard block |
| 后发制人 (right-side confirmation) | 🟢 | 4/4 right-side signals satisfied; MAs fully stacked. **A timing rule, not a price rule** — it confirms the trend, not the valuation |
| 买分歧卖共识 (buy divergence, sell consensus) | 🟡 | Downgraded from the engine's GREEN after review. Realised volatility is low (28%), which the engine reads as "divergence exists", but the price behaviour says otherwise: 1.97% from a 52-week high, +45.21% over 12 months, PE above its own 5-year maximum. Optimism is already in the price |
| 双账户制 (dual-account rule) | N/A | Process rule; a P-layer concern |
| 钱仓滚存 (profit-pool rollover) | N/A | No position exists |

### DK verdict, and one rule-tree conflict it exposes

**The hand ruling is WAIT @ 0%.** 息价原则 is **🔴 RED** (four of five checklist rows; §7.5 table above). The principle's own document states its L3 mapping in one line — *"L3碰撞 → 如果安全边际 < 30% → WAIT（还不够便宜）"* — so a RED 息价 driven by an insufficient margin of safety means **wait for a better price**, not *reject the business*. That is the ruling, and it is consistent with every other layer.

**But the engine cannot currently express that ruling, and the conflict is reported rather than papered over.**

`Tools/fengcollision.py` evaluates **Rule 10 — "any DK principle 🔴 → PASS" — *before* Rule 13 — "安全边际 < 30% or 息价 == 🔴 → WAIT"**. Two consequences:

1. Rule 13's `dk_price == "RED"` clause is **unreachable dead code**: any 息价 RED is intercepted by Rule 10 first and returned as PASS. Exercising the engine with real DK inputs (scratch harness, not the CLI) showed the dead code is **wider than that**: **Rule 11 (坐标原则 🔴 → WAIT) and Rule 12 (家国原则 🔴 → PASS) are unreachable too**, for the same reason. Only Rule 10, the `安全边际 < 30%` half of Rule 13, and the Rule 14 boost modifier can ever take effect.
2. If Apple's DK lights were wired in as assessed here, the engine would return **PASS @ 0%, high confidence** — *reject the company* — where the principled answer is **WAIT @ 0%, low confidence** — *reject the price*. Both are 0% positions, so no capital decision differs; the **diagnosis** differs, and the difference is exactly the one this report spends §1 arguing about. For **坐标原则** the divergence is worse than a labelling difference: the dead rule demands WAIT, and what runs instead returns PASS — a red coordinate becomes a rejection of the company rather than a demand for a lower price.

This run did **not** change the precedence. Which of the two rules owns a RED 息价 is a framework-semantic decision (Rule 10's blanket "DK 纪律高于一切" reads naturally for 家国/坐标, where the answer really is *don't touch*; it reads awkwardly for 息价, where the answer is *not at this price*). That call belongs to the founder, not to a tooling pass. Recorded here, in `06-collision.json`, and in TODO as an open item.

**What the engine actually did.** It ran with **no DK inputs at all** — the CLI passes no `dk` argument — so neither Rule 10 nor Rule 13 fired, and the fallback returned WAIT @ 0% on other grounds. The conclusion coincides with the hand ruling; the reasoning path does not. This is why the run emits `dk_input.supplied = false`, a `DK_INPUT_MISSING` conflict, and now a `dk_rules` block marking all five DK rules `not_evaluated` — machine-readable evidence that the family did not run, rather than an absence a reader has to infer.

---

## 8. Catalyst Calendar

| Timing | Event | Potential impact |
|:-------|:------|:-----------------|
| **Near term (Oct–Nov 2026)** | FY2026 Q4 earnings and full-year results | High. Tests whether the 50.06% gross margin and +16.2% revenue growth rates hold; also the first full-year disclosure against the FY2025 base of $416.161B |
| **Near term (ongoing)** | FOMC meetings | Medium-High. The 10-year at 4.784% is the discount rate on a 38x multiple; further long-end rises hit the multiple directly |
| **Near term (ongoing)** | US DOJ / EU DMA remedy proceedings | **High.** Any final remedy touching App Store commission or default-search economics strikes the profit pool that no valuation here nets out |
| **Medium term** | Apple's on-device AI positioning vs assistant-layer entrants | High. Determines whether the OS remains the primary user surface, on which all Services economics rest |
| **Medium term** | Greater China quarterly trend | Medium-High. Tests Li Lu's structural-re-fragmentation hypothesis against the cyclical-dip reading |
| **Long term** | Interface-shift resolution; installed-base monetization ceiling | High but slow-moving. Converts 好生意 and 护城河 from GREEN/YELLOW into a settled answer |

*(来源: L0 01-capability.md Q3 risk ranking; M层/macro_context; L2a定性/李录, 芒格)*

---

## 9. Position & Exit Plan

| Dimension | Content |
|:----------|:--------|
| **Current price** | $333.08 (close 2026-09-14) |
| **Target position** | **0%.** Engine decision WAIT; L2a layer RED on margin of safety |
| **Entry method** | When triggered, **DCA in tranches**, never one-shot. The signal to start is a *multiple*, not a price memory: **PE ≤ 30x on TTM EPS** is the first tranche gate ($262), **PE ≤ 27.58x** the second ($241), **PE ≤ 26.4x** the strongest-conviction band ($230) |
| **Add conditions** | 1. Price reaches the **$230–$262** band *with the business intact* (Services still growing, gross margin holding, no adverse final antitrust remedy). 2. 买分歧卖共识 returns to GREEN — valuation bears still exist and the price is no longer at the 96.9th percentile. 3. 年线法则 clears the YELLOW (>19% above the year line today): either the price falls toward the MA250 or the year line rises to meet it |
| **Take-profit condition** | Not applicable while unowned. If held, the discipline is 卖共识: a move toward ~49.7x TTM EPS ($433) would mean a decade of success is fully priced |
| **Stop-loss conditions** | 1. **Fundamental:** an adverse final antitrust remedy that strips App Store commission or default-search economics → 护城河 moves to RED, Rule 1 fires, PASS. 2. **Fundamental:** Greater China decline spreads to other regions → 需求稳定 to RED. 3. **Price:** if entered, a broken trend (price below MA120 297.95, then MA200 285.01) is a re-underwrite trigger, not an automatic sale. 4. **Time:** if the thesis is "wait for the multiple", a reversion that does not occur within 24 months is itself information about the multiple's new floor |
| **Trim signals** | 1. PE re-expands beyond the 5-year maximum *while* margin or Services growth decelerates. 2. The undisclosed default-search economics are resolved adversely. 3. A greater share of total revenue comes from legally contested rent |

**The drawdown test, answered in advance.** If the price falls 30% to **$233.16** (computed: $333.08 × 0.70), that implies ~26.7x TTM EPS — inside the re-entry band three of four masters named. The answer is **ADD, but conditional on the cause**: if it is multiple compression with the business intact, the 安全边际 lamp improves and the framework's Rule 3 fires; if it is a final adverse antitrust remedy or spreading China decline, 护城河 goes RED and the answer is **PASS — do not buy a broken business because it is cheaper**. (来源: L3/adversarial_check Q2)

**The +30% test.** At $433.00 (+30%) the stock would trade at ~49.7x TTM EPS, ~33% above the five-year maximum multiple. A rise **cannot manufacture a buy**; the correct response to a further 30% rise is to widen the required margin of safety, not lower it. (来源: L3/adversarial_check Q3)

---

## 10. Bias Check

| Bias | Risk level | Explanation |
|:-----|:----------:|:------------|
| **Confirmation bias** | **Low** | Evidence deliberately sought against the conclusion: **6 supporting items vs 9 opposing**. Opposing: 安全边际 RED 4/4; PE above the 5-year maximum; FCF yield vs 10Y at −197bp; 护城河/管理层/需求稳定 each split 2–2; Greater China −3.8%; L2b 5 BEAR : 2 BULL; M-layer valuation RED; year line +19.0% YELLOW. The analysis nonetheless did **not** conclude PASS — it concluded WAIT with a defined re-entry, which is the asymmetry that shows the business was not rejected for being expensive |
| **Anchoring** | **Low-Medium (mitigated)** | Live anchors exist: the $339.79 52-week high (price 1.97% below) and the prior run's $305.93. Structural mitigation: every valuation statement is expressed as a *multiple* against a five-year range, not as a price relative to a remembered high. The four masters' re-entry prices span $196–$262 — Li Lu's $215 sits *below* the 52-week low, which no anchoring process would produce |
| **Recency bias** | **Low** | The recent-positive price path was explicitly put in front of the panel: +45.21% 12M, +33.29% 6M, +9.11% 1M, 96.9th percentile of the 5-year range, VIX at the 6th percentile. The prior run said WAIT at $305.93 and the stock is 8.9% higher; every master saw that cost of waiting and refused the buy. The verdict was stable across an 8.9% price increase |
| **Overconfidence** | **Low** | Confidence is **0.35 (low)** by the engine's own rules, not by self-assessment — the engine fell to its generic fallback because the lamp combination matches none of rules 1–9, and it **refused to claim a rule fired** (`applicable_rule: null`). Its DK family (rules 10–13) could not participate at all, which is disclosed in §7.5 and §11 rather than counted as a clean pass. Two lamps are genuinely split, four information gaps are declared, and the position size is 0% |

*(来源: L3/06-collision.json adversarial_check.bias_check)*

---

## 11. Collision Engine Result and Rule Trace

**Engine output (verbatim):** `decision: WAIT` · `confidence: 0.35 (low)` · `position_pct: 0` · `applicable_rule: null`

**Rule-tree trace:**

| Rule | Test | Outcome |
|:-----|:-----|:--------|
| Rule 1 | 好生意 or 护城河 RED → PASS | **Not triggered** — 好生意 GREEN, 护城河 YELLOW |
| Rule 10 (DK) | Any DK principle RED → PASS | **Not evaluable** — **no DK was supplied to the engine**; all four principles defaulted internally. This is *not* "evaluated and not matched". Emitted as `DK_INPUT_MISSING` (conflict 9), `dk_input.supplied = false`, and — new this run — `dk_rules` with all five DK rules marked `not_evaluated` |
| L1 RED → Deep Value branch | L1 RED? | **Not entered** — L1 is YELLOW, not RED |
| Rule 2 | 好生意🟢 + 护城河🟢 + 安全边际🔴 → WAIT @ 0% | **Not exactly matched** — 护城河 is YELLOW, not GREEN |
| Rule 3 | 好生意🟢 + 安全边际🟡 → BUY low @ 40% | **Not matched** — 安全边际 is RED, not YELLOW |
| Rule 11 | 坐标原则 🔴 → downgrade | **Not evaluable** — same DK gap as Rule 10. **Unreachable even with DK supplied**: Rule 10's `dk_any_red` guard sits upstream of it |
| Rule 13 | 安全边际 < 30% or 息价 🔴 → WAIT | **Not evaluable** — same DK gap. The `安全边际` half *would* have fired (margin −22.2%) and returns the same WAIT @ 0%; the `息价 🔴` half is **unreachable even with DK supplied**. See §7.5 |
| **Fallback** | No rule 1–9 matched | **WAIT @ 0%, confidence low** — the engine declined to claim a rule fired |

**Reading the engine's `null` and its "未命中规则 1-13".** `applicable_rule: null` is **loud failure, not a defect**: the rule tree does not cover this lamp combination and the engine says so rather than impersonating a rule. But its verbatim reason — *"未命中规则 1-13"* — must be read precisely: rules **1–9 genuinely ran and missed**, while rules **10–13 were not evaluable at all** because the DK family had no inputs. A future auditor must not read "no rule matched" as "the rule tree cleared this stock on the merits." That distinction is now carried by the artifact itself: `06-collision.json → dk_rules` records each DK rule with its true condition and `status: not_evaluated`, emitted by the engine rather than written by hand.

The decision direction is **identical to Rule 2's** (好生意🟢 + 护城河🟢 + 安全边际🔴 → WAIT @ 0%) and to Rule 13's; only the confidence tier differs — fallback-low instead of Rule-2-medium — because the moat is YELLOW rather than GREEN. **The lower tier is the more honest of the two**, given the split moat and the four open information gaps. (来源: L3/06-collision.json confidence_note, rule_tree_note)

**Engine defects found and fixed this run (additive only, `tools/fengcollision.py`).**

1. `_read_market_data(ticker)` ignored the ticker and read only the global `research/market/latest.json`, filling `valuation` with a text summary. `deep_collision`'s `m_red` was therefore **permanently False** — this analysis's own M-layer valuation RED was **invisible to the rule tree**. Same defect class as the previously-fixed 159766.SZ case (the 2026-09-13 fix corrected the reader but not the source the caller fed it). Fixed at the source. **Materiality:** did not change this decision (fallback and Rule 2 both give WAIT @ 0%), but pre-fix, if L2a had been all-green, rules 5/6/7 would have opened a **BUY at 70–90%** without ever seeing the M-layer red.
2. The fallback branch described real qualitative output as a "proxy signal", which would lead a future auditor to read a completed four-master analysis as pending. Now branched on the `source` field.
3. Duplicate conflict labels ("估值" and "M-估值" from the same lamp) — deduped.
4. **`--market <file>` bypassed the M-layer flattening.** Passing `02-market.json` explicitly produced a *less* complete result than letting the engine auto-discover it (8 conflicts, `market_red_lights: ['M-估值']`) because the explicit path skipped `_flatten_m_layer` and so lost the top-level `overall_light`. Both paths now flatten. Verified identical output on both.
5. **DK never reached the engine — and this one was silently inflating position sizes.** The sole call site passes no `dk` argument, so: (a) rules 10–14 have **never run on any analysis**; and (b) `dk_boost = dk_all_green and l1_light == "GREEN"` was **vacuously true** whenever L1 was GREEN, silently raising rule 6/7/8 position sizes one tier (70→90%, 40→60%, 80→100%) plus a confidence upgrade and a "＋DK双验调高" suffix labelling a double-verification that never happened. Now: a missing principle set writes a `DK_INPUT_MISSING` conflict, a top-level `dk_input` field states `supplied: false` and lists the expected keys, and `dk_boost` is gated on `dk_supplied` first. Both directions tested — DK absent → **80% / medium**; fully-green DK supplied → **100% / high**. **Materiality for Apple: zero** — L1 is YELLOW, so `l1_light == "GREEN"` was already False and `dk_boost` was never granted; the decision is bit-identical before and after (WAIT / low / 0.35 / 0%). The reason it matters is the class of L1-green stocks it silently mis-sized.
6. **The DK family's status was prose-only.** `dk_input` recorded that DK was absent; nothing recorded what each DK rule would have done. The engine now emits a `dk_rules` block — `supplied`, the raw light given per principle (`null` where none was given), and each of rules 10–14 with its true condition and a `status` of `fired` / `evaluated_not_fired` / `not_evaluated` (Rule 14 additionally carries `active`). It is derived from the engine's own `applicable_rule` / `reason` / `conflicts` and re-implements no judgement condition. Verified additive: pre- and post-change outputs are identical on every key except the new one.

**Open item, not fixed (recorded for the founder).** Rule 10 ("any DK 🔴 → PASS") is evaluated *before* Rule 13 ("安全边际 < 30% or 息价 🔴 → WAIT"), which makes Rule 13's `dk_price == "RED"` clause **unreachable dead code** and would turn a RED 息价原则 into PASS where the principle's own documented L3 mapping says WAIT. Exercising the engine with real DK inputs showed the dead code is **wider than the 息价 case**: because Rule 10's `dk_any_red` guard sits upstream of the whole family, **Rule 11 (坐标原则 🔴 → WAIT) and Rule 12 (家国原则 🔴 → PASS) are unreachable as well**. Only Rule 10, the `安全边际 < 30%` half of Rule 13, and the Rule 14 boost modifier can ever take effect. For 坐标原则 the consequence is directional rather than cosmetic: the dead rule demands WAIT, and what actually runs returns PASS — a red coordinate becomes a rejection of the company instead of a demand for a lower price. Fixing this changes engine behaviour for every stock, and which rule owns a RED principle is a framework-semantic call. It is reported, not changed — see §7.5. Also logged in TODO.

**Registry note:** `tools/fengquant_local.py` was written this run as a local-DB data-source adapter (it copies no factor logic; it substitutes the ticker data source and calls the unmodified engine). It is a project-internal tool, not an open-source dependency.

---

## 12. Data Quality and Declared Limitations

**What is first-hand and cross-checked.** SEC EDGAR 10-K FY2025 (accession 0000320193-25-000079) and 10-Q FY26Q3 (0000320193-26-000020) are primary filings. TTM revenue ($466.823B), TTM net income ($128.93B) and TTM EPS ($8.72) were **recomputed independently from the filings and match stockanalysis.com exactly**. FY-end PE from local DB prices matches an independent provider within 1% for all five years. The M-layer quality gate passed with a 0.0% PE discrepancy.

**Known tool defect, disclosed.** `tools/fengdata.py` returned a boolean `ma120_above_ma200: false` while its own reported MA120 (297.9483) and MA200 (285.0136) imply TRUE. Independent recomputation from the local DB gives TRUE. The rule outcome (不接飞刀) is unaffected either way, but the boolean is wrong and is recorded as a tool defect. Likewise, `fengdata.py` reported `low_52w` 226.15 on an intraday basis versus 233.41 computed from closes; this analysis uses the close basis consistently.

**Search tooling failed completely.** `Search-King --backend lite` failed with DDG timeouts on every attempt; `--backend cloak` (Bing) returned query-independent generic results. **No claim anywhere in this analysis rests on a search-engine result.** The corollary, stated plainly: a material recent news event could in principle have been missed, and it is disclosed rather than papered over.

**Declared information gaps and limitations (5)** — items 1–4 are information gaps; item 5 is a tooling limitation, stated separately for the reason given below.

1. **Size of the Google default-search payment** — undisclosed by Apple. The profit pool under regulatory attack cannot be sized, so no valuation figure here nets it out.
2. **FY2026 installed-device count** — not retrieved. This is the single number most needed to confirm the 需求稳定 lamp.
3. **2026 insider ownership and share-sale record** — not retrieved. The 管理层 lamp is **provisional in both directions**: Munger's stated rule is GREEN if the proxy shows a value-conditioned repurchase policy or clean ownership data; RED if insiders were heavy sellers into the 96.9th percentile.
4. **CNN Fear & Greed index** — unavailable (page rendered without numeric values). VIX at its 6th percentile is used as a documented proxy; **no F&G value is asserted**.
5. **Search tooling** — as above.

---

## 13. Summary of Layer Verdicts

| Layer | Light | Key output |
|:------|:-----:|:-----------|
| **L0 能力圈** | 🟢 UNDERSTOOD | All three questions answered from filings. Coordinate principle 🟡 — the price gap is negative (a premium, not a discount) |
| **M 市场** | 🔴 RED | Valuation 🔴 (PE above the 5-year max); macro 🟡 (decelerating, easing into sticky 3.4% CPI); trend 🟢; sentiment 🟡 (VIX 6th percentile). Overall = worst = RED |
| **L1 硬纪律** | 🟡 YELLOW | 8 rules: seven GREEN, one YELLOW (年线法则, +19.0% above the year line). No fast-veto item triggered. No RED, so no forced interception |
| **L2b 量化** | 🟡 YELLOW | 5 BEAR : 2 BULL. The ROE BULL is a buyback artifact. Five factors pinned at the n=5 z-floor means "worst in group" on five dimensions |
| **L2a 定性** | 🔴 RED | 好生意 🟢 · 护城河 🟡 · **安全边际 🔴 (4/4 unanimous)** · 管理层 🟡 · 需求稳定 🟡 · 会计质量 🟢. All four masters: WAIT @ 0% |
| **L3 碰撞** | **WAIT** | confidence **0.35 (low)**, position **0%**. Four adversarial questions answered, four bias checks run, **9 conflicts** recorded — 8 market/quant signals plus 1 tooling gap (`DK_INPUT_MISSING`; rules 10–14 did not participate) |
| **L4 报告** | this file | Target **$259**; re-entry band **$230–$262**; no margin of safety at $333.08 |

**Final answer: WAIT @ 0% at $333.08.** The business is understood and of high quality, and the framework would want to own it at the right multiple. It is not the right multiple. Three layers — M valuation RED, L2a margin-of-safety RED 4/4, and L2b value factors at the group floor — independently say the same thing: **the company is not the question; the price is.**

---

*Analysis date 2026-09-15 · Price basis 2026-09-14 close · State: `research/state/temp_state_AAPL.json` · Engine artifacts archived verbatim in `sources/` · All arithmetic in this report was produced by `tools/financial_rigor.py`, never by hand.*
