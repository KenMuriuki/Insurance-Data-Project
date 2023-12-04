import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
from query import * 
import time

st.set_page_config(page_title="Dashboard", page_icon="🌲",layout="wide")
st.subheader("🛹 Insurance Descriptive Analytics")
st.markdown("##")

# show the sidebar
st.sidebar.image("data/logo.png", caption="Online Analytics")

# display the dataframe
result = view_all_data()
df = pd.DataFrame(result, columns=['Policy','Expiry','Location','State','Region','Investment','Construction','BusinessType','Earthquake','Flood','Rating','ID'])
#st.dataframe(df)


# switcher
st.sidebar.header("Please filter")
region = st.sidebar.multiselect(
    "Please select region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
location = st.sidebar.multiselect(
    "Please select location",
    options=df["Location"].unique(),
    default=df["Location"].unique()
)
construction = st.sidebar.multiselect(
    "Please select construction",
    options=df["Construction"].unique(),
    default=df["Construction"].unique()
)

df_selection = df.query(
    "Region==@region & Location==@location & Construction==@construction"
)


def Home():
    with st.expander("Tabular"):
        showData = st.multiselect("Filter: ",df_selection.columns, default=[])
        st.write(df_selection[showData])
    

    # top analytics
    total_investment = float(df_selection['Investment'].sum())
    investment_mode = float(df_selection['Investment'].mode())
    investment_mean = float(df_selection['Investment'].mean())
    investment_median = float(df_selection['Investment'].median())
    total_rating = float(df_selection['Rating'].sum())

    # creating the holding containers
    tab1, tab2, tab3, tab4, tab5 = st.columns(5, gap="medium")
    with tab1:
        st.info("Total investment", icon="📌")
        st.metric(label="Sum KES", value=f"{total_investment:,.0f}")
    with tab2:
        st.info("Most frequent investment", icon="📌")
        st.metric(label="mode KES", value=f"{investment_mode:,.0f}")
    with tab3:
        st.info("Average investment", icon="📌")
        st.metric(label="mean KES", value=f"{investment_mean:,.0f}")
    with tab4:
        st.info("Central investment", icon="📌")
        st.metric(label="median KES", value=f"{investment_median:,.0f}")
    with tab5:
        st.info("Rating", icon="📌")
        st.metric(label="Rating", value=numerize(total_rating), help=f""" Total Rating: {total_rating} """)
    st.markdown("""---""")

# graphs
def graphs():
    # bar graph
    investment_by_business_type = (
    df_selection.groupby(by="BusinessType").count()[['Investment']].sort_values(by="Investment")
    )
    fig_investment=px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b> Investment by business type </b>",
        color_discrete_sequence=["#0083b8"]*len(investment_by_business_type.index),
        template="plotly_white"
    )
    fig_investment.update_layout(
        plot_bgcolor= "rgba(0,0,0,0)",
        xaxis = (dict(showgrid=False))
    )

    # line graph
    investment_by_state = df_selection.groupby(by="State").count()[['Investment']]
    fig_state=px.line(
        investment_by_state,
        x=investment_by_state.index,
        y=['Investment'],
        orientation="v",
        title="<b> Investment by State </b>",
        color_discrete_sequence= ["#0083b8"]*len(investment_by_state),
        template="plotly_white"
    )
    fig_state.update_layout(
        xaxis = dict(tickmode="linear"),
        plot_bgcolor= "rgba(0,0,0,0)",
        yaxis = (dict(showgrid=False))
    )

    left, right = st.columns(2)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)


def Progressbar():
    st.markdown(""" <style>.stProgress > div > div > div> div { background-image: linear-gradients(to right, #99ff99, #FFFF00)} </style>""", unsafe_allow_html=True)
    target = 2500000000
    current = df_selection["Investment"].sum()
    percent = round((current/target)* 100)
    mybar  = st.progress(0)

    if percent > 100:
        st.subheader("Target achieved!")
    else:
        st.write("You have attained", percent, "%","of your KES", "{:,.2f}".format(target), "target.")
        for percent_complete in range(percent):
            time.sleep(0.01)
            mybar.progress(percent_complete + 1, text="Target Percentage")
    
def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    if selected == "Home":
        st.subheader(f'Page:{selected}')
        Home()
        graphs()
    if selected == "Progress":
        st.subheader(f"Page: {selected}")
        Progressbar()
        graphs()

sideBar()

# theme
hide_st_style="""
<stle>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""

