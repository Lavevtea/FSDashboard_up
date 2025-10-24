import streamlit as st 
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from io import BytesIO
import numpy as np
import datetime as dt

def render_statuschart(dfstat,exceldata):
    st.write("## Work Order Status Chart")  

    
    # dfstat["WorkOrderStatusItem"] = dfstat["WorkOrderStatusItem"].astype(str).str.strip().str.title()
    ubahheader={
        "WorkOrderTypeName":"Work Order Type",
        "DivisionName": "Division",
        "Region": "Region",
        "SubRegion":"Sub Region",
        "City": "City"
    }
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

    statusmap={
        "Open": "OPEN",
        
        "Assign To Technician": "ONPROGRESS",
        "Accept": "ONPROGRESS",
        "Travel": "ONPROGRESS",
        "Arrive": "ONPROGRESS",
        "On Progress": "ONPROGRESS",
        "Return": "ONPROGRESS",
        "Assign To Dispatch External": "ONPROGRESS",
        "Complete With Note Reject": "ONPROGRESS",
        "Revise": "ONPROGRESS",
        "Return By Technician": "ONPROGRESS",
        "Postpone Is Revised": "POSTPONE",
        "Return Is Revised": "ONPROGRESS",
        "Provisioning In Progress": "ONPROGRESS",
        "Provisioning Success": "ONPROGRESS",
        
        "Complete With Note Approve": "COMPLETE",
        "Complete": "COMPLETE",
        "Done": "COMPLETE",
        "Work Order Confirmation Approve": "COMPLETE",
        "Posted To Ax Integration Success": "COMPLETE",
        
        "Postpone": "POSTPONE",
        
        "Sms Integration Failed": "INTEGRATION FAILED",
        "Posted To Ax Integration Failed": "INTEGRATION FAILED",
        "Provisioning Failed": "INTEGRATION FAILED",
        
        "Complete With Note Request": "APPROVAL DISPATCHER FS",
        "Postpone Request": "APPROVAL DISPATCHER FS",
        
        "Cancel Work Order": "CANCEL"}
    
   
    dfstat["WorkOrderStatusItem"]= dfstat["WorkOrderStatusItem"].astype(str).str.strip().str.title()
    dfstat["StatusReport"]= dfstat["WorkOrderStatusItem"].map(statusmap).fillna("N/A")
     
    locfilter2,wotype2,division2,statfilter=st.columns(4)
    
    if "location2" not in st.session_state:
        st.session_state.location2= "Region"
    if "wotype2" not in st.session_state:
        st.session_state.wotype2=["Troubleshoot","Activation", "Dismantle", "Relocation Activation", "Relocation Dismantle", "Change Service"]
    if "division2" not in st.session_state:
        st.session_state.division2=["Broadband","LMS", "Fiberisasi"]
    if "stat" not in st.session_state:
        st.session_state.stat= ["OPEN", "COMPLETE", "ONPROGRESS", "POSTPONE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS","CANCEL"]
    

    with locfilter2:
        if "Region" in dfstat.columns:
            semuaregion= sorted(dfstat["Region"].dropna().astype(str).unique().tolist())
            selectedregion= st.multiselect("Select Region", options=semuaregion, default=semuaregion, key= "region_filter")
            if selectedregion:
                dfstat=dfstat[dfstat["Region"].astype(str).isin(selectedregion)]
        if "SubRegion" in dfstat.columns:
            semuasubregion= sorted(dfstat[dfstat["Region"].astype(str).isin(selectedregion)]["SubRegion"].dropna().astype(str).unique().tolist())
            selectedsubregion= st.multiselect("Select SubRegion", options=semuasubregion, default=semuasubregion, key= "subregion_filter")
            if selectedregion:
                dfstat=dfstat[dfstat["SubRegion"].astype(str).isin(selectedsubregion)]
        if "City" in dfstat.columns:
            semuacity= sorted(dfstat[dfstat["SubRegion"].astype(str).isin(selectedsubregion)]["City"].dropna().astype(str).unique().tolist())
            selectedcity= st.multiselect("Select City", options=semuacity, default=semuacity, key= "city_filter")
            if selectedregion:
                dfstat=dfstat[dfstat["City"].astype(str).isin(selectedcity)]

    with wotype2:
        st.markdown("WO Type")
        with st.expander("WO Type"):
            tipewo= ["Troubleshoot","Activation", "Dismantle", "Relocation Activation", "Relocation Dismantle", "Change Service"]
            jumlahtipe= dfstat["WorkOrderTypeName"].value_counts().to_dict()
            
            tipeygdipilih=[]
            
            for r in tipewo:
                itungg= jumlahtipe.get(r,0)
                if st.checkbox(f"{r} ({itungg})", value= r in st.session_state.wotype2, key=f"wotype_{r}" ):
                    tipeygdipilih.append(r) 
            st.session_state.wotype2= tipeygdipilih              
    if st.session_state.wotype2:
        dfstat= dfstat[dfstat["WorkOrderTypeName"].isin(st.session_state.wotype2)]
    else:
        st.warning("No Workorder type chosen")   
        
                
    with division2:
        st.markdown("Division")
        with st.expander("Division"):
            divwo= ["Broadband","LMS","Fiberisasi"]
            jumlahperdiv= dfstat["DivisionName"].value_counts().to_dict()
            divisiterpilih=[]
            for c in divwo:
                itung= jumlahperdiv.get(c,0)
                if st.checkbox(f"{c} ({itung})", value= c in st.session_state.division2, key=f"{c}"):
                    divisiterpilih.append(c)
            st.session_state.division2= divisiterpilih

    if divisiterpilih:
        dfstat= dfstat[dfstat["DivisionName"].isin(divisiterpilih)]
    else:
        st.warning("No division type chosen")
        
        

    with statfilter:
        st.markdown("Status")
        with st.expander("Status"):
            statwo= ["OPEN", "COMPLETE", "ONPROGRESS", "POSTPONE", "INTEGRATION FAILED","APPROVAL DISPATCHER FS", "CANCEL"]
            jumlahperstat= dfstat["StatusReport"].value_counts().to_dict()
            
            statusterpilih=[]
        
            for s in statwo:
                itung= jumlahperstat.get(s,0)
                if st.checkbox(f"{s} ({itung})", value= (s in st.session_state.stat), key=f"stat_{s}"):
                    statusterpilih.append(s)
            st.session_state.stat= statusterpilih
        # statwo= ["OPEN", "COMPLETE", "ONPROGRESS", "POSTPONE", "INTEGRATION FAILED","APPROVAL DISPATCHER FS", "CANCEL"]
        # jumlahperstat= dfstat["StatusReport"].value_counts().to_dict()
        # allstat= [a for a in statwo if a in dfstat["StatusReport"].unique()]
        # opsi= [f"{a} ({jumlahperstat.get(a, 0)})" for a in allstat]
        # default= opsi
        # statusterpilih = st.checkbox("Select Status", options= opsi, default= default, key= "status_filter")

    if statusterpilih:
        dfstat= dfstat[dfstat["StatusReport"].isin(statusterpilih)]
    else:
        st.warning("No status picked")
    
    if not dfstat.empty:
        st.divider()
        pie_wotipe, pie_divisi, pie_statusreport =  st.columns(3)
        with pie_wotipe:
            if "WorkOrderTypeName" in dfstat.columns:
                tipe_count= dfstat["WorkOrderTypeName"].value_counts().reset_index()
                tipe_count.columns= ["wotipe", "count"]
                pie_tipe= px.pie(tipe_count, names= "wotipe", values= "count", title= "WO Type Chart")
                st.plotly_chart(pie_tipe, use_container_width= True)
            else:
                st.warning("Tidak ada WO Type yang dipilih")
        with pie_divisi:
            if "DivisionName" in dfstat.columns:
                tipe_div= dfstat["DivisionName"].value_counts().reset_index()
                tipe_div.columns= ["divisi", "count"]
                pie_div= px.pie(tipe_div, names= "divisi", values= "count", title= "Division Chart")
                st.plotly_chart(pie_div, use_container_width= True)
            else:
                st.warning("Tidak ada Division yang dipilih")
        with pie_statusreport:
            if "StatusReport" in dfstat.columns:
                stat_count= dfstat["StatusReport"].value_counts().reset_index()
                stat_count.columns= ["stat", "count"]
                pie_stat= px.pie(stat_count, names= "stat", values= "count", title= "StatusReport Chart")
                st.plotly_chart(pie_stat, use_container_width= True)
            else:
                st.warning("Tidak ada Status yang dipilih")


    for s in dfstat.columns:
        if dfstat[s].dtype== object:
            dfstat[s]= dfstat[s].astype(str).str.strip()
    if "Region" not in dfstat.columns:
        dfstat["Region"]= dfstat["SubRegion"].map(regionmap).fillna(dfstat["SubRegion"])

    if tipeygdipilih:
        if (isinstance(exceldata, dict)and "HistoryWorkOrder" in exceldata):
            stathistory= exceldata["HistoryWorkOrder"].copy()
            stathistory.columns=stathistory.columns.astype(str).str.strip()
            his_wo= "WorkOrderNumber" if "WorkOrderNumber" in stathistory.columns else None
            his_stat= "WorkOrderStatusItem" if "WorkOrderStatusItem" in stathistory.columns else None
            his_time= "Modified" if "Modified" in stathistory.columns else None
            if all([his_wo, his_stat, his_time]):
                scannedwo=(dfstat[["WorkOrderNumber","WorkOrderStatusItem"]].dropna().copy())
                scannedwo["WorkOrderNumber"]= scannedwo["WorkOrderNumber"].astype(str).str.strip()
                scannedwo["wonum_key"]= scannedwo["WorkOrderNumber"].str.title()
                scannedwo["statusnormalized"]= scannedwo["WorkOrderStatusItem"].astype(str).fillna("").str.strip().str.title()
                simpen_wonum_key= set(scannedwo["wonum_key"].unique())
                stathistory["wonum_key"]=(stathistory[his_wo].astype(str).fillna("").str.strip().str.title())
                his_subset= stathistory[stathistory["wonum_key"].isin(simpen_wonum_key)].copy()
                his_subset["WorkOrderNumber"]= his_subset[his_wo].astype(str).str.strip()
                his_subset["StatusWO"]= his_subset[his_stat].astype(str).str.strip()
                his_subset["StatusTimestamp"]= pd.to_datetime(his_subset[his_time],errors="coerce")
                his_subset= his_subset.dropna(subset=["WorkOrderNumber","StatusWO","StatusTimestamp"])
                if his_subset.empty:
                    st.write("history stlh normalisasi kosong") 
                else:
                    openonly= (his_subset[his_subset["StatusWO"].str.title() == "Open"].groupby("WorkOrderNumber", as_index= False).agg({"StatusTimestamp":"min"}).rename(columns={"StatusTimestamp":"open_c"}))
                    others= (his_subset[his_subset["StatusWO"].str.title() != "Open"].groupby(["WorkOrderNumber","StatusWO"], as_index= False).agg({"StatusTimestamp":"max"}).rename(columns={"StatusTimestamp":"status_c"}))
                    gabung= others.merge(openonly, on="WorkOrderNumber", how="left")
                    showopen=openonly.copy()
                    showopen["StatusWO"]= "Open"
                    showopen["status_c"]= pd.NaT
                    showopen["terpilih_c"]= showopen["open_c"]
                    gabung["terpilih_c"]= gabung["status_c"]
                    kol=["WorkOrderNumber","StatusWO","status_c","open_c","terpilih_c"]
                    gabungsemua=pd.concat([showopen.loc[:, kol],gabung.loc[:, kol]], ignore_index=True, sort=False)
                    def statusreportmap(a):
                        if a in statusmap:
                            return statusmap[a]
                        return statusmap.get(str(a).title(), "OTHER")
                    gabungsemua["StatusReport"]=  gabungsemua["StatusWO"].apply(statusreportmap)
                    gabungsemua= gabungsemua[gabungsemua["StatusReport"].isin(["OPEN","ONPROGRESS","POSTPONE","COMPLETE", "INTEGRATION FAILED","APPROVAL DISPATCHER FS", "CANCEL"])].copy()
                    gabungsemua["wonum_key"]= gabungsemua["WorkOrderNumber"].astype(str).str.strip().str.title()                     
                    gabungsemua["statusnormalized"]= gabungsemua["StatusWO"].astype(str).fillna("").str.strip().str.title()
                    tergabung= gabungsemua.merge(scannedwo[["wonum_key", "statusnormalized"]], on="wonum_key", how="inner", suffixes=("", "wo"))
                    tergabung=tergabung[tergabung["statusnormalized"]==tergabung["statusnormalizedwo"]].copy()

                    if tergabung.empty:
                        st.write("gaada yg match antara history stat dan stat excel")       
                    else:
                        tergabung["WorkOrderNumber"]= tergabung["WorkOrderNumber"].astype(str).str.strip().str.upper()
                        dfstat["WorkOrderNumber"]= dfstat["WorkOrderNumber"].astype(str).str.strip().str.upper()
                        tergabung= tergabung.merge(dfstat[["WorkOrderNumber","uptime"]], on="WorkOrderNumber", how="left")
                        tergabung["duration"]=((tergabung["uptime"]-tergabung["terpilih_c"]).dt.total_seconds()/3600)
                        completeonly= tergabung["StatusReport"]=="COMPLETE"
                        tergabung.loc[completeonly, "duration"]= ((tergabung.loc[completeonly, "status_c"]-tergabung.loc[completeonly, "open_c"]).dt.total_seconds()/3600)
                        # st.write("Distribusi Duration (jam):", tergabung["duration"].describe())
                        # st.write(tergabung[["WorkOrderNumber","StatusReport","duration"]].head(20))

                        def slaoptions_general(hour):
                            if hour<=4:
                                return "0-4 Jam"
                            elif hour<=6:
                                return "4-6 Jam"
                            elif hour<=12:
                                return "6-12 Jam"
                            elif pd.isna(hour):
                                return None
                            else:
                                return ">12 Jam"
                        def slaoptions_broadband(hour):
                            if hour<=6:
                                return "0-6 Jam"
                            elif hour<=12:
                                return "6-12 Jam"
                            elif hour<=24:
                                return "12-24 Jam"
                            else:
                                return ">24 Jam"
                        broadband_only= (len(st.session_state.division2)==1 and "Broadband" in st.session_state.division2)
                        if broadband_only:
                            tergabung["slaoptions"]= tergabung["duration"].apply(slaoptions_broadband)
                            urutansla= ["0-6 Jam", "6-12 Jam", "12-24 Jam", ">24 Jam"]
                        else:
                            tergabung["slaoptions"]= tergabung["duration"].apply(slaoptions_general)
                            urutansla= ["0-4 Jam", "4-6 Jam", "6-12 Jam", ">12 Jam"]
                        priority_cols = [
                            ("Region", selectedregion),
                            ("SubRegion", selectedsubregion),
                            ("City", selectedcity)
                        ]

                        kol_area = None
                        for col, selected in priority_cols:
                            if col in dfstat.columns and len(selected) > 0:
                                kol_area = col
                                break  
                        if kol_area is None:
                            kol_area = "City"

                        tergabung= tergabung.merge(dfstat[["WorkOrderNumber", "uptime", "City", "SubRegion", "Region"]], on="WorkOrderNumber", how="left")
                        # st.write(tergabung)
                        tergabung_valid= tergabung.dropna(subset=["slaoptions"]).copy()
                        # st.write(tergabung_valid)

                        
                        slagroup=( tergabung_valid.groupby([kol_area, "StatusReport", "slaoptions"]).agg({"WorkOrderNumber": "nunique"}).reset_index())
                                                                                                        
                        if "WorkOrderNumber" in slagroup.columns:
                            slagroup=slagroup.rename(columns={"WorkOrderNumber":"Count"})
                        slagroup["Count"]= slagroup["Count"].astype(int)
                        urutanstatus=["OPEN","ONPROGRESS","POSTPONE","COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"]
                        def buat_sla_table(tergabung_valid, kol_area, urutansla, urutanstatus):
                            slagroup = (
                                tergabung_valid.groupby([kol_area, "StatusReport", "slaoptions"])
                                .agg({"WorkOrderNumber": "nunique"})
                                .reset_index()
                            )

                            if "WorkOrderNumber" in slagroup.columns:
                                slagroup = slagroup.rename(columns={"WorkOrderNumber":"Count"})
                            slagroup["Count"]= slagroup["Count"].astype(int)

                            pivot = slagroup.pivot_table(
                                index=[kol_area,"slaoptions"],
                                columns="StatusReport",
                                values="Count",
                                aggfunc="sum",
                                fill_value=0
                            )
                            pivot.index.set_names([kol_area, "SLA"], inplace=True)
                            area_list= tergabung_valid[kol_area].dropna().unique().tolist()
                            full_index= pd.MultiIndex.from_product([area_list, urutansla], names= [kol_area, "SLA"])
                            pivot= pivot.reindex(full_index, fill_value=0)
                            # st.write(area_list)
                            for u in urutanstatus:
                                if u not in pivot.columns:
                                    pivot[u]=0

                            pivot = pivot.reindex(columns=urutanstatus, fill_value=0)
                            pivot["TOTAL2"]= pivot[["OPEN","ONPROGRESS","POSTPONE"]].sum(axis=1)
                            pivot["TOTAL"]= pivot[["OPEN","ONPROGRESS","POSTPONE","COMPLETE","INTEGRATION FAILED","APPROVAL DISPATCHER FS","CANCEL"]].sum(axis=1)

                            pivot.index.set_names([kol_area, "SLA"], inplace=True)

                            areasum= pivot.groupby(level=0).sum()
                            areasum.index= pd.MultiIndex.from_tuples(
                                [(area,"Total") for area in areasum.index],
                                names=pivot.index.names
                            )

                            frameout=[]
                            for area in pivot.index.get_level_values(0).unique():
                                baris_area= pivot.loc[area]
                                baris_area= baris_area.reindex(urutansla, fill_value=0)
                                baris_area.index.name="SLA"
                                baris_area.index= pd.MultiIndex.from_product([[area], baris_area.index], names=pivot.index.names)
                                frameout.append(baris_area)
                                frameout.append(areasum.loc[[area]])

                            final= pd.concat(frameout)
                            totalperstatus= final.loc[(slice(None),["Total"]),:]
                            grandtotal= totalperstatus.sum(numeric_only=True).to_frame().T
                            grandtotal[kol_area]= "Grand Total"
                            grandtotal["SLA"]= ""
                            grandtotal= grandtotal[final.reset_index().columns]
                            final= final.reset_index()
                            final[kol_area]= final[kol_area].where(final["SLA"].isin([urutansla[0],"Grand Total"]), "")
                            final= pd.concat([final, grandtotal], ignore_index=True)
                            

                            statkolorder=[kol_area,"SLA","OPEN","ONPROGRESS","POSTPONE","TOTAL2","COMPLETE","INTEGRATION FAILED","APPROVAL DISPATCHER FS","CANCEL","TOTAL"]
                            finaltabel= final[statkolorder]

                            kolomheader=pd.MultiIndex.from_tuples([
                                ("", kol_area),("", "SLA"),
                                ("ONGOING-NOW","OPEN"),("ONGOING-NOW","ONPROGRESS"),("ONGOING-NOW","POSTPONE"),("ONGOING-NOW","TOTAL"),
                                ("OPEN-COMPLETE","COMPLETE"),("", "INTEGRATION FAILED"),
                                ("COMP NOTE REQ & POSTPONE REQ","APPROVAL DISPATCHER FS"),("", "CANCEL"),("", "TOTAL")
                            ], names=[None,None])
                            finaltabel.columns= kolomheader

                            return finaltabel
                        
                        finaltabel_region = buat_sla_table(tergabung_valid, "Region", urutansla, urutanstatus)
                        finaltabel_subregion = buat_sla_table(tergabung_valid, "SubRegion", urutansla, urutanstatus)
                        finaltabel_city = buat_sla_table(tergabung_valid, "City", urutansla, urutanstatus)
                        def styletotal(dfrender):
                            def warnain_baris(total):
                                text=" ".join(map(str, total.values))   
                                return ["background-color:rgb(240, 242, 246 " if "Total" in text else ""]*len(total)
                            
                            def warnain_kolom(total):
                                return ["background-color: rgb(240, 242, 246)" if total.name[1] in ["TOTAL2","TOTAL"] else ""]*len(total)
                            
                            def warnain_approval(col):
                                if col.name[1] == "APPROVAL DISPATCHER FS":
                                    return ["background-color: rgb(252, 236, 3)" if p>0 else "" for p in col.values]
                                else:
                                    return["" for g in col]
                            
                            def warnain_ongoing(row):
                                styles = [""] * len(row)  
                                sla = row[("", "SLA")]
                                divisi= st.session_state.get("division2", [])

                                for i, colname in enumerate(row.index):
                                    if colname[0] == "ONGOING-NOW" and colname[1] in ["OPEN", "ONPROGRESS", "POSTPONE"]:
                                        val = row[colname]
                                        if val>0:
                                            if any(d in ["LMS", "Fiberisasi"] for d in divisi):
                                                if sla == "4-6 Jam":
                                                    if colname[1] == "OPEN":
                                                        styles[i] = "background-color: rgb(252, 236, 3)"
                                                    elif colname[1] == "ONPROGRESS":
                                                        styles[i] = "background-color: rgb(252, 236, 3)"
                                                    elif colname[1] == "POSTPONE":
                                                        styles[i] = "background-color: rgb(252, 236, 3)"

                                                elif sla == "6-12 Jam":
                                                    if colname[1] == "OPEN":
                                                        styles[i] = "background-color: orange"
                                                    elif colname[1] == "ONPROGRESS":
                                                        styles[i] = "background-color: orange"
                                                    elif colname[1] == "POSTPONE":
                                                        styles[i] = "background-color: orange"
                                                        
                                                elif sla == ">12 Jam":
                                                    if colname[1] == "OPEN":
                                                        styles[i] = "background-color: red"
                                                    elif colname[1] == "ONPROGRESS":
                                                        styles[i] = "background-color: red"
                                                    elif colname[1] == "POSTPONE":
                                                        styles[i] = "background-color: red"
                                            elif "Broadband" in divisi:
                                                if sla == "12-24 Jam":
                                                    if colname[1] == "OPEN":
                                                        styles[i] = "background-color: rgb(252, 236, 3)"
                                                    elif colname[1] == "ONPROGRESS":
                                                        styles[i] = "background-color: rgb(252, 236, 3)"
                                                    elif colname[1] == "POSTPONE":
                                                        styles[i] = "background-color: rgb(252, 236, 3)"

                                                elif sla == ">24 Jam":
                                                    if colname[1] == "OPEN":
                                                        styles[i] = "background-color: red"
                                                    elif colname[1] == "ONPROGRESS":
                                                        styles[i] = "background-color: red"
                                                    elif colname[1] == "POSTPONE":
                                                        styles[i] = "background-color: red"

                                return styles

                                    
                            return(dfrender.style.apply(warnain_approval, axis=0).apply(warnain_ongoing, axis=1).apply(warnain_kolom, axis=0).apply(warnain_baris, axis=1))
                            
                        def rendersla(name, dfrender, kol_area=None, selected=None, height=420):
                            if kol_area and selected:
                                dfrender = dfrender[dfrender.iloc[:,0].isin(selected)]  
                            st.subheader(name)
                            st.dataframe(styletotal(dfrender), hide_index=True, height=height)
                    
                        regionbar= (tergabung_valid.groupby(["Region", "StatusReport"]).size().reset_index(name="Count"))
                        chart_region= px.bar(regionbar, x="Region", y="Count", color="StatusReport", barmode="stack", title="Status Chart per Region", labels={"Region":"Region","Count":"Jumlah"})
                        
                        
                        subregionbar= (tergabung_valid.groupby(["SubRegion", "StatusReport"]).size().reset_index(name="Count"))
                        chart_subregion= px.bar(subregionbar, x="SubRegion", y="Count", color="StatusReport", barmode="stack", title="Status Chart per Sub Region", labels={"SubRegion":"Sub Region","Count":"Jumlah"})
                        
                        
                        citybar= (tergabung_valid.groupby(["City", "StatusReport"]).size().reset_index(name="Count"))
                        chart_city= px.bar(citybar, x="City", y="Count", color="StatusReport", barmode="stack", title="Status Chart per City", labels={"City":"City","Count":"Jumlah"})
                        
                        st.plotly_chart(chart_region, use_container_width= True)
                        rendersla("SLA Summary per Region", finaltabel_region, kol_area="Region",height=500)
                        
                        st.plotly_chart(chart_subregion, use_container_width= True)
                        rendersla("SLA Summary per SubRegion", finaltabel_subregion, kol_area="SubRegion", height=500)
                        
                        st.plotly_chart(chart_city, use_container_width= True)
                        rendersla("SLA Summary per City", finaltabel_city, kol_area="City", height=500)
                        
                        st.session_state.tergabung_valid = tergabung_valid

                    
        else: 
            st.warning("Data kosong")
    

        # st.dataframe(statussummary)
    else:
        st.warning("No data available")












