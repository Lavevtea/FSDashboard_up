import streamlit as st 
import matplotlib.pyplot as plt
import time
import pandas as pd
from io import BytesIO
import datetime as dt

def exportsla(df, df_rca, df_history):
    st.write("### Export SLA Summary")
#     # st.write(df_rca)
#     # st.write(df_history)
    
#     if st.button("Export to Excel"):
#         start_time = time.time()
#         with st.spinner("Memproses data..."):
#             df["SubRegion"] = df["SubRegion"].astype(str).str.strip().str.title()
#             df["WorkOrderStatusItem"] = df["WorkOrderStatusItem"].astype(str).str.strip().str.title()
#             df_history["WorkOrderStatusItem"] = df_history["WorkOrderStatusItem"].astype(str).str.strip().str.title()
  
#             df = df.merge(
#                 df_rca[["WorkOrderNumber", "UpTime"]],
#                 on="WorkOrderNumber",
#                 how="left"
#             )
            
#             regionmap={
#                 "Bali": "East",
#                 "Central Java": "Central",
#                 "East Java": "East",
#                 "Jabodetabek":"Central",
#                 "West Java": "Central",
#                 "Kalimantan":"East",
#                 "Sulawesi":"East",
#                 "Internasional": "International",
#                 "Kepulauan Riau": "West",
#                 "Northern Sumatera":"West",
#                 "Southern Sumatera":"West"
#             }
#             df["Region"]= df["SubRegion"].map(regionmap).fillna("Unknown")
                
#             statusreportmap= {
#                 "Open": "OPEN",
                
#                 "Assign To Technician": "ONPROGRESS",
#                 "Accept": "ONPROGRESS",
#                 "Travel": "ONPROGRESS",
#                 "Arrive": "ONPROGRESS",
#                 "On Progress": "ONPROGRESS",
#                 "Return": "ONPROGRESS",
#                 "Assign To Dispatch External": "ONPROGRESS",
#                 "Complete With Note Reject": "ONPROGRESS",
#                 "Revise": "ONPROGRESS",
#                 "Return By Technician": "ONPROGRESS",
#                 "Postpone Is Revised": "POSTPONE",
#                 "Return Is Revised": "ONPROGRESS",
#                 "Provisioning In Progress": "ONPROGRESS",
#                 "Provisioning Success": "ONPROGRESS",
                
#                 "Complete With Note Approve": "COMPLETE",
#                 "Complete": "COMPLETE",
#                 "Done": "COMPLETE",
#                 "Work Order Confirmation Approve": "COMPLETE",
#                 "Posted To Ax Integration Success": "COMPLETE",
                
#                 "Postpone": "POSTPONE",
                
#                 "Sms Integration Failed": "INTEGRATION FAILED",
#                 "Posted To Ax Integration Failed": "INTEGRATION FAILED",
#                 "Provisioning Failed": "INTEGRATION FAILED",
                
#                 "Complete With Note Request": "APPROVAL DISPATCHER FS",
#                 "Postpone Request": "APPROVAL DISPATCHER FS",
                
#                 "Cancel Work Order": "CANCEL"}  
            
#             df["StatusReport"]= df["WorkOrderStatusItem"].map(statusreportmap).fillna("Unknown")
#             cols = [
#                 "WorkOrderNumber",
#                 "ReferenceCode",
#                 "WorkOrderTypeName",
#                 "DivisionName",
#                 "CustomerId",
#                 "CustomerName",
#                 "Cid",
#                 "CircuitId",
#                 "EndCustomerName",
#                 "Region",
#                 "SubRegion",
#                 "City",
#                 "DeviceAllocation",
#                 "VendorName",
#                 "DispatcherName",
#                 "TechnicianName",
#                 "UpTime",
#                 "WorkOrderStatusItem",
#                 "StatusReport",
#                 "Reason"
#             ]
#             df2=df[cols]
#             wo_to_type = df2.set_index("WorkOrderNumber")["WorkOrderTypeName"].to_dict()
            
#             urutan_troubleshoot=[
#                 'Open',
#                 'Assign To Dispatch External',
#                 'Assign To Technician',
#                 'Accept',
#                 'Travel',
#                 'Arrive',
#                 'On Progress',
#                 'Done',
#                 'Work Order Confirmation Approve',
#                 'Complete With Note Request',
#                 'Complete',
#                 'Complete With Note Approve',
#             ]
            
#             urutan_activation = [
#                 'Open',
#                 'Assign To Dispatch External',
#                 'Assign To Technician',
#                 'Accept',
#                 'Travel',
#                 'Arrive',
#                 'On Progress',
#                 'Provisioning In Progress',
#                 'Provisioning Success',
#                 'Done',
#                 'Work Order Confirmation Approve',
#                 'Posted To Ax Integration Success',
#                 'Complete With Note Request',
#                 'Complete',
#                 'Complete With Note Approve',
#             ]
#             df_history = df_history.sort_values(["WorkOrderNumber", "Modified"], kind="mergesort")
            
#             hasil_list = []
#             for wo, group in df_history.groupby("WorkOrderNumber"):
#                 tipewo = wo_to_type.get(wo, "Troubleshoot")
#                 urutanstatus = urutan_activation if "Activation" in tipewo else urutan_troubleshoot
#                 group = group.sort_values("Modified", kind="mergesort")
#                 modified_map = {}
#                 for status, s in group.groupby("WorkOrderStatusItem"):
#                     if status.lower()== "Open":
#                         modified_map[status]=s["Modified"].iloc[0]
#                     else:
#                         modified_map[status]=s["Modified"].iloc[-1]

#                 timeline = {"WorkOrderNumber": wo}
#                 last_time = None

#                 for status in urutanstatus:
#                     waktu = modified_map.get(status)
#                     if waktu and (last_time is None or waktu >= last_time):
#                         timeline[status] = waktu
#                         last_time = waktu
#                     else:
#                         timeline[status] = None

#                 hasil_list.append(timeline)

#             sla_timeline = pd.DataFrame(hasil_list)
#             df3 = df2.merge(sla_timeline, on="WorkOrderNumber", how="left")

#             # timeline_cols = [c for c in timeline_cols if c in sla_timeline.columns]
#             # sla_timeline = sla_timeline[timeline_cols]
#             buffer_xlsx = BytesIO()
#             with pd.ExcelWriter(buffer_xlsx, engine="xlsxwriter") as writer:
#                 df3.to_excel(writer, index=False, sheet_name="SLA")
#                 pd.DataFrame(list(statusreportmap.items()), columns=["Status", "Klasifikasi Status"]).to_excel(writer, index=False, sheet_name="KeteranganStatus")
#             buffer_xlsx.seek(0)
            
#             processtime= time.time()-start_time
            
#             st.success(f"Data berhasil diproses dalam {processtime:.2f} detik")
            
#         st.download_button(
#             label="Download Excel",
#             data=buffer_xlsx,
#             file_name=f"SLA_Summary_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
#             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#         )
