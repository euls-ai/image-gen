import base64

import streamlit as st

from pages.openai_utils import just_img

st.title("Freeform")

with st.expander("Overview"):
    st.markdown("""
- **Freeform Overview**  
    - Upload an image to generate a new image—either as an edit of the upload, or as a new creation using it as a reference.
    - Provide detailed descriptions to guide edits or create entirely new outputs.

- **Use Cases**  
    - Edit images created in *Sketch to Render* by uploading and describing desired changes.
    - Create new images based on a reference sketch and an in-depth description.
    - Not limited to top-down views—suitable for a wide range of outputs, including buildings, structures, interiors, and more.
    """)

st.info("💡 Ensure you download any images you like before refreshing the page.")
st.divider()

with st.form(key="Freeform Image Edit Form"):
    img = st.file_uploader(
        label="Reference",
        accept_multiple_files=False,
        help="The reference image used.",
        type=["jpeg"],
    )

    user_text = st.text_area(
        label="Description of request.",
        max_chars=1000,
        help="Describe your request and any specific rules. You can either request an image edit or a new image based on your reference.",
    )

    submitted = st.form_submit_button(label="✨ Generate", use_container_width=True)

if submitted:
    if not img or not user_text:
        st.error("🚨 Please upload an image and enter a description.")
    else:
        with st.spinner("Generating image... Please don't leave this page."):
            try:
                img_bytes = img.read()
                b64_str = base64.b64encode(img_bytes).decode("utf-8")
                g_img = just_img(
                    prompt="f_f_p",
                    user_text=user_text,
                    img_url=f"data:image/jpeg;base64,{b64_str}",
                )
                if g_img:
                    st.session_state.saved_images.append(
                        f"data:image/jpeg;base64,{g_img}"
                    )
                    st.image(
                        f"data:image/png;base64,{g_img}",
                        width=200,
                        use_container_width=True,
                    )
                else:
                    st.error("Error generating image...")
            except Exception:
                st.error("Error generating image...")
