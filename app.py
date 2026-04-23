import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد رشا القدسي",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. تصميم CSS محسن (يدعم الوضع المظلم والفاتح بوضوح عالٍ)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif; direction: rtl; }

    /* ضمان وضوح الخط في كل الأوضاع */
    html, body, [data-testid="stMarkdownContainer"] p {
        color: var(--text-color);
    }

    /* الهيدر الجديد بالاسم المطلوب */
    .mobile-header {
        background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
        padding: 30px 20px;
        border-radius: 20px;
        color: white !important;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3);
    }

    .stButton>button {
        width: 100%;
        height: 55px;
        border-radius: 15px;
        background: #7c3aed;
        color: white !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    
    .stButton>button:hover {
        background: #6d28d9;
        transform: scale(1.02);
    }

    /* تحسين شكل تبويبات الجوال */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 15px;
        border-radius: 10px;
    }
    </style>
    
    <div class="mobile-header">
        <h2 style='color: white; margin:0;'>🎓 مساعد رشا القدسي</h2>
        <p style='color: white; margin:5px 0 0 0; font-size:14px; opacity:0.9;'>شريكك الذكي في النجاح الأكاديمي</p>
    </div>
    """, unsafe_allow_html=True)

# 3. الربط مع Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def extract_pdf_text(files):
    text = ""
    for file in files:
        try:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        except: pass
    return text

# 4. واجهة المستخدم
st.markdown("### 📂 ارفع الملفات التعليمية")
lectures = st.file_uploader("اختر ملفات PDF للمحاضرات", type="pdf", accept_multiple_files=True)

if lectures:
    lecture_text = extract_pdf_text(lectures)
    tab1, tab2 = st.tabs(["📝 بناء اختبار", "💬 اسأل رشا"])

    with tab1:
        lang = st.radio("اللغة المطلوبة", ["العربية", "English"], horizontal=True)
        num_q = st.slider("كم سؤالاً تريد؟", 5, 40, 10)
        
        if st.button("توليد الأسئلة الآن ✨"):
            with st.spinner("جاري صياغة الأسئلة..."):
                prompt = f"Create {num_q} questions in {lang} from this content: {lecture_text[:15000]}. Show correct answers at the very end."
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.info(response.choices[0].message.content)

    with tab2:
        user_q = st.text_input("اطرح سؤالك حول المحاضرة:")
        if st.button("إرسال السؤال 🚀"):
            if user_q:
                with st.spinner("جاري البحث عن الإجابة..."):
                    prompt = f"Using this content: {lecture_text[:15000]}, Answer: {user_q}. Reply in Arabic."
                    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                    st.success(response.choices[0].message.content)

else:
    st.markdown("""
        <div style='text-align:center; padding: 40px 20px; color: gray;'>
            👋 مرحباً بك! يرجى رفع الملازم للبدء في توليد الاختبارات أو الدردشة مع المحتوى.
        </div>
    """, unsafe_allow_html=True)

# تذييل الصفحة
st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:11px;'>مساعد رشا القدسي الذكي • 2026</p>", unsafe_allow_html=True)
