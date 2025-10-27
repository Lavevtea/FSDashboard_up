import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from io import BytesIO
import numpy as np
import time
import os
import datetime as dt
import textwrap
from Sidebar import show_sidebar_menu
from features.WoChart import render_wochart
from features.StatusChart import render_statuschart
from features.Sla import render_slasum
from features.StatusInfo import render_guide
from features.ExportSla import exportsla  
# from features.merge_files import render_merge_files


st.set_page_config(layout="wide", page_title="FIELDSA DASHBOARD UP")
with open("header.html", "r") as head:
    st.markdown(head.read(), unsafe_allow_html=True)



uploaded=st.file_uploader("Upload Excel File", type=["xlsx", "csv"]) 

if uploaded is not None:
    up2webtime= pd.Timestamp.now()
    @st.cache_data
    def load(file):
        if file.name.endswith(".csv"):
            return {"WorkOrder": pd.read_csv(file)}
        else:
            return pd.read_excel(file, sheet_name=None)
    exceldata=load(uploaded)
    df= exceldata.get("WorkOrder")
    df_rca= exceldata.get("Rca")
    df_history= exceldata.get("HistoryWorkOrder")
    
    df["Created"]= pd.to_datetime(df["Created"], errors="coerce")
    df= df.dropna(subset=["Created"])
    firstdate= df["Created"].min().date()
    lastdate= df["Created"].max().date()
    rangetgl= st.date_input(
        "Select data range",
        (firstdate,lastdate),
        min_value= firstdate,
        max_value= lastdate
    )
    if len(rangetgl)== 2:
        tglawal,tglakhir= rangetgl
        df= df[(df["Created"]>=pd.to_datetime(tglawal)) &
                (df["Created"]<=pd.to_datetime(tglakhir)+pd.Timedelta(days=1)-pd.Timedelta(seconds=1))] 
    regionmap={
        "Bali": "East",
        "Central Java": "Central",
        "East Java": "East",
        "Jabodetabek":"Central",
        "West Java": "Central",
        "Kalimantan":"East",
        "Sulawesi":"East",
        "Internasional": "International",
        "Kepulauan Riau": "West",
        "Northern Sumatera":"West",
        "Southern Sumatera":"West"
    }

    if "SubRegion" in df.columns:
        df["SubRegion"] = df["SubRegion"].astype(str).str.title()
        df["Region"]= df["SubRegion"].map(regionmap).fillna("Unknown")
    if "City" in df.columns:
        df["City"] = df["City"].astype(str).str.title()
    
    if df is not None:
        df["uptime"]= up2webtime
        col1,col2, col3=st.columns([1,2,2])
        col1.metric("Total WO Number", len(df))
        try:
            identify= pd.to_datetime(uploaded.name.split("_")[1].split(".")[0], format="%Y%m%d%H%M%S")
            lastupdate= identify.strftime("%d %B %Y %H:%M:%S")
        except:
            lastupdate= "Date not valid"

        col2.metric("Date pulled from FIELDSA", lastupdate)
        last_input_refresh= df["uptime"].max().strftime("%d %B %Y %H:%M:%S")
        col3.metric("Last Input/Refresh", last_input_refresh)

        dfstat= df.copy()     
        
        show_sidebar_menu(df, uploaded)
        menu_sidebar = st.session_state.get("menu_sidebar", "WorkOrder Chart")
        
        st.divider()

        if menu_sidebar == "WorkOrder Chart":
            render_wochart(df)

        elif menu_sidebar == "Status Chart":
            render_statuschart(dfstat,exceldata)

        elif menu_sidebar == "SLA Summary":
            render_slasum(df, exceldata, df_history)
             
        elif menu_sidebar == "Export SLA":
            exportsla(df, df_rca, df_history)

        elif menu_sidebar == "Status Information":
            render_guide(df)
        


        # elif menu_sidebar == "Merge Files":
        #     st.subheader("Merge Files")
        #     st.info("Coming soon...")
    

    
          
                            
                            
                            
                            
                            
                            
                            
                            
