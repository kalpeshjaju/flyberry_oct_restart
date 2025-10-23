# DOCUMENT 00: CURRENT REALITY - SPECIFICATION

**Version**: 1.0
**Last Updated**: 2025-10-23
**Read Time**: 6 minutes

---

## PURPOSE

Revenue performance, channel breakdown, product winners/losers, customer reality, geographic spread, growth trajectory.

This document **establishes the baseline** - where Flyberry is today (Q1 FY26 data).

---

## DATA SOURCES

**Primary**:
- `INVESTOR-UPDATE-Q1-FY26.md` (revenue, channels, growth metrics)
- Revenue analytics (by product, channel, geography)
- Product performance data (sales, repeat rates)
- Customer data (segments, behavior, AOV)

**Derived**:
- Channel mix percentages
- Product performance rankings
- Customer segment analysis
- Growth projections

---

## SECTION STRUCTURE

### **Section 1: THE NUMBERS (Q1 FY26)**
**Purpose**: Revenue performance snapshot

**Content Template**:
```markdown
## THE NUMBERS (Q1 FY26)

**Revenue Performance**:
| Metric | Q1 FY26 | Q1 FY25 | YoY Growth | Reality Check |
|--------|---------|---------|------------|---------------|
| **Total Revenue** | ₹{revenue} | ₹{prev_revenue} | +{growth}% | {interpretation} |
| **E-Commerce** | ₹{ecomm} | ₹{prev_ecomm} | +{ecomm_growth}% | {ecomm_reality} |
| **Sales-in-Store** | ₹{retail} | ₹{prev_retail} | +{retail_growth}% | {retail_reality} |
| **Corporate Gifting** | ₹{corporate} | {prev_corporate} | {corp_growth} | {corp_reality} |

**What This Means**:
- ✅ **{strength_1}** ({metric})
- ⚠️ **{challenge_1}** ({metric})
- ✅ **{strength_2}** ({metric})
- ⚠️ **{challenge_2}** ({metric})

---
```

**Requirements**:
- All revenue figures from INVESTOR-UPDATE
- All growth rates calculated (YoY, QoQ)
- Reality Check column explains "so what"
- Include run-rate projection (quarterly → annual)

---

### **Section 2: CHANNEL BREAKDOWN**
**Purpose**: Deep dive into each revenue channel

**Content Template**:
```markdown
## CHANNEL BREAKDOWN

**E-Commerce ({ecomm_pct}% of revenue, fastest growth)**:
- **Swiggy Instamart**: {swiggy_growth}% YoY volume growth ({prev_units}K → {curr_units}K units)
  - **Reality**: {swiggy_reality}
  - **Opportunity**: {swiggy_opportunity}
- **Amazon**: {amazon_position}
  - **Reality**: {amazon_reality}
  - **Challenge**: {amazon_challenge}
- **Blinkit**: {blinkit_stores} stores, {blinkit_status}
- **Zepto**: {zepto_stores} stores, {zepto_status}

**Sales-in-Store ({retail_pct}% of revenue, stable)**:
- Modern Trade: {modern_trade_list}
- Traditional Retail: {traditional_status}
- **Reality**: {retail_reality}

**Corporate Gifting ({corp_pct}% of revenue, seasonal)**:
- **Clients**: {client_count}+ Fortune 500 ({client_examples})
- **Problem**: {seasonal_problem}
- **Missed Opportunity**: {year_round_opportunity}

---
```

**Requirements**:
- Calculate percentage mix for each channel
- Show unit economics where available (AOV, CAC)
- Identify growth drivers and constraints
- State opportunities clearly

---

### **Section 3: PRODUCT PERFORMANCE**
**Purpose**: Winners vs strugglers analysis

**Content Template**:
```markdown
## PRODUCT PERFORMANCE

**Winners** (Strong repeat, high growth):
1. **{product_1}**: {metric_1}
   - **Why It Works**: {reason_1}
   - **Reality**: {reality_1}

2. **{product_2}**: {metric_2}
   - **Why It Works**: {reason_2}
   - **Reality**: {reality_2}

3. **{product_3}**: {metric_3}
   - **Why It Works**: {reason_3}
   - **Reality**: {reality_3}

**Strugglers** (Low awareness, low repeat):
1. **{struggling_product_1}**: {price_point}
   - **Problem**: {problem_1}
   - **Reality**: {reality_1}

2. **{struggling_product_2}**: {description}
   - **Problem**: {problem_2}
   - **Reality**: {reality_2}

3. **{struggling_product_3}**: {description}
   - **Problem**: {problem_3}
   - **Reality**: {reality_3}

---
```

**Requirements**:
- Rank products by revenue OR repeat rate OR growth
- Show specific metrics (units sold, repeat %, revenue)
- Explain WHY winners win (not just that they do)
- Diagnose WHY strugglers struggle (root cause)

---

### **Section 4: CUSTOMER REALITY**
**Purpose**: Who actually buys, behavior patterns

**Content Template**:
```markdown
## CUSTOMER REALITY

**Who Actually Buys** (Data from Q1 FY26):

**Demographics**:
- **Age**: {age_range} ({percentage}% of buyers)
- **Income**: {income_bracket}+ households
- **Geography**: {city_breakdown}
- **Gender**: {gender_split}

**Purchase Behavior**:
- **Average Order Value**: ₹{aov} ({vs_benchmark})
- **Repeat Rate**: {repeat_pct}% ({timeframe})
- **Purchase Frequency**: {frequency} ({cadence})
- **Basket Composition**: {typical_basket}

**Customer Segments**:
1. **{segment_1}** ({pct}% of revenue)
   - **Profile**: {profile}
   - **Buying Behavior**: {behavior}
   - **Opportunity**: {opportunity}

2. **{segment_2}** ({pct}% of revenue)
   - **Profile**: {profile}
   - **Buying Behavior**: {behavior}
   - **Opportunity**: {opportunity}

3. **{segment_3}** ({pct}% of revenue)
   - **Profile**: {profile}
   - **Buying Behavior**: {behavior}
   - **Opportunity**: {opportunity}

---
```

**Requirements**:
- Use actual purchase data (not assumptions)
- Segment by behavior, not just demographics
- Show AOV, repeat rate, frequency for each segment
- Identify opportunity for each segment

---

### **Section 5: GEOGRAPHIC SPREAD**
**Purpose**: Where Flyberry sells, expansion opportunities

**Content Template**:
```markdown
## GEOGRAPHIC SPREAD

**Current Presence** (Revenue by Metro):

| City | Revenue (Q1) | % of Total | YoY Growth | Store Count |
|------|--------------|------------|------------|-------------|
| {city_1} | ₹{rev} | {pct}% | +{growth}% | {stores} |
| {city_2} | ₹{rev} | {pct}% | +{growth}% | {stores} |
| {city_3} | ₹{rev} | {pct}% | +{growth}% | {stores} |

**Geographic Concentration**:
- Top 3 cities: {concentration_pct}% of revenue
- **Risk**: {concentration_risk}
- **Opportunity**: {expansion_opportunity}

**Expansion Roadmap**:
- Tier 1: {tier1_cities} ({current_presence}/{total})
- Tier 2: {tier2_cities} ({current_presence}/{total})
- **Quick Wins**: {quick_win_cities}

---
```

**Requirements**:
- Show actual revenue by city (top 5-10)
- Calculate geographic concentration risk
- Identify underserved high-potential cities
- Prioritize expansion targets

---

### **Section 6: GROWTH TRAJECTORY**
**Purpose**: Where we're headed if nothing changes

**Content Template**:
```markdown
## GROWTH TRAJECTORY

**Current Run Rate**:
- Q1 FY26: ₹{q1_revenue}
- **Annual Run Rate**: ₹{annual_runrate} (Q1 × 4)
- **Reality**: {reality_check}

**Projection (If Current Trajectory Continues)**:

| Metric | FY26 Projected | FY27 Projected | FY28 Projected | ₹100 Cr Target |
|--------|----------------|----------------|----------------|----------------|
| Revenue | ₹{fy26} | ₹{fy27} | ₹{fy28} | ₹100 Cr |
| Gap | - | - | ₹{gap} | **{pct}% short** |

**What This Means**:
- ✅ Current growth ({current_cagr}% CAGR) is strong
- ⚠️ But insufficient to hit ₹100 Cr by FY28
- ⚠️ Need {required_cagr}% CAGR to hit target (vs {current_cagr}% current)
- ⚠️ Implies {acceleration_needed} acceleration required

**The Math**:
- To hit ₹100 Cr by FY28: Need ₹{q1_target} per quarter by Q4 FY28
- Current Q1 FY26: ₹{current_q1}
- **Gap**: {multiplier}× growth needed

---

**Data Sources**: INVESTOR-UPDATE-Q1-FY26.md, revenue analytics
**Confidence**: 95% (based on actual Q1 FY26 data)
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
```

**Requirements**:
- Use actual Q1 FY26 data for projections
- Show ₹100 Cr gap clearly
- Calculate required CAGR vs current CAGR
- State acceleration needed explicitly

---

## GENERATION NOTES

**Data Flow**:
1. Load INVESTOR-UPDATE-Q1-FY26.md (revenue data)
2. Calculate channel mix, growth rates
3. Load product performance data
4. Calculate customer segments
5. Build geographic breakdown
6. Project trajectory

**Formatting**:
- Tables for revenue/channel/geographic data
- Bullets for insights and reality checks
- Bold for key numbers and takeaways
- Use ✅ for strengths, ⚠️ for challenges

---

## QUALITY CHECKLIST

Before finalizing, verify:
- [ ] All Q1 FY26 revenue figures stated
- [ ] All YoY growth rates calculated
- [ ] All channel percentages sum to 100%
- [ ] Product winners/strugglers identified (3 each minimum)
- [ ] Customer segments defined with behavior data
- [ ] Geographic concentration calculated
- [ ] ₹100 Cr gap quantified
- [ ] Data sources cited
- [ ] Confidence score included
