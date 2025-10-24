import streamlit as st 

def render_guide(df):
    
    st.write("## Status Information") 
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.write("""
            ### ONPROGRESS  
            **Durasi ini dihitung mulai dari waktu terakhir WO berada pada salah satu status di bawah hingga waktu saat ini (real-time)**  
            - Assign To Technician  
            - Accept  
            - Travel  
            - Arrive  
            - On Progress  
            - Return  
            - Assign To Dispatch External  
            - Complete With Note Reject  
            - Revise  
            - Return By Technician  
            - Return Is Revised  
            - Provisioning In Progress  
            - Provisioning Success  
        """)
    
    with col2:
        st.write("""
            ### COMPLETE  
            **Durasi kategori ini dihitung dari saat WO dibuka (status “Open”) hingga WO dinyatakan selesai. Status yang termasuk dalam kategori ini antara lain:**  
            - Complete With Note Approve  
            - Complete  
            - Done  
            - Work Order Confirmation Approve  
            - Posted To Ax Integration Success  
        """)
    
    with col3:
        st.write("""
            ### POSTPONE  
            **Mencakup WO yang direschedule, dengan status sebagai berikut:**  
            - Postpone  
            - Postpone Is Revised  
        """)
    
    with col4:
        st.write("""
            ### INTEGRATION FAILED
            **Mencakup WO yang gagal diproses karena kendala pada proses integrasi sistem. Status yang termasuk di antaranya:**  
            - Sms Integration Failed  
            - Posted To Ax Integration Failed  
            - Provisioning Failed  
        """)
    
    with col5:
        st.write("""
            ### APPROVAL DISPATCHER FS  
            **Mencakup WO yang sedang menunggu persetujuan dari Dispatcher FS, dengan status berikut:**  
            - Complete With Note Request  
            - Postpone Request  
        """)
    
    with col6:
        st.write("""
            ### CANCEL  
            **Mencakup WO yang telah dibatalkan, dengan status:**  
            - Cancel Work Order  
        """)


# status: ISI DR OPEN ONGOING DLL, DAN WAKTUNYA DIAMBIL DR KAPAN SAMPAI KAPAN. integration failed. approval dispatcher 