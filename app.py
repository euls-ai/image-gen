import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "saved_images" not in st.session_state:
    st.session_state.saved_images = []


if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [st.Page("pages/home.py", title="Home", icon=":material/home:")],
            "Image Gen": [
                st.Page(
                    "pages/sketch_to_render.py",
                    title="Sketch to Render",
                    icon=":material/wand_stars:",
                ),
                st.Page(
                    "pages/freeform.py", title="Freeform", icon=":material/wand_stars:"
                ),
                st.Page(
                    "pages/pov.py", title="POV Renders", icon=":material/wand_stars:"
                ),
            ],
            "Temporary Storage": [
                st.Page(
                    "pages/storage.py",
                    title="Generated Images",
                    icon=":material/database:",
                )
            ],
        }
    )
else:
    pg = st.navigation(
        [st.Page("pages/login.py", title="Log in", icon=":material/login:")]
    )

pg.run()
