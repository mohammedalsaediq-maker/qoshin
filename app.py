import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# إعدادات الصفحة
st.set_page_config(page_title="المعد الذكي للاختبارات", page_icon="🎓", layout="centered")

# التنسيق البصري (CSS)
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; height: 3em; }
    .stSelectbox, .stSlider { margin-bottom: 20px; }
    </style>
    """, unsafe_index=True)

st.title("🎓 صانع الاختبارات الذكي")
st.write("خصص اختبارك بناءً على محاضراتك بضغطة زر.")

# مفتاح API الخاص بك (Groq)
GROQ_API_KEY = "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"

# دالة استخراج النص من الـ PDF
def extract_text(files):
    text = ""
    for file in files:
        pdf = PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# --- القائمة الجانبية للإعدادات ---
st.sidebar.header("⚙️ إعدادات الاختبار")
num_questions = st.sidebar.slider("عدد الأسئلة المطلوبة", 5, 50, 10)
difficulty = st.sidebar.selectbox("مستوى الصعوبة", ["سهل", "متوسط", "صعب", "تحدي (للمتميزين)"])
q_types = st.sidebar.multiselect(
    "أنواع الأسئلة", 
    ["اختيار من متعدد (MCQ)", "صح وخطأ", "أسئلة مقالية قصيرة", "أكمل الفراغ"],
    default=["اختيار من متعدد (MCQ)", "صح وخطأ"]
)

# --- واجهة رفع الملفات ---
st.subheader("1️⃣ ارفع المحاضرات (إلزامي)")
lecture_files = st.file_uploader("ارفع الملازم أو المحاضرات هنا", type="pdf", accept_multiple_files=True)

st.subheader("2️⃣ ارفع نماذج سابقة (اختياري)")
old_exam_files = st.file_uploader("ارفع نماذج سابقة لمحاكاة النمط", type="pdf", accept_multiple_files=True)

# --- زر التنفيذ ---
if st.button("توليد الاختبار الآن ✨"):
    if not lecture_files:
        st.error("الرجاء رفع ملفات المحاضرات أولاً!")
    elif not q_types:
        st.error("الرجاء اختيار نوع واحد على الأقل من الأسئلة.")
    else:
        with st.spinner("جاري صياغة الأسئلة بدقة..."):
            try:
                client = Groq(api_key=GROQ_API_KEY)
                
                # استخراج نصوص الملفات
                lecture_text = extract_text(lecture_files)
                exam_style_text = extract_text(old_exam_files) if old_exam_files else "لا يوجد نموذج سابق، استخدم أسلوبك الاحترافي."

                # بناء "الأمر" (Prompt)
                types_str = "، ".join(q_types)
                prompt = f"""
                أنت أستاذ جامعي خبير. قم بإعداد اختبار بناءً على المعايير التالية:
                1. المادة العلمية: {lecture_text[:15000]}
                2. نمط المحاكاة (اختياري): {exam_style_text[:4000]}
                
                المطلوب:
                - عدد الأسئلة: {num_questions} سؤال.
                - مستوى الصعوبة: {difficulty}.
                - أنواع الأسئلة المطلوبة: {types_str}.
                
                تعليمات إضافية:
                - إذا وجد نمط محاكاة، التزم بأسلوب الصياغة فيه.
                - إذا لم يوجد نمط، قم بتنويع الأسئلة بشكل احترافي.
                - اجعل اللغة عربية فصحى وسليمة.
                - ضع الإجابات النموذجية في قسم منفصل في نهاية الصفحة.
                """

                # إرسال الطلب لـ Groq
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.6,
                )

                # عرض النتيجة
                st.success("تم تجهيز الاختبار!")
                st.markdown("---")
                st.markdown(completion.choices[0].message.content)
                
                # زر التحميل
                st.download_button("تحميل الاختبار كملف نصي", completion.choices[0].message.content, file_name="my_exam.txt")

            except Exception as e:
                st.error(f"حدث خطأ تقني: {e}")
