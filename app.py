import streamlit as st
import google.generativeai as genai



if "image" not in st.session_state:
    st.session_state["image"] = None

if "data" not in st.session_state:
    st.session_state["data"] = None


st.set_page_config(page_title="Rock Analyzer", layout="centered")

st.title("Rock Analyzer")
st.write("Take a photo of your rock and get all the info about it!")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"]) # type: ignore


chosen_model = st.selectbox("Select Model", ["gemini-2.5-flash", "gemini-2.5-pro"])
if chosen_model:
    model = genai.GenerativeModel(chosen_model) # type: ignore

st.markdown("*gemini-2.5-flash: Faster and cheaper, suitable for quick analyses.*")
st.markdown("*gemini-2.5-pro: More advanced, provides deeper insights and better accuracy, is limited.*")

st.divider()
camera_image = st.camera_input("Take a photo of your rock")
if camera_image is not None:
    st.session_state.image = camera_image
else:
    st.info("Use the camera input above to capture an image of a rock to analyze.")


st.markdown(
"""
<div style="
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100px;
    font-size: 20px;
    font-weight: bold;
    opacity: 1;
">
    OR
</div>
""",
unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Upload an image of your rock", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.session_state.image = uploaded_file


if st.session_state.image is not None:
    st.image(st.session_state.image, caption="Captured image", use_container_width=True)
    
    image_data = st.session_state.image.read()
    
    if st.button("Get rock analysis"):
        with st.spinner("Analyzing your rock..."):
            response = model.generate_content([
                """Please analyze this image of a rock and provide detailed information about its type, composition, and any interesting facts. return it in this example format:
                {
                    "Rock Type":"Metamorphic - Gneiss"
                    
                    "Composition":["quartz", "feldspar", "biotite", "amphibole"]

                    "Color":["white", "black", "grey"]

                    "Texture": ["banded", "coarse-grained", "foliated"]

                    "Hardness (Mohs)":"6-7"

                    "Formation Process":"Formed from the intense metamorphism of pre-existing igneous (e.g., granite) or sedimentary rocks under high temperature and pressure, causing the segregation and alignment of different mineral grains into distinct light and dark bands (gneissic banding)."

                    "Uses":[
                    "dimension stone",
                    "building material",
                    "crushed stone aggregate",
                    "decorative stone (countertops, flooring)"
                    ]

                    "Interesting Facts":[
                    "It is a high-grade metamorphic rock, indicating significant heat and pressure during its formation.",
                    "The distinctive banding is called gneissic banding, resulting from mineral segregation.",
                    "Can exhibit a variety of compositions depending on the protolith (original rock type)."
                    ]
                    
                    "Confidence Level":"return only High or Medium or Low"
                }
                """,
                {"mime_type": "image/jpeg", "data": image_data}
            ])
            
            st.success("Analysis:")

            raw = response.text

            import re, json
            match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
            if match:
                json_str = match.group(0)
                st.session_state.data = json.loads(json_str)
            else:
                st.error("Model did not return valid JSON.")
                st.write(raw)     



if st.session_state.data is not None:
    data = st.session_state.data
    st.header("Rock Analysis Result")
    st.divider()

    with st.expander("Rock Type"):
        st.subheader("Rock Type")
        data["Rock Type"]

    with st.expander("Composition"):
        st.subheader("Composition")
        for mineral in data["Composition"]:
            st.markdown(f"- {mineral}")

    with st.expander("Color and Texture"):
        st.subheader("Color")
        for color in data["Color"]:
            st.markdown(f"- {color}")
        st.divider()
        st.subheader("Texture")
        for texture in data["Texture"]:
            st.markdown(f"- {texture}")

    with st.expander("Hardness"):
        st.subheader("Hardness (Mohs)")
        data["Hardness (Mohs)"]

    with st.expander("Formation Process"):
        st.subheader("Formation Process")
        data["Formation Process"]

    with st.expander("Uses"):
        uses = data.get("Uses", [])
        if uses:
            st.subheader("Uses")
            for use in uses:
                st.markdown(f"- {use}")
        
    with st.expander("Interesting Facts"):
        facts = data.get("Interesting Facts", [])
        if facts:
            st.subheader("Interesting Facts")
            for fact in facts:
                st.markdown(f"- {fact}")
        
    st.subheader("Confidence Level")
    if data["Confidence Level"] == "High":
        st.success("High")
    elif data["Confidence Level"] == "Medium":
        st.warning("Medium")
    else:
        st.error("Low")



