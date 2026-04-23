import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="المساعد الأكاديمي الذكي", page_icon="🎓", layout="wide")

# 2. تصميم الواجهة بأسلوب HTML & CSS احترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main { background-color: #f0f2f5; }
    
    /* الهيدر الاحترافي */
    .header-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* بطاقات الأقسام */
    .stCard {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* تحسين الأزرار */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(to right, #00b09b, #96c93d);
        color: white;
        font-weight: bold;
        border: none;
        padding: 15px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    </style>
    
    <div class="header-container">
        <h1>🎓 منصة الاختبارات والدردشة الذكية</h1>
        <p>بناء الأسئلة والمذاكرة التفاعلية باستخدام ذكاء Groq الخارق</p>
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

# 4. هيكل الصفحة الجانبي (Side Panel)
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
st.sidebar.title("⚙️ الإعدادات")
app_mode = st.sidebar.selectbox("اختر الخدمة", ["📝 إنشاء اختبار", "💬 دردشة مع الملازم"])
lang_opt = st.sidebar.radio("لغة المخرجات", ["العربية", "English"])

# 5. منطقة رفع الملفات
st.markdown('<div class="stCard">', unsafe_allow_html=True)
lectures = st.file_uploader("📂 أولاً: ارفع المحاضرات والملازم (PDF)", type="pdf", accept_multiple_files=True)
st.markdown('</div>', unsafe_allow_html=True)

if lectures:
    text_content = extract_pdf_text(lectures)
    
    if app_mode == "📝 إنشاء اختبار":
        col1, col2, col3 = st.columns(3)
        with col1:
            num_q = st.number_input("عدد الأسئلة", 5, 50, 10)
        with col2:
            diff = st.selectbox("المستوى", ["سهل", "متوسط", "صعب"])
        with col3:
            q_type = st.multiselect("الأنواع", ["MCQ", "صح وخطأ", "مقالي"], default=["MCQ"])
            
        patterns = st.file_uploader("ارفع نموذج سابق (اختياري)", type="pdf", accept_multiple_files=True)
        
        if st.button("صناعة الاختبار ✨"):
            with st.spinner("جاري التوليد..."):
                style_text = extract_pdf_text(patterns) if patterns else "Standard Academic"
                prompt = f"Create a {num_q} question exam in {lang_opt}. Content: {text_content[:15000]}. Style: {style_text[:3000]}. Difficulty: {diff}. Types: {q_type}. Show answers at the end."
                
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.success("تم التوليد!")
                st.markdown(f"```\n{response.choices[0].message.content}\n```")
                st.download_button("📥 تحميل كملف نصي", response.choices[0].message.content, "Exam.txt")

    elif app_mode == "💬 دردشة مع الملازم":
        st.info("اسأل أي سؤال وسأجيبك من واقع الملفات المرفقة.")
        user_query = st.text_input("اكتب سؤالك هنا...")
        if st.button("إرسال 🚀"):
            with st.spinner("جاري البحث..."):
                chat_prompt = f"Using this content: {text_content[:20000]}, Answer: {user_query}. Respond in {lang_opt}."
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": chat_prompt}])
                st.chat_message("assistant").write(response.choices[0].message.content)

else:
    st.info("💡 يرجى رفع ملفاتك في الأعلى لتبدأ العمل.")

st.markdown('---')
st.caption("تم التطوير بواسطة ذكاء اصطناعي لدعم مسيرتك الدراسية.")
