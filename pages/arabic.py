import streamlit as st
from groq import Groq
import base64

st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
p, div, input, label, h1, h2, h3, h4, h5, h6 {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

if "image" not in st.session_state:
    st.session_state["image"] = None

if "data" not in st.session_state:
    st.session_state["data"] = None

if "language" not in st.session_state:
    st.session_state["language"] = "Arabic"


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

st.set_page_config(page_title="محلل الصخر", layout="centered")



st.title("محلل الصخر")
st.subheader("خذ صورة لصخرتك واحصل على كل المعلومات عنها!")

client = Groq(api_key=st.secrets.GROQ_API_KEY) # type: ignore


chosen_model = "meta-llama/llama-4-maverick-17b-128e-instruct"


st.divider()
camera_image = st.camera_input("خذ صورة لصخرتك")
if camera_image is not None:
    st.session_state.image = camera_image
else:
    st.info("استخدم مدخل الكاميرا أعلاه لالتقاط صورة لصخرة لتحليلها.")


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
    أو
</div>
""",
unsafe_allow_html=True
)

uploaded_file = st.file_uploader("ارفق صورة لصخرتك", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.session_state.image = uploaded_file


if st.session_state.image is not None:
    st.image(st.session_state.image, use_container_width=True)
    
    st.session_state.image.seek(0)
    image_data = st.session_state.image.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    

    if st.button("حلل الصخرة"):
        with st.spinner("جاري تحليل الصخرة..."):
            response = client.chat.completions.create(
                model=chosen_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Please analyze this image of a rock and provide detailed information about its type, composition with info about how you identified each one from the image of the rock, and any interesting facts. return it in JSON ONLY using this example format and it must be in """ + st.session_state.language + """:
                {
                    "Rock Type": "Metamorphic - Gneiss",
                    
                    "Composition": ["quartz: identified from...", "feldspar: ...", "biotite: ...", "amphibole: ..."],

                    "Metals": ["Iron(Fe): identified from ...", "Magnesium(Mg): ...", ...],

                    "Color": ["white", "black", "grey"],

                    "Texture": ["banded", "coarse-grained", "foliated"],

                    "Hardness (Mohs)": "6-7",

                    "Formation Process":"Formed from the intense metamorphism of pre-existing igneous (e.g., granite) or sedimentary rocks under high temperature and pressure, causing the segregation and alignment of different mineral grains into distinct light and dark bands (gneissic banding).",

                    "Uses":[
                    "dimension stone",
                    "building material",
                    "crushed stone aggregate",
                    "decorative stone (countertops, flooring)"
                    ],

                    "Interesting Facts":[
                    "It is a high-grade metamorphic rock, indicating significant heat and pressure during its formation.",
                    "The distinctive banding is called gneissic banding, resulting from mineral segregation.",
                    "Can exhibit a variety of compositions depending on the protolith (original rock type)."
                    ],
                    
                    "Confidence Level":"return only High or Medium or Low"
                }
                """
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ]
            )
            
            st.success("التحليل:")

            raw = response.choices[0].message.content

            import re, json
            match = re.search(r"\{.*\}", raw, flags=re.DOTALL) # type: ignore
            if match:
                json_str = match.group(0)
                st.session_state.data = json.loads(json_str)
            else:
                st.error("النموذج لم يرجع نمط صالح.")
                st.write(raw)     



if st.session_state.data is not None:
    data = st.session_state.data
    
    st.header("نتيجة تحليل الصخر")
    st.divider()

    with st.expander("نوع الصخر"):
        st.subheader("نوع الصخر")
        data["Rock Type"]

    with st.expander("التركيب"):
        st.subheader("التركيب")
        for mineral in data["Composition"]:
            st.markdown(f"- {mineral}")

    with st.expander("المعادن"):
        st.subheader("المعادن")
        for metal in data["Metals"]:
            st.markdown(f"- {metal}")
        
    with st.expander("اللون والملمس"):
        st.subheader("اللون")
        for color in data["Color"]:
            st.markdown(f"- {color}")
            
        st.divider()

        st.subheader("الملمس")
        for texture in data["Texture"]:
            st.markdown(f"- {texture}")

    with st.expander("الصلابة (مقياس موهس)"):
        st.subheader("الصلابة (مقياس موهس)")
        data["Hardness (Mohs)"]

    with st.expander("عملية التكوين"):
        st.subheader("عملية التكوين")
        data["Formation Process"]

    with st.expander("الاستخدامات"):
        uses = data.get("Uses", [])
        if uses:
            st.subheader("الاستخدامات")
            for use in uses:
                st.markdown(f"- {use}")
        
    with st.expander("حقائق مثيرة للاهتمام"):
        facts = data.get("Interesting Facts", [])
        if facts:
            st.subheader("حقائق مثيرة للاهتمام")
            for fact in facts:
                st.markdown(f"- {fact}")
        
    st.subheader(" مستوى الثقة")
    if data["Confidence Level"] == "High":
        st.success("عالي")
    elif data["Confidence Level"] == "Medium":
        st.warning("متوسط")
    else:
        st.error("منخفض")
    
