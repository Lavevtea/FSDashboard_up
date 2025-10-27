import streamlit as st
import pandas as pd

def render_guide(df):
    st.write("## Status Information")

    table = {
        "ONPROGRESS": {
            "Pengertian": "Durasi WO yang dihitung mulai dari waktu terakhir WO berada pada salah satu status di bawah hingga waktu saat ini (real-time)",
            "Status Fieldsa": [
                "1. Assign To Technician",
                "2. Accept",
                "3. Travel",
                "4. Arrive",
                "5. On Progress",
                "6. Return",
                "7. Assign To Dispatch External",
                "8. Complete With Note Reject",
                "9. Revise",
                "10. Return By Technician",
                "11. Return Is Revised",
                "12. Provisioning In Progress",
                "13. Provisioning Success"
            ]
        },
        "COMPLETE": {
            "Pengertian": "Durasi WO yang dihitung dari saat WO dibuka (status 'Open') hingga WO dinyatakan selesai",
            "Status Fieldsa": [
                "1. Complete With Note Approve",
                "2. Complete",
                "3. Done",
                "4. Work Order Confirmation Approve",
                "5. Posted To Ax Integration Success"
            ]
        },
        "POSTPONE": {
            "Pengertian": "Mencakup WO yang direschedule",
            "Status Fieldsa": [
                "1. Postpone",
                "2. Postpone Is Revised"
            ]
        },
        "INTEGRATION FAILED": {
            "Pengertian": "Mencakup WO yang gagal diproses karena kendala pada proses integrasi sistem",
            "Status Fieldsa": [
                "1. Sms Integration Failed",
                "2. Posted To Ax Integration Failed",
                "3. Provisioning Failed"
            ]
        },
        "APPROVAL DISPATCHER FS": {
            "Pengertian": "Mencakup WO yang sedang menunggu persetujuan dari Dispatcher FS",
            "Status Fieldsa": [
                "1. Complete With Note Request",
                "2. Postpone Request"
            ]
        },
        "CANCEL": {
            "Pengertian": "Mencakup WO yang telah dibatalkan",
            "Status Fieldsa": [
                "1. Cancel Work Order"
            ]
        },
    }

    # Build markdown table
    header = "| Keterangan | " + " | ".join(table.keys()) + " |"
    separator = "|" + "-------------|" * (len(table) + 1)

    pengertian_row = "| **Pengertian** | " + " | ".join(
        [table[k]["Pengertian"] for k in table]
    ) + " |"

    status_row = "| **Status Fieldsa** | " + " | ".join(
        ["<br>".join(table[k]["Status Fieldsa"]) for k in table]
    ) + " |"

    table_render = f"{header}\n{separator}\n{pengertian_row}\n{status_row}"

    st.markdown(table_render, unsafe_allow_html=True)

