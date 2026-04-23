import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# إعدادات الصفحة
st.set_page_config(page_title="المعد الذكي والدردشة الأكاديمية", page_icon="📝", layout="wide")

# تنسيق CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; }
    .chat-box { padding: 20px; border-radius: 15px; background-color: #f0f2f6; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# مفتاح API الخاص بك
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

def extract_text(files):
    text = ""
    for file in files:
        try:
            pdf = PdfReader(file)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        except:
            pass
    return text

# --- واجهة رفع الملفات (عامة لكل التطبيق) ---
st.title("🎓 مساعدك الأكاديمي الشامل")
lecture_files = st.file_uploader("📂 ارفع المحاضرات أو الملازم أولاً (PDF)", type="pdf", accept_multiple_files=True)

if lecture_files:
    lecture_content = extract_text(lecture_files)
    
    # إنشاء تبويبين: واحد للاختبارات وواحد للدردشة
    tab1, tab2 = st.tabs(["✨ توليد اختبار كامل", "💬 اسأل عن معلومة محددة"])

    # --- التبويب الأول: توليد الاختبارات ---
    with tab1:
        st.subheader("إعدادات الاختبار")
        col1, col2 = st.columns(2)
        with col1:
            num_q = st.slider("عدد الأسئلة", 5, 50, 10)
            diff = st.selectbox("المستوى", ["سهل", "متوسط", "صعب"])
        with col2:
            types = st.multiselect("الأنواع", ["اختيار من متعدد", "صح وخطأ", "مقالي"], default=["اختيار من متعدد"])
            old_exams = st.file_uploader("ارفع نمط سابق (اختياري)", type="pdf", accept_multiple_files=True, key="old_ex")

        if st.button("توليد الاختبار ✨"):
            with st.spinner("جاري التوليد..."):
                style = extract_text(old_exams) if old_exams else "أسلوب أكاديمي قياسي"
                prompt = f"استخرج {num_q} سؤال {diff} من النوع {types} بناءً على هذه المحاضرة: {lecture_content[:15000]}. التزم بهذا النمط إذا وجد: {style[:3000]}. ضع الإجابات في النهاية."
                
                resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}])
                st.markdown("---")
                st.markdown(resp.choices[0].message.content)

    # --- التبويب الثاني: اسأل سؤالاً نصياً ---
    with tab2:
        st.subheader("اسأل ذكاء اصطناعي عن محتوى محاضراتك")
        user_question = st.text_input("اكتب سؤالك هنا (مثلاً: ما هي أهم النقاط في الفصل الثاني؟)")
        
        if st.button("إرسال السؤال 🚀"):
            if user_question:
                with st.spinner("جاري البحث في المحاضرات..."):
                    chat_prompt = f"""
                    أجب على السؤال التالي بناءً فقط على محتوى المحاضرات المرفق.
                    إذا لم تجد الإجابة، أخبر المستخدم أنها غير موجودة في الملازم.
                    
                    المحاضرات: {lecture_content[:20000]}
                    السؤال: {user_question}
                    """
                    resp = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": chat_prompt}])
                    st.markdown("#### الإجابة:")
                    st.success(resp.choices[0].message.content)
            else:
                st.warning("يرجى كتابة سؤال.")

else:
    st.info("👋 مرحباً! يرجى رفع ملفات المحاضرات (PDF) للبدء في توليد الأسئلة أو الدردشة معها.")
