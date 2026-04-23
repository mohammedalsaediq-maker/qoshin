import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="مساعد رشا القدسي",
    page_icon="🎓",
    layout="centered"
)

# 2. تصميم CSS محسن (يدعم الوضع المظلم والفاتح)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    * { font-family: 'Cairo', sans-serif; direction: rtl; }
    html, body, [data-testid="stMarkdownContainer"] p { color: var(--text-color); }
    .mobile-header {
        background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
        padding: 25px 15px;
        border-radius: 20px;
        color: white !important;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3);
    }
    .stButton>button {
        width: 100%;
        height: 50px;
        border-radius: 12px;
        background: #7c3aed;
        color: white !important;
        font-weight: bold;
        border: none;
    }
    </style>
    <div class="mobile-header">
        <h2 style='color: white; margin:0;'>🎓 مساعد رشا القدسي</h2>
        <p style='color: white; margin:5px 0 0 0; font-size:13px; opacity:0.9;'>نظام الاختبارات الذكي - نسخة الجوال</p>
    </div>
    """, unsafe_allow_html=True)

# 3. الربط مع Groq (تأكد من صحة المفتاح)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def extract_pdf_text(files):
    text = ""
    for file in files:
        try:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            st.error(f"خطأ في قراءة ملف: {file.name}")
    return text

# 4. واجهة المستخدم
st.markdown("### 📚 ارفع محاضراتك")
lectures = st.file_uploader("ارفع الملازم (PDF)", type="pdf", accept_multiple_files=True)

show_patterns = st.checkbox("🔄 هل تريد محاكاة نمط اختبار سابق؟ (اختياري)")
pattern_text = ""
if show_patterns:
    patterns = st.file_uploader("ارفع النماذج السابقة هنا", type="pdf", accept_multiple_files=True)
    if patterns:
        pattern_text = extract_pdf_text(patterns)

if lectures:
    lecture_text = extract_pdf_text(lectures)
    
    st.markdown("---")
    tab1, tab2 = st.tabs(["📝 بناء اختبار", "💬 اسأل رشا"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            lang = st.radio("اللغة", ["العربية", "English"], horizontal=True)
        with col2:
            num_q = st.number_input("عدد الأسئلة", 5, 50, 10)
        
        diff = st.select_slider("مستوى الصعوبة", options=["سهل", "متوسط", "صعب"])
        
        if st.button("توليد الأسئلة ✨"):
            with st.spinner("جاري التحليل والتوليد..."):
                try:
                    # تقليص النص لضمان عدم تجاوز حدود الـ API
                    safe_lecture_text = lecture_text[:12000] 
                    safe_pattern_text = pattern_text[:3000]

                    prompt = f"""
                    أنت مساعد أكاديمي خبير. قم بإنشاء اختبار من {num_q} سؤال باللغة {lang}.
                    المستوى: {diff}. 
                    المحتوى: {safe_lecture_text}. 
                    النمط المطلوب: {safe_pattern_text}.
                    ضع الإجابات في النهاية.
                    """
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile", 
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.5 # تقليل الحرارة لنتائج أكثر دقة وأقل أخطاء
                    )
                    st.info(response.choices[0].message.content)
                except Exception as e:
                    st.error("⚠️ حدث خطأ في الاتصال بـ API. قد يكون السبب ضغط على السيرفر أو نص طويل جداً. حاول مرة أخرى بعد قليل أو ارفع ملفات أصغر.")

    with tab2:
        user_q = st.text_input("اسأل رشا أي شيء عن المنهج:")
        if st.button("إرسال السؤال 🚀"):
            if user_q:
                with st.spinner("جاري استخراج الإجابة..."):
                    try:
                        prompt = f"Using this content: {lecture_text[:15000]}, Answer: {user_q} in Arabic."
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile", 
                            messages=[{"role": "user", "content": prompt}]
                        )
                        st.success(response.choices[0].message.content)
                    except:
                        st.error("عذراً، لم أتمكن من الرد حالياً. حاول صياغة السؤال بشكل أقصر.")
else:
    st.info("👋 يرجى رفع ملفات المحاضرات أولاً للبدء.")

st.markdown("<br><p style='text-align:center; color:#94a3b8; font-size:11px;'>مساعد رشا القدسي • 2026</p>", unsafe_allow_html=True)
