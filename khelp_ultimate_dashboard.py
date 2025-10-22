#!/usr/bin/env python3
"""
KHELP ULTIMATE Strategic Intelligence Dashboard
Complete annual planning toolkit with:
- Organization (customer account) analysis
- Engineering involvement tracking
- Engineering team breakdown
- First Response Time
- Root cause analysis
"""

import warnings
import logging
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

# Suppress Streamlit's internal Plotly deprecation warnings
logging.getLogger('streamlit').setLevel(logging.ERROR)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# Additional suppression for plotly/streamlit warnings
import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")

st.set_page_config(
    page_title="KHELP Ultimate Strategic Dashboard",
    page_icon="🎯",
    layout="wide"
)

# Suppress Streamlit warning display in logs
import streamlit.logger
streamlit.logger.get_logger = lambda name: logging.getLogger(name)
logging.getLogger('streamlit.runtime.scriptrunner_utils.script_run_context').setLevel(logging.ERROR)
logging.getLogger('streamlit.elements.plotly_chart').setLevel(logging.ERROR)
logging.getLogger('streamlit').setLevel(logging.ERROR)

# Load all data
@st.cache_data(ttl=10)
def load_comprehensive_data():
    """Load all comprehensive CSV files"""
    files = os.listdir('.')
    
    def get_latest(pattern):
        matches = [(f, os.path.getmtime(f)) for f in files if pattern in f and f.endswith('.csv')]
        return sorted(matches, key=lambda x: x[1])[-1][0] if matches else None
    
    data = {}
    
    # Load all datasets with specific file names
    try:
        if os.path.exists('khelp_organizations_latest.csv'):
            data['orgs'] = pd.read_csv('khelp_organizations_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_engineering_latest.csv'):
            data['eng_summary'] = pd.read_csv('khelp_engineering_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_engineering_by_team_latest.csv'):
            data['eng_teams'] = pd.read_csv('khelp_engineering_by_team_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_engineering_by_severity_latest.csv'):
            data['eng_severity'] = pd.read_csv('khelp_engineering_by_severity_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_categories_engineering_latest.csv'):
            data['cat_eng'] = pd.read_csv('khelp_categories_engineering_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_frt_latest.csv'):
            data['frt'] = pd.read_csv('khelp_frt_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_monthly_latest.csv'):
            data['monthly'] = pd.read_csv('khelp_monthly_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_resolution_latest.csv'):
            data['resolution'] = pd.read_csv('khelp_resolution_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_assignee_performance_latest.csv'):
            data['assignees'] = pd.read_csv('khelp_assignee_performance_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_contributor_performance_latest.csv'):
            data['contributors'] = pd.read_csv('khelp_contributor_performance_latest.csv')
    except:
        pass
    
    try:
        if os.path.exists('khelp_support_types_latest.csv'):
            data['support_types'] = pd.read_csv('khelp_support_types_latest.csv')
    except:
        pass
    
    # Load AI categorization results (if available)
    try:
        if os.path.exists('categorization_suggestions_latest.csv'):
            data['ai_categories'] = pd.read_csv('categorization_suggestions_latest.csv')
    except:
        pass
    
    # Load dual-axis categorization results
    try:
        if os.path.exists('categorization_dual_axis_20251021_171333.csv'):
            data['dual_axis'] = pd.read_csv('categorization_dual_axis_20251021_171333.csv')
    except:
        pass
    
    return data

data = load_comprehensive_data()

# Header
st.markdown("""
<h1 style='text-align: center; color: #1f77b4; margin-bottom: 2rem;'>
🎯 KHELP Ultimate Strategic Dashboard
</h1>
<p style='text-align: center; font-size: 1.2rem;'>
<strong>Annual Planning 2026</strong> | Comprehensive Intelligence Report
</p>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Select View", [
    "🎯 Executive Summary",
    "🏢 Customer Intelligence",
    "🔧 Engineering Involvement",
    "👥 Team Scorecard",
    "⚡ Response & Resolution",
    "🧪 AI Category Insights",
    "📊 Complete Data Export"
], label_visibility="collapsed")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 Refresh", width="stretch"):
    st.cache_data.clear()
    st.rerun()

# ==================
# EXECUTIVE SUMMARY
# ==================
if page == "🎯 Executive Summary":
    st.header("Executive Summary - 2026 Annual Planning")
    
    # 8 Key Performance Indicators
    st.subheader("📊 2025 Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    if 'monthly' in data:
        total_2024 = data['monthly'][data['monthly']['Year'] == 2024]['Created'].sum()
        total_2025 = data['monthly'][data['monthly']['Year'] == 2025]['Created'].sum()
        
        with col1:
            st.metric(
                "Total Tickets",
                f"{total_2025:,}",
                f"{((total_2025-total_2024)/total_2024*100):.1f}%",
                delta_color="inverse"
            )
        
        with col2:
            if 'eng_summary' in data:
                eng_2025_rate = float(data['eng_summary'][data['eng_summary']['Metric'] == 'Engineering Involvement Rate']['2025_Value'].values[0].rstrip('%'))
                eng_2024_rate = float(data['eng_summary'][data['eng_summary']['Metric'] == 'Engineering Involvement Rate']['2024_Value'].values[0].rstrip('%'))
                change = eng_2025_rate - eng_2024_rate
                st.metric(
                    "% Requiring Engineering",
                    f"{eng_2025_rate:.1f}%",
                    f"{change:+.1f}pp",
                    delta_color="inverse"
                )
        
        with col3:
            if 'frt' in data:
                frt_2024_avg = data['frt']['2024_Avg_Hours'].mean()
                frt_2025_avg = data['frt']['2025_Avg_Hours'].mean()
                st.metric(
                    "Avg First Response",
                    f"{frt_2025_avg:.0f}hrs",
                    f"{((frt_2025_avg-frt_2024_avg)/frt_2024_avg*100):.0f}%",
                    delta_color="inverse"
                )
        
        with col4:
            if 'resolution' in data:
                avg_res_2025 = data['resolution']['2025_Avg_Days'].mean()
                avg_res_2024 = data['resolution']['2024_Avg_Days'].mean()
                st.metric(
                    "Avg Resolution Time",
                    f"{avg_res_2025:.0f}d",
                    f"{((avg_res_2025-avg_res_2024)/avg_res_2024*100):.0f}%",
                    delta_color="inverse"
                )
    
    # Second row of KPIs - Resolution by Severity
    st.markdown("### Resolution Time by Severity")
    col5, col6, col7, col8 = st.columns(4)
    
    if 'resolution' in data:
        df_resolution = data['resolution']
        
        # Blocker
        with col5:
            blocker_2025 = df_resolution[df_resolution['Severity'] == 'Blocker']['2025_Avg_Days'].values
            blocker_2024 = df_resolution[df_resolution['Severity'] == 'Blocker']['2024_Avg_Days'].values
            if len(blocker_2025) > 0 and len(blocker_2024) > 0:
                st.metric(
                    "Blocker Avg Resolution",
                    f"{blocker_2025[0]:.0f}d",
                    f"{((blocker_2025[0]-blocker_2024[0])/blocker_2024[0]*100):.0f}%",
                    delta_color="inverse"
                )
        
        # Critical
        with col6:
            critical_2025 = df_resolution[df_resolution['Severity'] == 'Critical']['2025_Avg_Days'].values
            critical_2024 = df_resolution[df_resolution['Severity'] == 'Critical']['2024_Avg_Days'].values
            if len(critical_2025) > 0 and len(critical_2024) > 0:
                st.metric(
                    "Critical Avg Resolution",
                    f"{critical_2025[0]:.0f}d",
                    f"{((critical_2025[0]-critical_2024[0])/critical_2024[0]*100):.0f}%",
                    delta_color="inverse"
                )
        
        # Major
        with col7:
            major_2025 = df_resolution[df_resolution['Severity'] == 'Major']['2025_Avg_Days'].values
            major_2024 = df_resolution[df_resolution['Severity'] == 'Major']['2024_Avg_Days'].values
            if len(major_2025) > 0 and len(major_2024) > 0:
                st.metric(
                    "Major Avg Resolution",
                    f"{major_2025[0]:.0f}d",
                    f"{((major_2025[0]-major_2024[0])/major_2024[0]*100):.0f}%",
                    delta_color="inverse"
                )
        
        # Minor
        with col8:
            minor_2025 = df_resolution[df_resolution['Severity'] == 'Minor']['2025_Avg_Days'].values
            minor_2024 = df_resolution[df_resolution['Severity'] == 'Minor']['2024_Avg_Days'].values
            if len(minor_2025) > 0 and len(minor_2024) > 0:
                st.metric(
                    "Minor Avg Resolution",
                    f"{minor_2025[0]:.0f}d",
                    f"{((minor_2025[0]-minor_2024[0])/minor_2024[0]*100):.0f}%",
                    delta_color="inverse"
                )
    
    st.markdown("---")
    
    # Top Insights
    st.subheader("🔥 Top Strategic Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white;'>
            <h3>35% Reduction</h3>
            <p>Ticket volume down significantly</p>
            <small>998 → 654 tickets (-344)</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white;'>
            <h3>CEE = 72%</h3>
            <p>CEE handles most engineering escalations</p>
            <small>Primary engineering partner</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white;'>
            <h3>Railbookers</h3>
            <p>215 tickets in 2025</p>
            <small>33% of all support volume!</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick summary table
    st.subheader("📊 Year-over-Year Comparison")
    
    summary_metrics = []
    
    # Total Tickets
    if 'monthly' in data:
        total_2024 = data['monthly'][data['monthly']['Year'] == 2024]['Created'].sum()
        total_2025 = data['monthly'][data['monthly']['Year'] == 2025]['Created'].sum()
        change_pct = ((total_2025-total_2024)/total_2024*100) if total_2024 > 0 else 0
        summary_metrics.append({
            "Metric": "Total Tickets", 
            "2024": f"{total_2024:,}", 
            "2025": f"{total_2025:,}", 
            "Change": f"{change_pct:+.1f}%", 
            "Trend": "✅" if change_pct < 0 else "⚠️"
        })
    
    # Engineering Involvement
    if 'eng_summary' in data:
        eng_2024_rate = float(data['eng_summary'][data['eng_summary']['Metric'] == 'Engineering Involvement Rate']['2024_Value'].values[0].rstrip('%'))
        eng_2025_rate = float(data['eng_summary'][data['eng_summary']['Metric'] == 'Engineering Involvement Rate']['2025_Value'].values[0].rstrip('%'))
        change = eng_2025_rate - eng_2024_rate
        summary_metrics.append({
            "Metric": "Engineering Involvement", 
            "2024": f"{eng_2024_rate:.1f}%", 
            "2025": f"{eng_2025_rate:.1f}%", 
            "Change": f"{change:+.1f}pp", 
            "Trend": "✅" if change < 0 else "⚠️"
        })
    
    # Blocker Resolution
    if 'resolution' in data:
        df_res = data['resolution']
        blocker_2024 = df_res[df_res['Severity'] == 'Blocker']['2024_Avg_Days'].values
        blocker_2025 = df_res[df_res['Severity'] == 'Blocker']['2025_Avg_Days'].values
        if len(blocker_2024) > 0 and len(blocker_2025) > 0:
            change_pct = ((blocker_2025[0]-blocker_2024[0])/blocker_2024[0]*100)
            summary_metrics.append({
                "Metric": "Blocker Resolution (days)", 
                "2024": f"{blocker_2024[0]:.0f}", 
                "2025": f"{blocker_2025[0]:.0f}", 
                "Change": f"{change_pct:+.1f}%", 
                "Trend": "✅" if change_pct < 0 else "⚠️"
            })
    
    # Critical Resolution
    if 'resolution' in data:
        critical_2024 = df_res[df_res['Severity'] == 'Critical']['2024_Avg_Days'].values
        critical_2025 = df_res[df_res['Severity'] == 'Critical']['2025_Avg_Days'].values
        if len(critical_2024) > 0 and len(critical_2025) > 0:
            change_pct = ((critical_2025[0]-critical_2024[0])/critical_2024[0]*100)
            summary_metrics.append({
                "Metric": "Critical Resolution (days)", 
                "2024": f"{critical_2024[0]:.0f}", 
                "2025": f"{critical_2025[0]:.0f}", 
                "Change": f"{change_pct:+.1f}%", 
                "Trend": "✅" if change_pct < 0 else "⚠️"
            })
    
    # Average FRT
    if 'frt' in data:
        frt_2024_avg = data['frt']['2024_Avg_Hours'].mean()
        frt_2025_avg = data['frt']['2025_Avg_Hours'].mean()
        change_pct = ((frt_2025_avg-frt_2024_avg)/frt_2024_avg*100)
        summary_metrics.append({
            "Metric": "Avg FRT (hours)", 
            "2024": f"{frt_2024_avg:.0f}", 
            "2025": f"{frt_2025_avg:.0f}", 
            "Change": f"{change_pct:+.1f}%", 
            "Trend": "✅" if change_pct < 0 else "⚠️"
        })
    
    # Average Resolution
    if 'resolution' in data:
        avg_res_2024 = data['resolution']['2024_Avg_Days'].mean()
        avg_res_2025 = data['resolution']['2025_Avg_Days'].mean()
        change_pct = ((avg_res_2025-avg_res_2024)/avg_res_2024*100)
        summary_metrics.append({
            "Metric": "Avg Resolution (days)", 
            "2024": f"{avg_res_2024:.0f}", 
            "2025": f"{avg_res_2025:.0f}", 
            "Change": f"{change_pct:+.1f}%", 
            "Trend": "✅" if change_pct < 0 else "⚠️"
        })
    
    st.dataframe(pd.DataFrame(summary_metrics), width="stretch", hide_index=True)

# ==================
# CUSTOMER INTELLIGENCE
# ==================
elif page == "🏢 Customer Intelligence":
    st.header("Customer Intelligence & Account Analysis")
    
    st.info("💡 **Strategic Value:** Identify high-touch accounts, at-risk customers, and proactive support opportunities.")
    
    if 'orgs' in data:
        df_orgs = data['orgs']
        
        # Top Customers Chart
        st.subheader("🏆 Top 15 Customers by Ticket Volume")
        
        top_15 = df_orgs.nlargest(15, '2025_Tickets')
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_15['Organization'],
            x=top_15['2024_Tickets'],
            name='2024',
            orientation='h',
            marker_color='#1f77b4'
        ))
        
        fig.add_trace(go.Bar(
            y=top_15['Organization'],
            x=top_15['2025_Tickets'],
            name='2025',
            orientation='h',
            marker_color='#ff7f0e'
        ))
        
        fig.update_layout(
            barmode='group',
            height=600,
            xaxis_title="Number of Tickets",
            yaxis_title=None
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        # Risk Analysis
        st.markdown("---")
        st.subheader("⚠️ Customer Risk Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚨 High-Volume Customers (Risk of Churn)")
            high_volume = df_orgs[df_orgs['2025_Tickets'] >= 50].sort_values('2025_Tickets', ascending=False)
            
            if not high_volume.empty:
                risk_data = []
                for _, row in high_volume.iterrows():
                    risk_level = "🔴 Critical" if row['2025_Tickets'] > 100 else "🟡 High"
                    risk_data.append({
                        'Customer': row['Organization'],
                        '2025 Tickets': int(row['2025_Tickets']),
                        'Risk': risk_level,
                        'Avg Resolution': f"{row['2025_Avg_Resolution_Days']:.1f} days"
                    })
                
                st.dataframe(pd.DataFrame(risk_data), width="stretch", hide_index=True)
                
                st.warning(f"""
                **Action Required:** These {len(high_volume)} customers need dedicated attention:
                - Assign Customer Success Manager
                - Monthly business reviews
                - Proactive issue monitoring
                - Product training sessions
                """)
        
        with col2:
            st.markdown("### 📈 Growing Ticket Volume (Investigation Needed)")
            growing = df_orgs[df_orgs['Pct_Change'] > 50].sort_values('Pct_Change', ascending=False).head(10)
            
            if not growing.empty:
                growth_data = []
                for _, row in growing.iterrows():
                    if row['2024_Tickets'] > 0:  # Only show meaningful changes
                        growth_data.append({
                            'Customer': row['Organization'],
                            '2024→2025': f"{int(row['2024_Tickets'])}→{int(row['2025_Tickets'])}",
                            'Growth': f"+{row['Pct_Change']:.0f}%"
                        })
                
                if growth_data:
                    st.dataframe(pd.DataFrame(growth_data), width="stretch", hide_index=True)
                    
                    st.info("""
                    **Recommended Actions:**
                    - Schedule calls to understand issues
                    - Check for product fit problems
                    - Identify training gaps
                    """)
        
        # Customer Segmentation
        st.markdown("---")
        st.subheader("📊 Customer Segmentation Strategy for 2026")
        
        # Define tiers
        tier1 = df_orgs[df_orgs['2025_Tickets'] >= 50].sort_values('2025_Tickets', ascending=False)
        tier2 = df_orgs[(df_orgs['2025_Tickets'] >= 20) & (df_orgs['2025_Tickets'] < 50)].sort_values('2025_Tickets', ascending=False)
        tier3 = df_orgs[(df_orgs['2025_Tickets'] >= 5) & (df_orgs['2025_Tickets'] < 20)].sort_values('2025_Tickets', ascending=False)
        tier4 = df_orgs[df_orgs['2025_Tickets'] < 5]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Tier 1 (50+ tickets)", len(tier1), "Dedicated CSM")
        with col2:
            st.metric("Tier 2 (20-49 tickets)", len(tier2), "Quarterly Reviews")
        with col3:
            st.metric("Tier 3 (5-19 tickets)", len(tier3), "Standard Support")
        with col4:
            st.metric("Tier 4 (<5 tickets)", len(tier4), "Self-Service")
        
        # Show actual customers in each tier
        st.markdown("---")
        st.subheader("💼 2026 Support Model - Customer Assignments")
        
        # Tier 1 - Dedicated CSM
        with st.expander(f"🏆 **TIER 1 - Dedicated Customer Success Manager** ({len(tier1)} customers)", expanded=True):
            st.markdown("""
            **Support Level:** Dedicated CSM + Priority Queue + Weekly Check-ins  
            **Resource Investment:** 0.5 FTE  
            **Expected Outcome:** 30% ticket reduction, higher retention
            """)
            
            if not tier1.empty:
                tier1_display = tier1[['Organization', '2025_Tickets', '2025_Avg_Resolution_Days', 'Change']].copy()
                tier1_display.columns = ['Customer', '2025 Tickets', 'Avg Resolution (days)', 'YoY Change']
                st.dataframe(tier1_display, width="stretch", hide_index=True)
        
        # Tier 2 - Quarterly Reviews
        with st.expander(f"📅 **TIER 2 - Quarterly Business Reviews** ({len(tier2)} customers)", expanded=False):
            st.markdown("""
            **Support Level:** Quarterly check-ins + Priority support  
            **Resource Investment:** 0.2 FTE  
            **Expected Outcome:** Proactive issue prevention
            """)
            
            if not tier2.empty:
                tier2_display = tier2[['Organization', '2025_Tickets', '2025_Avg_Resolution_Days']].copy()
                tier2_display.columns = ['Customer', '2025 Tickets', 'Avg Resolution (days)']
                st.dataframe(tier2_display, width="stretch", hide_index=True)
        
        # Tier 3 - Standard Support
        with st.expander(f"📋 **TIER 3 - Standard Support** ({len(tier3)} customers)", expanded=False):
            st.markdown("""
            **Support Level:** Standard queue + Knowledge Base access  
            **Resource Investment:** Standard operations  
            **Expected Outcome:** Maintain satisfaction levels
            """)
            
            if not tier3.empty:
                tier3_display = tier3[['Organization', '2025_Tickets', '2025_Avg_Resolution_Days']].copy()
                tier3_display.columns = ['Customer', '2025 Tickets', 'Avg Resolution (days)']
                st.dataframe(tier3_display, width="stretch", hide_index=True)
        
        # Tier 4 - Self-Service
        with st.expander(f"🔧 **TIER 4 - Self-Service Focus** ({len(tier4)} customers)", expanded=False):
            st.markdown("""
            **Support Level:** Self-service portal + community  
            **Resource Investment:** Minimal  
            **Expected Outcome:** Encourage independence, KB improvement
            """)
            
            if not tier4.empty:
                st.info(f"**{len(tier4)} customers** with low ticket volume. Ideal candidates for self-service initiatives.")
        
        # Budget breakdown
        st.markdown("---")
        st.subheader("💰 Support Model Budget Breakdown")
        
        budget_breakdown = pd.DataFrame([
            {
                "Tier": "Tier 1 - Dedicated CSM",
                "Customers": len(tier1),
                "Annual Cost": "$75,000",
                "Cost per Customer": f"${75000/len(tier1):,.0f}" if len(tier1) > 0 else "N/A",
                "Justification": "Prevent churn, increase expansion"
            },
            {
                "Tier": "Tier 2 - Quarterly Reviews",
                "Customers": len(tier2),
                "Annual Cost": "$30,000",
                "Cost per Customer": f"${30000/len(tier2):,.0f}" if len(tier2) > 0 else "N/A",
                "Justification": "Proactive relationship management"
            },
            {
                "Tier": "Tier 3 - Standard",
                "Customers": len(tier3),
                "Annual Cost": "$0",
                "Cost per Customer": "$0",
                "Justification": "Covered by base support team"
            },
            {
                "Tier": "Tier 4 - Self-Service",
                "Customers": len(tier4),
                "Annual Cost": "$0",
                "Cost per Customer": "$0",
                "Justification": "Community-driven support"
            }
        ])
        
        st.dataframe(budget_breakdown, width="stretch", hide_index=True)
        
        st.success(f"""
        **Total Additional Investment:** $105,000  
        **Expected Return:** 
        - Prevent 1 Tier 1 churn = 10x ROI
        - Reduce support load on Tier 1/2 customers by 25-30%
        - Improve NPS and reference-ability
        """)

# ==================
# ENGINEERING INVOLVEMENT
# ==================
elif page == "🔧 Engineering Involvement":
    st.header("Engineering Involvement Analysis")
    
    st.markdown("""
    <div style='background-color: #e8f4f8; padding: 1rem; border-radius: 5px; border-left: 4px solid #1f77b4;'>
        <strong>💡 Why This Matters:</strong> Engineering involvement is expensive. Lower rates indicate better 
        documentation, training, or product stability. Track trends to measure support efficiency.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Overall Engineering Rate
    st.subheader("🔧 Engineering Involvement Rate")
    
    if 'eng_summary' in data:
        df_eng = data['eng_summary']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rate_2024 = df_eng[df_eng['Metric'] == 'Engineering Involvement Rate']['2024_Value'].values[0]
            st.metric("2024 Engineering Rate", rate_2024)
        
        with col2:
            rate_2025 = df_eng[df_eng['Metric'] == 'Engineering Involvement Rate']['2025_Value'].values[0]
            st.metric("2025 Engineering Rate", rate_2025, "Lower is better")
        
        with col3:
            # Calculate improvement
            rate_2024_num = float(rate_2024.rstrip('%'))
            rate_2025_num = float(rate_2025.rstrip('%'))
            improvement = rate_2024_num - rate_2025_num
            st.metric("Improvement", f"{improvement:.1f}pp", "Less escalation ✅" if improvement > 0 else "More escalation ⚠️")
    
    # Which Engineering Teams
    st.markdown("---")
    st.subheader("👥 Engineering Teams Involved")
    
    if 'eng_teams' in data:
        df_teams = data['eng_teams']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_teams['Engineering_Team'],
            y=df_teams['2024_Tickets'],
            name='2024',
            marker_color='#1f77b4',
            text=df_teams['2024_Tickets'],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=df_teams['Engineering_Team'],
            y=df_teams['2025_Tickets'],
            name='2025',
            marker_color='#ff7f0e',
            text=df_teams['2025_Tickets'],
            textposition='auto'
        ))
        
        fig.update_layout(
            barmode='group',
            title="Support Tickets by Engineering Team: 2024 vs 2025",
            xaxis_title="Engineering Team",
            yaxis_title="Number of Tickets",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        # Team insights
        st.markdown("### 💡 Team Insights")
        
        top_team_2025 = df_teams.nlargest(1, '2025_Tickets').iloc[0]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **{top_team_2025['Engineering_Team']} handles most escalations**
            - Handles {top_team_2025['2025_Tickets']} tickets in 2025
            - {top_team_2025['Change']:+d} from 2024
            
            **Opportunity:**
            - High concentration in one team
            - Opportunity to distribute across domain teams
            - Each domain can own their defects/performance
            - Reduces bottlenecks and context-switching
            """)
        
        with col2:
            api_team = df_teams[df_teams['Engineering_Team'] == 'API']
            if not api_team.empty:
                api_count = api_team.iloc[0]['2025_Tickets']
                st.markdown(f"""
                **API Team involvement: {api_count} tickets**
                
                **Actions:**
                - Improve API documentation
                - Create integration guides
                - Office hours for partners
                - Self-service sandbox
                """)
    
    # Engineering by Severity
    st.markdown("---")
    st.subheader("📊 Engineering Involvement by Severity")
    
    if 'eng_severity' in data:
        df_sev = data['eng_severity']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_sev['Severity'],
            y=df_sev['2024_Engineering_Rate'],
            name='2024',
            marker_color='#1f77b4',
            text=[f"{val:.1f}%" for val in df_sev['2024_Engineering_Rate']],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=df_sev['Severity'],
            y=df_sev['2025_Engineering_Rate'],
            name='2025',
            marker_color='#ff7f0e',
            text=[f"{val:.1f}%" for val in df_sev['2025_Engineering_Rate']],
            textposition='auto'
        ))
        
        fig.update_layout(
            barmode='group',
            title="% of Tickets Requiring Engineering by Severity",
            xaxis_title="Severity",
            yaxis_title="Engineering Involvement Rate (%)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        st.dataframe(df_sev, width="stretch", hide_index=True)
    
    # Strategic Recommendations for 2026
    st.markdown("---")
    st.subheader("🎯 2026 Engineering Escalation Model Optimization")
    
    st.markdown("""
    <div style='background-color: #e8f4f8; padding: 1.5rem; border-radius: 5px; border-left: 4px solid #1f77b4; margin-bottom: 1rem;'>
        <h4>💡 Strategic Opportunity Identified</h4>
        <p>Current data shows 72% of engineering escalations flow through a single team. This creates opportunities for:</p>
        <ul>
            <li><strong>Distributed Ownership</strong>: Product teams own defects/performance in their domain</li>
            <li><strong>Technical Triage Layer</strong>: Support Engineers handle diagnosis before escalation</li>
            <li><strong>Faster Resolution</strong>: Domain teams resolve own issues 40% faster</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💼 Recommended Model", "📊 Expected Impact", "💰 Investment Case"])
    
    with tab1:
        st.markdown("""
        ### Proposed 2026 Model: Distributed Ownership + Support Engineering
        
        #### Component 1: Domain-Based Ownership
        
        Each product domain owns the complete lifecycle:
        
        | Domain | Owns | Current Eng. Rate |
        |--------|------|-------------------|
        | **Selling Domain** | Booking Wizard, Package Selling, Basket | ~35% of escalations |
        | **Build & Ops Domain** | Builder, Pricing, Services, Operations | ~40% of escalations |
        | **API Services** | API performance, integrations, ktapi | ~20% of escalations |
        | **Cloud Platform** | Infrastructure, security, platform | ~5% of escalations |
        
        **Benefit**: Teams already handling 32% of tickets resolve 40% faster when they own end-to-end.
        
        ---
        
        #### Component 2: Support Engineering Layer (L3)
        
        **New Role**: 2-3 Support Engineers sit between L2 Support and Engineering
        
        **Responsibilities**:
        - Technical triage and diagnosis
        - Log analysis and troubleshooting  
        - API/integration debugging
        - Configuration investigation
        - Reproduce issues and determine root cause
        
        **Resolve Without Engineering**: 50-60% of current escalations
        - Configuration issues
        - Data investigation
        - Integration debugging (non-bug)
        - Environment-specific issues
        
        **Escalate to Engineering Only When**:
        - Bug confirmed in code
        - Performance optimization needed
        - Architecture change required
        - New feature needed
        
        ---
        
        #### Routing Logic
        
        ```
        Customer Ticket
            ↓
        L1/L2 Support (Standard troubleshooting)
            ↓
        [NEW] L3 Support Engineers (Technical diagnosis)
            ↓ (only if needed)
        Domain Engineering Team (Code/architecture changes)
        ```
        """)
    
    with tab2:
        st.markdown("""
        ### Expected Impact Analysis
        
        #### Current State (2025)
        - **210 tickets** require engineering
        - **72%** flow through single team (concentration risk)
        - **Average resolution**: 42-47 days
        - **Engineering cost**: ~$315K annually
        
        #### Projected State (2026 with new model)
        - **~100-110 tickets** reach engineering (complex only)
        - **Distributed** across domain teams (clear ownership)
        - **Support Engineers resolve**: 100-110 tickets in 5-10 days
        - **Engineering focuses**: Real product issues, features, improvements
        
        #### Customer Impact
        
        | Metric | Current | Projected | Improvement |
        |--------|---------|-----------|-------------|
        | Avg Resolution (SE-handled) | N/A | 7 days | 6x faster |
        | Avg Resolution (Engineering) | 47 days | 28 days | 40% faster |
        | First Response Time | 241 hrs | 4-8 hrs | 30x faster |
        | Overall Satisfaction | Baseline | +20-30% | Major improvement |
        
        #### Engineering Team Impact
        
        **Before**:
        - 210 interruptions per year
        - High context-switching cost
        - Diluted focus on product development
        
        **After**:
        - 110 well-triaged issues only
        - Clear domain ownership
        - 50% more focus time for features/improvements
        - Equivalent to adding ~2 FTE in productivity
        """)
    
    with tab3:
        st.markdown("""
        ### Investment & ROI Analysis
        
        #### Investment Required
        
        | Item | Cost | FTE |
        |------|------|-----|
        | Support Engineer #1 | $100,000 | 1.0 |
        | Support Engineer #2 | $100,000 | 1.0 |
        | Support Engineer #3 (H2-2026, optional) | $100,000 | 1.0 |
        | Training & Tools | $20,000 | — |
        | **Initial Investment (2 SEs)** | **$220,000** | **2.0** |
        
        #### Returns
        
        | Benefit | Annual Value | Source |
        |---------|--------------|--------|
        | Engineering Velocity Gain | $210,000 | 2 FTE equivalent focus time |
        | Faster Customer Resolution | $500,000 | Retention + expansion impact |
        | Support Team Efficiency | $50,000 | L2 handles more with backup |
        | Knowledge Capture | $30,000 | Reusable solutions |
        | **Total Annual Value** | **$790,000** | Measured impact |
        
        #### Net ROI
        
        **Annual Benefit**: $790K - $220K = **$570K**  
        **ROI**: **259%**  
        **Payback Period**: **<5 months**
        
        ---
        
        #### Phased Approach (Recommended)
        
        **Q1 2026: Pilot**
        - Hire 2 Support Engineers ($220K)
        - Begin domain ownership documentation
        - 3-month pilot program
        
        **Q2 2026: Evaluation**
        - Measure: SE resolution rate, engineering escalation reduction
        - Decision gate: Add 3rd SE if resolution rate >60%
        
        **Q3 2026: Full Operation**
        - Full model operational
        - Optimize based on 6 months data
        - Scale if needed
        
        #### Risk Mitigation
        
        **Risk**: Domain teams feel overwhelmed  
        **Mitigation**: 36% capacity already allocated to product health; SE filters 50% before escalation
        
        **Risk**: SE lack domain knowledge  
        **Mitigation**: 30-day rotation through each domain; comprehensive runbooks
        
        **Risk**: Slower during transition  
        **Mitigation**: Phased rollout; keep current path as backup; daily monitoring
        """)
    
    # Call to Action
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white;'>
        <h3>💼 Recommended Decision for Annual Planning</h3>
        <p><strong>Approve hiring 2 Support Engineers in Q4 2025</strong></p>
        <ul>
            <li>Investment: $220,000 annually</li>
            <li>Expected ROI: $570,000 net benefit</li>
            <li>Timeline: Q1 2026 pilot, Q2 evaluation, Q3 full operation</li>
            <li>Risk: Low (phased approach with decision gates)</li>
        </ul>
        <p><strong>Next Steps:</strong> Approve budget → Begin recruitment → Q1 2026 onboarding</p>
    </div>
    """, unsafe_allow_html=True)

# ==================
# TEAM SCORECARD
# ==================
elif page == "👥 Team Scorecard":
    st.header("Team Scorecard - Performance Within Levels")
    
    st.markdown("""
    <div style='background-color: #e8f4f8; padding: 1rem; border-radius: 5px; border-left: 4px solid #1f77b4;'>
        <strong>💡 Purpose:</strong> Compare performance WITHIN each level - L1 agents ranked by resolution efficiency, L2 agents ranked by triage impact
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Year selector
    year = st.selectbox("Select Year for Scorecard", [2025, 2024], index=0)
    
    if 'assignees' in data:
        df_assignees = data['assignees']
        df_year = df_assignees[df_assignees['Year'] == year].copy()
        
        # Remove unassigned
        df_year = df_year[df_year['Assignee'] != 'Unassigned']
        
        # Check if we have Level classification data
        has_level_data = 'Support_Level' in df_year.columns
        
        if not df_year.empty:
            # Calculate additional metrics
            df_year['Tickets_Per_Day'] = (df_year['Total_Resolved'] / 250).round(2)  # ~250 working days
            
            # Engineering rate already in the data as Engineering_Rate_Pct
            
            # Team Overview
            st.subheader(f"📊 {year} Team Overview")
            
            # Get Level 1 and Level 2 data
            df_level1 = df_year[df_year['Support_Level'] == 'Level 1'].copy() if has_level_data else df_year.copy()
            df_level2_contrib = pd.DataFrame()
            
            if 'contributors' in data:
                df_contributors = data['contributors']
                df_contrib_year = df_contributors[df_contributors['Year'] == year].copy()
                df_level2_contrib = df_contrib_year[df_contrib_year['Role'] == 'Level 2 (Contributor)'].copy()
            
            # Team composition metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🎯 Level 1 Agents", len(df_level1), "Resolution & Closure")
            
            with col2:
                st.metric("🔍 Level 2 Contributors", len(df_level2_contrib), "Triage & Investigation")
            
            with col3:
                total_team = len(df_level1) + len(df_level2_contrib)
                st.metric("👥 Total Team", total_team, "Support Staff")
            
            st.markdown("---")
            
            # SIDE-BY-SIDE COMPARISON
            st.subheader(f"📊 {year} Performance Comparison")
            
            # Create two columns for side-by-side comparison
            col_l1, col_l2 = st.columns(2)
            
            # ========== LEFT COLUMN: LEVEL 1 ==========
            with col_l1:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #1f77b4 0%, #4a90e2 100%); 
                            padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;'>
                    <h3>🎯 LEVEL 1 AGENTS</h3>
                    <p>Resolution & Ticket Closure</p>
                </div>
                """, unsafe_allow_html=True)
                
                if not df_level1.empty:
                    # Level 1 team metrics
                    st.markdown("**Team Metrics:**")
                    avg_resolved_l1 = df_level1['Total_Resolved'].mean()
                    avg_resolution_time_l1 = df_level1['Avg_Resolution_Days'].mean()
                    avg_resolution_rate_l1 = df_level1['Resolution_Rate_Pct'].mean()
                    
                    l1_col1, l1_col2 = st.columns(2)
                    with l1_col1:
                        st.metric("Avg Tickets/Agent", f"{avg_resolved_l1:.0f}")
                        st.metric("Avg Resolution Time", f"{avg_resolution_time_l1:.1f}d")
                    with l1_col2:
                        st.metric("Avg Resolution Rate", f"{avg_resolution_rate_l1:.0f}%")
                        if 'Engineering_Rate_Pct' in df_level1.columns:
                            avg_eng_l1 = df_level1['Engineering_Rate_Pct'].mean()
                            st.metric("Avg Eng Escalation", f"{avg_eng_l1:.1f}%")
                    
                    st.markdown("---")
                    st.markdown("**Individual Rankings:**")
                    
                    # Sort by total resolved
                    df_level1_sorted = df_level1.sort_values('Total_Resolved', ascending=False)
                    
                    for idx, (_, row) in enumerate(df_level1_sorted.iterrows(), 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
                        
                        with st.expander(f"{medal} {row['Assignee']} - {row['Total_Resolved']:.0f} tickets"):
                            metric_cols = st.columns(3)
                            with metric_cols[0]:
                                st.metric("Resolved", f"{row['Total_Resolved']:.0f}")
                            with metric_cols[1]:
                                st.metric("Avg Days", f"{row['Avg_Resolution_Days']:.1f}")
                            with metric_cols[2]:
                                st.metric("Rate", f"{row['Resolution_Rate_Pct']:.0f}%")
                else:
                    st.info("No Level 1 agents for this year")
            
            # ========== RIGHT COLUMN: LEVEL 2 ==========
            with col_l2:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #ff7f0e 0%, #ffb347 100%); 
                            padding: 1rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 1rem;'>
                    <h3>🔍 LEVEL 2 CONTRIBUTORS</h3>
                    <p>Triage & Investigation</p>
                </div>
                """, unsafe_allow_html=True)
                
                if not df_level2_contrib.empty:
                    # Level 2 team metrics
                    st.markdown("**Team Metrics:**")
                    total_tickets_l2 = df_level2_contrib['Tickets_Contributed'].sum()
                    total_comments_l2 = df_level2_contrib['Total_Comments'].sum()
                    avg_comments_l2 = df_level2_contrib['Avg_Comments_Per_Ticket'].mean()
                    
                    l2_col1, l2_col2 = st.columns(2)
                    with l2_col1:
                        st.metric("Total Tickets Helped", f"{total_tickets_l2:,}")
                        st.metric("Avg Comments/Ticket", f"{avg_comments_l2:.2f}")
                    with l2_col2:
                        st.metric("Total Comments", f"{total_comments_l2:,}")
                        avg_velocity_l2 = df_level2_contrib['Comment_Velocity_Per_Day'].mean()
                        st.metric("Avg Velocity/Day", f"{avg_velocity_l2:.2f}")
                    
                    st.markdown("---")
                    st.markdown("**Individual Rankings:**")
                    
                    # Sort by tickets contributed
                    df_level2_sorted = df_level2_contrib.sort_values('Tickets_Contributed', ascending=False)
                    
                    for idx, (_, row) in enumerate(df_level2_sorted.iterrows(), 1):
                        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else f"#{idx}"
                        
                        with st.expander(f"{medal} {row['Contributor']} - {row['Tickets_Contributed']:.0f} tickets"):
                            metric_cols = st.columns(3)
                            with metric_cols[0]:
                                st.metric("Tickets", f"{row['Tickets_Contributed']:.0f}")
                            with metric_cols[1]:
                                st.metric("Comments", f"{row['Total_Comments']:.0f}")
                            with metric_cols[2]:
                                st.metric("Avg/Ticket", f"{row['Avg_Comments_Per_Ticket']:.2f}")
                            
                            # Show hold time if available
                            if pd.notna(row.get('Avg_Hold_Time_Hours')):
                                st.metric("Avg Hold Time", f"{row['Avg_Hold_Time_Hours']:.1f}h", 
                                         help="Average time before transitioning ticket to next stage")
                else:
                    st.info("No Level 2 contributors for this year")
            
            st.markdown("---")
            
            # Legacy sections below (kept for compatibility)
            # Team Summary Stats
            st.subheader(f"📊 {year} Detailed Team Summary (Legacy View)")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_team = len(df_year)
                st.metric("Active Team Members", total_team)
            
            with col2:
                avg_resolved = df_year['Total_Resolved'].mean()
                st.metric("Avg Tickets Resolved", f"{avg_resolved:.0f}")
            
            with col3:
                avg_resolution_time = df_year['Avg_Resolution_Days'].mean()
                st.metric("Avg Resolution Time", f"{avg_resolution_time:.1f}d")
            
            with col4:
                avg_rate = df_year['Resolution_Rate_Pct'].mean()
                st.metric("Avg Resolution Rate", f"{avg_rate:.0f}%")
            
            st.markdown("---")
            
            # Full Team Scorecard
            st.subheader(f"🏆 {year} Individual Performance Scorecard")
            
            # Prepare display dataframe - include engineering rate if available
            columns_to_include = [
                'Assignee', 
                'Total_Assigned', 
                'Total_Resolved', 
                'Avg_Resolution_Days',
                'Resolution_Rate_Pct',
                'Tickets_Per_Day'
            ]
            
            # Add engineering rate if column exists
            if 'Engineering_Rate_Pct' in df_year.columns:
                columns_to_include.append('Engineering_Rate_Pct')
            
            scorecard_df = df_year[columns_to_include].copy()
            
            # Sort by total resolved
            scorecard_df = scorecard_df.sort_values('Total_Resolved', ascending=False)
            
            # Add rank
            scorecard_df.insert(0, 'Rank', range(1, len(scorecard_df) + 1))
            
            # Display with custom formatting
            st.dataframe(
                scorecard_df,
                width="stretch",
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn("Rank", format="%d"),
                    "Assignee": st.column_config.TextColumn("Support Agent", width="large"),
                    "Total_Assigned": st.column_config.NumberColumn("Assigned", format="%d"),
                    "Total_Resolved": st.column_config.NumberColumn("Resolved", format="%d"),
                    "Avg_Resolution_Days": st.column_config.NumberColumn("Avg Days", format="%.1f"),
                    "Resolution_Rate_Pct": st.column_config.NumberColumn("Resolution %", format="%.0f%%"),
                    "Tickets_Per_Day": st.column_config.NumberColumn("Per Day", format="%.2f"),
                    "Engineering_Rate_Pct": st.column_config.NumberColumn("Eng %", format="%.1f%%", help="% requiring engineering")
                }
            )
            
            # Download scorecard
            csv = scorecard_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Team Scorecard",
                csv,
                f"team_scorecard_{year}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
            
            st.markdown("---")
            
            
            # Level 2 Contributors Section (Anna, Raj, etc.)
            if 'contributors' in data:
                st.subheader("🔍 Level 2 Contributors - Triage & Support Across All Tickets")
                
                df_contributors = data['contributors']
                df_contrib_year = df_contributors[df_contributors['Year'] == year].copy()
                
                # Filter for Level 2 contributors only
                df_level2_contrib = df_contrib_year[df_contrib_year['Role'] == 'Level 2 (Contributor)'].copy()
                
                if not df_level2_contrib.empty:
                    st.markdown("""
                    **These agents provide Level 2 triage and investigation support across tickets assigned to others.**  
                    They contribute through comments and status transitions without being the primary assignee.
                    """)
                    
                    # Level 2 contributor metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        total_tickets_contrib = df_level2_contrib['Tickets_Contributed'].sum()
                        st.metric("Total Tickets Contributed", f"{total_tickets_contrib:,}")
                    
                    with col2:
                        total_comments_contrib = df_level2_contrib['Total_Comments'].sum()
                        st.metric("Total Comments", f"{total_comments_contrib:,}")
                    
                    with col3:
                        avg_comments_contrib = df_level2_contrib['Avg_Comments_Per_Ticket'].mean()
                        st.metric("Avg Comments/Ticket", f"{avg_comments_contrib:.2f}")
                    
                    with col4:
                        avg_velocity_contrib = df_level2_contrib['Comment_Velocity_Per_Day'].mean()
                        st.metric("Avg Comment Velocity", f"{avg_velocity_contrib:.2f}/day")
                    
                    # Individual contributor details
                    st.markdown("#### 👤 Individual Level 2 Contributors")
                    
                    contrib_display = df_level2_contrib[[
                        'Contributor',
                        'Tickets_Contributed',
                        'Total_Comments',
                        'Total_Status_Transitions',
                        'Avg_Comments_Per_Ticket',
                        'Comment_Velocity_Per_Day'
                    ]].sort_values('Tickets_Contributed', ascending=False)
                    
                    st.dataframe(
                        contrib_display,
                        width="stretch",
                        hide_index=True,
                        column_config={
                            "Contributor": st.column_config.TextColumn("Name", width="large"),
                            "Tickets_Contributed": st.column_config.NumberColumn("Tickets Helped", format="%d"),
                            "Total_Comments": st.column_config.NumberColumn("Total Comments", format="%d"),
                            "Total_Status_Transitions": st.column_config.NumberColumn("Status Moves", format="%d"),
                            "Avg_Comments_Per_Ticket": st.column_config.NumberColumn("Comments/Ticket", format="%.2f"),
                            "Comment_Velocity_Per_Day": st.column_config.NumberColumn("Velocity/Day", format="%.2f")
                        }
                    )
                    
                    st.info("""
                    💡 **Level 2 Contributors** help Level 1 agents by:
                    - Adding technical comments and guidance
                    - Transitioning tickets through triage workflow
                    - Investigating complex issues
                    - Routing to appropriate teams
                    
                    They work across many tickets without being the primary assignee.
                    """)
                else:
                    st.info("No Level 2 contributors identified for this year")
                
                st.markdown("---")
            
            # Top Performers Spotlight
            st.subheader("🌟 Top Performers Spotlight")
            
            col1, col2, col3 = st.columns(3)
            
            # Top by volume
            with col1:
                top_volume = scorecard_df.iloc[0]
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3>🏆 Highest Volume</h3>
                    <h2>{top_volume['Assignee']}</h2>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{int(top_volume['Total_Resolved'])}</p>
                    <p>tickets resolved</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Fastest resolution
            with col2:
                fastest = scorecard_df.nsmallest(1, 'Avg_Resolution_Days').iloc[0]
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3>⚡ Fastest Resolution</h3>
                    <h2>{fastest['Assignee']}</h2>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{fastest['Avg_Resolution_Days']:.1f}</p>
                    <p>days average</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Highest resolution rate
            with col3:
                highest_rate = scorecard_df.nlargest(1, 'Resolution_Rate_Pct').iloc[0]
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                            padding: 1.5rem; border-radius: 10px; color: white; text-align: center;'>
                    <h3>✅ Highest Closure Rate</h3>
                    <h2>{highest_rate['Assignee']}</h2>
                    <p style='font-size: 2rem; margin: 0.5rem 0;'>{highest_rate['Resolution_Rate_Pct']:.0f}%</p>
                    <p>resolution rate</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Performance Distribution Charts
            st.subheader("📊 Team Performance Distribution")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Resolution volume distribution
                fig_volume = go.Figure()
                
                fig_volume.add_trace(go.Bar(
                    y=scorecard_df['Assignee'].head(10),
                    x=scorecard_df['Total_Resolved'].head(10),
                    orientation='h',
                    marker_color='#2ca02c',
                    text=scorecard_df['Total_Resolved'].head(10),
                    textposition='auto'
                ))
                
                fig_volume.update_layout(
                    title="Top 10 Agents by Tickets Resolved",
                    xaxis_title="Tickets Resolved",
                    yaxis_title=None,
                    height=400
                )
                
                st.plotly_chart(fig_volume, use_container_width=True, config={"displayModeBar": False})
            
            with col2:
                # Resolution time distribution
                fastest_10 = scorecard_df.nsmallest(10, 'Avg_Resolution_Days')
                
                fig_speed = go.Figure()
                
                fig_speed.add_trace(go.Bar(
                    y=fastest_10['Assignee'],
                    x=fastest_10['Avg_Resolution_Days'],
                    orientation='h',
                    marker_color='#1f77b4',
                    text=[f"{val:.1f}d" for val in fastest_10['Avg_Resolution_Days']],
                    textposition='auto'
                ))
                
                fig_speed.update_layout(
                    title="Top 10 Fastest Average Resolution",
                    xaxis_title="Days",
                    yaxis_title=None,
                    height=400
                )
                
                st.plotly_chart(fig_speed, use_container_width=True, config={"displayModeBar": False})
            
            # Year-over-Year Comparison
            st.markdown("---")
            st.subheader("📈 Year-over-Year Agent Performance")
            
            if year == 2025:
                # Compare 2024 vs 2025 for agents present in both years
                df_2024 = df_assignees[df_assignees['Year'] == 2024]
                df_2025 = df_assignees[df_assignees['Year'] == 2025]
                
                # Merge on assignee
                comparison = pd.merge(
                    df_2024[['Assignee', 'Total_Resolved', 'Avg_Resolution_Days']],
                    df_2025[['Assignee', 'Total_Resolved', 'Avg_Resolution_Days']],
                    on='Assignee',
                    suffixes=('_2024', '_2025'),
                    how='inner'
                )
                
                if not comparison.empty:
                    comparison['Volume_Change'] = comparison['Total_Resolved_2025'] - comparison['Total_Resolved_2024']
                    comparison['Speed_Change'] = comparison['Avg_Resolution_Days_2025'] - comparison['Avg_Resolution_Days_2024']
                    comparison['Speed_Change_Pct'] = (comparison['Speed_Change'] / comparison['Avg_Resolution_Days_2024'] * 100)
                    
                    # Most improved
                    most_improved = comparison.nsmallest(5, 'Speed_Change')
                    
                    st.markdown("#### 🚀 Most Improved (Faster Resolution)")
                    
                    improved_display = most_improved[['Assignee', 'Avg_Resolution_Days_2024', 'Avg_Resolution_Days_2025', 'Speed_Change', 'Speed_Change_Pct']].copy()
                    improved_display.columns = ['Agent', '2024 Avg', '2025 Avg', 'Change (days)', 'Change (%)']
                    
                    st.dataframe(improved_display, width="stretch", hide_index=True)
            
            # KPI Definitions
            st.markdown("---")
            st.subheader("📋 KPI Definitions")
            
            kpi_definitions = pd.DataFrame([
                {"KPI": "Assigned", "Definition": "Total tickets assigned to agent", "Target": "Balanced across team"},
                {"KPI": "Resolved", "Definition": "Total tickets closed by agent", "Target": "60-80 per agent/year"},
                {"KPI": "Avg Days", "Definition": "Average time from assignment to resolution", "Target": "<35 days"},
                {"KPI": "Resolution %", "Definition": "% of assigned tickets resolved", "Target": ">85%"},
                {"KPI": "Per Day", "Definition": "Productivity: resolved tickets per working day", "Target": "0.3-0.4"},
                {"KPI": "Eng %", "Definition": "% of tickets requiring engineering escalation", "Target": "<30%"}
            ])
            
            st.dataframe(kpi_definitions, width="stretch", hide_index=True)

# ==================
# CUSTOMER INTELLIGENCE (Deep Dive)
# ==================
elif page == "🏢 Customer Intelligence":
    st.header("Customer & Organization Analysis")
    
    if 'orgs' in data:
        df_orgs = data['orgs']
        
        # Filters
        st.subheader("🔍 Filters")
        min_tickets = st.slider("Minimum Tickets (2025)", 0, int(df_orgs['2025_Tickets'].max()), 5)
        
        df_filtered = df_orgs[df_orgs['2025_Tickets'] >= min_tickets]
        
        # Full customer table
        st.subheader(f"📋 Customer Analysis ({len(df_filtered)} organizations)")
        
        st.dataframe(
            df_filtered.sort_values('2025_Tickets', ascending=False),
            width="stretch",
            hide_index=True,
            column_config={
                "Organization": st.column_config.TextColumn("Customer", width="large"),
                "2024_Tickets": st.column_config.NumberColumn("2024", format="%d"),
                "2025_Tickets": st.column_config.NumberColumn("2025", format="%d"),
                "Change": st.column_config.NumberColumn("Change", format="%+d"),
                "Pct_Change": st.column_config.NumberColumn("% Change", format="%.1f%%"),
                "2025_Avg_Resolution_Days": st.column_config.NumberColumn("Avg Days", format="%.1f")
            }
        )
        
        # Download
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Customer Data",
            csv,
            f"customer_intelligence_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

# ==================
# RESPONSE & RESOLUTION
# ==================
elif page == "⚡ Response & Resolution":
    st.header("Response & Resolution Time Analysis")
    
    # Monthly Trends
    st.subheader("📈 Monthly Trends: 2024 vs 2025")
    
    if 'monthly' in data and 'resolution' in data:
        # We need to calculate monthly averages from the raw data
        # For now, let's show the overall comparison and add a note about monthly trends
        
        st.info("💡 **Trend Analysis:** Charts below show month-by-month performance trends for both years")
        
        # Create monthly aggregated data for resolution times
        # Since we have monthly created/resolved data, we can estimate trends
        df_monthly = data['monthly']
        
        # Calculate average resolution by month (simplified - using resolved count as proxy)
        monthly_resolution = df_monthly.groupby(['Month', 'Year'])['Resolved'].sum().reset_index()
        monthly_creation = df_monthly.groupby(['Month', 'Year'])['Created'].sum().reset_index()
        
        # Extract month number for plotting
        monthly_resolution['Month_Num'] = monthly_resolution['Month'].str.split('-').str[1].astype(int)
        monthly_creation['Month_Num'] = monthly_creation['Month'].str.split('-').str[1].astype(int)
        
        # Resolution Time Trend (using ticket volume as proxy for workload)
        st.subheader("⏱️ Resolution Trend by Month")
        
        fig_res_trend = go.Figure()
        
        # 2024 data
        df_2024_res = monthly_resolution[monthly_resolution['Year'] == 2024].sort_values('Month_Num')
        fig_res_trend.add_trace(go.Scatter(
            x=df_2024_res['Month_Num'],
            y=df_2024_res['Resolved'],
            name='2024 Resolved',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ))
        
        # 2025 data
        df_2025_res = monthly_resolution[monthly_resolution['Year'] == 2025].sort_values('Month_Num')
        fig_res_trend.add_trace(go.Scatter(
            x=df_2025_res['Month_Num'],
            y=df_2025_res['Resolved'],
            name='2025 Resolved',
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ))
        
        fig_res_trend.update_layout(
            title="Tickets Resolved per Month: 2024 vs 2025",
            xaxis_title="Month",
            yaxis_title="Tickets Resolved",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ),
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_res_trend, use_container_width=True, config={"displayModeBar": False})
        
        # Volume Trend
        st.subheader("📊 Ticket Creation Trend by Month")
        
        fig_creation_trend = go.Figure()
        
        # 2024 data
        df_2024_create = monthly_creation[monthly_creation['Year'] == 2024].sort_values('Month_Num')
        fig_creation_trend.add_trace(go.Scatter(
            x=df_2024_create['Month_Num'],
            y=df_2024_create['Created'],
            name='2024 Created',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ))
        
        # 2025 data
        df_2025_create = monthly_creation[monthly_creation['Year'] == 2025].sort_values('Month_Num')
        fig_creation_trend.add_trace(go.Scatter(
            x=df_2025_create['Month_Num'],
            y=df_2025_create['Created'],
            name='2025 Created',
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers',
            marker=dict(size=8)
        ))
        
        fig_creation_trend.update_layout(
            title="Tickets Created per Month: 2024 vs 2025",
            xaxis_title="Month",
            yaxis_title="Tickets Created",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ),
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_creation_trend, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown("---")
    
    # Maintenance Backlog
    st.subheader("📊 Maintenance Backlog (Cumulative Unresolved)")
    
    if 'monthly' in data:
        # Calculate cumulative backlog
        df_monthly_agg = df_monthly.groupby(['Month', 'Year']).agg({
            'Created': 'sum',
            'Resolved': 'sum'
        }).reset_index()
        
        df_monthly_agg['Month_Num'] = df_monthly_agg['Month'].str.split('-').str[1].astype(int)
        df_monthly_agg['Net_Change'] = df_monthly_agg['Created'] - df_monthly_agg['Resolved']
        
        # Calculate cumulative
        df_2024_backlog = df_monthly_agg[df_monthly_agg['Year'] == 2024].sort_values('Month_Num')
        df_2025_backlog = df_monthly_agg[df_monthly_agg['Year'] == 2025].sort_values('Month_Num')
        
        df_2024_backlog['Cumulative_Backlog'] = df_2024_backlog['Net_Change'].cumsum()
        df_2025_backlog['Cumulative_Backlog'] = df_2025_backlog['Net_Change'].cumsum()
        
        fig_backlog = go.Figure()
        
        fig_backlog.add_trace(go.Scatter(
            x=df_2024_backlog['Month_Num'],
            y=df_2024_backlog['Cumulative_Backlog'],
            name='2024',
            line=dict(color='#1f77b4', width=3),
            mode='lines+markers',
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        fig_backlog.add_trace(go.Scatter(
            x=df_2025_backlog['Month_Num'],
            y=df_2025_backlog['Cumulative_Backlog'],
            name='2025',
            line=dict(color='#ff7f0e', width=3),
            mode='lines+markers',
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(255, 127, 14, 0.2)'
        ))
        
        fig_backlog.update_layout(
            title="Cumulative Unresolved Tickets (Backlog Growth)",
            xaxis_title="Month",
            yaxis_title="Cumulative Unresolved Tickets",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(1, 13)),
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            ),
            height=450,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_backlog, use_container_width=True, config={"displayModeBar": False})
        
        # Insight
        final_backlog_2024 = df_2024_backlog['Cumulative_Backlog'].iloc[-1]
        final_backlog_2025 = df_2025_backlog['Cumulative_Backlog'].iloc[-1]
        
        if final_backlog_2024 > 0 and final_backlog_2025 < final_backlog_2024:
            st.success(f"✅ **Backlog Improvement**: 2025 ended with {abs(final_backlog_2025 - final_backlog_2024):.0f} fewer unresolved tickets than 2024")
        elif final_backlog_2025 > final_backlog_2024:
            st.warning(f"⚠️ **Backlog Growth**: 2025 accumulated {abs(final_backlog_2025 - final_backlog_2024):.0f} more unresolved tickets than 2024")
    
    st.markdown("---")
    
    # By Severity Comparison
    st.subheader("📊 Performance by Severity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚡ First Response Time by Severity")
        
        if 'frt' in data:
            df_frt = data['frt']
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_frt['Severity'],
                y=df_frt['2024_Avg_Hours'],
                name='2024',
                marker_color='#1f77b4'
            ))
            
            fig.add_trace(go.Bar(
                x=df_frt['Severity'],
                y=df_frt['2025_Avg_Hours'],
                name='2025',
                marker_color='#2ca02c'
            ))
            
            fig.update_layout(
                barmode='group',
                title="Avg Hours to First Response",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with col2:
        st.markdown("#### ⏱️ Resolution Time by Severity")
        
        if 'resolution' in data:
            df_res = data['resolution']
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_res['Severity'],
                y=df_res['2024_Avg_Days'],
                name='2024',
                marker_color='#1f77b4'
            ))
            
            fig.add_trace(go.Bar(
                x=df_res['Severity'],
                y=df_res['2025_Avg_Days'],
                name='2025',
                marker_color='#ff7f0e'
            ))
            
            fig.update_layout(
                barmode='group',
                title="Avg Days to Resolution",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    st.markdown("---")
    
    # Performance by Support Type
    st.subheader("📋 Performance by Support Type")
    
    st.info("💡 **Support Type** refers to which internal team handled the ticket (TEAM Support, Program Delivery, Product Division, etc.)")
    
    if 'support_types' in data:
        df_types = data['support_types']
        
        # Filter out very low volume types
        df_types_main = df_types[df_types['2025_Tickets'] >= 10].copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Ticket Volume by Support Type")
            
            fig_type_vol = go.Figure()
            
            fig_type_vol.add_trace(go.Bar(
                x=df_types_main['Support_Type'],
                y=df_types_main['2024_Tickets'],
                name='2024',
                marker_color='#1f77b4',
                text=df_types_main['2024_Tickets'],
                textposition='auto'
            ))
            
            fig_type_vol.add_trace(go.Bar(
                x=df_types_main['Support_Type'],
                y=df_types_main['2025_Tickets'],
                name='2025',
                marker_color='#ff7f0e',
                text=df_types_main['2025_Tickets'],
                textposition='auto'
            ))
            
            fig_type_vol.update_layout(
                barmode='group',
                title="Tickets by Support Type: 2024 vs 2025",
                xaxis_title="Support Type",
                yaxis_title="Number of Tickets",
                height=400,
                xaxis={'tickangle': -45}
            )
            
            st.plotly_chart(fig_type_vol, use_container_width=True, config={"displayModeBar": False})
        
        with col2:
            st.markdown("#### 📈 Support Type Distribution (2025)")
            
            fig_type_pie = go.Figure()
            
            fig_type_pie.add_trace(go.Pie(
                labels=df_types_main['Support_Type'],
                values=df_types_main['2025_Tickets'],
                hole=0.4
            ))
            
            fig_type_pie.update_layout(
                title="2025 Ticket Distribution",
                height=400
            )
            
            st.plotly_chart(fig_type_pie, use_container_width=True, config={"displayModeBar": False})
        
        # Full support type table
        st.markdown("#### 📋 Support Type Performance Details")
        
        st.dataframe(
            df_types.sort_values('2025_Tickets', ascending=False),
            width="stretch",
            hide_index=True,
            column_config={
                "Support_Type": st.column_config.TextColumn("Support Type", width="large"),
                "2024_Tickets": st.column_config.NumberColumn("2024", format="%d"),
                "2025_Tickets": st.column_config.NumberColumn("2025", format="%d"),
                "Change": st.column_config.NumberColumn("Change", format="%+d"),
                "Pct_Change": st.column_config.NumberColumn("% Change", format="%.1f%%")
            }
        )
        
        # Insights
        st.markdown("---")
        st.markdown("### 💡 Support Type Insights")
        
        team_support_2025 = df_types[df_types['Support_Type'] == 'TEAM Support']['2025_Tickets'].values[0] if 'TEAM Support' in df_types['Support_Type'].values else 0
        total_2025 = df_types['2025_Tickets'].sum()
        team_support_pct = (team_support_2025 / total_2025 * 100) if total_2025 > 0 else 0
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **TEAM Support handles {team_support_pct:.0f}% of all tickets**
            - Primary support team is core operation
            - Consistent year-over-year
            - Well-defined ownership
            """)
        
        with col2:
            unknown_2025 = df_types[df_types['Support_Type'] == 'Unknown']['2025_Tickets'].values[0] if 'Unknown' in df_types['Support_Type'].values else 0
            unknown_pct = (unknown_2025 / total_2025 * 100) if total_2025 > 0 else 0
            
            if unknown_pct > 5:
                st.warning(f"""
                **{unknown_pct:.1f}% tickets have Unknown support type**
                - Opportunity to improve tagging
                - Better routing and reporting
                - Action: Enforce support type on all tickets
                """)
            else:
                st.success(f"""
                **Only {unknown_pct:.1f}% Unknown support type**
                - Good tagging discipline
                - Clear ownership tracking
                    """)

# ==================
# AI CATEGORY INSIGHTS
# ==================
elif page == "🧪 AI Category Insights":
    st.header("🎯 2026 Strategic Priorities - Dual-Axis AI Analysis")
    
    st.markdown("""
    <div style='background-color: #e8f5e8; padding: 1rem; border-radius: 5px; border-left: 4px solid #28a745;'>
        <strong>🎯 Strategic Intelligence:</strong> Complete dual-axis analysis of 693 tickets with both CATEGORY (what area) and TYPE (bug/how-to/feature) classifications, 
        revealing actionable 2026 priorities with ROI calculations.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if 'dual_axis' in data:
        df_dual = data['dual_axis']
        
        # Hero Section
        st.subheader("📊 Analysis Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tickets Analyzed", len(df_dual))
        
        with col2:
            high_conf = len(df_dual[df_dual['confidence'] >= 90])
            st.metric("High Confidence", high_conf, f"{(high_conf/len(df_dual)*100):.0f}%")
        
        with col3:
            unique_cats = df_dual['category'].nunique()
            st.metric("Unique Categories", unique_cats)
        
        with col4:
            avg_conf = df_dual['confidence'].mean()
            st.metric("Avg Confidence", f"{avg_conf:.0f}%")
        
        st.markdown("---")
        
        # Type Distribution
        st.subheader("📈 Ticket Type Distribution")
        
        type_counts = df_dual['type'].value_counts()
        type_pct = (type_counts / len(df_dual) * 100).round(1)
        
        # Create donut chart
        fig_donut = go.Figure(data=[go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(
                colors=['#dc3545', '#007bff', '#28a745', '#ffc107', '#6f42c1', '#6c757d'],
                line=dict(color='#FFFFFF', width=2)
            )
        )])
        
        fig_donut.update_layout(
            title="Distribution of Ticket Types (693 tickets)",
            height=500,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.01
            )
        )
        
        # Add center text
        fig_donut.add_annotation(
            text=f"<b>{len(df_dual)}<br>Tickets</b>",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )
        
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})
        
        # Type breakdown table
        col1, col2 = st.columns([2, 1])
        
        with col1:
            type_breakdown = pd.DataFrame({
                'Type': type_counts.index,
                'Count': type_counts.values,
                'Percentage': type_pct.values
            })
            st.dataframe(type_breakdown, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("""
            **Type Definitions:**
            - **Bug-Defect:** System malfunctions requiring fixes
            - **How-To-Question:** User guidance and training needs
            - **Feature-Request:** Product enhancement requests
            - **Configuration-Setup:** System setup and configuration
            - **Performance-Issue:** Speed and optimization problems
            - **Data-Issue:** Data quality and integrity problems
            """)
        
        st.markdown("---")
        
        # 2026 Strategic Priorities
        st.subheader("🎯 2026 Strategic Priorities")
        
        tab1, tab2, tab3 = st.tabs(["🐛 Top Bug Categories", "📚 KB Opportunities", "⚙️ Config Wizards"])
        
        with tab1:
            st.markdown("### 🐛 Top 5 Bug Categories - Engineering Sprint Priorities")
            
            # Get top bug categories
            bug_tickets = df_dual[df_dual['type'] == 'Bug-Defect']
            bug_categories = bug_tickets['category'].value_counts().head(5)
            
            # Create horizontal bar chart
            fig_bugs = go.Figure()
            
            fig_bugs.add_trace(go.Bar(
                y=bug_categories.index,
                x=bug_categories.values,
                orientation='h',
                marker_color='#dc3545',
                text=bug_categories.values,
                textposition='auto'
            ))
            
            fig_bugs.update_layout(
                title="Top 5 Bug Categories by Volume",
                xaxis_title="Number of Bugs",
                yaxis_title=None,
                height=400
            )
            
            st.plotly_chart(fig_bugs, use_container_width=True, config={"displayModeBar": False})
            
            # Bug category details
            bug_details = []
            for category, count in bug_categories.items():
                category_tickets = bug_tickets[bug_tickets['category'] == category]
                avg_conf = category_tickets['confidence'].mean()
                bug_details.append({
                    'Category': category,
                    'Bug Count': count,
                    'Avg Confidence': f"{avg_conf:.0f}%",
                    'Expected Fix Impact': f"{count * 0.25:.0f} fewer tickets/year"
                })
            
            bug_df = pd.DataFrame(bug_details)
            st.dataframe(bug_df, use_container_width=True, hide_index=True)
            
            st.info("💡 **Engineering Impact:** Fixing these top 5 categories could reduce 47 tickets/year = $7,050 savings")
        
        with tab2:
            st.markdown("### 📚 Top 5 Knowledge Base Opportunities")
            
            # Get how-to questions
            howto_tickets = df_dual[df_dual['type'] == 'How-To-Question']
            howto_categories = howto_tickets['category'].value_counts().head(5)
            
            # Create KB opportunities table
            kb_opportunities = []
            for category, count in howto_categories.items():
                deflection_rate = 0.67 if 'Configuration' in category else 0.70
                expected_deflection = int(count * deflection_rate)
                kb_opportunities.append({
                    'Category': category,
                    'How-To Tickets': count,
                    'Deflection Rate': f"{deflection_rate*100:.0f}%",
                    'Expected Deflection': expected_deflection,
                    'Article Investment': '$500',
                    'Annual Savings': f"${expected_deflection * 150:.0f}"
                })
            
            kb_df = pd.DataFrame(kb_opportunities)
            st.dataframe(kb_df, use_container_width=True, hide_index=True)
            
            # KB impact visualization
            fig_kb = go.Figure()
            
            fig_kb.add_trace(go.Bar(
                name='Current Tickets',
                x=kb_df['Category'],
                y=kb_df['How-To Tickets'],
                marker_color='#ffc107'
            ))
            
            fig_kb.add_trace(go.Bar(
                name='Expected Deflection',
                x=kb_df['Category'],
                y=kb_df['Expected Deflection'],
                marker_color='#28a745'
            ))
            
            fig_kb.update_layout(
                title="Knowledge Base Impact: Current vs Expected Deflection",
                xaxis_title="Category",
                yaxis_title="Number of Tickets",
                barmode='group',
                height=400
            )
            
            st.plotly_chart(fig_kb, use_container_width=True, config={"displayModeBar": False})
            
            st.info("💡 **KB Impact:** 5 articles × $500 = $2,500 investment → 31 deflections/year = $4,650 savings (186% ROI)")
        
        with tab3:
            st.markdown("### ⚙️ Top Configuration Issues - Setup Wizards Needed")
            
            # Get configuration tickets
            config_tickets = df_dual[df_dual['type'] == 'Configuration-Setup']
            config_categories = config_tickets['category'].value_counts().head(3)
            
            # Create config wizard opportunities
            config_opportunities = []
            for category, count in config_categories.items():
                deflection_rate = 0.50 if 'Data-Configuration' in category else 0.45
                expected_deflection = int(count * deflection_rate)
                config_opportunities.append({
                    'Category': category,
                    'Config Tickets': count,
                    'Deflection Rate': f"{deflection_rate*100:.0f}%",
                    'Expected Deflection': expected_deflection,
                    'Wizard Type': 'Setup Templates' if 'Data' in category else 'Permission Guide',
                    'Development Cost': '$2,500' if 'Data' in category else '$2,500'
                })
            
            config_df = pd.DataFrame(config_opportunities)
            st.dataframe(config_df, use_container_width=True, hide_index=True)
            
            st.info("💡 **Wizard Impact:** $5,000 development → 18 deflections/year = $2,700 savings (54% ROI)")
        
        st.markdown("---")
        
        # ROI Summary Dashboard
        st.subheader("💰 ROI Summary Dashboard")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Investment",
                "$7,500",
                help="Bug fixes: $0 (engineering time) + KB articles: $2,500 + Wizards: $5,000"
            )
        
        with col2:
            st.metric(
                "Annual Savings",
                "$14,400",
                help="Bug reduction: $7,050 + KB deflection: $4,650 + Wizard deflection: $2,700"
            )
        
        with col3:
            st.metric(
                "Net Benefit",
                "$6,900/year",
                delta_color="normal"
            )
        
        with col4:
            st.metric(
                "ROI",
                "92%",
                delta_color="normal"
            )
        
        st.markdown("---")
        
        # Drill-Down Data Tables
        st.subheader("🔍 Drill-Down Analysis")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            type_filter = st.selectbox(
                "Filter by Type",
                ["All"] + list(df_dual['type'].unique()),
                key="type_filter"
            )
        
        with col2:
            confidence_threshold = st.slider(
                "Confidence Threshold",
                min_value=85,
                max_value=100,
                value=90,
                key="confidence_slider"
            )
        
        with col3:
            search_key = st.text_input(
                "Search Ticket Key",
                placeholder="e.g., KHELP-11561",
                key="search_key"
            )
        
        # Apply filters
        filtered_df = df_dual.copy()
        
        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]
        
        filtered_df = filtered_df[filtered_df['confidence'] >= confidence_threshold]
        
        if search_key:
            filtered_df = filtered_df[filtered_df['ticket_key'].str.contains(search_key, case=False, na=False)]
        
        st.markdown(f"**Showing {len(filtered_df)} tickets** (filtered from {len(df_dual)} total)")
        
        # Display filtered data
        if len(filtered_df) > 0:
            # Create display dataframe with truncated reasoning
            display_df = filtered_df.copy()
            display_df['reasoning_short'] = display_df['reasoning'].str[:100] + "..." if display_df['reasoning'].str.len() > 100 else display_df['reasoning']
            
            # Color code confidence
            def color_confidence(val):
                if val >= 95:
                    return 'background-color: #d4edda'  # green
                elif val >= 90:
                    return 'background-color: #fff3cd'  # yellow
                else:
                    return 'background-color: #f8d7da'  # red
            
            styled_df = display_df[['ticket_key', 'category', 'type', 'confidence', 'reasoning_short', 'components']].style.applymap(
                color_confidence, subset=['confidence']
            )
            
            st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "ticket_key": "Ticket Key",
                    "category": "Category",
                    "type": "Type",
                    "confidence": "Confidence %",
                    "reasoning_short": "Reasoning",
                    "components": "Components"
                }
            )
            
            # Export functionality
            st.markdown("---")
            st.subheader("📥 Export & Actions")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📊 Download Filtered Data",
                    data=csv,
                    file_name=f"dual_axis_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                if st.button("🎯 Generate Executive Summary", use_container_width=True):
                    st.info("Executive summary generation coming soon! Use the ROI dashboard above for now.")
            
            with col3:
                if st.button("📋 Create Action Plan", use_container_width=True):
                    st.info("Action plan creation coming soon! Use the strategic priorities above for now.")
        
        else:
            st.warning("No tickets match the current filters. Try adjusting your criteria.")
    
    else:
        st.warning("No dual-axis categorization data available. The analysis file 'categorization_dual_axis_20251021_171333.csv' was not found.")

# ==================
# COMPLETE DATA EXPORT
# ==================
elif page == "📊 Complete Data Export":
    st.header("Complete Data Export")
    
    st.markdown("""
    Download all strategic intelligence datasets for custom analysis, presentations, or further processing.
    """)
    
    # List all available datasets
    available_data = {
        "Organizations": data.get('orgs'),
        "Engineering Summary": data.get('eng_summary'),
        "Engineering by Team": data.get('eng_teams'),
        "Engineering by Severity": data.get('eng_severity'),
        "Categories with Engineering": data.get('cat_eng'),
        "Support Types": data.get('support_types'),
        "Team Scorecard": data.get('assignees'),
        "First Response Times": data.get('frt'),
        "Monthly Trends": data.get('monthly'),
        "Resolution Times": data.get('resolution')
    }
    
    for name, df in available_data.items():
        if df is not None:
            st.subheader(f"📥 {name}")
            st.dataframe(df.head(10), width="stretch")
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                f"Download {name}",
                csv,
                f"{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                key=f"download_{name}"
            )
            
            st.markdown("---")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>KHELP Ultimate Strategic Dashboard</strong></p>
    <p>Complete intelligence for data-driven support leadership</p>
    <p style='font-size: 0.9rem;'>Data includes: Organizations, Engineering Involvement, Team Performance, Customer Risk</p>
</div>
""", unsafe_allow_html=True)

