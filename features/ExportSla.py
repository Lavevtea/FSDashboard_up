import streamlit as st 
import matplotlib.pyplot as plt
import time
import pandas as pd
from io import BytesIO
import datetime as dt
from datetime import timedelta

def exportsla(df, df_rca, df_history):
    st.write("### Export SLA Summary")
    # st.write(df_rca)
    # st.write(df_history)
    
    if st.button("Export to Excel"):
        start_time = time.time()
        with st.spinner("Memproses data..."):
            df["SubRegion"] = df["SubRegion"].astype(str).str.strip().str.title()
            df["WorkOrderStatusItem"] = df["WorkOrderStatusItem"].astype(str).str.strip().str.title()
            df_history["WorkOrderStatusItem"] = df_history["WorkOrderStatusItem"].astype(str).str.strip().str.title()
  
            df = df.merge(
                df_rca[["WorkOrderNumber", "UpTime"]],
                on="WorkOrderNumber",
                how="left"
            )
            
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
            df["Region"]= df["SubRegion"].map(regionmap).fillna("Unknown")
                
            statusreportmap= {
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
            
            df["StatusReport"]= df["WorkOrderStatusItem"].map(statusreportmap).fillna("Unknown")
            cols = [
                "WorkOrderNumber",
                "ReferenceCode",
                "WorkOrderTypeName",
                "DivisionName",
                "CustomerId",
                "CustomerName",
                "Cid",
                "CircuitId",
                "EndCustomerName",
                "Region",
                "SubRegion",
                "City",
                "DeviceAllocation",
                "VendorName",
                "DispatcherName",
                "TechnicianName",
                "UpTime",
                "WorkOrderStatusItem",
                "StatusReport",
                "Reason"
            ]
            df2=df[cols]
            wo_to_type = df2.set_index("WorkOrderNumber")["WorkOrderTypeName"].to_dict()
            
            urutan_troubleshoot=[
                'Open',
                'Assign To Dispatch External',
                'Assign To Technician',
                'Accept',
                'Travel',
                'Arrive',
                'On Progress',
                'Done',
                'Work Order Confirmation Approve',
                'Complete With Note Request',
                'Complete',
                'Complete With Note Approve',
            ]
            
            urutan_activation = [
                'Open',
                'Assign To Dispatch External',
                'Assign To Technician',
                'Accept',
                'Travel',
                'Arrive',
                'On Progress',
                'Provisioning In Progress',
                'Provisioning Success',
                'Done',
                'Work Order Confirmation Approve',
                'Posted To Ax Integration Success',
                'Complete With Note Request',
                'Complete',
                'Complete With Note Approve',
            ]
            df_history = df_history.sort_values(["WorkOrderNumber", "Modified"], kind="mergesort")
            
            hasil_list = []
            for wo, group in df_history.groupby("WorkOrderNumber"):
                tipewo = wo_to_type.get(wo, "Troubleshoot")
                urutanstatus = urutan_activation if "Activation" in tipewo else urutan_troubleshoot
                group = group.sort_values("Modified", kind="mergesort")
                modified_map = {}
                for status, s in group.groupby("WorkOrderStatusItem"):
                    if status.lower()== "Open":
                        modified_map[status]=s["Modified"].iloc[0]
                    else:
                        modified_map[status]=s["Modified"].iloc[-1]

                timeline = {"WorkOrderNumber": wo}
                last_time = None

                for status in urutanstatus:
                    waktu = modified_map.get(status)
                    if waktu and (last_time is None or waktu >= last_time):
                        timeline[status] = waktu
                        last_time = waktu
                    else:
                        timeline[status] = None

                hasil_list.append(timeline)

            sla_timeline = pd.DataFrame(hasil_list)
            df3 = df2.merge(sla_timeline, on="WorkOrderNumber", how="left")
            for col in ["Open", "Assign To Dispatch External", "Assign To Technician", "Accept", "Done","Complete", "Complete With Note Approve", "Complete With Note Request"]:
                if col in df3.columns:
                     df3[col] = pd.to_datetime(df3[col], errors="coerce")
            def format_durasi(delta):
                if pd.isna(delta):
                    return "N/A"
                if isinstance(delta, pd.Timestamp):
                    delta = timedelta(seconds=delta)
                days = delta.days
                hours, remains = divmod(delta.seconds, 3600)
                minutes, seconds = divmod(remains, 60)
                return f"{days:02}:{hours:02}:{minutes:02}:{seconds:02}"
            
            def sla_durasi(delta, mode):
                if pd.isna(delta):
                    return "N/A"
                menit = delta.total_seconds() / 60
                jam = menit / 60
                if mode == "jam":
                    if jam <= 8:
                        return "<8 Jam"
                    elif jam <= 16:
                        return "8–16 Jam"
                    elif jam <= 24:
                        return "16–24 Jam"
                    else:
                        return ">24 Jam"
                else:  # default menit
                    if menit <= 15:
                        return "<15 Menit"
                    elif menit <= 30:
                        return "15–30 Menit"
                    else:
                        return ">30 Menit"

            def hitung_durasi(df, start, end, nama_kolom):
                durasi_col = nama_kolom
                sla_col = f"SLA {nama_kolom}"
    
                durasi_list, sla_list = [], []
                for _, row in df.iterrows():
                    start_time = row.get(start)
                    end_time = row.get(end)
                    if pd.notna(start_time) and pd.notna(end_time):
                        delta = end_time - start_time
                        durasi_list.append(format_durasi(delta))

                        mode = "jam" if nama_kolom == "Accept - Done" else "menit"
                        sla_list.append(sla_durasi(delta, mode))
                    else:
                        durasi_list.append("N/A")
                        sla_list.append("N/A")

                df[durasi_col] = durasi_list
                df[sla_col] = sla_list
                
            df3["CompleteStat"] = df3["Complete"].combine_first(df3["Complete With Note Approve"])
            hitung_durasi(df3, "Open", "Assign To Dispatch External", "Open - Assign To Dispatch External")
            hitung_durasi(df3, "Assign To Dispatch External", "Assign To Technician", "Assign To Dispatch External - Assign To Technician")
            hitung_durasi(df3, "Assign To Technician", "Accept", "Assign To Technician - Accept")
            hitung_durasi(df3, "Accept", "Done", "Accept - Done")
            hitung_durasi(df3, "Done", "CompleteStat", "Done - Complete")
            df3 = df3.drop(columns=["CompleteStat"], errors="ignore")

            reindex_cols= ["WorkOrderStatusItem", "StatusReport", "Reason"]
            other_cols= [col for col in df3.columns if col not in reindex_cols]
            df3=df3[other_cols+reindex_cols]
            
            buffer_xlsx = BytesIO()
            with pd.ExcelWriter(buffer_xlsx, engine="xlsxwriter") as writer:
                df3.to_excel(writer, index=False, sheet_name="SLA")
                pd.DataFrame(list(statusreportmap.items()), columns=["Status", "Klasifikasi Status"]).to_excel(writer, index=False, sheet_name="KeteranganStatus")
            buffer_xlsx.seek(0)
            
            processtime= time.time()-start_time
            
            st.write(df3)
            st.success(f"Data berhasil diproses dalam {processtime:.2f} detik")
            
        st.download_button(
            label="Download Excel",
            data=buffer_xlsx,
            file_name=f"Dashboard_FIELDSA_{dt.datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
