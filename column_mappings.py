# CRM Column Mapping Definitions
# Maps vendor-specific column names to our standard fields

COLUMN_MAPPINGS = {
    'hubspot': {
        'opportunity_name': ['dealname', 'deal name', 'name'],
        'company_name': ['company', 'company name', 'associatedcompany'],
        'deal_value': ['amount', 'deal amount', 'dealstage', 'value', 'deal value'],
        'pipeline_stage': ['dealstage', 'stage', 'pipeline stage', 'hs_pipeline_stage'],
        'last_activity_date': ['hs_lastactivity', 'last activity date', 'lastactivitydate'],
        'next_step_scheduled': ['hs_nextStep_scheduled', 'next step', 'next_step_scheduled'],
        'next_step_date': ['hs_nextStep_date', 'next step date', 'next_step_date'],
        'proposal_sent_date': ['proposal_sent', 'proposal sent date', 'hs_proposal_date'],
        'last_buyer_response_date': ['last_buyer_response', 'buyer response', 'hs_buyer_response_date'],
        'stakeholder_count': ['stakeholder', 'stakeholders', 'number of stakeholders'],
        'expected_close_date': ['closedate', 'close date', 'expected close date', 'hs_closedate'],
        'days_in_stage': ['days_in_stage', 'time in stage', 'stage age'],
    },
    'salesforce': {
        'opportunity_name': ['name', 'opportunity name', 'opportunity'],
        'company_name': ['accountname', 'account name', 'company'],
        'deal_value': ['amount', 'opportunity amount', 'estimated value'],
        'pipeline_stage': ['stagename', 'stage', 'sales stage'],
        'last_activity_date': ['lastactivitydate', 'last activity', 'last activity date'],
        'next_step_scheduled': ['next_step', 'next step scheduled'],
        'next_step_date': ['next_step_date', 'next step date'],
        'proposal_sent_date': ['description', 'proposal date'],
        'last_buyer_response_date': ['last_update_from_buyer', 'buyer response date'],
        'stakeholder_count': ['number_of_contacts', 'contact count', 'stakeholders'],
        'expected_close_date': ['closedate', 'close date', 'expected close date'],
        'days_in_stage': ['stagename', 'stage tenure'],
    },
    'pipedrive': {
        'opportunity_name': ['title', 'deal title', 'name'],
        'company_name': ['org_id', 'organization', 'company'],
        'deal_value': ['value', 'deal value', 'amount'],
        'pipeline_stage': ['stage', 'pipeline stage', 'status'],
        'last_activity_date': ['add_time', 'update_time', 'last activity'],
        'next_step_scheduled': ['next_step_title', 'next step'],
        'next_step_date': ['next_step_date', 'next step date'],
        'proposal_sent_date': ['custom_proposal_date'],
        'last_buyer_response_date': ['custom_response_date'],
        'stakeholder_count': ['custom_stakeholders', 'stakeholder count'],
        'expected_close_date': ['expected_close_date', 'close date', 'won_time'],
        'days_in_stage': ['add_time', 'stage duration'],
    },
    'generic': {
        'opportunity_name': ['deal', 'opportunity', 'deal name', 'name', 'title'],
        'company_name': ['company', 'account', 'company name', 'organization'],
        'deal_value': ['value', 'amount', 'deal value', 'revenue'],
        'pipeline_stage': ['stage', 'status', 'pipeline stage'],
        'last_activity_date': ['last activity', 'activity date', 'updated'],
        'next_step_scheduled': ['next step', 'next action'],
        'next_step_date': ['next step date', 'action date'],
        'proposal_sent_date': ['proposal date', 'proposal sent'],
        'last_buyer_response_date': ['buyer response', 'response date'],
        'stakeholder_count': ['stakeholders', 'contacts', 'people'],
        'expected_close_date': ['close date', 'expected close'],
        'days_in_stage': ['days in stage', 'stage duration'],
    }
}

# Required fields (must be present)
REQUIRED_FIELDS = ['opportunity_name', 'company_name', 'deal_value', 'pipeline_stage']

# Optional fields (nice to have)
OPTIONAL_FIELDS = [
    'last_activity_date',
    'next_step_scheduled',
    'next_step_date',
    'proposal_sent_date',
    'last_buyer_response_date',
    'stakeholder_count',
    'expected_close_date',
    'days_in_stage'
]
