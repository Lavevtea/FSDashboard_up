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

    html = """
    <style>
        table.guide-table {
            border-collapse: collapse;
            width: 100%;
        }
        table.guide-table th, table.guide-table td {
            border: 1px solid #ddd;
            padding: 8px;
            vertical-align: middle;
        }
        table.guide-table th {
            background-color: #f37336; 
            color: white;
            text-align: center;
        }
        table.guide-table td {
            background-color: #F9F9F9;
        }
    </style>
    <table class="guide-table">
        <tr>
            <th>Keterangan</th>
    """

    for key in table.keys():
        html += f"<th>{key}</th>"
    html += "</tr>"

    html += "<tr><td><b>Pengertian</b></td>"
    for key in table.keys():
        html += f"<td>{table[key]['Pengertian']}</td>"
    html += "</tr>"

    html += "<tr><td><b>Status Fieldsa</b></td>"
    for key in table.keys():
        status_list = "<br>".join(table[key]["Status Fieldsa"])
        html += f"<td>{status_list}</td>"
    html += "</tr></table>"

    st.markdown(html, unsafe_allow_html=True)

