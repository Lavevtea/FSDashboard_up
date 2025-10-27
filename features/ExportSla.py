import streamlit as st 
import matplotlib.pyplot as plt
import time
import pandas as pd
from io import BytesIO
import datetime as dt

def exportsla(df, df_rca, df_history):
    st.write("### Export SLA Summary")
    # st.write(df_rca)
    # st.write(df_history)
    
    # if st.button("Export to Excel"):
    #     start_time = time.time()
    #     with st.spinner("Memproses data..."):
    #         for col in ["SubRegion", "WorkOrderStatusItem"]:
    #             df[col] = df[col].astype(str).str.strip().str.title()
                
    #         df = df.merge(
    #             df_rca[["WorkOrderNumber", "UpTime"]],
    #             on="WorkOrderNumber",
    #             how="left"
    #         )
            
    #         regionmap={
    #             "Bali": "East",
    #             "Central Java": "Central",
    #             "East Java": "East",
    #             "Jabodetabek":"Central",
    #             "West Java": "Central",
    #             "Kalimantan":"East",
    #             "Sulawesi":"East",
    #             "Internasional": "International",
    #             "Kepulauan Riau": "West",
    #             "Northern Sumatera":"West",
    #             "Southern Sumatera":"West"
    #         }
    #         df["Region"]= df["SubRegion"].map(regionmap).fillna("Unknown")~
                
    #         statusreportmap= {
    #             "Open": "OPEN",
                
    #             "Assign To Technician": "ONPROGRESS",
    #             "Accept": "ONPROGRESS",
    #             "Travel": "ONPROGRESS",
    #             "Arrive": "ONPROGRESS",
    #             "On Progress": "ONPROGRESS",
    #             "Return": "ONPROGRESS",
    #             "Assign To Dispatch External": "ONPROGRESS",
    #             "Complete With Note Reject": "ONPROGRESS",
    #             "Revise": "ONPROGRESS",
    #             "Return By Technician": "ONPROGRESS",
    #             "Postpone Is Revised": "POSTPONE",
    #             "Return Is Revised": "ONPROGRESS",
    #             "Provisioning In Progress": "ONPROGRESS",
    #             "Provisioning Success": "ONPROGRESS",
                
    #             "Complete With Note Approve": "COMPLETE",
    #             "Complete": "COMPLETE",
    #             "Done": "COMPLETE",
    #             "Work Order Confirmation Approve": "COMPLETE",
    #             "Posted To Ax Integration Success": "COMPLETE",
                
    #             "Postpone": "POSTPONE",
                
    #             "Sms Integration Failed": "INTEGRATION FAILED",
    #             "Posted To Ax Integration Failed": "INTEGRATION FAILED",
    #             "Provisioning Failed": "INTEGRATION FAILED",
                
    #             "Complete With Note Request": "APPROVAL DISPATCHER FS",
    #             "Postpone Request": "APPROVAL DISPATCHER FS",
                
    #             "Cancel Work Order": "CANCEL"}  
            
    #         df["StatusReport"]= df["WorkOrderStatusItem"].map(statusreportmap).fillna("Unknown")
    #         cols = [
    #             "WorkOrderNumber",
    #             "ReferenceCode",
    #             "WorkOrderTypeName",
    #             "DivisionName",
    #             "CustomerId",
    #             "CustomerName",
    #             "Cid",
    #             "CircuitId",
    #             "EndCustomerName",
    #             "Region",
    #             "SubRegion",
    #             "City",
    #             "DeviceAllocation",
    #             "VendorName",
    #             "DispatcherName",
    #             "TechnicianName",
    #             "UpTime",
    #             "WorkOrderStatusItem",
    #             "StatusReport",
    #             "Reason"
    #         ]
    #         df2=df[cols]
    #         df_ketstat= pd.DataFrame(list(statusreportmap.items()),columns=["Status", "Klasifikasi Status"])
            
    #         buffer_xlsx = BytesIO()
    #         with pd.ExcelWriter(buffer_xlsx, engine="xlsxwriter") as writer:
    #             df2.to_excel(writer, index=False, sheet_name="SLA")
    #             df_ketstat.to_excel(writer, index=False, sheet_name="KeteranganStatus")
    #         buffer_xlsx.seek(0)
            
    #         processtime= time.time()- start_time
            
    #         st.success(f"Data berhasil diproses dalam {processtime:.2f} detik")
            
    #     st.download_button(
    #         label="Download Excel",
    #         data=buffer_xlsx,
    #         file_name=f"SLA_Summary_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
    #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )
