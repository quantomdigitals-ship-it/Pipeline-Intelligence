"""
Complete Pipeline: CSV → Parse → Score → Analyze
Phase 3 Integration
"""

import csv
import json
from csv_parser import parse_csv
from pipeline_intelligence import calculate_risk_score
from demo_ai_analyzer import demo_analyze_deal

def process_pipeline(csv_path, output_csv='pipeline_results.csv', output_json='analysis_results.json'):
    """
    Complete pipeline processing:
    1. Parse CSV (auto-detect columns)
    2. Normalize data
    3. Calculate risk scores
    4. Add AI analysis
    5. Export results

    Returns:
        dict: Summary with all deals and analysis
    """

    print("\n" + "="*80)
    print("PIPELINE INTELLIGENCE — COMPLETE ANALYSIS")
    print("="*80)

    # STEP 1: Parse CSV
    print("\n📖 STEP 1: Parsing CSV...")
    normalized_data = parse_csv(csv_path)

    if not normalized_data:
        print("❌ Failed to parse CSV")
        return None

    # STEP 2: Score and Analyze
    print("\n🧮 STEP 2: Calculating risk scores...")
    analyzed_deals = []

    for i, deal in enumerate(normalized_data, 1):
        # Calculate risk score
        scored = calculate_risk_score(deal)

        # Add AI analysis
        ai_analysis = demo_analyze_deal(scored)
        scored['ai_analysis'] = ai_analysis

        analyzed_deals.append(scored)

        # Progress indicator
        if i % 10 == 0:
            print(f"  ✓ Analyzed {i}/{len(normalized_data)} deals")

    # STEP 3: Sort by priority
    print("\n📊 STEP 3: Ranking deals...")
    analyzed_deals.sort(key=lambda x: x['priority_score'], reverse=True)

    # STEP 4: Generate summary
    print("\n📈 STEP 4: Generating summary...")

    total_deals = len(analyzed_deals)
    total_pipeline = sum(d['amount'] for d in analyzed_deals)
    at_risk_deals = [d for d in analyzed_deals if d['risk_score'] >= 60]
    watch_deals = [d for d in analyzed_deals if 30 <= d['risk_score'] < 60]
    healthy_deals = [d for d in analyzed_deals if d['risk_score'] < 30]
    at_risk_revenue = sum(d['amount'] for d in at_risk_deals)

    summary = {
        'metadata': {
            'source_file': csv_path,
            'total_deals_analyzed': total_deals,
            'analysis_complete': True,
        },
        'metrics': {
            'total_pipeline': total_pipeline,
            'total_deals': total_deals,
            'at_risk_revenue': at_risk_revenue,
            'at_risk_percent': round((at_risk_revenue / total_pipeline * 100) if total_pipeline > 0 else 0, 1),
            'at_risk_count': len(at_risk_deals),
            'watch_count': len(watch_deals),
            'healthy_count': len(healthy_deals),
            'avg_risk_score': round(sum(d['risk_score'] for d in analyzed_deals) / len(analyzed_deals), 1) if analyzed_deals else 0,
        },
        'top_5_deals': analyzed_deals[:5],
        'all_deals': analyzed_deals,
    }

    # STEP 5: Export results
    print("\n💾 STEP 5: Exporting results...")

    # Export as CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['opportunity_name', 'company_name', 'amount', 'stage', 'risk_score', 'risk_level', 'priority_score']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for deal in analyzed_deals:
            writer.writerow({
                'opportunity_name': deal['opportunity_name'],
                'company_name': deal['company_name'],
                'amount': deal['amount'],
                'stage': deal['stage'],
                'risk_score': deal['risk_score'],
                'risk_level': deal['risk_level'],
                'priority_score': deal['priority_score'],
            })

    print(f"  ✓ Exported to {output_csv}")

    # Export as JSON (with AI analysis)
    with open(output_json, 'w') as f:
        # Make it JSON serializable
        json_data = []
        for deal in analyzed_deals:
            json_data.append({
                'opportunity_name': deal['opportunity_name'],
                'company_name': deal['company_name'],
                'amount': deal['amount'],
                'stage': deal['stage'],
                'risk_score': deal['risk_score'],
                'risk_level': deal['risk_level'],
                'priority_score': deal['priority_score'],
                'ai_analysis': deal['ai_analysis'],
            })
        json.dump(json_data, f, indent=2)

    print(f"  ✓ Exported to {output_json}")

    # STEP 6: Print summary
    print("\n" + "="*80)
    print("ANALYSIS SUMMARY")
    print("="*80)
    print(f"\n💰 Total Pipeline: ${total_pipeline:,}")
    print(f"⚠️  Revenue at Risk: ${at_risk_revenue:,} ({summary['metrics']['at_risk_percent']}%)")
    print(f"🔴 At-Risk Deals: {len(at_risk_deals)}")
    print(f"🟡 Watch Deals: {len(watch_deals)}")
    print(f"🟢 Healthy Deals: {len(healthy_deals)}")
    print(f"📊 Average Risk Score: {summary['metrics']['avg_risk_score']}/100")

    print("\n" + "="*80)
    print("TOP 5 DEALS REQUIRING ACTION")
    print("="*80)

    for i, deal in enumerate(analyzed_deals[:5], 1):
        print(f"\n{i}. {deal['opportunity_name']} — {deal['company_name']}")
        print(f"   Amount: ${deal['amount']:,} | Risk: {deal['risk_score']}/100")
        print(f"   Why: {deal['ai_analysis']['explanation']}")
        print(f"   Action: {deal['ai_analysis']['recommended_action']}")

    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE")
    print("="*80)

    return summary

if __name__ == '__main__':
    # Run complete pipeline
    summary = process_pipeline('sample-pipeline-raw.csv')

    if summary:
        print("\n✅ Results saved to:")
        print("   • pipeline_results.csv (for spreadsheet view)")
        print("   • analysis_results.json (with AI analysis)")
