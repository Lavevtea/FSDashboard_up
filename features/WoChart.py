import streamlit as st 
import plotly.express as px
import pandas as pd

@st.cache_data
def process_wochart(df):
    return df.copy()

def render_wochart(df):
    st.write("## WorkOrder Chart")
    
    if df is None or df.empty:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    key_prefix = "wochart_"
    ubahheader={
        "WorkOrderTypeName":"Work Order Type",
        "DivisionName": "Division",
        "Region": "Region",
        "SubRegion":"Sub Region",
        "City": "City"
    }
    
    filter1,filter2, filter3=st.columns(3)
    
    # if "locfilter" not in st.session_state:
    #     st.session_state.locfilter= "Region"
    if "divfilter" not in st.session_state:
        st.session_state.divfilter= ["Broadband", "LMS", "Fiberisasi"]
    if "tipefilter" not in st.session_state:
        st.session_state.tipefilter= ["Troubleshoot","Activation", "Dismantle", "Relocation Activation", "Relocation Dismantle", "Change Service"]
    
    
    with filter1:
        if "Region" in df.columns:
            semuaregion= sorted(df["Region"].dropna().astype(str).unique().tolist())
            selectedregion= st.multiselect("Select Region", options=semuaregion, default=semuaregion, key= "region_filter")
            if selectedregion:
                df=df[df["Region"].astype(str).isin(selectedregion)]
        if "SubRegion" in df.columns:
            semuasubregion= sorted(df[df["Region"].astype(str).isin(selectedregion)]["SubRegion"].dropna().astype(str).unique().tolist())
            selectedsubregion= st.multiselect("Select SubRegion", options=semuasubregion, default=semuasubregion, key= "subregion_filter")
            if selectedregion:
                df=df[df["SubRegion"].astype(str).isin(selectedsubregion)]
        if "City" in df.columns:
            semuacity= sorted(df[df["SubRegion"].astype(str).isin(selectedsubregion)]["City"].dropna().astype(str).unique().tolist())
            selectedcity= st.multiselect("Select City", options=semuacity, default=semuacity, key= "city_filter")
            if selectedregion:
                df=df[df["City"].astype(str).isin(selectedcity)]
        
                
    with filter2:
        st.markdown("WO Type")
        with st.expander("WO Type"):
            tipewo= ["Troubleshoot","Activation", "Dismantle", "Relocation Activation", "Relocation Dismantle", "Change Service"]
            jumlahtipe= df["WorkOrderTypeName"].value_counts().to_dict()
            
            tipeygdipilih=[]
            
            for r in tipewo:
                itungg= jumlahtipe.get(r,0)
                if st.checkbox(f"{r} ({itungg})", value= r in st.session_state.tipefilter, key=f"{r}" ):
                    tipeygdipilih.append(r) 
            st.session_state.tipefilter= tipeygdipilih              
            
    with filter3:
        st.markdown("Division")
        with st.expander("Division"):
            divwo= ["Broadband","LMS","Fiberisasi"]
            jumlahperdiv= df["DivisionName"].value_counts().to_dict()
            divisiterpilih=[]
            for c in divwo:
                itung= jumlahperdiv.get(c,0)
                if st.checkbox(f"{c} ({itung})", value= c in st.session_state.divfilter, key=f"{c}"):
                    divisiterpilih.append(c)
            st.session_state.divfilter= divisiterpilih

    if divisiterpilih:
        df= df[df["DivisionName"].isin(divisiterpilih)]
    else:
        st.warning("No division type chosen")
        
    if tipeygdipilih:
        df= df[df["WorkOrderTypeName"].isin(tipeygdipilih)]
    else:
        st.warning("No Workorder type chosen")

    st.divider()
    pie_wotype, pie_wodiv= st.columns(2)
    with pie_wotype:
        if "WorkOrderTypeName" in df.columns:
            hitung_type= df["WorkOrderTypeName"].value_counts().reset_index()
            hitung_type.columns= ["wotype", "count"]
            tipe= px.pie(hitung_type, names="wotype", values="count",title="WO Type Chart")
            st.plotly_chart(tipe, use_container_width=True)
        else:
            st.warning("Tidak ada WO type yang dipilih")
    with pie_wodiv:
        if "DivisionName" in df.columns:
            hitung_divisi= df["DivisionName"].value_counts().reset_index()
            hitung_divisi.columns =  ["division", "count"]
            divisi= px.pie(hitung_divisi, names="division", values="count", title="Division Chart")
            st.plotly_chart(divisi, use_container_width=True)
        else:
            st.warning("Tidak ada Division yang dipilih")
    st.divider()
    if not df.empty:
        for col in ["Region","SubRegion", "City"]:
            if col in df.columns:
                itungisi= df[col].astype(str).value_counts().reset_index()
                itungisi.columns= [col, "Count"]
                wo_barchart= px.bar(itungisi, x=col, y="Count", color= col, title=f"WorkOrder per {ubahheader.get(col,col)}", labels={col:ubahheader.get(col, col),"Count":"Jumlah"})
                st.plotly_chart(wo_barchart, use_container_width= True)
                st.dataframe(itungisi)
                st.divider()
    else: 
        st.warning("Data kosong")
    # if loccol in df.columns:
    #     normcol = df[loccol].astype(str)
    #     itungisi = normcol.value_counts().reset_index()
    #     itungisi.columns = [loccol, "Count"]

    #     bar = px.bar(
    #         itungisi,
    #         x= loccol,
    #         y= "Count",
    #         color= loccol,
    #         title= f"Based on {ubahheader.get(loccol, loccol)}",
    #         labels= {loccol: ubahheader.get(loccol,loccol), "Count": "Jumlah"}
    #     )
    #     st.plotly_chart(bar, use_container_width=True)
    # else:
    #     st.warning("gaada kolom yang bisa dipakai")
    tambahcols = ["CustomerName", "VendorName", "Reason"]
    colkotak = st.columns(len(tambahcols))
    
    
    for index, namadicol in enumerate(tambahcols):
        with colkotak[index]:
            if namadicol in df.columns:
                addcoldata = df[namadicol].astype(str).value_counts().reset_index()
                addcoldata.columns = [namadicol, "Amount"]
                total= pd.DataFrame({namadicol: ["Total"], "Amount": [addcoldata["Amount"].sum()]})
                addcoldata= pd.concat([addcoldata, total])
                addcoldata.index = range(1, len(addcoldata) + 1)
                st.markdown(f"**{namadicol}**")
                st.dataframe(addcoldata)
            else:
                st.warning(f"Kolom {namadicol} tidak ditemukan")   