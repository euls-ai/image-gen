import streamlit as st


st.metric(
    label="Credits",
    value=f"{(round(60 - st.session_state.t_c, 2))}$",
    border=True,
    delta=f"{round(-60 - (-60 + st.session_state.t_c), 2)}$",
)


st.header(body="Features")
st.page_link(
    "pages/sketch_to_render.py", label="Sketch to Render", icon=":material/wand_stars:"
)
st.page_link("pages/freeform.py", label="Freeform", icon=":material/wand_stars:")
st.page_link("pages/pov.py", label="POV Renders", icon=":material/wand_stars:")
st.header(body="Temporary Storage")
st.page_link("pages/storage.py", label="Generated Images", icon=":material/database:")
