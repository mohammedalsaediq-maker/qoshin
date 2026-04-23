import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد رشا القدسي",
    page_icon="🎓",
    layout="centered"
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
    }
    
    /* تنسيق خاص لصناديق الرفع لتكون بارزة */
    .upload-box {
        border: 1px solid #7c3aed;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
    }
    </style>
    
    <div class="mobile-header">
        <h2 style='color: white; margin:0;'>🎓 مساعد رشا القدسي</h2>
        <p style='color: white; margin:5px 0 0 0; font-size:14px; opacity:0.9;'>نظام توليد الاختبارات والدردشة الذكي</p>
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

# 4. واجهة الرفع الرئيسية (جعلناها واضحة جداً هنا)
st.markdown("### 📚 الخطوة 1: ارفع ملفاتك")
lectures = st.file_uploader("1️⃣ ارفع المحاضرات والملازم (إلزامي)", type="pdf", accept_multiple_files=True)
patterns = st.file_uploader("2️⃣ ارفع نماذج اختبارات سابقة (اختياري لمحاكاة النمط)", type="pdf", accept_multiple_files=True)

if lectures:
    lecture_text = extract_pdf_text(lectures)
    pattern_text = extract_pdf_text(patterns) if patterns else ""
    
    st.markdown("---")
    tab1, tab2 = st.tabs(["📝 بناء اختبار", "💬 اسأل رشا"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            lang = st.radio("اللغة", ["العربية", "English"], horizontal=True)
        with col2:
            num_q = st.number_input("عدد الأسئلة", 5, 50, 10)
        
        diff = st.select_slider("مستوى الصعوبة", options=["سهل", "متوسط", "صعب"])
        
        if st.button("توليد الأسئلة الآن ✨"):
            with st.spinner("جاري تحليل المحتوى والنمط..."):
                prompt = f"""
                Create {num_q} questions in {lang}. 
                Difficulty: {diff}. 
                Source Content: {lecture_text[:15000]}. 
                Style to Mimic (if exists): {pattern_text[:4000]}. 
                Provide correct answers at the end.
                """
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.info(response.choices[0].message.content)

    with tab2:
        user_q = st.text_input("اسأل رشا أي شيء عن المنهج:")
        if st.button("إرسال السؤال 🚀"):
            with st.spinner("جاري استخراج الإجابة..."):
                prompt = f"Using: {lecture_text[:15000]}, Answer: {user_q} in Arabic."
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.success(response.choices[0].message.content)
else:
    st.info("👋 يرجى رفع ملفات المحاضرات أولاً لتفعيل أدوات الذكاء الاصطناعي.")
