import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Password protection function
def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "healthcare2025":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1>🏥 Healthcare Analytics Dashboard</h1>
            <h2>Global Suicide Statistics</h2>
            <p style="color: #666; font-size: 1.1em;">Consultant Access Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1>🏥 Healthcare Analytics Dashboard</h1>
            <h2>Global Suicide Statistics</h2>
            <p style="color: #666; font-size: 1.1em;">Consultant Access Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Password", type="password", on_change=password_entered, key="password")
            st.error("❌ Password incorrect")
        return False
    else:
        return True

# Check password first - if wrong, stop here
if not check_password():
    st.stop()

# YOUR ORIGINAL WORKING CODE STARTS HERE - UNCHANGED
# Configure page
st.set_page_config(
    page_title="Global Suicide Statistics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    # Chart Row 1: Time series, Age groups, and Geographic map (3 charts)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Suicide Rates Over Time</div>', unsafe_allow_html=True)
        
        yearly_data = filtered_df.groupby(['Year', 'Sex']).agg({
            'Suicides Count': 'sum',
            'Population': 'sum'
        }).reset_index()
        yearly_data['Rate per 100K'] = (yearly_data['Suicides Count'] / yearly_data['Population']) * 100000
        
        fig_time = px.line(
            yearly_data, 
            x='Year', 
            y='Rate per 100K', 
            color='Sex',
            color_discrete_map={'Male': '#20b2aa', 'Female': '#ff6b6b'}
        )
        fig_time.update_layout(
            height=200,
            margin=dict(l=40, r=20, t=30, b=40),
            font=dict(size=12),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=11)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_time.update_xaxes(title_font_size=12, tickfont_size=11)
        fig_time.update_yaxes(title_font_size=12, tickfont_size=11)
        st.plotly_chart(fig_time, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
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
            height=200,
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
    
    with col3:
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
            height=200,
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
        st.markdown('<div class="chart-title">Suicide Rates by Generation</div>', unsafe_allow_html=True)
        
        gen_data = filtered_df.groupby(['Generation', 'Sex']).agg({
            'Suicides Count': 'sum',
            'Population': 'sum'
        }).reset_index()
        gen_data['Rate per 100K'] = (gen_data['Suicides Count'] / gen_data['Population']) * 100000
        
        # Define the proper chronological order
        generation_order = ['G.I. Generation', 'Silent', 'Boomers', 'Generation X', 'Millennials', 'Generation Z']
        # Only include generations that exist in the filtered data
        available_generations = [gen for gen in generation_order if gen in gen_data['Generation'].values]
        
        gen_data['Generation'] = pd.Categorical(gen_data['Generation'], categories=available_generations, ordered=True)
        gen_data = gen_data.sort_values('Generation')
        
        fig_gen = px.bar(
            gen_data,
            x='Generation',
            y='Rate per 100K',
            color='Sex',
            color_discrete_map={'Male': '#20b2aa', 'Female': '#ff6b6b'}
        )
        fig_gen.update_layout(
            height=200,
            margin=dict(l=40, r=20, t=30, b=50),
            font=dict(size=12),
            xaxis_tickangle=-45,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(size=11)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_gen.update_xaxes(title_font_size=12, tickfont_size=11)
        fig_gen.update_yaxes(title_font_size=12, tickfont_size=11)
        st.plotly_chart(fig_gen, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
    
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Economic Factors</div>', unsafe_allow_html=True)
        
        gdp_data = filtered_df.groupby(['Country', 'Year']).agg({
            'Suicides Count': 'sum',
            'Population': 'sum',
            'GDP Per Capita ($)': 'mean'
        }).reset_index()
        gdp_data['Rate per 100K'] = (gdp_data['Suicides Count'] / gdp_data['Population']) * 100000
        
        # Create income level categories based on World Bank classifications
        def categorize_income(gdp):
            if gdp < 1000:
                return 'Low Income (<$1K)'
            elif gdp < 4000:
                return 'Lower Middle Income ($1K-$4K)'
            elif gdp < 12000:
                return 'Upper Middle Income ($4K-$12K)'
            else:
                return 'High Income (>$12K)'
        
        gdp_data['Income Level'] = gdp_data['GDP Per Capita ($)'].apply(categorize_income)
        
        # Define the order for the legend
        income_order = ['Low Income (<$1K)', 'Lower Middle Income ($1K-$4K)', 
                       'Upper Middle Income ($4K-$12K)', 'High Income (>$12K)']
        gdp_data['Income Level'] = pd.Categorical(gdp_data['Income Level'], categories=income_order, ordered=True)
        
        fig_gdp = px.scatter(
            gdp_data,
            x='GDP Per Capita ($)',
            y='Rate per 100K',
            color='Income Level',
            size='Suicides Count',
            hover_data=['Country', 'Year'],
            color_discrete_map={
                'Low Income (<$1K)': '#d62728',
                'Lower Middle Income ($1K-$4K)': '#ff7f0e', 
                'Upper Middle Income ($4K-$12K)': '#2ca02c',
                'High Income (>$12K)': '#1f77b4'
            },
            title="Suicide Rate vs Economic Development",
            category_orders={'Income Level': income_order}
        )
        fig_gdp.update_layout(
            height=200,
            margin=dict(l=40, r=80, t=40, b=40),
            font=dict(size=12),
            showlegend=True,
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02, font=dict(size=10)),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig_gdp.update_xaxes(title_font_size=12, tickfont_size=11)
        fig_gdp.update_yaxes(title_font_size=12, tickfont_size=11)
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
    
    # Analysis insights panel
    st.markdown("---")
    st.markdown("### 📋 Key Insights & Analysis Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Risk assessment
        high_risk_countries = country_data[country_data['Rate per 100K'] > 20]
        crisis_countries = country_data[country_data['Rate per 100K'] > 30]
        
        st.markdown(f"""
        **🚨 Risk Assessment:**
        - **{len(crisis_countries)} countries** in CRISIS (>30 per 100K)
        - **{len(high_risk_countries)} countries** at HIGH RISK (>20 per 100K)
        - Global average: **{filtered_df['Suicides/100K Population'].mean():.1f} per 100K**
        """)
        
        if len(crisis_countries) > 0:
            st.markdown(f"**Crisis Countries:** {', '.join(crisis_countries['Country'].head(3).tolist())}")
    
    with col2:
        st.markdown("""
        **💡 Analysis Tips:**
        - Compare **rates per 100K**, not raw numbers
        - Small countries with high rates need urgent attention
        - Filter by individual countries for accurate comparison
        - Focus on 15-24 age group for youth crisis identification
        - Use recent years (2010+) for policy relevance
        """)

if __name__ == "__main__":
    main()
