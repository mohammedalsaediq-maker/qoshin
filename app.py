import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة - محسنة للجوال
st.set_page_config(
    page_title="مساعدي الأكاديمي",
    page_icon="🎓",
    layout="centered", # مناسب أكثر لشاشات الجوال
    initial_sidebar_state="collapsed" # إخفاء القائمة الجانبية تلقائياً لتوفير مساحة
)

# 2. تصميم CSS احترافي للجوال
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    
    /* خلفية مريحة للعين */
    .stApp { background-color: #f9f9fb; }
    
    /* تصميم الهيدر بشكل مبسط للجوال */
    .mobile-header {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        color: white;
        text-align: center;
        margin: -60px -20px 20px -20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* تكبير الأزرار لتسهيل اللمس */
    .stButton>button {
        width: 100%;
        height: 55px;
        border-radius: 15px;
        background: #2563eb;
        color: white;
        font-size: 18px !important;
        font-weight: bold;
        border: none;
        margin-top: 10px;
    }
    
    /* تحسين شكل صناديق الرفع */
    .stFileUploader {
        border: 2px dashed #cbd5e1;
        border-radius: 15px;
        padding: 10px;
        background: white;
    }

    /* تبسيط التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 15px;
        background: #eee;
        border-radius: 10px;
        font-size: 14px;
    }
    </style>
    
    <div class="mobile-header">
        <h2 style='margin:0;'>🎓 المساعد الأكاديمي</h2>
        <p style='margin:5px 0 0 0; font-size:14px; opacity:0.9;'>صناعة اختبارات ودردشة ذكية</p>
    </div>
    """, unsafe_allow_html=True)

# 3. الربط مع Groq
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def extract_pdf_text(files):
    text = ""
    for file in files:
        pdf = PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# 4. واجهة رفع الملفات
st.markdown("### 📂 ارفع محاضراتك")
lectures = st.file_uploader("اختر ملفات الـ PDF", type="pdf", accept_multiple_files=True)

if lectures:
    lecture_text = extract_pdf_text(lectures)
    
    tab1, tab2 = st.tabs(["📝 إنشاء اختبار", "💬 اسأل سؤالاً"])

    # --- التبويب الأول: الاختبار ---
    with tab1:
        st.write("---")
        lang = st.selectbox("لغة الاختبار", ["العربية", "English"])
        
        with st.expander("⚙️ خيارات إضافية"):
            num_q = st.select_slider("عدد الأسئلة", options=[5, 10, 15, 20, 30])
            diff = st.select_slider("المستوى", options=["سهل", "متوسط", "صعب"])
            q_types = st.multiselect("الأنواع", ["MCQ", "صح وخطأ", "مقالي"], default=["MCQ"])
            patterns = st.file_uploader("نماذج سابقة (اختياري)", type="pdf", accept_multiple_files=True)

        if st.button("توليد الاختبار ✨"):
            with st.spinner("جاري التوليد..."):
                style = extract_pdf_text(patterns) if patterns else "Standard"
                prompt = f"Create {num_q} questions in {lang}. Difficulty: {diff}. Types: {q_types}. Content: {lecture_text[:15000]}. Style Reference: {style[:2000]}. Provide answers."
                
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown("### 📋 النتيجة:")
                st.markdown(response.choices[0].message.content)
                st.download_button("📥 حفظ النتيجة", response.choices[0].message.content, "Exam.txt")

    # --- التبويب الثاني: الدردشة ---
    with tab2:
        st.write("---")
        user_q = st.text_input("اسأل أي شيء عن المحاضرة:")
        if st.button("إرسال السؤال 🚀"):
            if user_q:
                with st.spinner("جاري البحث..."):
                    prompt = f"Using this content: {lecture_text[:15000]}, Answer this question: {user_q}. Respond in Arabic if not specified."
                    response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                    st.info(response.choices[0].message.content)

else:
    st.info("💡 ارفع ملفات الـ PDF لتبدأ الاستخدام.")

# تذييل الصفحة
st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:12px;'>بصمة غرناطة - الحلول الذكية 2026</p>", unsafe_allow_html=True)
