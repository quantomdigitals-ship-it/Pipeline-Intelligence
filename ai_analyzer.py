import os
import json
from datetime import datetime
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def build_deal_context(deal: dict) -> str:
    """Build a concise context string for Claude to analyze."""
    context = f"""
Deal: {deal.get('opportunity_name', 'Unknown')} at {deal.get('company_name', 'Unknown')}
Amount: ${deal.get('amount', 0):,}
Stage: {deal.get('stage', 'Unknown')}
Risk Score: {deal.get('risk_score', 0)}/100 ({deal.get('risk_level', 'Unknown')})

Summary: This is a {deal.get('risk_level', 'Unknown').lower()} deal with risk score {deal.get('risk_score', 0)}/100.
"""
    return context.strip()

def analyze_deal_with_claude(deal: dict) -> dict:
    """
    Call Claude API to generate contextual analysis for a deal.

    Args:
        deal: Dict with keys: opportunity_name, company_name, amount, stage,
              risk_score, risk_level

    Returns:
        Dict with keys: explanation, recommended_action, confidence_level
    """
    try:
        context = build_deal_context(deal)

        prompt = f"""{context}

Based on this deal's risk score and stage, provide:
1. A 1-2 sentence explanation of why this deal has this risk level
2. A specific, actionable next step

Format your response as JSON:
{{
    "explanation": "Why this deal is at this risk level",
    "recommended_action": "Specific action to take",
    "confidence_level": "High or Medium or Low"
}}

Only respond with valid JSON, no other text."""

        message = client.messages.create(
            model="claude-opus-5",
            max_tokens=300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract JSON from response
        response_text = message.content[0].text.strip()

        # Try to parse JSON
        analysis = json.loads(response_text)

        return {
            "explanation": analysis.get("explanation", ""),
            "recommended_action": analysis.get("recommended_action", ""),
            "confidence_level": analysis.get("confidence_level", "Medium")
        }

    except json.JSONDecodeError:
        return {
            "explanation": "Unable to parse analysis response",
            "recommended_action": "Review deal details manually",
            "confidence_level": "Low"
        }
    except Exception as e:
        return {
            "explanation": f"Error: {str(e)}",
            "recommended_action": "Check API configuration",
            "confidence_level": "Low"
        }

def analyze_pipeline_with_ai(deals: list) -> list:
    """
    Add AI analysis to a list of scored deals.

    Args:
        deals: List of deal dicts with scoring results

    Returns:
        List of deals with ai_analysis field added
    """
    analyzed_deals = []

    for deal in deals:
        # Get AI analysis
        ai_analysis = analyze_deal_with_claude(deal)

        # Add to deal
        deal_with_analysis = {
            **deal,
            "ai_analysis": ai_analysis
        }
        analyzed_deals.append(deal_with_analysis)

        # Print progress
        print(f"✓ Analyzed: {deal.get('opportunity_name', 'Unknown')}")

    return analyzed_deals

def format_deal_report(deal: dict) -> str:
    """Format a deal with its AI analysis for display."""
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
    # Test with a sample deal
    test_deal = {
        "opportunity_name": "CloudFirst Migration",
        "company_name": "CloudFirst",
        "amount": 120000,
        "stage": "Proposal",
        "risk_score": 57,
        "risk_level": "Watch"
    }

    print("Testing AI Analyzer...")
    analysis = analyze_deal_with_claude(test_deal)
    print("\nAnalysis Result:")
    print(json.dumps(analysis, indent=2))

    print("\n" + "="*60)
    print("Formatted Report:")
    test_deal["ai_analysis"] = analysis
    print(format_deal_report(test_deal))
