import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# وضع المفتاح الخاص بك الذي أرسلته
GROQ_API_KEY = "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"

st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("📝 مولد الاختبارات الذكي")
st.info("ارفع ملفاتك وسأقوم بصناعة أسئلة مطابقة للنمط تماماً.")

# وظيفة استخراج النص
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

col1, col2 = st.columns(2)
with col1:
    exam_pdf = st.file_uploader("📂 نماذج قديمة (النمط)", type="pdf", accept_multiple_files=True)
with col2:
    lecture_pdf = st.file_uploader("📚 الملازم/المحاضرات", type="pdf", accept_multiple_files=True)

if st.button("ابدأ إنشاء الأسئلة"):
    if exam_pdf and lecture_pdf:
        with st.spinner("جاري المعالجة بسرعة Groq الخارقة..."):
            client = Groq(api_key=GROQ_API_KEY)
            
            exams_text = get_pdf_text(exam_pdf)
            lectures_text = get_pdf_text(lecture_pdf)
            
            prompt = f"""
            حلل نمط الأسئلة من هذا النص (نماذج قديمة): {exams_text[:4000]}
            بناءً على هذا النمط، أنشئ أسئلة جديدة من المحتوى التالي (المحاضرة): {lectures_text[:12000]}
            اجعل الأسئلة باللغة العربية واكتب الإجابات في النهاية.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            
            st.markdown("### 📄 الأسئلة المقترحة:")
            st.write(chat_completion.choices[0].message.content)
    else:
        st.error("يرجى رفع الملفات أولاً!")