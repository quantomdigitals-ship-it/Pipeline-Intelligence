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
        explanation = "Deal has stalled with no buyer contact for 20+ days. No decision timeline defined. Approval process unclear."
        action = "Contact buyer to confirm project priority and decision timeline. Escalate if no response within 48 hours."
    elif risk_score >= 60:
        explanation = "Deal aging in current stage with limited activity. Buyer engagement has declined in past 2 weeks."
        action = "Schedule call to establish next steps and decision date. Clarify remaining questions or concerns."
    elif risk_score >= 40:
        explanation = "Deal showing slower-than-expected progress. Activity declining but still moving forward."
        action = "Increase touch frequency. Identify any obstacles or competitive threats blocking forward momentum."
    else:
        explanation = "Deal progressing on schedule with regular buyer engagement and defined next steps."
        action = "Continue current cadence. Monitor for any changes in buyer engagement or timeline."

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
    print("PIPELINE INTELLIGENCE - ANALYSIS DEMO")
    print("="*80)

    for deal in test_deals:
        analysis = demo_analyze_deal(deal)
        deal["ai_analysis"] = analysis
        print(format_deal_report(deal))
        print("\n" + "-"*80 + "\n")

    print("Demo mode: Analysis based on deal metrics and activity patterns.")
    print("\nFor real Claude AI analysis, add ANTHROPIC_API_KEY to Streamlit secrets.")
