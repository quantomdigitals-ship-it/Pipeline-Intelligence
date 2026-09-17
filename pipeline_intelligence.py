import csv
from datetime import datetime
from config import STAGE_DEFAULTS, RISK_LEVELS

def calculate_days_since(date_str: str) -> int:
    if not date_str:
        return 999
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        days = (datetime.now() - date).days
        return max(0, days)
    except:
        return 999

def signal_1_no_activity(days_since_activity: int) -> int:
    if days_since_activity == 999:
        return 0
    if days_since_activity <= 3:
        return 0
    elif days_since_activity <= 7:
        return 5
    elif days_since_activity <= 14:
        return 10
    elif days_since_activity <= 30:
        return 15
    else:
        return 20

def signal_2_no_next_step(next_step_scheduled: str, next_step_date: str) -> int:
    if next_step_scheduled == 'Yes' and next_step_date:
        try:
            next_date = datetime.strptime(next_step_date, '%Y-%m-%d')
            days_until = (next_date - datetime.now()).days
            if days_until <= 3:
                return 0
            elif days_until <= 7:
                return 10
            else:
                return 15
        except:
            return 20
    else:
        return 20

def signal_3_proposal_stalled(proposal_sent_date: str, last_buyer_response_date: str) -> int:
    if not proposal_sent_date:
        return 0
    days_since_proposal = calculate_days_since(proposal_sent_date)
    if days_since_proposal == 999:
        return 0
    if days_since_proposal < 7:
        return 0
    if last_buyer_response_date:
        try:
            proposal_date = datetime.strptime(proposal_sent_date, '%Y-%m-%d')
            response_date = datetime.strptime(last_buyer_response_date, '%Y-%m-%d')
            if response_date > proposal_date:
                return 0
        except:
            pass
    if days_since_proposal <= 14:
        return 10
    else:
        return 20

def signal_4_buyer_silent(last_buyer_response_date: str) -> int:
    days_since_response = calculate_days_since(last_buyer_response_date)
    if days_since_response == 999:
        return 0
    if days_since_response <= 7:
        return 0
    elif days_since_response <= 14:
        return 3
    elif days_since_response <= 30:
        return 5
    else:
        return 10

def signal_5_stage_aging(days_in_stage: int, stage: str) -> int:
    expected_days = STAGE_DEFAULTS.get(stage, 10)
    if days_in_stage <= expected_days:
        return 0
    percent_over = ((days_in_stage - expected_days) / expected_days) * 100
    if percent_over <= 20:
        return 5
    elif percent_over <= 40:
        return 10
    else:
        return 15

def signal_6_close_date_passed(close_date: str) -> int:
    days_until_close = calculate_days_since(close_date)
    if days_until_close == 999:
        return 0
    days_past = -days_until_close
    if days_past <= 0:
        return 0
    elif days_past <= 7:
        return 5
    elif days_past <= 14:
        return 10
    else:
        return 15

def bonus_single_threaded(stakeholder_count: int, days_in_stage: int) -> int:
    try:
        stakeholder_count = int(stakeholder_count)
        days_in_stage = int(days_in_stage)
        if stakeholder_count == 1 and days_in_stage > 10:
            return 10
    except:
        pass
    return 0

def get_risk_level(risk_score: int) -> str:
    if risk_score <= 29:
        return 'Healthy'
    elif risk_score <= 59:
        return 'Watch'
    else:
        return 'At Risk'

def calculate_priority_score(risk_score: int, amount: int) -> float:
    try:
        amount = int(amount)
        normalized_amount = amount / 10000
        priority = risk_score * normalized_amount
        return round(priority, 1)
    except:
        return 0

def calculate_risk_score(row: dict) -> dict:
    days_since_activity = calculate_days_since(row.get('last_activity_date', ''))
    signal1 = signal_1_no_activity(days_since_activity)
    signal2 = signal_2_no_next_step(row.get('next_step_scheduled', 'No'), row.get('next_step_date', ''))
    signal3 = signal_3_proposal_stalled(row.get('proposal_sent_date', ''), row.get('last_buyer_response_date', ''))
    signal4 = signal_4_buyer_silent(row.get('last_buyer_response_date', ''))
    signal5 = signal_5_stage_aging(int(row.get('days_in_stage', 0)), row.get('pipeline_stage', 'Qualification'))
    signal6 = signal_6_close_date_passed(row.get('expected_close_date', ''))
    bonus = bonus_single_threaded(row.get('stakeholder_count', 1), row.get('days_in_stage', 0))
    
    risk_score = min(100, signal1 + signal2 + signal3 + signal4 + signal5 + signal6 + bonus)
    risk_level = get_risk_level(risk_score)
    amount = int(row.get('deal_value', 0))
    priority_score = calculate_priority_score(risk_score, amount)
    
    return {
        'opportunity_name': row.get('opportunity_name', ''),
        'company_name': row.get('company_name', ''),
        'amount': amount,
        'stage': row.get('pipeline_stage', ''),
        'risk_score': risk_score,
        'risk_level': risk_level,
        'priority_score': priority_score,
    }

def analyze_pipeline(csv_path: str) -> dict:
    results = []
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                result = calculate_risk_score(row)
                results.append(result)
    except FileNotFoundError:
        print(f'Error: Could not find {csv_path}')
        return None
    except Exception as e:
        print(f'Error reading CSV: {e}')
        return None
    
    print(f'\n📊 Loaded {len(results)} deals from {csv_path}\n')
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

def print_summary(summary: dict):
    if not summary:
        return
    
    print('=' * 80)
    print('PIPELINE INTELLIGENCE — RISK ANALYSIS')
    print('=' * 80)
    
    print(f'\n💰 TOTAL PIPELINE: ${summary["total_pipeline"]:,}')
    print(f'⚠️  REVENUE AT RISK: ${summary["at_risk_revenue"]:,} ({summary["at_risk_percent"]}%)')
    print(f'🔴 AT-RISK DEALS: {summary['at_risk_count']}')
    print(f'🟡 WATCH DEALS: {summary['watch_count']}')
    print(f'🟢 HEALTHY DEALS: {summary['healthy_count']}')
    print(f'📊 AVERAGE RISK SCORE: {summary['avg_risk_score']}/100')
    
    print('\n' + '=' * 80)
    print('TOP 5 DEALS TO ACT ON')
    print('=' * 80)
    
    for i, deal in enumerate(summary['top_5_deals'], 1):
        print(f'\n{i}. {deal["opportunity_name"]} — {deal["company_name"]}')
        print(f'   Amount: ${deal["amount"]:,} | Score: {deal["risk_score"]}/100 ({deal["risk_level"]})')

def export_results(summary: dict, output_path: str = 'pipeline_results.csv'):
    if not summary:
        return
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['opportunity_name', 'company_name', 'amount', 'stage', 'risk_score', 'risk_level', 'priority_score']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for deal in summary['all_deals']:
                writer.writerow({
                    'opportunity_name': deal['opportunity_name'],
                    'company_name': deal['company_name'],
                    'amount': deal['amount'],
                    'stage': deal['stage'],
                    'risk_score': deal['risk_score'],
                    'risk_level': deal['risk_level'],
                    'priority_score': deal['priority_score'],
                })
        
        print(f'\n✅ Results exported to {output_path}')
    except Exception as e:
        print(f'Error exporting results: {e}')

if __name__ == '__main__':
    summary = analyze_pipeline('sample-pipeline-raw.csv')
    if summary:
        print_summary(summary)
        export_results(summary, 'pipeline_results.csv')
        print('\n' + '=' * 80)
        print('✅ ANALYSIS COMPLETE')
        print('=' * 80)
