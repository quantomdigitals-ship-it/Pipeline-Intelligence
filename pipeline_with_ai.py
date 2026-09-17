import csv
from pipeline_intelligence import analyze_pipeline, calculate_risk_score
from ai_analyzer import analyze_deal_with_claude

def analyze_pipeline_full(csv_path: str) -> dict:
    """
    Full pipeline analysis: scoring + AI explanations.

    Args:
        csv_path: Path to CSV file with deal data

    Returns:
        Dict with summary and deals (with AI analysis added)
    """
    results = []
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Calculate risk score
                result = calculate_risk_score(row)

                # Add AI analysis for high-risk deals (optional: only score 50+)
                if result['risk_score'] >= 30:  # Watch or At Risk
                    print(f"🤖 Analyzing: {result['opportunity_name']}...")
                    ai_analysis = analyze_deal_with_claude(result)
                    result['ai_analysis'] = ai_analysis
                else:
                    result['ai_analysis'] = None

                results.append(result)
    except FileNotFoundError:
        print(f'Error: Could not find {csv_path}')
        return None
    except Exception as e:
        print(f'Error reading CSV: {e}')
        return None

    print(f'\n📊 Analyzed {len(results)} deals with AI insights\n')

    # Build summary
    results_sorted = sorted(results, key=lambda x: x['priority_score'], reverse=True)
    total_pipeline = sum(r['amount'] for r in results)
    at_risk_deals = [r for r in results if r['risk_score'] >= 60]
    at_risk_revenue = sum(r['amount'] for r in at_risk_deals)
    watch_deals = [r for r in results if 30 <= r['risk_score'] <= 59]
    healthy_deals = [r for r in results if r['risk_score'] <= 29]

    summary = {
        'total_deals': len(results),
        'total_pipeline': total_pipeline,
        'at_risk_revenue': at_risk_revenue,
        'at_risk_percent': round((at_risk_revenue / total_pipeline * 100) if total_pipeline > 0 else 0, 1),
        'at_risk_count': len(at_risk_deals),
        'watch_count': len(watch_deals),
        'healthy_count': len(healthy_deals),
        'avg_risk_score': round(sum(r['risk_score'] for r in results) / len(results), 1) if results else 0,
        'top_5_deals': results_sorted[:5],
        'all_deals': results_sorted
    }

    return summary

def print_full_analysis(summary: dict):
    """Print analysis with AI insights for top deals."""
    if not summary:
        return

    print('=' * 80)
    print('PIPELINE INTELLIGENCE — RISK ANALYSIS + AI INSIGHTS')
    print('=' * 80)

    print(f'\n💰 TOTAL PIPELINE: ${summary["total_pipeline"]:,}')
    print(f'⚠️  REVENUE AT RISK: ${summary["at_risk_revenue"]:,} ({summary["at_risk_percent"]}%)')
    print(f'🔴 AT-RISK DEALS: {summary["at_risk_count"]}')
    print(f'🟡 WATCH DEALS: {summary["watch_count"]}')
    print(f'🟢 HEALTHY DEALS: {summary["healthy_count"]}')
    print(f'📊 AVERAGE RISK SCORE: {summary["avg_risk_score"]}/100')

    print('\n' + '=' * 80)
    print('TOP 5 DEALS TO ACT ON (WITH AI ANALYSIS)')
    print('=' * 80)

    for i, deal in enumerate(summary['top_5_deals'], 1):
        print(f'\n{i}. {deal["opportunity_name"]} — {deal["company_name"]}')
        print(f'   Amount: ${deal["amount"]:,} | Score: {deal["risk_score"]}/100 ({deal["risk_level"]})')

        if deal.get('ai_analysis'):
            print(f'\n   📌 WHY AT RISK:')
            print(f'      {deal["ai_analysis"]["explanation"]}')
            print(f'\n   ✅ RECOMMENDED ACTION:')
            print(f'      {deal["ai_analysis"]["recommended_action"]}')
            print(f'\n   Confidence: {deal["ai_analysis"]["confidence_level"]}')

if __name__ == '__main__':
    print("Starting full analysis with AI insights...\n")
    summary = analyze_pipeline_full('sample-pipeline-raw.csv')
    if summary:
        print_full_analysis(summary)
        print('\n' + '=' * 80)
        print('✅ ANALYSIS COMPLETE WITH AI INSIGHTS')
        print('=' * 80)
