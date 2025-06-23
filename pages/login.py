import streamlit as st

from pages.openai_utils import get_total_cost

with st.form(key="login form"):
    u = st.text_input(label="Username", max_chars=30)
    p = st.text_input(label="Password", type="password", max_chars=30)
    submitted = st.form_submit_button("🔓 Login", use_container_width=True)

if submitted:
    if u == st.secrets.u and p == st.secrets.p:
        with st.spinner(text="Retrieving credits..."):
            try:
                st.session_state.t_c = get_total_cost()
            except:
                st.session_state.t_c = 0
            if st.session_state.t_c > 50:
                st.error("🚨 No credits remaining.")
            else:
                st.session_state.logged_in = True
                st.rerun()
    else:
        st.error("🚨 Invalid credentials.")
