import streamlit as st

c1, c2, c3 = st.columns([1, 6, 1])
with c2:
    if st.button("English", use_container_width=True):
        st.switch_page("pages/app.py", query_params={"lang": "English"})
    if st.button("العربية", use_container_width=True):
        st.switch_page("pages/app.py", query_params={"lang": "Arabic"})

def hide_sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"],
            [data-testid="collapsedControl"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


hide_sidebar()

