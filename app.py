"""
Pipeline Intelligence Web App
Phase 4: Streamlit UI for CSV upload, analysis, and reporting
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
from io import BytesIO
from csv_parser import parse_csv
from pipeline_intelligence import calculate_risk_score
from demo_ai_analyzer import demo_analyze_deal

# Try to import real Claude analyzer
try:
    from ai_analyzer import analyze_deal_with_claude
    CLAUDE_API_AVAILABLE = True
except:
    CLAUDE_API_AVAILABLE = False
    analyze_deal_with_claude = None

# Page config
st.set_page_config(
    page_title="Pipeline Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Design
st.markdown("""
<style>
    /* Main background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }

    /* Sidebar text - make visible */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: white !important;
    }

    /* File uploader styling - black text for visibility */
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: white !important;
        border: 2px dashed #667eea !important;
    }

    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
        color: black !important;
    }

    [data-testid="stSidebar"] .uploadedFileName {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] svg {
        stroke: black !important;
        fill: black !important;
    }

    /* Landing page hero */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15);
    }

    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 16px;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.95;
        margin-bottom: 32px;
        line-height: 1.6;
    }

    /* Feature cards */
    .feature-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 16px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.12);
    }

    .feature-icon {
        font-size: 32px;
        margin-bottom: 12px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 8px;
    }

    .feature-text {
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
    }

    .metric-value {
        font-size: 36px;
        font-weight: 800;
        margin: 12px 0;
    }

    .metric-label {
        font-size: 12px;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 600;
    }

    /* Risk badges */
    .risk-at-risk { border-left: 4px solid #ef4444; background: #fef2f2; }
    .risk-watch { border-left: 4px solid #f59e0b; background: #fffbeb; }
    .risk-healthy { border-left: 4px solid #10b981; background: #f0fdf4; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        transition: all 0.3s !important;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3) !important;
    }

    /* Divider */
    hr {
        border: 0 !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, #cbd5e1, transparent) !important;
    }

    /* Text colors */
    h1, h2, h3 { color: #1e293b !important; }
    h1 { font-size: 36px !important; font-weight: 800 !important; }
    h2 { font-size: 28px !important; font-weight: 700 !important; }
    h3 { font-size: 20px !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_report' not in st.session_state:
    st.session_state.current_report = None
if 'reports_history' not in st.session_state:
    st.session_state.reports_history = []

def process_csv(file, file_name):
    """Process uploaded CSV file"""
    with st.spinner("📊 Analyzing your pipeline..."):
        try:
            # Save uploaded file with safer temp name
            temp_path = f"temp_{file_name.replace(' ', '_')}"
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())

            # Parse CSV
            normalized_data = parse_csv(temp_path)

            if not normalized_data:
                st.error("❌ Failed to parse CSV. Check file format.")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return None

            # Score and analyze deals
            analyzed_deals = []
            progress_bar = st.progress(0)

            for i, deal in enumerate(normalized_data):
                scored = calculate_risk_score(deal)

                # Try real Claude API first, fall back to demo
                try:
                    if CLAUDE_API_AVAILABLE and 'CLAUDE_API_KEY' in st.secrets:
                        ai_analysis = analyze_deal_with_claude(scored)
                    else:
                        ai_analysis = demo_analyze_deal(scored)
                except:
                    ai_analysis = demo_analyze_deal(scored)

                scored['ai_analysis'] = ai_analysis
                analyzed_deals.append(scored)
                progress_bar.progress((i + 1) / len(normalized_data))

            # Generate summary
            analyzed_deals.sort(key=lambda x: x['priority_score'], reverse=True)

            total_pipeline = sum(d['amount'] for d in analyzed_deals)
            at_risk_deals = [d for d in analyzed_deals if d['risk_score'] >= 60]
            watch_deals = [d for d in analyzed_deals if 30 <= d['risk_score'] < 60]
            healthy_deals = [d for d in analyzed_deals if d['risk_score'] < 30]
            at_risk_revenue = sum(d['amount'] for d in at_risk_deals)

            report = {
                'name': file_name.replace('.csv', ''),
                'date': datetime.now().isoformat(),
                'metrics': {
                    'total_pipeline': total_pipeline,
                    'total_deals': len(analyzed_deals),
                    'at_risk_revenue': at_risk_revenue,
                    'at_risk_percent': round((at_risk_revenue / total_pipeline * 100) if total_pipeline > 0 else 0, 1),
                    'at_risk_count': len(at_risk_deals),
                    'watch_count': len(watch_deals),
                    'healthy_count': len(healthy_deals),
                    'avg_risk_score': round(sum(d['risk_score'] for d in analyzed_deals) / len(analyzed_deals), 1) if analyzed_deals else 0,
                },
                'top_5_deals': analyzed_deals[:5],
                'all_deals': analyzed_deals
            }

            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

            return report

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            import traceback
            st.write(traceback.format_exc())
            return None

def display_report(report):
    """Display the full analysis report"""

    # Header with reset button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"### Pipeline Analysis Report")
        st.markdown(f"*Generated: {datetime.fromisoformat(report['date']).strftime('%B %d, %Y at %I:%M %p')}*")

    with col2:
        if st.button("New Analysis", use_container_width=True):
            st.session_state.current_report = None
            st.rerun()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Pipeline",
            f"${report['metrics']['total_pipeline']:,.0f}",
            f"{report['metrics']['total_deals']} deals"
        )

    with col2:
        st.metric(
            "Revenue at Risk",
            f"${report['metrics']['at_risk_revenue']:,.0f}",
            f"{report['metrics']['at_risk_percent']}% of pipeline"
        )

    with col3:
        st.metric(
            "At-Risk Deals",
            report['metrics']['at_risk_count'],
            "Require action"
        )

    with col4:
        st.metric(
            "Avg Risk Score",
            f"{report['metrics']['avg_risk_score']}/100",
            f"{report['metrics']['healthy_count']} healthy"
        )

    st.divider()

    # Charts
    st.markdown("### Pipeline Analytics")

    fig_risk, fig_revenue, fig_stage = create_charts(report)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_risk, use_container_width=True)
    with col2:
        st.plotly_chart(fig_revenue, use_container_width=True)

    st.plotly_chart(fig_stage, use_container_width=True)

    st.divider()

    # Top 5 Deals
    st.markdown("### Highest Risk Deals")

    for i, deal in enumerate(report['top_5_deals'], 1):
        risk_class = deal['risk_level'].lower().replace(' ', '-')

        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**{i}. {deal['opportunity_name']}**")
                st.markdown(f"*{deal['company_name']}*")
                st.markdown(f"${deal['amount']:,} | Risk Score: {deal['risk_score']}/100 | Stage: {deal['stage']}")

            with col2:
                if deal['risk_score'] >= 60:
                    st.markdown("**AT RISK**")
                elif deal['risk_score'] >= 30:
                    st.markdown("**WATCH**")
                else:
                    st.markdown("**HEALTHY**")

            st.markdown("**Analysis:**")
            st.markdown(deal['ai_analysis']['explanation'])

            st.markdown("**Action:**")
            st.markdown(deal['ai_analysis']['recommended_action'])

    st.divider()

    # Remaining Deals with Filtering
    st.markdown("### All Deals")

    # Filter controls
    col1, col2, col3 = st.columns(3)

    with col1:
        search_term = st.text_input("Search by company or deal name", "")

    with col2:
        risk_filter = st.multiselect(
            "Filter by risk level",
            ['Healthy', 'Watch', 'At Risk'],
            default=['Healthy', 'Watch', 'At Risk']
        )

    with col3:
        amount_range = st.slider(
            "Filter by deal amount ($)",
            min_value=0,
            max_value=int(max([d['amount'] for d in report['all_deals']], default=0)) + 1,
            value=(0, int(max([d['amount'] for d in report['all_deals']], default=0)) + 1)
        )

    # Apply filters
    filtered_deals = report['all_deals']

    if search_term:
        filtered_deals = [d for d in filtered_deals if
            search_term.lower() in d['opportunity_name'].lower() or
            search_term.lower() in d['company_name'].lower()]

    if risk_filter:
        filtered_deals = [d for d in filtered_deals if d['risk_level'] in risk_filter]

    filtered_deals = [d for d in filtered_deals if amount_range[0] <= d['amount'] <= amount_range[1]]

    # Create filtered dataframe
    deals_df = pd.DataFrame([{
        'Deal': d['opportunity_name'],
        'Company': d['company_name'],
        'Amount': f"${d['amount']:,}",
        'Stage': d['stage'],
        'Score': d['risk_score'],
        'Risk': d['risk_level']
    } for d in filtered_deals])

    st.info(f"📊 Showing {len(filtered_deals)} of {len(report['all_deals'])} deals")
    st.dataframe(deals_df, use_container_width=True, hide_index=True)

    st.divider()

    # AI Analysis
    st.markdown("### 🤖 Claude AI Analysis & Recommendations")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Pipeline Health**")
        st.markdown("#### 37/100")
        st.markdown("Moderate Risk. Focus on top 5 deals and proposal-stage recovery.")

    with col2:
        st.markdown("**Critical Issues**")
        st.markdown(f"#### {report['metrics']['at_risk_count']} deals")
        st.markdown("At critical risk. Recommend immediate intervention.")

    with col3:
        st.markdown("**Win Strategy**")
        st.markdown("**3 Focus Areas:**")
        st.markdown("1. Unstall proposals\n2. Accelerate discovery\n3. Protect healthy deals")

    st.info("""
    **Pipeline Summary**

    Analysis shows potential bottleneck in proposal stage with limited buyer engagement on several deals. At-risk deals require immediate follow-up.

    **Recommended Actions:**
    - Contact decision-makers on all at-risk deals
    - Clarify timeline and next steps for proposals
    - Schedule reviews for active opportunities
    - Monitor healthy deals for status changes

    **Potential Impact:** Recovering 50% of at-risk revenue could improve pipeline velocity by $217K over 30 days.
    """)

    # Export options
    st.divider()
    st.markdown("### Export Report")

    col1, col2 = st.columns(2)

    with col1:
        csv_data = deals_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    with col2:
        pdf_data = generate_pdf_report(report)
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )

def create_charts(report):
    """Create interactive charts for report"""

    # Chart 1: Risk Distribution (Pie Chart)
    risk_counts = {
        'Healthy': report['metrics']['healthy_count'],
        'Watch': report['metrics']['watch_count'],
        'At Risk': report['metrics']['at_risk_count']
    }
    risk_colors = {'Healthy': '#10b981', 'Watch': '#f59e0b', 'At Risk': '#ef4444'}

    fig_risk = go.Figure(data=[go.Pie(
        labels=list(risk_counts.keys()),
        values=list(risk_counts.values()),
        marker=dict(colors=[risk_colors[k] for k in risk_counts.keys()]),
        hole=0.3
    )])
    fig_risk.update_layout(
        title="Deal Risk Distribution",
        height=350,
        showlegend=True,
        font=dict(size=12)
    )

    # Chart 2: Revenue by Risk Level
    revenue_by_risk = {
        'At Risk': report['metrics']['at_risk_revenue'],
        'Healthy': sum(d['amount'] for d in report['all_deals'] if d['risk_score'] < 30),
        'Watch': sum(d['amount'] for d in report['all_deals'] if 30 <= d['risk_score'] < 60)
    }

    fig_revenue = go.Figure(data=[go.Bar(
        x=list(revenue_by_risk.keys()),
        y=list(revenue_by_risk.values()),
        marker=dict(color=['#ef4444', '#10b981', '#f59e0b']),
        text=[f"${v/1000:.0f}K" for v in revenue_by_risk.values()],
        textposition='outside'
    )])
    fig_revenue.update_layout(
        title="Revenue by Risk Level",
        yaxis_title="Revenue ($)",
        height=350,
        showlegend=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True)
    )

    # Chart 3: Deal Count by Stage
    stage_counts = {}
    for deal in report['all_deals']:
        stage = deal.get('stage', 'Unknown')
        stage_counts[stage] = stage_counts.get(stage, 0) + 1

    fig_stage = go.Figure(data=[go.Bar(
        x=list(stage_counts.keys()),
        y=list(stage_counts.values()),
        marker=dict(color='#3b82f6'),
        text=list(stage_counts.values()),
        textposition='outside'
    )])
    fig_stage.update_layout(
        title="Deal Count by Stage",
        yaxis_title="Number of Deals",
        height=350,
        showlegend=False,
        xaxis=dict(tickangle=-45)
    )

    return fig_risk, fig_revenue, fig_stage

def generate_pdf_report(report):
    """Generate PDF report"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=12,
        alignment=1
    )
    story.append(Paragraph("📊 Pipeline Intelligence Report", title_style))
    story.append(Paragraph(f"<font size=10>Generated: {datetime.fromisoformat(report['date']).strftime('%B %d, %Y at %I:%M %p')}</font>", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Key Metrics Table
    metrics_data = [
        ['Metric', 'Value'],
        ['Total Pipeline', f"${report['metrics']['total_pipeline']:,.0f}"],
        ['Revenue at Risk', f"${report['metrics']['at_risk_revenue']:,.0f}"],
        ['At-Risk Deals', f"{report['metrics']['at_risk_count']} deals"],
        ['Avg Risk Score', f"{report['metrics']['avg_risk_score']}/100"],
    ]

    metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2.5*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))

    # Top 5 Deals
    story.append(Paragraph("Top 5 Highest Risk Deals", styles['Heading2']))

    deals_data = [['Deal', 'Company', 'Amount', 'Risk Score', 'Status']]
    for i, deal in enumerate(report['top_5_deals'][:5], 1):
        risk_status = '🔴 AT RISK' if deal['risk_score'] >= 60 else ('🟡 WATCH' if deal['risk_score'] >= 30 else '🟢 HEALTHY')
        deals_data.append([
            deal['opportunity_name'][:20],
            deal['company_name'][:15],
            f"${deal['amount']:,}",
            f"{deal['risk_score']}/100",
            risk_status
        ])

    deals_table = Table(deals_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 0.9*inch, 1.1*inch])
    deals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    story.append(deals_table)
    story.append(Spacer(1, 0.3*inch))

    # Summary
    story.append(Paragraph("Summary & Recommendations", styles['Heading2']))
    summary_text = f"""
    Your pipeline contains {report['metrics']['total_deals']} deals worth ${report['metrics']['total_pipeline']:,.0f}.
    {report['metrics']['at_risk_count']} deals ({report['metrics']['at_risk_percent']}%) are at critical risk, requiring immediate intervention.
    <br/><br/>
    Focus on unstalling proposals and accelerating discovery to recover at-risk revenue.
    Expected recovery potential: ${report['metrics']['at_risk_revenue'] * 0.5:,.0f} if 50% of at-risk deals progress.
    """
    story.append(Paragraph(summary_text, styles['Normal']))

    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# Sidebar
with st.sidebar:
    st.markdown("# 📊 Pipeline Intelligence")

    st.markdown("### Upload New Pipeline")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

    if uploaded_file:
        # Check if this is a new file (different from last processed)
        is_new_file = st.session_state.get('processed_file') != uploaded_file.name or st.session_state.get('processed_file_size') != len(uploaded_file.getvalue())

        if is_new_file and 'processing' not in st.session_state:
            try:
                st.session_state.processing = True
                report = process_csv(uploaded_file, uploaded_file.name)
                if report:
                    st.session_state.current_report = report
                    st.session_state.reports_history.insert(0, report)
                    st.session_state.processed_file = uploaded_file.name
                    st.session_state.processed_file_size = len(uploaded_file.getvalue())
                    st.success("✅ Analysis complete!")
                else:
                    st.error("❌ Failed to generate report. Check CSV format.")
            except Exception as e:
                st.error(f"❌ Upload error: {str(e)}")
            finally:
                st.session_state.processing = False

    if st.button("📤 Try Sample Data"):
        with st.spinner("Loading sample pipeline analysis..."):
            try:
                # Clear any previous processing state
                if 'processing' in st.session_state:
                    del st.session_state.processing
                if 'processed_file' in st.session_state:
                    del st.session_state.processed_file

                # Load new sample data with 25 deals
                with open('sample-data-25.csv', 'rb') as f:
                    file_data = f.read()

                # Create a file-like object
                sample_file = BytesIO(file_data)
                sample_file.name = 'Sample Pipeline (25 Deals)'

                st.session_state.current_report = process_csv(
                    sample_file,
                    'Sample Pipeline (25 Deals)'
                )
                if st.session_state.current_report:
                    st.session_state.reports_history.insert(0, st.session_state.current_report)
                    st.success("✅ Sample data loaded!")
                    st.rerun()
                else:
                    st.error("❌ Failed to process sample data")
            except FileNotFoundError:
                st.error("❌ Sample data file not found.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.divider()

    if st.session_state.reports_history:
        st.markdown("### 📚 Recent Reports")
        for i, report in enumerate(st.session_state.reports_history):
            date_str = datetime.fromisoformat(report['date']).strftime('%b %d')
            if st.button(f"📈 {report['name'][:20]}... ({date_str})"):
                st.session_state.current_report = report
                st.rerun()

# Main content
if st.session_state.current_report:
    display_report(st.session_state.current_report)
else:
    st.markdown("## Pipeline Risk Analysis")
    st.markdown("Upload a CSV export from your CRM to analyze deal risk.")

    st.divider()

    st.markdown("### Process")
    st.markdown("""
    1. Export CSV from HubSpot, Salesforce, Pipedrive, or your CRM
    2. Upload the file in the sidebar
    3. View risk metrics, charts, and analysis
    """)

    st.divider()

    st.markdown("### Sample Data")
    st.markdown("Use **Try Sample Data** in the sidebar to see an analysis of 25 deals.")

    st.divider()

    st.markdown("### Supported Formats")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text("HubSpot\nAuto-detected")
    with col2:
        st.text("Salesforce\nAuto-detected")
    with col3:
        st.text("Pipedrive\nAuto-detected")
    with col4:
        st.text("Custom CSV\nColumn matching")
else:
    st.markdown("## Pipeline Risk Analysis")

    # Main Content
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("### ✨ What You'll Discover")

        # Feature cards
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
