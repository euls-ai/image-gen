import base64

import streamlit as st

from pages.openai_utils import just_img

st.title("POV Renders")

with st.expander("Overview"):
    st.info(
        "⚠️ For better results: Indicate the intended render perspective by drawing a red arrow on the sketch."
    )
    st.markdown("""
- **Overview**  
    - Generate one photorealistic point-of-view render from a user-supplied top-down architectural site sketch.

- **Inputs**  
    - Sketch Image (must be a top-down site sketch)  
    - Accuracy Level (1–5)  
    - Time of Day (Morning | Afternoon | Evening | Night)  
    - Terrain / Location (free text description)

- **How it Works**  
    - If the upload is not a valid top-view site sketch, the system will halt and display an error.
    - The first red arrow in the sketch determines the camera viewpoint and direction. If no arrow exists, the system selects a viewpoint that shows the whole site.
    - The camera is placed at the arrow start, 1.7m above the ground, with ±35mm full-frame FOV for a natural human perspective.
    - The Accuracy slider controls how faithfully sketch details are replicated—1 (loose massing), 5 (exact replication), with intermediate levels interpolating.
    - Lighting and atmosphere are matched to the selected Time of Day.
    - Terrain/location cues (vegetation, ground, climate, materials) are adapted from the provided description.

- **Style & Output**  
    - Strictly photorealistic (no filters, text, watermarks, or stylized effects).
    - Returns a single image with no descriptive text or metadata.
    """)
st.info("💡 Ensure you download any images you like before refreshing the page.")
st.divider()

with st.form(key="POV Views Form"):
    accuracy = st.slider(
        label="Surroundings Accuracy",
        min_value=1,
        max_value=5,
        value=2,
        help="How strict the model should be with its surroundings.",
    )

    time_of_day = st.selectbox(
        label="Time of Day",
        options=("Morning", "Afternoon", "Evening", "Night"),
        index=0,
        help="Time of day for the render.",
    )

    terrain = st.text_input(
        label="Terrain / Location",
        max_chars=50,
        help="Any details that could improve the render, including terrain or location (e.g., 'Urban Park').",
    )

    img = st.file_uploader(
        label="Site Sketch",
        accept_multiple_files=False,
        help="A top-down site sketch is expected here.",
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
                    prompt="pov_p",
                    user_text=f"Accuracy: {accuracy}, Time of day: {time_of_day}, Terrain: {terrain}.",
                    img_url=f"data:image/jpeg;base64,{b64_str}",
                )
                if g_img:
                    st.session_state.saved_images.append(
                        f"data:image/jpeg;base64,{g_img}"
                    )
                    st.image(
                        f"data:image/jpeg;base64,{g_img}",
                        width=200,
                        caption=f"{time_of_day} – {terrain}",
                        use_container_width=True,
                    )
                else:
                    st.error("❌ Error generating image.")
            except Exception:
                st.error("❌ Error generating image.")
