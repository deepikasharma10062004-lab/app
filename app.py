import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(page_title="Social Media Dashboard", layout="wide")

st.title("📊 Social Media Analytics Dashboard")

# =========================
# File Upload
# =========================
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file to continue")
    st.stop()


# =========================
# Load & Process Data
# =========================
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)

    # Cleaning
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    # Convert Date
    df['Date'] = pd.to_datetime(df['Date'])

    # Feature Engineering
    df['Hour'] = df['Date'].dt.hour
    df['Engagement'] = df['Likes'] + df['Comments'] + df['Shares']

    return df


df = load_data(uploaded_file)

# =========================
# Sidebar Filters
# =========================
st.sidebar.header("🔍 Filters")

platforms = st.sidebar.multiselect(
    "Select Platform",
    options=df['Platform'].unique(),
    default=df['Platform'].unique()
)

date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Date'].min(), df['Date'].max()]
)

# Apply Filters
filtered_df = df[
    (df['Platform'].isin(platforms)) &
    (df['Date'].dt.date >= date_range[0]) &
    (df['Date'].dt.date <= date_range[1])
    ]

# =========================
# Show Data
# =========================
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df)

# =========================
# KPI Metrics
# =========================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Posts", len(filtered_df))
col2.metric("Avg Engagement", int(filtered_df['Engagement'].mean()))
col3.metric("Max Engagement", int(filtered_df['Engagement'].max()))

# =========================
# Charts
# =========================

# Platform Engagement
st.subheader("📊 Average Engagement by Platform")
platform_engagement = filtered_df.groupby('Platform')['Engagement'].mean()

fig1, ax1 = plt.subplots()
platform_engagement.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_ylabel("Engagement")
st.pyplot(fig1)

# Engagement Over Time
st.subheader("📈 Engagement Over Time")
df_sorted = filtered_df.sort_values('Date')

fig2, ax2 = plt.subplots()
ax2.plot(df_sorted['Date'], df_sorted['Engagement'], color='green')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Post Type Pie Chart
st.subheader("🥧 Post Type Distribution")
fig3, ax3 = plt.subplots()
filtered_df['Post_Type'].value_counts().plot(
    kind='pie', autopct='%1.1f%%', ax=ax3
)
ax3.set_ylabel("")
st.pyplot(fig3)

# Heatmap
st.subheader("🔥 Correlation Heatmap")
fig4, ax4 = plt.subplots()
corr = filtered_df[['Likes', 'Comments', 'Shares', 'Engagement']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

# Best Time to Post
st.subheader("⏰ Best Time to Post")
best_time = filtered_df.groupby('Hour')['Engagement'].mean()

fig5, ax5 = plt.subplots()
best_time.plot(ax=ax5, marker='o', color='purple')
ax5.set_ylabel("Avg Engagement")
st.pyplot(fig5)

# =========================
# Top Posts
# =========================
st.subheader("🏆 Top 5 Posts")
top_posts = filtered_df.sort_values(by='Engagement', ascending=False).head(5)
st.dataframe(top_posts)

# =========================
# Insights
# =========================
st.subheader("💡 Insights")

st.write("""
- Platforms with higher engagement stand out clearly in the bar chart  
- Video/Reel content usually dominates engagement  
- Evening hours tend to perform better  
- Engagement strongly correlates with likes and shares  
""")