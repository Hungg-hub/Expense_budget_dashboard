import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Personal Expense Dashboard", layout="wide", page_icon="💳")

# --- Helper Function: Rule-based Categorization ---
def categorize_expense(description: str) -> str:
    desc = str(description).lower()
    if any(k in desc for k in ["supermarket", "life", "maruetsu", "seiyu", "7-eleven", "lawson", "familymart", "bento", "grocer", "hanamasa"]):
        return "Groceries & Food"
    elif any(k in desc for k in ["starbucks", "cafe", "coffee", "uber eats", "restaurant", "dinner", "doutor", "ichiran", "sukiya", "saizeriya", "kura sushi"]):
        return "Dining Out"
    elif any(k in desc for k in ["metro", "pasmo", "suica", "jr", "train", "bus", "taxi", "transit"]):
        return "Transportation"
    elif any(k in desc for k in ["amazon", "uniqlo", "bic camera", "shopping", "rakuten", "yodobashi", "muji"]):
        return "Shopping & Tech"
    else:
        return "Other"

# --- Sidebar: File Upload & Controls ---
st.sidebar.header("📁 Data Input")
uploaded_file = st.sidebar.file_uploader("Upload your transactions CSV", type=["csv"])

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("transactions.csv")
    except Exception:
        sample_data = {
            "Date": ["2026-08-01", "2026-08-02", "2026-08-03", "2026-08-05", "2026-08-08", "2026-08-10", "2026-08-12", "2026-08-20"],
            "Description": ["Starbucks Cafe", "Life Supermarket", "Tokyo Metro Pass", "Amazon Order", "7-Eleven Snack", "Uniqlo Clothing", "Uber Eats Delivery", "Maruetsu Grocery"],
            "Amount": [650, 4200, 2000, 1890, 720, 5990, 2450, 3100]
        }
        df = pd.DataFrame(sample_data)

# --- Data Cleaning & Processing ---
try:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"])
    df["Category"] = df["Description"].apply(categorize_expense)
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
except KeyError:
    st.error("CSV must contain 'Date', 'Description', and 'Amount' columns.")
    st.stop()

# --- Sidebar Month Filter ---
all_months = sorted(df["Month"].unique().tolist())
selected_month = st.sidebar.selectbox("📅 Select Month View", options=["All Months"] + all_months)

# Apply month filter to active view
if selected_month != "All Months":
    active_df = df[df["Month"] == selected_month]
else:
    active_df = df.copy()

# --- Top Key Metrics (KPIs) ---
st.title("💳 Personal Expense & Budget Dashboard")
if selected_month != "All Months":
    st.caption(f"Showing financial metrics for **{selected_month}**")
else:
    st.caption("Showing financial metrics across **All Months**")

total_spending = active_df["Amount"].sum()
avg_transaction = active_df["Amount"].mean() if len(active_df) > 0 else 0
total_transactions = len(active_df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Expenses", f"¥{total_spending:,.0f}")
col2.metric("Average Transaction", f"¥{avg_transaction:,.0f}")
col3.metric("Total Transactions", total_transactions)

st.divider()

# --- Monthly Comparison Section ---
st.subheader("📊 Monthly Expense Analysis")
monthly_summary = (
    df.groupby("Month")["Amount"]
    .agg(Total_Spent="sum", Transactions="count", Average_Spent="mean")
    .reset_index()
)
monthly_summary["Average_Spent"] = monthly_summary["Average_Spent"].round(0)

m_col1, m_col2 = st.columns([1, 1])

with m_col1:
    # Monthly Total Comparison Bar Chart
    fig_monthly = px.bar(
        monthly_summary,
        x="Month",
        y="Total_Spent",
        text_auto=",.0f",
        title="Total Spending by Month (¥)",
        labels={"Total_Spent": "Total Spent (¥)", "Month": "Month"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig_monthly.update_layout(yaxis_title="Amount (¥)", xaxis_title="Month")
    st.plotly_chart(fig_monthly, use_container_width=True)

with m_col2:
    # Stacked Monthly Category Breakdown
    monthly_cat = df.groupby(["Month", "Category"])["Amount"].sum().reset_index()
    fig_cat_monthly = px.bar(
        monthly_cat,
        x="Month",
        y="Amount",
        color="Category",
        title="Monthly Spending Breakdown by Category (¥)",
        labels={"Amount": "Amount (¥)"},
        barmode="stack",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_cat_monthly, use_container_width=True)

# Monthly Summary Table
with st.expander("🔎 View Monthly Summary Data Table"):
    st.dataframe(
        monthly_summary.rename(
            columns={
                "Month": "Month",
                "Total_Spent": "Total Expense (¥)",
                "Transactions": "Number of Transactions",
                "Average_Spent": "Average Spend / Transaction (¥)"
            }
        ),
        use_container_width=True
    )

st.divider()

# --- Current View Visualizations ---
st.subheader("📈 Detailed Category & Daily Trends")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("**Spending by Category**")
    category_df = active_df.groupby("Category")["Amount"].sum().reset_index()
    fig_pie = px.pie(
        category_df,
        values="Amount",
        names="Category",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.markdown("**Daily Spending Trend**")
    daily_df = active_df.groupby(active_df["Date"].dt.date)["Amount"].sum().reset_index()
    fig_line = px.bar(
        daily_df,
        x="Date",
        y="Amount",
        labels={"Amount": "Spent (¥)", "Date": "Date"},
        color_discrete_sequence=["#3366CC"]
    )
    st.plotly_chart(fig_line, use_container_width=True)

# --- Transaction Table with Filter ---
st.subheader("🧾 Transaction History")
available_categories = active_df["Category"].unique().tolist()
selected_category = st.multiselect(
    "Filter by Category:",
    options=available_categories,
    default=available_categories
)

filtered_df = active_df[active_df["Category"].isin(selected_category)].sort_values(by="Date", ascending=False)
st.dataframe(
    filtered_df[["Date", "Description", "Category", "Amount"]].assign(
        Date=lambda x: x["Date"].dt.strftime("%Y-%m-%d"),
        Amount=lambda x: x["Amount"].map("¥{:,.0f}".format)
    ),
    use_container_width=True
)