import streamlit as st

def navbar():
    st.markdown("""
        <style>
        .nav-container {
            display: flex;
            justify-content: center;
            background-color: #f8bbd0; /* pastel pink */
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .nav-item {
            margin: 0 15px;
            font-size: 18px;
            font-weight: bold;
            color: #6a1b9a; /* deep purple */
            text-decoration: none;
        }
        .nav-item:hover {
            color: #d81b60; /* dark pink */
        }
        </style>
        <div class="nav-container">
            <a class="nav-item" href="/">Home</a>
            <a class="nav-item" href="/Profile">Profile</a>
            <a class="nav-item" href="/Appointments">Appointments</a>
            <a class="nav-item" href="/Medicines">Medicines</a>
            <a class="nav-item" href="/Reports">Reports</a>
            <a class="nav-item" href="/Settings">Settings</a>
        </div>
    """, unsafe_allow_html=True)
