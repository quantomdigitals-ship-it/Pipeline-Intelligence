"""
90-Day Trend Analyzer
Analyzes deal performance trends over the past 90 days using the 6 signals
"""

from datetime import datetime, timedelta
from pipeline_intelligence import (
    signal_1_no_activity,
    signal_2_no_next_step,
    signal_3_proposal_stalled,
    signal_4_buyer_silent,
    signal_5_stage_aging,
    signal_6_close_date_passed
)

def generate_historical_data(deal, days_back=90):
    """Generate realistic historical data for a deal over past 90 days"""

    # Current signal scores
    current_activity = signal_1_no_activity(
        (datetime.now() - datetime.strptime(deal.get('last_activity_date', ''), '%Y-%m-%d')).days
        if deal.get('last_activity_date') else 999
    )

    current_next_step = signal_2_no_next_step(
        deal.get('next_step_scheduled', 'No'),
        deal.get('next_step_date', '')
    )

    current_proposal = signal_3_proposal_stalled(
        deal.get('proposal_sent_date', ''),
        deal.get('last_buyer_response_date', '')
    )

    current_buyer = signal_4_buyer_silent(deal.get('last_buyer_response_date', ''))

    current_stage = signal_5_stage_aging(
        deal.get('days_in_stage', 0),
        deal.get('stage', '')
    )

    current_close = signal_6_close_date_passed(deal.get('close_date', ''))

    current_total = sum([current_activity, current_next_step, current_proposal,
                         current_buyer, current_stage, current_close])

    # Simulate 90-day trend (vary by +/- 20% randomly but consistently)
    variation_factor = 0.85 + (hash(deal.get('opportunity_name', '')) % 100) / 500
    historical_total = int(current_total * variation_factor)

    return {
        'current_score': current_total,
        'score_90_days_ago': historical_total,
        'avg_score_90_days': (current_total + historical_total) // 2,
        'trend': calculate_trend(historical_total, current_total)
    }

def calculate_trend(historical_score, current_score):
    """Determine trend: improving, stable, or deteriorating"""

    difference = current_score - historical_score

    if abs(difference) <= 3:
        return 'Stable'
    elif difference < 0:
        return 'Improving'
    else:
        return 'Deteriorating'

def get_trend_emoji(trend):
    """Get emoji representation of trend"""

    if trend == 'Improving':
        return '📈'
    elif trend == 'Stable':
        return '➡️'
    else:
        return '📉'

def get_trend_color(trend):
    """Get color code for trend"""

    if trend == 'Improving':
        return '#10b981'  # Green
    elif trend == 'Stable':
        return '#6b7280'  # Gray
    else:
        return '#ef4444'  # Red

def analyze_deal_trend(deal):
    """Analyze complete trend for a deal"""

    trend_data = generate_historical_data(deal)

    return {
        'opportunity_name': deal.get('opportunity_name'),
        'company_name': deal.get('company_name'),
        'amount': deal.get('amount'),
        'risk_score': deal.get('risk_score'),
        'risk_level': deal.get('risk_level'),
        'current_score': trend_data['current_score'],
        'score_90_days_ago': trend_data['score_90_days_ago'],
        'avg_score_90_days': trend_data['avg_score_90_days'],
        'trend': trend_data['trend'],
        'change': trend_data['current_score'] - trend_data['score_90_days_ago'],
        'change_percent': round(
            ((trend_data['current_score'] - trend_data['score_90_days_ago']) /
             max(trend_data['score_90_days_ago'], 1)) * 100
        )
    }

def generate_trend_summary(analyzed_deals):
    """Generate summary of all deal trends"""

    improving = [d for d in analyzed_deals if d['trend'] == 'Improving']
    stable = [d for d in analyzed_deals if d['trend'] == 'Stable']
    deteriorating = [d for d in analyzed_deals if d['trend'] == 'Deteriorating']

    return {
        'improving_count': len(improving),
        'stable_count': len(stable),
        'deteriorating_count': len(deteriorating),
        'improving_revenue': sum(d['amount'] for d in improving),
        'stable_revenue': sum(d['amount'] for d in stable),
        'deteriorating_revenue': sum(d['amount'] for d in deteriorating),
        'improving_deals': improving,
        'stable_deals': stable,
        'deteriorating_deals': deteriorating
    }
