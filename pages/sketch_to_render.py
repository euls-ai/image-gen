import base64

import streamlit as st

from pages.openai_utils import just_img

st.title("Top-Down Sketch → Render")

with st.expander("Overview"):
    st.markdown("""
- **Input**  
    - Upload a top-down site sketch (legend optional).
- **Adjust**  
    - Set desired parameters.
- **Generate**  
    - Image creation may take up to 2 minutes.
- **Save**  
    - Download images you want to keep; images do not persist across sessions.
- **Edit Workflow**  
    1. Generate image from sketch.  
    2. Download the rendered image.  
    3. Re-upload and use *Freeform* mode with a description of the changes.
- **For Building Sketches**  
    - For individual structures (not site plans), use *Freeform* mode and describe your desired output.
""")

st.info("💡 Ensure you download any images you like before refreshing the page.")
st.divider()

with st.form(key="Sketch to Render Form"):
    accuracy = st.slider(
        label="Sketch-to-Render Accuracy",
        min_value=1,
        max_value=5,
        value=2,
        help="How strict the model should be when converting the sketch into a render.",
    )

    c1, c2 = st.columns(2)
    with c1:
        time_of_day = st.selectbox(
            label="Time of Day",
            options=("Morning", "Afternoon", "Evening", "Night"),
            index=0,
            help="Select the time of day for the render.",
        )
    with c2:
        style = st.selectbox(
            label="Style",
            options=(
                "Watercolor",
                "Photorealistic 3D",
                "Minimalist",
                "Digital 3D Render",
                "Pen & Ink",
                "Collage",
            ),
            index=2,
            help="Choose the render style.",
        )

    terrain = st.text_input(
        label="Terrain / Location",
        max_chars=50,
        help="Additional details to improve the render, e.g., terrain or geographical context (e.g., 'Urban Park').",
    )

    img = st.file_uploader(
        label="Site Sketch",
        accept_multiple_files=False,
        help="Upload a top-down site sketch here.",
        type=["jpeg"],
    )

    submitted = st.form_submit_button(label="✨ Generate", use_container_width=True)

if submitted:
    if not img or not terrain:
        st.error("🚨 Please upload a sketch and enter a terrain/location description.")
    else:
        with st.spinner("Generating image... Please don't leave this page."):
            try:
                img_bytes = img.read()
                b64_str = base64.b64encode(img_bytes).decode("utf-8")
                g_img = just_img(
                    prompt="s_t_r_p",
                    user_text=(
                        f"Accuracy: {accuracy}, Time of Day: {time_of_day}, "
                        f"Style: {style}, Terrain: {terrain}."
                    ),
                    img_url=f"data:image/jpeg;base64,{b64_str}",
                )
                if g_img:
                    st.session_state.saved_images.append(
                        f"data:image/jpeg;base64,{g_img}"
                    )
                    st.image(
                        f"data:image/jpeg;base64,{g_img}",
                        width=200,
                        caption=f"{time_of_day} – {style}",
                        use_container_width=True,
                    )
                else:
                    st.error("❌ Error generating image.")
            except Exception:
                st.error("❌ Error generating image.")
