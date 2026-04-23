import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة والجماليات
st.set_page_config(page_title="المساعد الأكاديمي الذكي", page_icon="🎓", layout="wide")

# تحسين الواجهة باستخدام CSS
st.markdown("""
    <style>
    /* تحسين الخلفية والخطوط */
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 10px 10px 0px 0px;
        gap: 1px;
        padding-top: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #007bff; color: white !important; }
    
    /* تنسيق الصناديق والأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background-image: linear-gradient(to right, #007bff, #00d4ff);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(0,123,255,0.3); }
    
    /* تنسيق قسم النتائج */
    .result-box {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border-right: 5px solid #007bff;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# مفتاح API الخاص بك (Groq)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# دالة استخراج النص
def extract_text(files):
    text = ""
    for file in files:
        try:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        except: pass
    return text

# --- واجهة المستخدم ---
st.title("🚀 المساعد الأكاديمي الذكي")
st.markdown("قم برفع ملفاتك وسأقوم بتجهيز كل ما تحتاجه للمذاكرة")

# قسم الرفع الرئيسي
with st.container():
    st.subheader("📁 خطوة 1: رفع المحتوى")
    lecture_files = st.file_uploader("ارفع المحاضرات أو الملازم (PDF)", type="pdf", accept_multiple_files=True)

if lecture_files:
    lecture_content = extract_text(lecture_files)
    
    # تبويبات العمليات
    tab1, tab2 = st.tabs(["📝 إنشاء اختبار شامل", "💬 دردشة مع المحاضرة"])

    # --- التبويب الأول: توليد الاختبارات ---
    with tab1:
        with st.expander("🛠️ إعدادات الاختبار المتقدمة", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                lang = st.radio("لغة الأسئلة", ["العربية", "English"], horizontal=True)
                diff = st.select_slider("مستوى الصعوبة", options=["سهل", "متوسط", "صعب", "تحدي"])
            with col2:
                num_q = st.number_input("عدد الأسئلة", min_value=1, max_value=50, value=10)
                types = st.multiselect("أنواع الأسئلة", ["MCQ", "صح وخطأ", "مقالي", "أكمل الفراغ"], default=["MCQ"])
            with col3:
                old_exams = st.file_uploader("محاكاة نمط قديم (اختياري)", type="pdf", accept_multiple_files=True)

        if st.button("توليد الأسئلة الآن ✨"):
            with st.spinner("جاري صياغة الأسئلة بدقة عالية..."):
                style = extract_text(old_exams) if old_exams else "Professional academic style"
                prompt = f"""
                Create an exam in {lang} language.
                - Source Content: {lecture_content[:15000]}
                - Style Reference (Optional): {style[:3000]}
                - Parameters: {num_q} questions, Difficulty: {diff}, Types: {types}.
                - Important: Provide the correct answers at the end.
                - Format: Clear and organized.
                """
                
                resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown("### 📋 النسخة المقترحة للاختبار")
                st.markdown(f'<div class="result-box">{resp.choices[0].message.content}</div>', unsafe_allow_html=True)
                st.download_button("📥 تحميل الأسئلة", resp.choices[0].message.content, file_name="Exam.txt")

    # --- التبويب الثاني: الدردشة ---
    with tab2:
        st.subheader("💬 اسأل ذكاءك الاصطناعي")
        chat_lang = st.selectbox("لغة الإجابة", ["نفس لغة السؤال", "العربية دائماً", "English Always"])
        user_input = st.text_input("ماذا تريد أن تعرف من هذه الملازم؟")
        
        if st.button("بحث وإجابة 🔍"):
            if user_input:
                with st.spinner("جاري استخراج المعلومة..."):
                    chat_prompt = f"Answer the following question based ONLY on this content: {lecture_content[:20000]}. Question: {user_input}. Respond in {chat_lang}."
                    resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": chat_prompt}])
                    st.markdown("#### الإجابة المستخرجة:")
                    st.info(resp.choices[0].message.content)

else:
    st.warning("⚠️ يرجى رفع ملفات المحاضرات لتفعيل أدوات الذكاء الاصطناعي.")
