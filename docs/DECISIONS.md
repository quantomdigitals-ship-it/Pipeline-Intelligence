# Decision Log - Pipeline Intelligence Project

**Project**: Day 1-2 Pipeline Risk Scoring Review  
**Date Started**: September 14, 2026

---

## Decision 1: Approve Discovery Stage Baseline Uplift

**Date**: 2026-09-14  
**Decision**: Increase all Discovery stage deals by 10-15 risk points minimum

**Rationale**:
- Analysis revealed systematic underscoring: Discovery deals averaged 26.2/100 vs. healthy 35-40 baseline
- Early-stage deals inherently carry higher qualification risk
- Current scoring pattern inconsistent with pipeline industry standards
- 4 critical discovery deals (TechStart, SalesFlow, VideoCo, POSCo) moved to 35-45 range

**Impact**:
- +$309K moved to higher risk categories
- Better reflects early-stage execution uncertainty
- Improves forecast accuracy for Day 2

**Status**: ✅ APPROVED & IMPLEMENTED

**Note**: MarketingCo, InventoryCo, BrandCo remain at 28-30 (classified as minor adjustments for next cycle)

---

## Decision 2: Correct CloudFirst Risk Score

**Date**: 2026-09-14  
**Decision**: Increase CloudFirst from 30 → 57 (Watch category)

**Rationale**:
- CloudFirst is the largest deal in pipeline ($120K)
- Proposal stage deals averaging 60-90 risk score
- Current 30 score under-represents deal complexity and value at stake
- Recommended range for similar deals: 50-65
- Score of 57 aligns with proposal stage peer assessment

**Impact**:
- Brings highest-value deal into proper watch status
- Priority score increases from 360.0 → 684.0 (highest attention needed)
- Allows sales team to focus mitigation efforts

**Status**: ✅ APPROVED & IMPLEMENTED

**Decision Maker**: Day 1 Review Analysis
**Follow-up**: Sales leadership to confirm deal complexity assessment

---

## Decision 3: Realign Proposal Stage Outliers (HRPlus & Acme Inc)

**Date**: 2026-09-14  
**Decisions**:
- HRPlus: 13 → 57 (low Healthy to mid-Watch)
- Acme Inc: 28 → 67 (low Healthy to At-Risk)

**Rationale**:
- Proposal stage cohort shows 60-90 risk pattern (n=12 deals)
- HRPlus (13) and Acme Inc (28) are extreme outliers
- Both have complex deal characteristics requiring proposal engagement
- Scoring inconsistency either indicates:
  - Special deal circumstances NOT documented, OR
  - Measurement/methodology error requiring correction
- Applied mid-range corrections pending sales verification

**Impact**:
- HRPlus: 40K deal now properly flagged for proposal-stage attention
- Acme Inc: 45K deal elevated to At-Risk, requiring active management
- Improves consistency across proposal stage assessment

**Status**: ✅ APPROVED & IMPLEMENTED

**Follow-up Actions**:
- [ ] Sales team to validate if HRPlus/Acme Inc have special circumstances
- [ ] If justified, document exceptions in deal records
- [ ] If measurement error, confirm scoring methodology updates

---

## Decision 4: Adjust EComm Co Execution Risk Assessment

**Date**: 2026-09-14  
**Decision**: Increase EComm Co from 8 → 20 (remain Healthy but elevated)

**Rationale**:
- EComm Co: $85K deal in Negotiation stage (most advanced)
- Previous score (8) suggests near-zero execution risk
- Unrealistic for late-stage deal of this size:
  - Contract finalization risk
  - Implementation complexity
  - Stakeholder alignment
- Recommended range: 15-25 (healthy but with caution)
- Score of 20 reflects execution risk without full escalation

**Impact**:
- Better captures execution-phase risks
- Prevents over-confidence as deal nears close
- Priority score increases from 68.0 → 170.0 (more visible)

**Status**: ✅ APPROVED & IMPLEMENTED

**Reasoning**: Even healthy late-stage deals carry non-zero risk. Score change acknowledges this reality without false alarms.

---

## Decision 5: Adopt Risk Level Mapping

**Date**: 2026-09-14  
**Decision**: Standardize risk level categorization:
- **At Risk**: Score 60+
- **Watch**: Score 30-59
- **Healthy**: Score <30

**Rationale**:
- Provides clear decision boundaries for pipeline management
- Aligns with post-adjustment score distribution
- Enables consistent follow-up actions per category

**Impact**:
- At Risk (10 deals) → Daily monitoring required
- Watch (9 deals) → Weekly review, risk mitigation planning
- Healthy (11 deals) → Standard management

**Status**: ✅ APPROVED & IMPLEMENTED

---

## Decision 6: Defer Minor Adjustments to Next Cycle

**Date**: 2026-09-14  
**Decision**: Hold MarketingCo, InventoryCo, BrandCo (Discovery stage) at current scores (28-30) for Day 2

**Rationale**:
- These deals were flagged for minor adjustment (target: 35-40)
- Critical path items take precedence
- Can address in next refinement without timeline impact
- Allows time for sales validation of earlier changes

**Impact**:
- Reduces risk of adjustment fatigue
- Provides feedback loop before broader baseline changes
- Maintains focus on 8 critical deals already adjusted

**Status**: ✅ APPROVED & SCHEDULED FOR NEXT REVIEW

**Next Review**: Post-Day 2 analysis (September 15, 2026)

---

## Decision 7: Lock Scores for Day 2 Analysis

**Date**: 2026-09-14  
**Decision**: Finalize adjusted pipeline_results.csv for Day 2 forecasting

**Rationale**:
- All critical adjustments complete
- Verification dashboard confirms accuracy
- Ready for downstream analysis & forecasting
- Need stable baseline for Day 2 comparisons

**Impact**:
- Day 2 analysis can proceed with confidence
- Creates audit trail for scoring changes
- Enables before/after comparison

**Status**: ✅ APPROVED & LOCKED

**File**: C:\pipeline-intelligence\pipeline_results.csv (v2, adjusted)

---

## Summary of All Decisions

| Decision | Type | Status | Deals Affected | Value |
|----------|------|--------|---|---|
| Discovery baseline uplift | Policy | ✅ Implemented | 4 critical | +$309K |
| CloudFirst correction | Individual | ✅ Implemented | 1 | +$120K |
| HRPlus/Acme realignment | Individual | ✅ Implemented | 2 | +$85K |
| EComm Co adjustment | Individual | ✅ Implemented | 1 | +$85K |
| Risk level mapping | Policy | ✅ Implemented | All 30 | - |
| Minor adjustments deferral | Policy | ✅ Scheduled | 3 | ~$170K |
| Score lock for Day 2 | Process | ✅ Implemented | All 30 | $1.562M |

---

## Pending Decisions (Day 2)

### D8: Day 2 Validation
**Question**: Do adjusted scores align with sales team's risk assessments?
**Timeline**: Before Day 2 completion
**Owner**: Sales Leadership

### D9: Root Cause Analysis
**Question**: Why was Discovery baseline systematically underscored?
**Options**:
- A) Methodology issue in scoring algorithm
- B) Data quality issue in source system
- C) Intentional conservative stance (document if so)
**Timeline**: Week 1 post-Day 2
**Owner**: Analytics Team

### D10: Future Scoring Updates
**Question**: Update scoring algorithm to prevent future baseline drift?
**Options**:
- A) Implement automated guardrails by stage
- B) Add quarterly recalibration cycle
- C) Require manual approval for outliers
**Timeline**: Post-validation
**Owner**: Product Team

---

## Decision Audit Trail

All decisions documented with:
- ✅ Clear rationale
- ✅ Quantified impact
- ✅ Status tracking
- ✅ Follow-up actions where needed
- ✅ Owner accountability

This log serves as the source of truth for all changes made to Day 1 pipeline scoring.
