"""
Demo version of AI analyzer showing expected output format.
Use this to test the integration without API calls.
"""

import json

def demo_analyze_deal(deal: dict) -> dict:
    """Mock analysis for demonstration."""
    risk_score = deal.get('risk_score', 0)
    stage = deal.get('stage', 'Unknown')
    amount = deal.get('amount', 0)

    # Generate contextual response based on risk profile
    if risk_score >= 80:
        explanation = "Deal has been stalled in proposal stage for 3+ weeks with zero buyer engagement, indicating approval blockers or lost interest."
        action = "Schedule urgent stakeholder alignment call to identify decision obstacles."
    elif risk_score >= 60:
        explanation = "Deal is aging in current stage faster than baseline, with limited next-step definition blocking momentum."
        action = "Request formal timeline from buyer with specific decision dates and next touchpoint."
    elif risk_score >= 40:
        explanation = "Deal shows early warning signs with long gaps between activities, suggesting buyer deprioritization."
        action = "Confirm buyer still engaged; propose trial or pilot to re-energize discussion."
    else:
        explanation = "Deal is progressing normally with active engagement and defined next steps."
        action = "Continue standard follow-up cadence and prepare for next stage gate."

    return {
        "explanation": explanation,
        "recommended_action": action,
        "confidence_level": "High"
    }

def format_deal_report(deal: dict) -> str:
    """Format a deal with its analysis for display."""
    report = f"""
{deal['opportunity_name']} — {deal['company_name']}
Amount: ${deal['amount']:,} | Stage: {deal['stage']}
Risk Score: {deal['risk_score']}/100 ({deal['risk_level']})

WHY AT RISK:
{deal.get('ai_analysis', {}).get('explanation', 'N/A')}

RECOMMENDED ACTION:
{deal.get('ai_analysis', {}).get('recommended_action', 'N/A')}

Confidence: {deal.get('ai_analysis', {}).get('confidence_level', 'N/A')}
"""
    return report.strip()

if __name__ == "__main__":
    # Demo with sample deals
    test_deals = [
        {
            "opportunity_name": "CRM Implementation",
            "company_name": "CRMPro",
            "amount": 95000,
            "stage": "Discovery",
            "risk_score": 75,
            "risk_level": "At Risk"
        },
        {
            "opportunity_name": "Compliance Automation",
            "company_name": "ComplianceCo",
            "amount": 67000,
            "stage": "Proposal",
            "risk_score": 90,
            "risk_level": "At Risk"
        },
        {
            "opportunity_name": "CloudFirst Migration",
            "company_name": "CloudFirst",
            "amount": 120000,
            "stage": "Proposal",
            "risk_score": 57,
            "risk_level": "Watch"
        }
    ]

    print("="*80)
    print("PIPELINE INTELLIGENCE — AI ANALYSIS DEMO")
    print("="*80)

    for deal in test_deals:
        analysis = demo_analyze_deal(deal)
        deal["ai_analysis"] = analysis
        print(format_deal_report(deal))
        print("\n" + "-"*80 + "\n")

    print("✅ This is what the real AI analyzer will produce.")
    print("\nTo enable real Claude API analysis:")
    print("1. Set ANTHROPIC_API_KEY environment variable")
    print("2. Run: python pipeline_with_ai.py")
