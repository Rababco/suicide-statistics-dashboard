import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configure page FIRST - before any other Streamlit commands
st.set_page_config(
    page_title="Global Suicide Statistics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Password Protection with Username and Password
def check_password():
    """Returns `True` if the user had the correct credentials."""
    
    # Define authorized users with their credentials
    AUTHORIZED_USERS = {
        "sh137": "Healthcare@2025!Prof",  # Professor credentials
        "ras96": "Analytics&Health#2025"  # Your credentials
    }
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state.get("username", "").strip()
        password = st.session_state.get("password", "")
        
        if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == password:
            st.session_state["password_correct"] = True
            st.session_state["authenticated_user"] = username
            # Clear the credentials from session state for security
            del st.session_state["username"]
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
            if "authenticated_user" in st.session_state:
                del st.session_state["authenticated_user"]

    # Return True if password is validated
    if st.session_state.get("password_correct", False):
        return True

    # Custom CSS for the login page
    st.markdown("""
<style>
.main > div {
    padding-top: 2rem;
    background-color: #f5f5f5;
}
.aub-logo {
    text-align: center;
    margin-bottom: 2rem;
}
.aub-logo img {
    max-width: 400px;
    height: auto;
}
.login-container {
    max-width: 450px;
    margin: 0 auto;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
}
.login-header {
    background: #008b8b;
    color: white;
    padding: 2rem;
    text-align: center;
}
.login-title {
    font-size: 1.75rem;
    font-weight: 600;
    margin: 0;
    letter-spacing: -0.5px;
}
.login-subtitle {
    font-size: 0.95rem;
    margin-top: 0.5rem;
    opacity: 0.9;
    font-weight: 300;
}
.login-body {
    padding: 2.5rem 2rem;
}
.prepared-by {
    background: #e8f5e8;
    border: 1px solid #20b2aa;
    border-radius: 6px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    text-align: center;
    font-size: 0.9rem;
    color: #008b8b;
    font-weight: 500;
}
.security-notice {
    background: #f8f9fa;
    border-left: 3px solid #008b8b;
    padding: 1rem;
    margin-bottom: 2rem;
    font-size: 0.9rem;
    color: #495057;
}
.auth-label {
    color: #495057;
    font-size: 0.875rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}
.data-info {
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #e9ecef;
    font-size: 0.875rem;
    color: #6c757d;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
    
    # Add AUB logo at the top
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        try:
            st.image("aub_logo.png", width=350)
        except:
            # Fallback if image not found
            st.markdown("""
            <div style="background: linear-gradient(135deg, #8B0000, #A52A2A); color: white; padding: 2rem; border-radius: 8px; text-align: center; margin-bottom: 2rem;">
                <h2 style="margin: 0; font-size: 1.5rem;">American University of Beirut</h2>
                <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">Suliman S. Olayan School of Business</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Create the login interface
    st.markdown("""
<div class="login-container">
    <div class="login-header">
        <div class="login-title">Healthcare Analytics Platform</div>
        <div class="login-subtitle">Global Suicide Statistics Dashboard</div>
    </div>
    <div class="login-body">
        <div class="prepared-by">
            Created by: Rabab Swaidan, MSBA Class of 2026
        </div>
        <div class="security-notice">
            <strong>Protected Resource</strong><br>
            This dashboard contains sensitive healthcare data and statistical analysis. 
            Access is restricted to authorized personnel only.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center the inputs with narrower middle column
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        st.text_input(
            "Username", 
            key="username",
            placeholder="Enter your username"
        )
        
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="Enter access password"
        )
        
        if "password_correct" in st.session_state:
            if not st.session_state["password_correct"]:
                st.error("⚠️ Authentication failed. Please verify your credentials.")
    
    # Add footer information
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
<div class="data-info">
    <strong>Dataset Information</strong><br>
    Coverage: 101 countries • Time Period: 1985-2016 • Updated: Quarterly<br>
    <br>
    <span style="color: #adb5bd; font-size: 0.8rem;">
    For access requests or technical support, please contact the Healthcare Analytics team.
    </span>
</div>
""", unsafe_allow_html=True)
    
    return False

# Check password first - if wrong, stop here
if not check_password():
    st.stop()

# Display welcome message with authenticated user
# if "authenticated_user" in st.session_state:
#     user_role = "Healthcare Analytics Supervisor" if st.session_state["authenticated_user"] == "sh137" else "Healthcare Data Analyst"
#     st.success(f"✅ Welcome, {st.session_state['authenticated_user']} ({user_role})")

# Custom CSS for compact layout
st.markdown("""
<style>
    .main > div {
        padding-top: 0.5rem;
        background-color: #f8f9fa;
    }
    .stApp {
        background-color: #f8f9fa;
    }
    .metric-card {
        background: linear-gradient(135deg, #20b2aa, #008b8b);
        color: white;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.2rem;
        height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.75rem;
        margin: 0;
        opacity: 0.9;
        line-height: 1.1;
    }
    .chart-container {
        background-color: white;
        padding: 0.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    .chart-title {
        color: #008b8b;
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.3rem;
        text-align: center;
    }
    h1 {
        color: #008b8b;
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 1.8rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #e0f7fa, #b2dfdb);
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .stMultiSelect > div > div {
        background-color: white;
    }
    
    /* Fix filter colors to match blue theme */
    .stMultiSelect > div > div > div > div > div {
        background-color: #20b2aa !important;
        color: white !important;
    }
    
    /* Style the multiselect tags */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #20b2aa !important;
        color: white !important;
    }
    
    /* Style slider */
    .stSlider > div > div > div > div {
        background-color: #20b2aa !important;
    }
    /* Hide streamlit header and footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Compact sidebar */
    .css-1d391kg {
        padding-top: 1rem;
    }
    
    /* Reduce padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess the data"""
    try:
        df = pd.read_csv('Suicide_dashboard.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please check the file path.")
        return None

def main():
    # Compact title
    st.markdown('<h1>Global Suicide Statistics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Fix data quality issues
    # Correct the typo in Generation column
    df['Generation'] = df['Generation'].replace('Millenials', 'Millennials')
    
    # Compact sidebar filters
    st.sidebar.markdown("### Filters")
    
    # Country filter - more compact
    countries = ['All'] + sorted(df['Country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Countries",
        countries,
        default=['All'],
        help="💡 TIP: Select individual countries to compare their rates meaningfully"
    )
    
    # Year range - more compact
    year_range = st.sidebar.slider(
        "Year Range",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(int(df['Year'].min()), int(df['Year'].max())),
        help="💡 TIP: Use recent years (2010+) for current policy relevance"
    )
    
    # Sex filter
    selected_sex = st.sidebar.multiselect(
        "Sex",
        df['Sex'].unique(),
        default=df['Sex'].unique()
    )
    
    # Age group filter
    age_order = ['5-14 years', '15-24 years', '25-34 years', '35-54 years', '55-74 years', '75+ years']
    selected_ages = st.sidebar.multiselect(
        "Age Groups",
        age_order,
        default=age_order,
        help="💡 TIP: Focus on '15-24 years' to identify youth suicide crises"
    )
    
    # Filter data
    filtered_df = df.copy()
    filtered_df = filtered_df[
        (filtered_df['Year'] >= year_range[0]) & 
        (filtered_df['Year'] <= year_range[1])
    ]
    filtered_df = filtered_df[filtered_df['Sex'].isin(selected_sex)]
    filtered_df = filtered_df[filtered_df['Age'].isin(selected_ages)]
    
    if 'All' not in selected_countries:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
    
    # Compact Key Metrics Row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_suicides = filtered_df['Suicides Count'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Suicides</p>
            <p class="metric-value">{total_suicides:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_rate = filtered_df['Suicides/100K Population'].mean()
        # Color code the rate - red if high, green if low
        rate_color = "#ff4444" if avg_rate > 20 else "#20b2aa"
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, {rate_color}, #008b8b);">
            <p class="metric-label">Avg Rate per 100K</p>
            <p class="metric-value">{avg_rate:.1f}</p>
            <p class="metric-label">{'HIGH RISK' if avg_rate > 20 else 'MODERATE' if avg_rate > 10 else 'LOW RISK'}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_population = filtered_df['Population'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Total Population</p>
            <p class="metric-value">{total_population/1000000:.1f}M</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        countries_count = filtered_df['Country'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Countries</p>
            <p class="metric-value">{countries_count}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        years_span = year_range[1] - year_range[0] + 1
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">Years Selected</p>
            <p class="metric-value">{years_span}</p>
            <p class="metric-label">{year_range[0]}-{year_range[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chart Row 1: Age groups and Geographic map (2 charts)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Suicide Rates by Age Group</div>', unsafe_allow_html=True)
        
        age_data = filtered_df.groupby(['Age', 'Sex']).agg({
            'Suicides Count': 'sum',
            'Population': 'sum'
        }).reset_index()
        age_data['Rate per 100K'] = (age_data['Suicides Count'] / age_data['Population']) * 100000
        
        age_data['Age'] = pd.Categorical(age_data['Age'], categories=age_order, ordered=True)
        age_data = age_data.sort_values('Age')
        
        fig_age = px.bar(
            age_data,
            x='Age',
            y='Rate per 100K',
            color='Sex',
            color_discrete_map={'Male': '#20b2aa', 'Female': '#ff6b6b'}
        )
        fig_age.update_layout(
            height=250,
            margin=dict(l=40, r=20, t=30, b=50),
            font=dict(size=12),
            xaxis_tickangle=-45,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=11)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_age.update_xaxes(title_font_size=12, tickfont_size=11)
        fig_age.update_yaxes(title_font_size=12, tickfont_size=11)
        st.plotly_chart(fig_age, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Geographic Distribution</div>', unsafe_allow_html=True)
        
        country_data = filtered_df.groupby('Country').agg({
            'Suicides Count': 'sum',
            'Population': 'sum'
        }).reset_index()
        country_data['Rate per 100K'] = (country_data['Suicides Count'] / country_data['Population']) * 100000
        
        fig_map = px.choropleth(
            country_data,
            locations='Country',
            locationmode='country names',
            color='Rate per 100K',
            hover_name='Country',
            hover_data={'Suicides Count': True, 'Rate per 100K': ':.1f', 'Population': ':,'},
            color_continuous_scale=['#e8f5e8', '#20b2aa', '#ffa500', '#ff6b6b', '#cc0000'],
            range_color=[0, 50]
        )
        fig_map.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=30, b=10),
            font=dict(size=11),
            geo=dict(
                showframe=False, 
                showcoastlines=True, 
                projection_type='natural earth',
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart Row 2: Generation analysis, GDP correlation, and Top countries (3 charts)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Gender Gap Analysis Over Time</div>', unsafe_allow_html=True)
        
        # Calculate gender gap trends
        gender_trends = filtered_df.groupby(['Year', 'Sex']).agg({
            'Suicides Count': 'sum',
            'Population': 'sum'
        }).reset_index()
        gender_trends['Rate per 100K'] = (gender_trends['Suicides Count'] / gender_trends['Population']) * 100000
        
        # Pivot to calculate male-to-female ratio
        gender_pivot = gender_trends.pivot(index='Year', columns='Sex', values='Rate per 100K').reset_index()
        if 'Male' in gender_pivot.columns and 'Female' in gender_pivot.columns:
            gender_pivot['Male-to-Female Ratio'] = gender_pivot['Male'] / gender_pivot['Female']
            gender_pivot['Gender Gap'] = gender_pivot['Male'] - gender_pivot['Female']
            
            # Create dual-axis chart showing both rates and ratio
            fig_gender = go.Figure()
            
            # Add male and female rates
            fig_gender.add_trace(go.Scatter(
                x=gender_pivot['Year'], 
                y=gender_pivot['Male'],
                name='Male Rate',
                line=dict(color='#20b2aa', width=3),
                yaxis='y'
            ))
            
            fig_gender.add_trace(go.Scatter(
                x=gender_pivot['Year'], 
                y=gender_pivot['Female'],
                name='Female Rate',
                line=dict(color='#ff6b6b', width=3),
                yaxis='y'
            ))
            
            # Add ratio line on secondary axis
            fig_gender.add_trace(go.Scatter(
                x=gender_pivot['Year'], 
                y=gender_pivot['Male-to-Female Ratio'],
                name='M/F Ratio',
                line=dict(color='#ffa500', width=2, dash='dash'),
                yaxis='y2'
            ))
            
            fig_gender.update_layout(
                height=200,
                margin=dict(l=40, r=40, t=30, b=40),
                font=dict(size=11),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=10)),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(
                    title="Rate per 100K",
                    side="left",
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)'
                ),
                yaxis2=dict(
                    title="M/F Ratio",
                    side="right",
                    overlaying="y",
                    showgrid=False,
                    range=[0, max(gender_pivot['Male-to-Female Ratio']) * 1.1] if not gender_pivot['Male-to-Female Ratio'].empty else [0, 5]
                ),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='rgba(128,128,128,0.2)'
                )
            )
        else:
            # Fallback if data doesn't have both sexes
            fig_gender = px.line(
                gender_trends,
                x='Year',
                y='Rate per 100K',
                color='Sex',
                color_discrete_map={'Male': '#20b2aa', 'Female': '#ff6b6b'}
            )
            fig_gender.update_layout(
                height=200,
                margin=dict(l=40, r=20, t=30, b=40),
                font=dict(size=12),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=11)),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        
        fig_gender.update_xaxes(title_font_size=11, tickfont_size=10)
        fig_gender.update_yaxes(title_font_size=11, tickfont_size=10)
        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Economic Factors</div>', unsafe_allow_html=True)
        
        # Add toggle for economic view
        econ_view = st.radio(
            "View:",
            ["Time Trends", "GDP Correlation", "Country Overview"],
            horizontal=True,
            label_visibility="collapsed",
            key="econ_view"
        )
        
        # Create income level categories based on GDP per capita distribution
        # These are adapted for GDP (not GNI) and based on the actual data distribution
        def categorize_income(gdp):
            if gdp < 3000:
                return 'Low Income'
            elif gdp < 9000:
                return 'Lower Middle'
            elif gdp < 25000:
                return 'Upper Middle'
            else:
                return 'High Income'
        
        # Add income level to filtered_df for both views
        filtered_df['Income Level'] = filtered_df['GDP Per Capita ($)'].apply(categorize_income)
        income_order = ['Low Income', 'Lower Middle', 'Upper Middle', 'High Income']
        
        if econ_view == "Time Trends":
            # Line chart showing trends over time for selected countries
            if 'All' in selected_countries or len(selected_countries) > 10:
                # If too many countries, show top 10 by average rate
                avg_rates = filtered_df.groupby('Country')['Suicides/100K Population'].mean().sort_values(ascending=False)
                top_countries_list = avg_rates.head(10).index.tolist()
                trend_data = filtered_df[filtered_df['Country'].isin(top_countries_list)]
                chart_title = "Top 10 Countries - Trends Over Time"
            else:
                trend_data = filtered_df
                chart_title = "Selected Countries - Trends Over Time"
            
            # Aggregate by country and year
            trend_summary = trend_data.groupby(['Country', 'Year']).agg({
                'Suicides Count': 'sum',
                'Population': 'sum',
                'GDP Per Capita ($)': 'mean'
            }).reset_index()
            trend_summary['Rate per 100K'] = (trend_summary['Suicides Count'] / trend_summary['Population']) * 100000
            trend_summary['Income Level'] = trend_summary['GDP Per Capita ($)'].apply(categorize_income)
            
            fig_gdp = px.line(
                trend_summary,
                x='Year',
                y='Rate per 100K',
                color='Country',
                markers=True,
                hover_data=['GDP Per Capita ($)', 'Income Level']
            )
            
            fig_gdp.update_traces(
                marker=dict(size=6),
                line=dict(width=2)
            )
            
            fig_gdp.update_layout(
                title=dict(text=chart_title, font=dict(size=12), y=0.98),
                hovermode='x unified'
            )
            
        elif econ_view == "GDP Correlation":
            # Original scatter plot view - country-year combinations
            gdp_data = filtered_df.groupby(['Country', 'Year']).agg({
                'Suicides Count': 'sum',
                'Population': 'sum',
                'GDP Per Capita ($)': 'mean'
            }).reset_index()
            gdp_data['Rate per 100K'] = (gdp_data['Suicides Count'] / gdp_data['Population']) * 100000
            gdp_data['Income Level'] = gdp_data['GDP Per Capita ($)'].apply(categorize_income)
            
            # Get only the income levels present in the filtered data
            present_income_levels = gdp_data['Income Level'].unique()
            present_income_order = [level for level in income_order if level in present_income_levels]
            
            # Create color map with only present income levels
            full_color_map = {
                'Low Income': '#d62728',
                'Lower Middle': '#ff7f0e', 
                'Upper Middle': '#2ca02c',
                'High Income': '#1f77b4'
            }
            color_map = {k: v for k, v in full_color_map.items() if k in present_income_levels}
            
            gdp_data['Income Level'] = pd.Categorical(gdp_data['Income Level'], categories=present_income_order, ordered=True)
            
            # Make size proportional to the rate itself for better visualization
            gdp_data['Size'] = gdp_data['Rate per 100K'] ** 1.5  # Use power to make differences more visible
            
            # Add option for animation
            animate_option = st.checkbox("Animate by Year", value=False, key="animate_gdp")
            
            if animate_option and len(gdp_data['Year'].unique()) > 1:
                fig_gdp = px.scatter(
                    gdp_data,
                    x='GDP Per Capita ($)',
                    y='Rate per 100K',
                    color='Income Level',
                    size='Size',
                    hover_data=['Country', 'Suicides Count'],
                    color_discrete_map=color_map,
                    category_orders={'Income Level': present_income_order},
                    size_max=15,
                    animation_frame='Year',
                    animation_group='Country',
                    range_x=[gdp_data['GDP Per Capita ($)'].min() * 0.9, gdp_data['GDP Per Capita ($)'].max() * 1.1],
                    range_y=[0, gdp_data['Rate per 100K'].max() * 1.1]
                )
                fig_gdp.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
            else:
                fig_gdp = px.scatter(
                    gdp_data,
                    x='GDP Per Capita ($)',
                    y='Rate per 100K',
                    color='Income Level',
                    size='Size',
                    hover_data=['Country', 'Year', 'Suicides Count'],
                    color_discrete_map=color_map,
                    category_orders={'Income Level': present_income_order},
                    size_max=15
                )
            
        else:  # Country Overview view - one dot per country
            # Average across all years for each country
            country_overview = filtered_df.groupby('Country').agg({
                'Suicides Count': 'sum',
                'Population': 'sum',
                'GDP Per Capita ($)': 'mean'
            }).reset_index()
            country_overview['Rate per 100K'] = (country_overview['Suicides Count'] / country_overview['Population']) * 100000
            country_overview['Income Level'] = country_overview['GDP Per Capita ($)'].apply(categorize_income)
            
            # Get only the income levels present in the filtered data
            present_income_levels = country_overview['Income Level'].unique()
            present_income_order = [level for level in income_order if level in present_income_levels]
            
            # Create color map with only present income levels
            full_color_map = {
                'Low Income': '#d62728',
                'Lower Middle': '#ff7f0e', 
                'Upper Middle': '#2ca02c',
                'High Income': '#1f77b4'
            }
            color_map = {k: v for k, v in full_color_map.items() if k in present_income_levels}
            
            country_overview['Income Level'] = pd.Categorical(country_overview['Income Level'], categories=present_income_order, ordered=True)
            
            # Make size proportional to the rate itself for better visualization
            country_overview['Size'] = country_overview['Rate per 100K'] ** 1.5  # Use power to make differences more visible
            
            fig_gdp = px.scatter(
                country_overview,
                x='GDP Per Capita ($)',
                y='Rate per 100K',
                color='Income Level',
                size='Size',
                hover_data=['Country', 'Suicides Count'],
                color_discrete_map=color_map,
                category_orders={'Income Level': present_income_order},
                size_max=20
            )
        
        # Adjust x-axis range based on the data
        if econ_view == "Time Trends":
            # For time trends, we don't need to adjust x-axis range
            pass
        elif econ_view == "GDP Correlation":
            if not gdp_data.empty:
                min_gdp = gdp_data['GDP Per Capita ($)'].min()
                max_gdp = gdp_data['GDP Per Capita ($)'].max()
                gdp_range = max_gdp - min_gdp
                x_min = max(0, min_gdp - gdp_range * 0.1)
                x_max = max_gdp + gdp_range * 0.1
            else:
                x_min = 0
                x_max = 82000
        else:  # Country Overview
            if not country_overview.empty:
                min_gdp = country_overview['GDP Per Capita ($)'].min()
                max_gdp = country_overview['GDP Per Capita ($)'].max()
                gdp_range = max_gdp - min_gdp
                x_min = max(0, min_gdp - gdp_range * 0.1)
                x_max = max_gdp + gdp_range * 0.1
            else:
                x_min = 0
                x_max = 82000
        
        fig_gdp.update_layout(
            height=170,
            margin=dict(l=40, r=40, t=10, b=40),
            font=dict(size=11),
            showlegend=True,
            legend=dict(
                orientation="h", 
                yanchor="bottom", 
                y=1.02, 
                xanchor="center", 
                x=0.5, 
                font=dict(size=10),
                itemsizing='constant'
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(
                tickformat='$,.0f' if econ_view != "Time Trends" else None,
                showgrid=True,
                gridcolor='rgba(128,128,128,0.2)',
                range=[x_min, x_max] if econ_view != "Time Trends" else None
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(128,128,128,0.2)'
            )
        )
        fig_gdp.update_xaxes(
            title_font_size=11, 
            tickfont_size=10
        )
        fig_gdp.update_yaxes(title_font_size=11, tickfont_size=10)
        
        st.plotly_chart(fig_gdp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top Countries by Rate</div>', unsafe_allow_html=True)
        
        top_countries = country_data.nlargest(10, 'Rate per 100K')
        
        # Add risk categorization
        top_countries['Risk Level'] = top_countries['Rate per 100K'].apply(
            lambda x: 'CRISIS' if x > 30 else 'HIGH' if x > 20 else 'ELEVATED' if x > 10 else 'MODERATE'
        )
        
        fig_top = px.bar(
            top_countries,
            x='Rate per 100K',
            y='Country',
            orientation='h',
            color='Rate per 100K',
            color_continuous_scale=['#20b2aa', '#ffa500', '#ff6b6b', '#cc0000'],
            hover_data=['Risk Level', 'Suicides Count']
        )
        fig_top.update_layout(
            height=200,
            margin=dict(l=80, r=20, t=30, b=40),
            font=dict(size=12),
            showlegend=False,
            yaxis={'categoryorder':'total ascending'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_top.update_xaxes(title_font_size=12, tickfont_size=11)
        fig_top.update_yaxes(title_font_size=12, tickfont_size=11)
        st.plotly_chart(fig_top, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
