import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import os
import time

# Set up the page configuration
st.set_page_config(page_title="Insurance Dashboard", page_icon="📶", layout="wide")
st.subheader("📶 Insurance Analytical Reporting")
st.markdown("###")

# Define file path
file_path = os.path.join("Data", "Insurance Data.csv")

# Load CSV file
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    
    # Check if the ID column exists; if not, add it
    if 'ID' not in df.columns:
        df['ID'] = range(1, len(df) + 1)
        # Save the updated DataFrame to a new CSV file
        df.to_csv(file_path, index=False)
    
    # Ensure the DataFrame contains the expected columns
    expected_columns = ["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating","ID"]
    if not all(column in df.columns for column in expected_columns):
        st.error("The CSV file does not contain the required columns.")
        st.stop()

    # Sidebar logo and main menu
    st.sidebar.image("Images/Insurance.jpg", caption="Insurance Data Analytics")
    with st.sidebar:
        selected = option_menu(
            menu_title="",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon='cast',
            default_index=0
        )
        st.sidebar.header("Please Apply filters")
        region = st.sidebar.multiselect(
            "Select Region",
            options=df["Region"].unique(),
            default=df['Region'].unique()
        )
        location = st.sidebar.multiselect(
            "Select Location",
            options=df["Location"].unique(),
            default=df['Location'].unique()
        )
        construction = st.sidebar.multiselect(
            "Select Construction",
            options=df["Construction"].unique(),
            default=df['Construction'].unique()
        )

    df_selection = df.query(
        "Region == @region & Location == @location & Construction == @construction"
    )

    def Home():
        with st.expander("Tabular"):
            showData = st.multiselect('Filter:', df_selection.columns, default=[])
            st.write(df_selection[showData])
        
        total_investment = float(df_selection["Investment"].sum())
        investment_mode_series = df_selection["Investment"].mode()
        investment_mode = float(investment_mode_series[0]) if not investment_mode_series.empty else float('nan')
        investment_median = float(df_selection["Investment"].median())
        investment_mean = float(df_selection["Investment"].mean())
        rating = float(df_selection["Rating"].sum())

        total1, total2, total3, total4, total5 = st.columns(5, gap='large')

        with total1:
            st.info('Total Investment', icon='📌')
            st.metric(label="sum TZS", value=f"{total_investment:,.0f}")

        with total2:
            st.info('Most frequent', icon='📌')
            st.metric(label="mode TZS", value=f"{investment_mode:,.0f}")
        
        with total3:
            st.info('Average', icon='📌')
            st.metric(label="average TZS", value=f"{investment_mean:,.0f}")
        
        with total4:
            st.info('Central Earnings', icon='📌')
            st.metric(label="median TZS", value=f"{investment_median:,.0f}")
        
        with total5:
            st.info('Ratings', icon='📌')
            st.metric(label="Rating", value=numerize(rating), help=f"Total Rating: {rating}")

        st.markdown("""---""")

    def graphs():
        investment_by_businesstype = (
            df_selection.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
        )
        fig_investment = px.bar(
            x=investment_by_businesstype["Investment"],
            y=investment_by_businesstype.index,
            orientation="h",
            title="<b> Investment by Business Type",
            color_discrete_sequence=["#0083b8"] * len(investment_by_businesstype),
            template="plotly_white",
        )

        fig_investment.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=(dict(showgrid=False))
        )

        investment_state = (
            df_selection.groupby(by=["State"]).count()[["Investment"]]
        )
        fig_state = px.line(
            investment_state,
            x=investment_state.index,
            y="Investment",
            orientation="v",
            title="<b> Investment by State",
            color_discrete_sequence=["#0083b8"] * len(investment_state),
            template="plotly_white",
        )

        fig_state.update_layout(
            xaxis=dict(tickmode="linear"),
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=(dict(showgrid=False))
        )
        
        left, right = st.columns(2)
        left.plotly_chart(fig_state, use_container_width=True)
        right.plotly_chart(fig_investment, use_container_width=True)

    def Progressbar():
        st.markdown(
            """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99, #FFFF00)}</style>""",
            unsafe_allow_html=True,
        )
        target = 300000000
        current = df_selection["Investment"].sum()
        percent = round((current / target * 100))
        mybar = st.progress(0)

        if percent > 100:
            st.subheader("Target Done !")
        else:
            st.write("you have ", percent, "% ", " of ", (format(target, 'd')), "TZS")
            for percent_complete in range(percent):
                time.sleep(0.1)
                mybar.progress(percent_complete + 1, text="Target Percentage")

    if selected == "Home":
        st.subheader(f"{selected}")
        Home()
        graphs()
    elif selected == "Progress":
        st.subheader(f"{selected}")
        Progressbar()
        graphs()

    hide_st_style = """
    <style>
    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    header {visibility:hidden;}
    </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
else:
    st.info("Please ensure the file 'Insurance Data.csv' is in the 'Data' folder.")