import streamlit as st
from openai import OpenAI
import base64

language = st.query_params["lang"]

if language == "English":
    title_text = "Rock Analyzer"
    title_info = "Take a photo of your rock and get all the info about it!"
    camera_info = "Take a photo of your rock"
    camera_additional_info = "Use the camera input above to capture an image of a rock to analyze."
    upload_info = "Upload an image of your rock"
    capture_info = "Captured image"
    get_analysis_button = "Get rock analysis"
    spinner_info = "Analyzing your rock..."
    analysis = "Analysis:"
    model_error_info = "Model did not return valid JSON."
    rock_analysis_result = "Rock Analysis Result"
    rock_type = "Rock Type"
    composition = "Composition"
    metals = "Metals"
    color_and_texture = "Color and Texture"
    color = "Color"
    texture = "Texture"
    hardness = "Hardness (Mohs)"
    formation_process = "Formation Process"
    uses = "Uses"
    interesting_facts = "Interesting Facts"
    confidence_level = "Confidence Level"
    high = "High"
    medium = "Medium"
    low = "Low"
else:
    title_text = "محلل الصخور"
    title_info = "التقط صورة لصخرتك واحصل على كل المعلومات عنها!"
    camera_info = "التقط صورة لصخرتك"
    camera_additional_info = "استخدم مدخل الكاميرا أعلاه لالتقاط صورة لصخرة لتحليلها."
    upload_info = "قم بتحميل صورة لصخرتك"
    capture_info = "الصورة الملتقطة"
    get_analysis_button = "احصل على تحليل الصخرة"
    spinner_info = "جارٍ تحليل صخرتك..."
    analysis = "التحليل:"
    model_error_info = "لم يُرجع النموذج JSON صالح."
    rock_analysis_result = "نتيجة تحليل الصخر"
    rock_type = "نوع الصخر"
    composition = "التركيب"
    metals = "المعادن"
    color_and_texture = "اللون والملمس"
    color = "اللون"
    texture = "الملمس"
    hardness = "الصلابة (مقياس موهس)"
    formation_process = "عملية التكوين"
    uses = "الاستخدامات"
    interesting_facts = "حقائق مثيرة للاهتمام"
    confidence_level = " مستوى الثقة"
    high = "عالي"
    medium = "متوسط"
    low = "منخفض"

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
    st.session_state["language"] = None


st.set_page_config(page_title=title_text, layout="centered")


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


st.title(title_text)
st.write(title_info)

# Initialize OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets.OPENROUTER_API_KEY
)

# Set the model to Qwen
chosen_model = "qwen/qwen3-vl-235b-a22b-instruct"


st.divider()
camera_image = st.camera_input(camera_info)
if camera_image is not None:
    st.session_state.image = camera_image
else:
    st.info(camera_additional_info)


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

uploaded_file = st.file_uploader(upload_info, type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    st.session_state.image = uploaded_file


if st.session_state.image is not None:
    st.image(st.session_state.image, caption=capture_info, use_container_width=True)
    
    st.session_state.image.seek(0)
    image_data = st.session_state.image.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    

    if st.button(get_analysis_button):
        with st.spinner(spinner_info):
            response = client.chat.completions.create(
                model=chosen_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """Please analyze this image of a rock and provide detailed information about its type, composition with info about how you identified each one from the image of the rock, and any interesting facts. return it in JSON ONLY using this example format and the content must be in """ + language + """, but the dictionary keys must remain in English:
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
            
            st.success(analysis)

            raw = response.choices[0].message.content

            import re, json
            match = re.search(r"\{.*\}", raw, flags=re.DOTALL) # type: ignore
            if match:
                json_str = match.group(0)
                st.session_state.data = json.loads(json_str)
            else:
                st.error(model_error_info)
                st.write(raw)     



if st.session_state.data is not None:
    data = st.session_state.data
    
    st.header(rock_analysis_result)
    st.divider()

    with st.expander(rock_type):
        st.subheader(rock_type)
        data["Rock Type"]

    with st.expander(composition):
        st.subheader(composition)
        for mineral in data["Composition"]:
            st.markdown(f"- {mineral}")

    with st.expander(metals):
        st.subheader(metals)
        for metal in data["Metals"]:
            st.markdown(f"- {metal}")
        
    with st.expander(color_and_texture):
        st.subheader(color)
        for color in data["Color"]:
            st.markdown(f"- {color}")
            
        st.divider()

        st.subheader(texture)
        for texture in data["Texture"]:
            st.markdown(f"- {texture}")

    with st.expander(hardness):
        st.subheader(hardness)
        data["Hardness (Mohs)"]

    with st.expander(formation_process):
        st.subheader(formation_process)
        data["Formation Process"]

    with st.expander(uses):
        uses = data.get("Uses", [])
        if uses:
            st.subheader(uses)
            for use in uses:
                st.markdown(f"- {use}")
        
    with st.expander(interesting_facts):
        facts = data.get("Interesting Facts", [])
        if facts:
            st.subheader(interesting_facts)
            for fact in facts:
                st.markdown(f"- {fact}")
        
    st.subheader(confidence_level)
    if data["Confidence Level"] == "High":
        st.success(high)
    elif data["Confidence Level"] == "Medium":
        st.warning(medium)
    else:
        st.error(low)
