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
    
    return data

# Load data
data = load_comprehensive_data()

# Sidebar navigation
st.sidebar.title("🎯 KHELP Strategic Dashboard")
st.sidebar.markdown("---")

# Navigation
pages = [
    "🎯 Executive Summary",
    "👥 Team Scorecard", 
    "🏢 Customer Intelligence",
    "⚙️ Engineering Analysis",
    "📊 Resolution Analysis"
]

page = st.sidebar.selectbox("Navigate", pages)

# ==================
# EXECUTIVE SUMMARY
# ==================
if page == "🎯 Executive Summary":
    st.header("🎯 Executive Summary")
    
    # Check if we have data
    if not data:
        st.error("No data files found. Please ensure CSV files are uploaded to the repository.")
        st.stop()
    
    # First row of KPIs
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'monthly' in data:
            total_2025 = data['monthly'][data['monthly']['Year'] == 2025]['Created'].sum()
            st.metric("Total Tickets (2025)", f"{total_2025:,}")
        else:
            st.metric("Total Tickets (2025)", "N/A")
    
    with col2:
        if 'eng_summary' in data:
            eng_rate = data['eng_summary'][data['eng_summary']['Metric'] == 'Engineering Involvement Rate']['2025_Value'].values[0]
            st.metric("Engineering Involvement", eng_rate)
        else:
            st.metric("Engineering Involvement", "N/A")
    
    with col3:
        if 'frt' in data:
            avg_frt = data['frt']['2025_Avg_Hours'].mean()
            st.metric("Avg First Response (hrs)", f"{avg_frt:.0f}")
        else:
            st.metric("Avg First Response (hrs)", "N/A")
    
    with col4:
        if 'resolution' in data:
            avg_res = data['resolution']['2025_Avg_Days'].mean()
            st.metric("Avg Resolution (days)", f"{avg_res:.0f}")
        else:
            st.metric("Avg Resolution (days)", "N/A")
    
    # Second row of KPIs - Resolution by Severity
    st.markdown("### Resolution Time by Severity")
    col5, col6, col7, col8 = st.columns(4)
    
    if 'resolution' in data:
        df_resolution = data['resolution']
        
        with col5:
            blocker_2025 = df_resolution[df_resolution['Severity'] == 'Blocker']['2025_Avg_Days'].values
            blocker_2024 = df_resolution[df_resolution['Severity'] == 'Blocker']['2024_Avg_Days'].values
            if len(blocker_2025) > 0:
                change = ((blocker_2025[0]-blocker_2024[0])/blocker_2024[0]*100) if len(blocker_2024) > 0 else 0
                st.metric("Blocker (days)", f"{blocker_2025[0]:.0f}", f"{change:+.1f}%")
            else:
                st.metric("Blocker (days)", "N/A")
        
        with col6:
            critical_2025 = df_resolution[df_resolution['Severity'] == 'Critical']['2025_Avg_Days'].values
            critical_2024 = df_resolution[df_resolution['Severity'] == 'Critical']['2024_Avg_Days'].values
            if len(critical_2025) > 0:
                change = ((critical_2025[0]-critical_2024[0])/critical_2024[0]*100) if len(critical_2024) > 0 else 0
                st.metric("Critical (days)", f"{critical_2025[0]:.0f}", f"{change:+.1f}%")
            else:
                st.metric("Critical (days)", "N/A")
        
        with col7:
            major_2025 = df_resolution[df_resolution['Severity'] == 'Major']['2025_Avg_Days'].values
            major_2024 = df_resolution[df_resolution['Severity'] == 'Major']['2024_Avg_Days'].values
            if len(major_2025) > 0:
                change = ((major_2025[0]-major_2024[0])/major_2024[0]*100) if len(major_2024) > 0 else 0
                st.metric("Major (days)", f"{major_2025[0]:.0f}", f"{change:+.1f}%")
            else:
                st.metric("Major (days)", "N/A")
        
        with col8:
            minor_2025 = df_resolution[df_resolution['Severity'] == 'Minor']['2025_Avg_Days'].values
            minor_2024 = df_resolution[df_resolution['Severity'] == 'Minor']['2024_Avg_Days'].values
            if len(minor_2025) > 0:
                change = ((minor_2025[0]-minor_2024[0])/minor_2024[0]*100) if len(minor_2024) > 0 else 0
                st.metric("Minor (days)", f"{minor_2025[0]:.0f}", f"{change:+.1f}%")
            else:
                st.metric("Minor (days)", "N/A")
    else:
        st.warning("Resolution data not available")
    
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
    
    if summary_metrics:
        st.dataframe(pd.DataFrame(summary_metrics), width="stretch", hide_index=True)
    else:
        st.warning("No data available for comparison")

# ==================
# TEAM SCORECARD
# ==================
elif page == "👥 Team Scorecard":
    st.header("Team Scorecard - Performance Within Levels")
    
    if 'assignees' not in data or 'contributors' not in data:
        st.error("Team performance data not available. Please ensure CSV files are uploaded.")
        st.stop()
    
    # Side-by-side layout
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
            <h3>LEVEL 1 AGENTS</h3>
            <p>Direct customer support and ticket resolution</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Level 1 Team Metrics
        l1_agents = data['assignees'][data['assignees']['Support_Level'] == 'Level 1']
        if not l1_agents.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_tickets = l1_agents['Total_Resolved'].mean()
                st.metric("Avg Tickets/Agent", f"{avg_tickets:.0f}")
            
            with col2:
                avg_res_time = l1_agents['Avg_Resolution_Days'].mean()
                st.metric("Avg Resolution Time", f"{avg_res_time:.1f}d")
            
            with col3:
                avg_res_rate = l1_agents['Resolution_Rate_Pct'].mean()
                st.metric("Avg Resolution Rate", f"{avg_res_rate:.1f}%")
            
            with col4:
                avg_eng_esc = l1_agents['Engineering_Escalation_Rate_Pct'].mean()
                st.metric("Avg Eng Escalation", f"{avg_eng_esc:.1f}%")
            
            # Individual Rankings
            st.subheader("Individual Rankings")
            l1_sorted = l1_agents.sort_values('Total_Resolved', ascending=False)
            
            for idx, row in l1_sorted.iterrows():
                with st.expander(f"{row['Assignee']} - {row['Total_Resolved']} tickets"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Resolution Rate", f"{row['Resolution_Rate_Pct']:.1f}%")
                    with col2:
                        st.metric("Avg Resolution", f"{row['Avg_Resolution_Days']:.1f}d")
                    with col3:
                        st.metric("Eng Escalation", f"{row['Engineering_Escalation_Rate_Pct']:.1f}%")
        else:
            st.warning("No Level 1 agent data available")
    
    with col_l2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
            <h3>LEVEL 2 CONTRIBUTORS</h3>
            <p>Technical triage and expert guidance</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Level 2 Team Metrics
        l2_contributors = data['contributors']
        if not l2_contributors.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_helped = l2_contributors['Tickets_Contributed'].sum()
                st.metric("Total Tickets Helped", f"{total_helped}")
            
            with col2:
                total_comments = l2_contributors['Total_Comments'].sum()
                st.metric("Total Comments", f"{total_comments}")
            
            with col3:
                avg_comments = l2_contributors['Avg_Comments_Per_Ticket'].mean()
                st.metric("Avg Comments/Ticket", f"{avg_comments:.1f}")
            
            with col4:
                avg_velocity = l2_contributors['Avg_Velocity_Per_Day'].mean()
                st.metric("Avg Velocity/Day", f"{avg_velocity:.1f}")
            
            # Individual Rankings
            st.subheader("Individual Rankings")
            l2_sorted = l2_contributors.sort_values('Tickets_Contributed', ascending=False)
            
            for idx, row in l2_sorted.iterrows():
                with st.expander(f"{row['Contributor']} - {row['Tickets_Contributed']} tickets helped"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Comments", f"{row['Total_Comments']}")
                    with col2:
                        st.metric("Avg Comments/Ticket", f"{row['Avg_Comments_Per_Ticket']:.1f}")
                    with col3:
                        if 'Avg_Hold_Time_Hours' in row and pd.notna(row['Avg_Hold_Time_Hours']):
                            st.metric("Avg Hold Time", f"{row['Avg_Hold_Time_Hours']:.1f}h")
                        else:
                            st.metric("Avg Hold Time", "N/A")
        else:
            st.warning("No Level 2 contributor data available")

# ==================
# CUSTOMER INTELLIGENCE
# ==================
elif page == "🏢 Customer Intelligence":
    st.header("🏢 Customer Intelligence")
    
    if 'orgs' not in data:
        st.error("Customer data not available. Please ensure CSV files are uploaded.")
        st.stop()
    
    # Customer metrics
    st.subheader("Top Customers by Volume")
    
    if not data['orgs'].empty:
        # Display top customers
        top_customers = data['orgs'].head(10)
        st.dataframe(top_customers, use_container_width=True)
    else:
        st.warning("No customer data available")

# ==================
# ENGINEERING ANALYSIS
# ==================
elif page == "⚙️ Engineering Analysis":
    st.header("⚙️ Engineering Analysis")
    
    if 'eng_summary' not in data:
        st.error("Engineering data not available. Please ensure CSV files are uploaded.")
        st.stop()
    
    # Engineering involvement metrics
    st.subheader("Engineering Involvement Summary")
    
    if not data['eng_summary'].empty:
        st.dataframe(data['eng_summary'], use_container_width=True)
    else:
        st.warning("No engineering data available")

# ==================
# RESOLUTION ANALYSIS
# ==================
elif page == "📊 Resolution Analysis":
    st.header("📊 Resolution Analysis")
    
    if 'resolution' not in data:
        st.error("Resolution data not available. Please ensure CSV files are uploaded.")
        st.stop()
    
    # Resolution times by severity
    st.subheader("Resolution Times by Severity")
    
    if not data['resolution'].empty:
        st.dataframe(data['resolution'], use_container_width=True)
    else:
        st.warning("No resolution data available")

# Footer
st.markdown("---")
st.markdown("**Kaptio Help Strategic Dashboard** | Data-driven insights for support team optimization")
