import streamlit as st

if not st.session_state.saved_images:
    st.write("No images have been generated yet.")

st.info("💡 Ensure you download any images you like before refreshing the page.")

for img in st.session_state.saved_images:
    st.image(img, width=200, use_container_width=True)
