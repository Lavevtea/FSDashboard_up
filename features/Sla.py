import streamlit as st 
import pandas as pd

def render_slasum(df,exceldata):
    st.write("## Status Report SLA WorkOrder Summary")
    
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


    statusmap1={
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

    
    sladf= df.copy()
    sladf["WorkOrderStatusItem"] = sladf["WorkOrderStatusItem"].astype(str).str.strip().str.title()
    sladf["StatusReport"]= sladf["WorkOrderStatusItem"].map(statusmap1).fillna("N/A")
    
    

    
    kolsla1, kolsla2, kolsla3,kolsla4 = st.columns(4)
    if "kolsla1" not in st.session_state:
        st.session_state.kolsla1= "Region"
    if "kolsla2" not in st.session_state:
        st.session_state.kolsla2=["Troubleshoot","Activation", "Dismantle", "Relocation Activation", "Relocation Dismantle", "Change Service"]
    if "kolsla3" not in st.session_state:
        st.session_state.kolsla3=["Broadband","LMS", "Fiberisasi"]
    if "kolsla4" not in st.session_state:
        st.session_state.kolsla4= ["OPEN", "COMPLETE", "ONPROGRESS", "POSTPONE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS","CANCEL"]
        
    with kolsla1:
        if "Region" in sladf.columns:
            semuaregion= sorted(sladf["Region"].dropna().astype(str).unique().tolist())
            selectedregion= st.multiselect("Select Region", options=semuaregion, default=semuaregion, key= "region_fil")
            if selectedregion:
                sladf=sladf[sladf["Region"].astype(str).isin(selectedregion)]
        if "SubRegion" in sladf.columns:
            semuasubregion= sorted(sladf[sladf["Region"].astype(str).isin(selectedregion)]["SubRegion"].dropna().astype(str).unique().tolist())
            selectedsubregion= st.multiselect("Select SubRegion", options=semuasubregion, default=semuasubregion, key= "subregion_fil")
            if selectedregion:
                sladf=sladf[sladf["SubRegion"].astype(str).isin(selectedsubregion)]
        if "City" in sladf.columns:
            semuacity= sorted(sladf[sladf["SubRegion"].astype(str).isin(selectedsubregion)]["City"].dropna().astype(str).unique().tolist())
            selectedcity= st.multiselect("Select City", options=semuacity, default=semuacity, key= "city_fil")
            if selectedregion:
                sladf=sladf[sladf["City"].astype(str).isin(selectedcity)]
                
    with kolsla2:
        st.markdown("WO Type")
        with st.expander("WO Type"):
            wotype= ["Troubleshoot","Activation", "Dismantle", "Relocation Activation", "Relocation Dismantle", "Change Service"]
            jumlahtype= sladf["WorkOrderTypeName"].value_counts().to_dict()
            type_terpilih=[]
            for w in wotype:
                count= jumlahtype.get(w,0)
                if st.checkbox(f"{w}({count})", value=w in st.session_state.kolsla2, key=f"wotypesla_{w}"):
                    type_terpilih.append(w)
            st.session_state.kolsla2=type_terpilih
    if st.session_state.kolsla2:
        sladf= sladf[sladf["WorkOrderTypeName"].isin(st.session_state.kolsla2)]
    else:
        st.warning("No Workorder type chosen")
            
    with kolsla3:
        st.markdown("Division")
        with st.expander("Division"):
            divwo= ["Broadband","LMS","Fiberisasi"]
            jumlahperdiv= sladf["DivisionName"].value_counts().to_dict()
            div_terpilih=[]
            for c in divwo:
                itung= jumlahperdiv.get(c,0)
                if st.checkbox(f"{c} ({itung})", value= c in st.session_state.kolsla3, key=f"{c}_sla"):
                    div_terpilih.append(c)
            st.session_state.kolsla3= div_terpilih
    if div_terpilih:
        sladf= sladf[sladf["DivisionName"].isin(div_terpilih)]
    else:
        st.warning("No Division type chosen")
        
            
    with kolsla4:
        st.markdown("Status")
        with st.expander("Status"):
            statwo= ["OPEN", "COMPLETE", "ONPROGRESS", "POSTPONE", "INTEGRATION FAILED","APPROVAL DISPATCHER FS", "CANCEL"]
            jumlahperstat= sladf["StatusReport"].value_counts().to_dict()
            
            status_terpilih=[]
        
            for s in statwo:
                itung= jumlahperstat.get(s,0)
                if st.checkbox(f"{s} ({itung})", value= (s in st.session_state.kolsla4), key=f"status_{s}"):
                    status_terpilih.append(s)
            st.session_state.kolsla4= status_terpilih
        
    if status_terpilih:
        sladf= sladf[sladf["StatusReport"].isin(status_terpilih)]
    else:
        st.warning("No status picked")

            

    for a in sladf.columns:
        if sladf[a].dtype== object:
            sladf[a]= sladf[a].astype(str).str.strip()
    if "Region" not in sladf.columns:
        sladf["Region"]= sladf["SubRegion"].map(regionmap).fillna(sladf["SubRegion"])
    


    for s in sladf.columns:
        if sladf[s].dtype== object:
            sladf[s]= sladf[s].astype(str).str.strip()
    if "Region" not in sladf.columns:
        sladf["Region"]= sladf["SubRegion"].map(regionmap).fillna(sladf["SubRegion"])
        
                
                
    if type_terpilih:          
        if (isinstance(exceldata, dict)and "HistoryWorkOrder" in exceldata):
            stathistory= exceldata["HistoryWorkOrder"].copy()
            stathistory.columns=stathistory.columns.astype(str).str.strip()
            his_wo= "WorkOrderNumber" if "WorkOrderNumber" in stathistory.columns else None
            his_stat= "WorkOrderStatusItem" if "WorkOrderStatusItem" in stathistory.columns else None
            his_time= "Modified" if "Modified" in stathistory.columns else None
            if all([his_wo, his_stat, his_time]):
                scannedwo=(sladf[["WorkOrderNumber","WorkOrderStatusItem"]].dropna().copy())
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
                        if a in statusmap1:
                            return statusmap1[a]
                        return statusmap1.get(str(a).title(), "OTHER")
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
                        sladf["WorkOrderNumber"]= sladf["WorkOrderNumber"].astype(str).str.strip().str.upper()
                        tergabung= tergabung.merge(sladf[["WorkOrderNumber","uptime"]], on="WorkOrderNumber", how="left")
                        tergabung["duration"]=((tergabung["uptime"]-tergabung["terpilih_c"]).dt.total_seconds()/3600)
                        completeonly= tergabung["StatusReport"]=="COMPLETE"
                        tergabung.loc[completeonly, "duration"]= ((tergabung.loc[completeonly, "status_c"]-tergabung.loc[completeonly, "open_c"]).dt.total_seconds()/3600)
                        def slaoptions_general(hour):
                            if hour<=4:
                                return "0-4 Jam"
                            elif hour<=6:
                                return "4-6 Jam"
                            elif hour<=12:
                                return "6-12 Jam"
                            elif hour<=24:
                                return "12-24 Jam"
                            elif pd.isna(hour):
                                return None
                            else:
                                return ">24 Jam"
                        def slaoptions_broadband(hour):
                            if hour<=6:
                                return "0-6 Jam"
                            elif hour<=12:
                                return "6-12 Jam"
                            elif hour<=24:
                                return "12-24 Jam"
                            else:
                                return ">24 Jam"
                        broadband_only= (len(st.session_state.kolsla3)==1 and "Broadband" in st.session_state.kolsla3)
                        if broadband_only:
                            tergabung["slaoptions"]= tergabung["duration"].apply(slaoptions_broadband)
                            urutansla= ["0-6 Jam", "6-12 Jam", "12-24 Jam", ">24 Jam"]
                        else:
                            tergabung["slaoptions"]= tergabung["duration"].apply(slaoptions_general)
                            urutansla= ["0-4 Jam", "4-6 Jam", "6-12 Jam","12-24 Jam", ">24 Jam"]
                        priority_cols = [
                            ("Region", selectedregion),
                            ("SubRegion", selectedsubregion),
                            ("City", selectedcity)
                        ]

                        kol_area = None
                        for col, selected in priority_cols:
                            if col in sladf.columns and len(selected) > 0:
                                kol_area = col
                                break  
                        if kol_area is None:
                            kol_area = "City"

                        tergabung= tergabung.merge(sladf[["WorkOrderNumber", "uptime", "City", "SubRegion", "Region"]], on="WorkOrderNumber", how="left")
                        # st.write(tergabung)
                        tergabung_valid= tergabung.dropna(subset=["slaoptions"]).copy()
                        # st.write(tergabung_valid)

                        
                        slagroup=( tergabung_valid.groupby([kol_area, "StatusReport", "slaoptions"]).agg({"WorkOrderNumber": "nunique"}).reset_index())
                                                                                                        
                        
                        urutanstatus=["OPEN","ONPROGRESS","POSTPONE","COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"]
                        def buat_sla_table(tergabung_valid, kol_area, urutansla, urutanstatus):
                            slagroup = (
                                tergabung_valid.groupby([kol_area, "StatusReport", "slaoptions"])
                                .agg({"WorkOrderNumber": "nunique"})
                                .reset_index()
                            )
                            if "WorkOrderNumber" in slagroup.columns:
                                slagroup=slagroup.rename(columns={"WorkOrderNumber":"Count"})
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
                                divisi= st.session_state.get("kolsla3", [])

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
                                                        
                                                elif sla == "12-24 Jam":
                                                    if colname[1] == "OPEN":
                                                        styles[i] = "background-color: red"
                                                    elif colname[1] == "ONPROGRESS":
                                                        styles[i] = "background-color: red"
                                                    elif colname[1] == "POSTPONE":
                                                        styles[i] = "background-color: red"
                                                        
                                                elif sla == ">24 Jam":
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
                            
                       
                        region, subregion, city,  vendor= st.tabs(["Region","Sub Region", "City",  "Vendor"])
                        with region:
                            rendersla("SLA Summary per Region", finaltabel_region, kol_area="Region",height=500)
                            for region in sorted(tergabung_valid["Region"].dropna().unique()):
                                with st.expander(f"{region}"):
                                    region_df= tergabung_valid[tergabung_valid["Region"]== region]
                                    status_sum=(
                                        region_df.groupby("StatusReport")["WorkOrderNumber"].nunique().reindex(["OPEN", "ONPROGRESS", "POSTPONE", "COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"], fill_value=0).reset_index()
                                    )
                                    for _, row in status_sum.iterrows():
                                        status = row["StatusReport"]
                                        count = row["WorkOrderNumber"]

                                        if count > 0:
                                            with st.expander(f"{status} ({count} WO)"):
                                                filtered = region_df[region_df["StatusReport"] == status]
                                                if "slaoptions" in filtered.columns:
                                                    sla_sum = (
                                                        filtered.groupby("slaoptions")["WorkOrderNumber"]
                                                        .nunique()
                                                        .reset_index()
                                                    )
                                                    for _, srow in sla_sum.iterrows():
                                                        sla_label = srow["slaoptions"]
                                                        sla_count = srow["WorkOrderNumber"]
                                                        with st.expander(f"{sla_label} ({sla_count} WO)"):
                                                            filtered_sla = filtered[filtered["slaoptions"] == sla_label]
                                                            addinfo_fromdf = (df[["WorkOrderNumber","ReferenceCode","VendorName","CustomerName","Created"]].drop_duplicates())
                                                            wo_info = pd.merge(filtered_sla,addinfo_fromdf,on="WorkOrderNumber",how="left")
                                                            wo_info= wo_info.rename(columns={"status_c":"Modified"})
                                                            wo_info = wo_info[["WorkOrderNumber", "ReferenceCode","City","VendorName","CustomerName", "Created", "Modified"]]
                                                            st.dataframe(wo_info, hide_index=True, width="stretch")
                                
                        with subregion:
                            rendersla("SLA Summary per SubRegion", finaltabel_subregion, kol_area="SubRegion", height=500)
                            for subregion in sorted(tergabung_valid["SubRegion"].dropna().unique()):
                                with st.expander(f"{subregion}"):
                                    subregion_df= tergabung_valid[tergabung_valid["SubRegion"]== subregion]
                                    status_sum=(
                                        subregion_df.groupby("StatusReport")["WorkOrderNumber"].nunique().reindex(["OPEN", "ONPROGRESS", "POSTPONE", "COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"], fill_value=0).reset_index()
                                    )
                                    for _, row in status_sum.iterrows():
                                        status = row["StatusReport"]
                                        count = row["WorkOrderNumber"]

                                        if count > 0:
                                            with st.expander(f"{status} ({count} WO)"):
                                                filtered = subregion_df[subregion_df["StatusReport"] == status]
                                                if "slaoptions" in filtered.columns:
                                                    sla_sum = (
                                                        filtered.groupby("slaoptions")["WorkOrderNumber"]
                                                        .nunique()
                                                        .reset_index()
                                                    )
                                                    for _, srow in sla_sum.iterrows():
                                                        sla_label = srow["slaoptions"]
                                                        sla_count = srow["WorkOrderNumber"]
                                                        with st.expander(f"{sla_label} ({sla_count} WO)"):
                                                            filtered_sla = filtered[filtered["slaoptions"] == sla_label]
                                                            addinfo_fromdf = (df[["WorkOrderNumber","ReferenceCode","VendorName","CustomerName","Created"]].drop_duplicates())
                                                            wo_info = pd.merge(filtered_sla,addinfo_fromdf,on="WorkOrderNumber",how="left")
                                                            wo_info= wo_info.rename(columns={"status_c":"Modified"})
                                                            wo_info = wo_info[["WorkOrderNumber", "ReferenceCode","City","VendorName", "CustomerName","Created", "Modified"]]
                                                            st.dataframe(wo_info, hide_index=True, width="stretch")
                        with city:
                            rendersla("SLA Summary per City", finaltabel_city, kol_area="City", height=500) 
                            for city in sorted(tergabung_valid["City"].dropna().unique()):
                                with st.expander(f"{city}"):
                                    city_df= tergabung_valid[tergabung_valid["City"]== city]
                                    status_sum=(
                                        city_df.groupby("StatusReport")["WorkOrderNumber"].nunique().reindex(["OPEN", "ONPROGRESS", "POSTPONE", "COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"], fill_value=0).reset_index()
                                    )
                                    for _, row in status_sum.iterrows():
                                        status = row["StatusReport"]
                                        count = row["WorkOrderNumber"]

                                        if count > 0:
                                            with st.expander(f"{status} ({count} WO)"):
                                                filtered = city_df[city_df["StatusReport"] == status]
                                                if "slaoptions" in filtered.columns:
                                                    sla_sum = (
                                                        filtered.groupby("slaoptions")["WorkOrderNumber"]
                                                        .nunique()
                                                        .reset_index()
                                                    )
                                                    for _, srow in sla_sum.iterrows():
                                                        sla_label = srow["slaoptions"]
                                                        sla_count = srow["WorkOrderNumber"]
                                                        with st.expander(f"{sla_label} ({sla_count} WO)"):
                                                            filtered_sla = filtered[filtered["slaoptions"] == sla_label]
                                                            addinfo_fromdf = (df[["WorkOrderNumber","ReferenceCode","VendorName","CustomerName","Created"]].drop_duplicates())
                                                            wo_info = pd.merge(filtered_sla,addinfo_fromdf,on="WorkOrderNumber",how="left")
                                                            wo_info= wo_info.rename(columns={"status_c":"Modified"})
                                                            wo_info = wo_info[["WorkOrderNumber", "ReferenceCode","City","VendorName","CustomerName","Created", "Modified"]]
                                                            st.dataframe(wo_info, hide_index=True, width="stretch")
                    
                                        
                        with vendor:
                            st.write("## Vendor")
                            vendorpivot=(tergabung.merge(sladf[["WorkOrderNumber","VendorName"]].drop_duplicates(), on="WorkOrderNumber", how="left").groupby(["VendorName","slaoptions", "StatusReport"]).agg({"WorkOrderNumber": "nunique"}).reset_index())
                            vendorpivot["VendorName"] = vendorpivot["VendorName"].fillna("No Vendor")
                            vendorpivot= vendorpivot.pivot_table(index=["VendorName","slaoptions"], columns="StatusReport", values="WorkOrderNumber", aggfunc="sum", fill_value=0).reset_index()
                            urutanstatus=["OPEN","ONPROGRESS","POSTPONE","COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"]
                            for ur in urutanstatus:
                                if ur not in vendorpivot.columns:
                                    vendorpivot[ur]=0
                            vendorpivot["TOTAL2"]=vendorpivot[["OPEN", "ONPROGRESS", "POSTPONE"]].sum(axis=1)
                            vendorpivot["Total"]=vendorpivot[["OPEN", "ONPROGRESS", "POSTPONE","COMPLETE", "INTEGRATION FAILED","APPROVAL DISPATCHER FS", "CANCEL"]].sum(axis=1)
                            
                            frame=[]
                            for v in vendorpivot["VendorName"].unique():
                                
                                baris_vendor=vendorpivot[vendorpivot["VendorName"] == v].copy()
                                baris_vendor= baris_vendor.set_index("slaoptions").reindex(urutansla, fill_value= 0).reset_index()
                                baris_vendor["VendorName"]= v
                                frame.append(baris_vendor)
                                total= baris_vendor[urutanstatus+["TOTAL2","Total"]].sum().to_dict()
                                total["slaoptions"]= "Total"
                                total["VendorName"]= v
                                frame.append(pd.DataFrame([total]))
                            
                            finaldf= pd.concat(frame, ignore_index=True)
                            
                            finaldf["slaoptions"]= pd.Categorical(finaldf["slaoptions"],categories=urutanstatus+["Total"], ordered=True)
                            finaldf=finaldf.sort_values(["VendorName", "slaoptions"])
                            finaldf= pd.concat(frame, ignore_index=True)
                            finaldf["VendorName"] = finaldf["VendorName"].fillna("No Vendor")
                            listvendor= sorted(finaldf["VendorName"].unique().tolist())
                            filtervendor= st.multiselect("Select Vendor", options= listvendor, default= listvendor, key="vendor_filter")
                            if filtervendor:
                                finaldf= finaldf[finaldf["VendorName"].isin(filtervendor)]
                                
                            grand_total=finaldf.loc[finaldf["slaoptions"]=="Total", urutanstatus+["TOTAL2","Total"]].sum().to_dict()
                            grand_total["VendorName"]="Grand Total"
                            grand_total["slaoptions"]= ""
                            finaldf= pd.concat([finaldf, pd.DataFrame([grand_total])], ignore_index= True)
                            
                            
                            finaldf["VendorName"]= finaldf["VendorName"].mask(finaldf["VendorName"].duplicated(),"")
                            finaldf["VendorName"]= finaldf["VendorName"].replace(["nan", None, pd.NA], "No Vendor").fillna("No Vendor")
                            barisheader=pd.MultiIndex.from_tuples([("", "Vendor"),("", "SLA"),("ONGOING-NOW", "OPEN"),("ONGOING-NOW", "ONPROGRESS"),("ONGOING-NOW", "POSTPONE"),("ONGOING-NOW", "TOTAL"),("OPEN-COMPLETE", "COMPLETE"),("", "INTEGRATION FAILED"),("COMP NOTE REQ & POSTPONE REQ", "APPROVAL DISPATCHER FS"), ("", "CANCEL"), ("", "TOTAL")], names=[None, None])
                            finaldf=finaldf.reindex(columns=["VendorName", "slaoptions"]+urutanstatus[:3]+["TOTAL2"]+urutanstatus[3:]+["Total"])
                            finaldf.columns=barisheader
                            
                            rendersla("SLA Summary per Vendor", finaldf, height=800) 
                                                 
                            addinfo_fromdf= df[["WorkOrderNumber", "ReferenceCode", "CustomerName", "VendorName"]].drop_duplicates()
                            addinfo_fromdf["VendorName"] = addinfo_fromdf["VendorName"].fillna("No Vendor")
                            tergabung_valid= pd.merge(tergabung_valid, addinfo_fromdf, on="WorkOrderNumber", how="left")
                            tergabung_valid["VendorName"] = tergabung_valid["VendorName"].fillna("No Vendor")
                            for vendor in sorted(tergabung_valid["VendorName"].dropna().unique()):
                                with st.expander(f"{vendor}"):
                                    vendor_df= tergabung_valid[tergabung_valid["VendorName"]== vendor]
                                    status_sum=(
                                        vendor_df.groupby("StatusReport")["WorkOrderNumber"].nunique().reindex(["OPEN", "ONPROGRESS", "POSTPONE", "COMPLETE", "INTEGRATION FAILED", "APPROVAL DISPATCHER FS", "CANCEL"], fill_value=0).reset_index()
                                    )
                                    for m, row in status_sum.iterrows():
                                        status= row["StatusReport"]
                                        count= row["WorkOrderNumber"]
                                        
                                        if count > 0:
                                            with st.expander(f"{status} ({count} WO)"):
                                                filtered = vendor_df[vendor_df["StatusReport"] == status]
                                                if "slaoptions" in filtered.columns:
                                                    sla_sum = (
                                                        filtered.groupby("slaoptions")["WorkOrderNumber"].nunique().reset_index()
                                                    )
                                                    for _, srow in sla_sum.iterrows():
                                                        sla_label = srow["slaoptions"]
                                                        sla_count = srow["WorkOrderNumber"]
                                                        with st.expander(f"{sla_label} ({sla_count} WO)"):
                                                            filtered_sla = filtered[filtered["slaoptions"] == sla_label]
                                                            filtered_sla= filtered_sla.rename(columns={"open_c":"Created", "status_c":"Modified"})
                                                            wo_info = filtered_sla[["WorkOrderNumber", "ReferenceCode","City","CustomerName","Created","Modified"]]
                                                            st.dataframe(wo_info, hide_index=True, width="stretch")
                           
                                            
                                                
                                                
                                                
                            
        

        else:
            st.warning("data kolomny galengkap di sheet historyworkorder")
            
    else:
        st.warning ("ganemu historywo")
        
    

        
        
    # dataframesla= tergabung_valid.copy()
    # if uploaded is not None:
    #     out, filename= exportfile(uploaded)
    # st.caption("Click the button below to calculate the status duration, status SLA and export as Excel")  
    # # exportbutton, fillerexpbutton1, fillerexpbutton2= st.columns([1, 2, 3])
    # # with exportbutton:
    # if st.button("Export to Excel", type="primary", use_container_width= True):

    #     with st.spinner("Processing..."):
            
    #         if "finalcopy" in st.session_state:
    #             final2= st.session_state.finalcopy.copy()
    #             if{"WorkOrderNumber", "StatusReport"}.issubset(dataframesla.columns):
    #                 temp_df= dataframesla[["WorkOrderNumber", "StatusReport", "duration"]].copy()
    #                 temp_df= temp_df.rename(columns={"WorkOrderNumber":"WO Fieldsa"})
    #                 final2= final2.merge(temp_df,  on=["WO Fieldsa", "StatusReport"], how="left")
                    
    #                 statusreportmap={
    #                     "Open": "OPEN",
    #                     "Assign To Technician": "ONPROGRESS",
    #                     "Accept": "ONPROGRESS",
    #                     "Travel": "ONPROGRESS",
    #                     "Arrive": "ONPROGRESS",
    #                     "On Progress": "ONPROGRESS",
    #                     "Return": "ONPROGRESS",
    #                     "Assign To Dispatch External": "ONPROGRESS",
    #                     "Complete With Note Reject": "ONPROGRESS",
    #                     "Revise": "ONPROGRESS",
    #                     "Return By Technician": "ONPROGRESS",
    #                     "Postpone Is Revised": "POSTPONE",
    #                     "Return Is Revised": "ONPROGRESS",
    #                     "Provisioning In Progress": "ONPROGRESS",
    #                     "Provisioning Success": "ONPROGRESS",
                        
    #                     "Complete With Note Approve": "COMPLETE",
    #                     "Complete": "COMPLETE",
    #                     "Done": "COMPLETE",
    #                     "Work Order Confirmation Approve": "COMPLETE",
    #                     "Posted To Ax Integration Success": "COMPLETE",
                        
    #                     "Postpone": "POSTPONE",
                        
    #                     "Sms Integration Failed": "INTEGRATION FAILED",
    #                     "Posted To Ax Integration Failed": "INTEGRATION FAILED",
    #                     "Provisioning Failed": "INTEGRATION FAILED",
                        
    #                     "Complete With Note Request": "APPROVAL DISPATCHER FS",
    #                     "Postpone Request": "APPROVAL DISPATCHER FS",
                        
    #                     "Cancel Work Order": "CANCEL"}
                    
    #                 def slaoptions_general(hour):
    #                     if pd.isna(hour):
    #                         return None
    #                     if hour <= 4:
    #                         return "0-4 Jam"
    #                     elif hour <= 6:
    #                         return "4-6 Jam"
    #                     elif hour <= 12:
    #                         return "6-12 Jam"
    #                     else:
    #                         return ">12 Jam"

    #                 def slaoptions_broadband(hour):
    #                     if pd.isna(hour):
    #                         return None
    #                     if hour <= 6:
    #                         return "0-6 Jam"
    #                     elif hour <= 12:
    #                         return "6-12 Jam"
    #                     elif hour <= 24:
    #                         return "12-24 Jam"
    #                     else:
    #                         return ">24 Jam"
                        
    #                 def get_sla(row):
    #                     div= str(row["DivisionName"])
    #                     dur_sla= row["duration"]
    #                     if "Broadband" in div:
    #                         return slaoptions_broadband(dur_sla)
    #                     elif "LMS" in div or "Fiberisasi" in div:
    #                         return slaoptions_general(dur_sla)
    #                     else:
    #                         return None
    #                 final2["SLA Summary"]= final2.apply(get_sla, axis=1)
    #                 final2 = final2.drop(columns=["duration"])
    #                 # st.write("liat")
    #                 # st.dataframe(final2)
                    
    #                 buffer= BytesIO()
    #                 with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
    #                     final2.to_excel(writer, index=False, sheet_name= "SLA")
    #                     df_status= pd.DataFrame(list(statusreportmap.items()), columns=["Status", "Klasifikasi Status"])
    #                     df_status.to_excel(writer, index=False, sheet_name= "KeteranganStatus")
    #                 buffer.seek(0)
    #                 nameformat = f"Dashboard_FIELDSA_{pd.Timestamp.now():%Y%m%d_%H%M%S}.xlsx"
                    
    #                 st.success("Export ready")
    #                 st.download_button("Download Excel", data= buffer.getvalue(), file_name=nameformat, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True )
    #             else:
    #                 st.write("gabisa")
        