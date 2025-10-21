# Kaptio Help Strategic Dashboard

A comprehensive Streamlit dashboard for analyzing Kaptio support team performance, including Level 1 vs Level 2 agent analysis, customer intelligence, and year-over-year metrics.

## Features

- **Executive Summary**: Key performance indicators with YoY comparisons
- **Team Scorecard**: Level 1 vs Level 2 performance analysis  
- **Customer Intelligence**: Customer-specific metrics and trends
- **Engineering Analysis**: Escalation patterns and resolution times
- **Resolution Analysis**: Severity-based resolution tracking

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the dashboard:
```bash
streamlit run khelp_ultimate_dashboard.py
```

## Data Requirements

The dashboard expects CSV files in the same directory:
- `khelp_assignee_performance_*.csv` - Agent performance data
- `khelp_contributor_performance_*.csv` - Contributor analysis data
- `khelp_monthly_*.csv` - Monthly trends
- `khelp_engineering_*.csv` - Engineering escalation data
- `khelp_resolution_*.csv` - Resolution time data
- `khelp_frt_*.csv` - First response time data

## Deployment

This dashboard is designed to be deployed on Streamlit Cloud. Simply connect this repository and the app will automatically deploy.

## Team Structure

- **Level 1 Agents**: Chris Gaines, Mitchell Newman, Mark Horvat, Diego Manalang, Kenneth Frandolf Alsay
- **Level 2 Contributors**: Anna Dauzhuk, Raj Peshawaria

## Metrics Tracked

- First Response Time (FRT)
- Resolution times by severity
- Engineering escalation rates
- Team performance comparisons
- Customer-specific analytics