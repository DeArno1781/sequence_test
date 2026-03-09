import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ==========================================
# 1. Number Series Logic (จากเวอร์ชันเดิม)
# ==========================================
def gen_number_series(level):
    if level == "ง่าย (Easy)":
        start = random.randint(5, 50)
        step = random.choice([-8, -7, -6, 6, 7, 8, 9, 12, 15])
        seq = [start + (step * i) for i in range(6)]
        answer = seq.pop()
        logic = f"ขยับทีละ {step}"
        return seq, answer, logic
    elif level == "ปานกลาง (Medium)":
        start1 = random.randint(10, 50)
        step1 = random.choice([-5, -4, 4, 5, 6])
        start2 = random.randint(10, 50)
        step2 = random.choice([-3, -2, 2, 3])
        seq = []
        for i in range(4):
            seq.append(start1 + (step1 * i))
            seq.append(start2 + (step2 * i))
        answer = seq.pop()
        logic = f"อนุกรมซ้อน 2 ชุด (สลับฟันปลา): ชุดคี่ขยับ {step1}, ชุดคู่ขยับ {step2}"
        return seq, answer, logic
    else:
        start = random.randint(2, 10)
        mul = random.randint(2, 4)
        sub = random.randint(1, 5)
        seq = [start]
        current = start
        for i in range(6):
            current = current * mul if i % 2 == 0 else current - sub
            seq.append(current)
        answer = seq.pop()
        logic = f"สลับเครื่องหมาย: คูณ {mul} สลับกับ ลบ {sub}"
        return seq, answer, logic

def get_new_ns_question():
    seq, ans, logic = gen_number_series(st.session_state.ns_difficulty)
    st.session_state.ns_sequence = seq
    st.session_state.ns_answer = ans
    st.session_state.ns_logic = logic
    st.session_state.ns_show_answer = False
    st.session_state.ns_feedback = None
    st.session_state.timer_id = str(time.time())

# ==========================================
# 2. Symbol Addition Logic (หมวดใหม่)
# ==========================================
SYMBOLS = ['♒', '😃', '✌', '♌', '✈', '⌘', '◆', '💀', '⬤']

def init_symbol_test():
    # สุ่มค่าให้สัญลักษณ์ใหม่ทุกรอบ
    st.session_state.sym_map = {sym: random.randint(3, 25) for sym in SYMBOLS}
    # สุ่มโจทย์มา 10 ตัว
    st.session_state.sym_seq = [random.choice(SYMBOLS) for _ in range(10)]
    st.session_state.sym_submitted = False
    st.session_state.timer_id = str(time.time())

# ==========================================
# Main App Setup
# ==========================================
st.set_page_config(page_title="Aptitude Test Gym", layout="wide")

# Sidebar Menu
with st.sidebar:
    st.title("🎯 เลือกโหมดฝึกซ้อม")
    app_mode = st.radio(
        "โหมดการทดสอบ:",
        ["🔢 Number Series", "🔣 Symbol Addition (ใหม่)"]
    )
    st.divider()
    st.caption("พัฒนาด้วย Streamlit")

# ==========================================
# MODE 1: Number Series (อนุกรม)
# ==========================================
if app_mode == "🔢 Number Series":
    if 'ns_difficulty' not in st.session_state:
        st.session_state.ns_difficulty = "ยาก (Hard)"
        get_new_ns_question()

    st.title("🧠 Number Series Gym")
    
    col_diff, col_timer = st.columns([2, 1])
    with col_diff:
        new_diff = st.radio("เลือกระดับความยาก:", ["ง่าย (Easy)", "ปานกลาง (Medium)", "ยาก (Hard)"], horizontal=True)
        if new_diff != st.session_state.ns_difficulty:
            st.session_state.ns_difficulty = new_diff
            get_new_ns_question()
            st.rerun()
    with col_timer:
        use_timer = st.toggle("⏱️ เปิดจับเวลา 30 วิ", value=True)

    st.divider()
    seq_str = ", ".join(map(str, st.session_state.ns_sequence))
    st.header(f"Sequence: {seq_str}, ?")

    if use_timer:
        timer_html = f"""
        <div id="t_{st.session_state.timer_id}" style="font-size: 2rem; font-family: monospace; font-weight: bold; color: #1f77b4;">30 วินาที</div>
        <script>
            (function() {{
                var t = 30, e = document.getElementById("t_{st.session_state.timer_id}");
                var id = setInterval(function() {{
                    t--; if(t<=0) {{ clearInterval(id); e.innerHTML="⏰ หมดเวลา!"; e.style.color="red"; }}
                    else {{ e.innerHTML=t+" วินาที"; if(t<=5) e.style.color="orange"; }}
                }}, 1000);
            }})();
        </script>
        """
        components.html(timer_html, height=50)

    with st.form(key='ns_form', clear_on_submit=True):
        guess = st.text_input("คำตอบ:", placeholder="พิมพ์ตัวเลขแล้วกด Enter...")
        if st.form_submit_button('ส่งคำตอบ ⏎'):
            try:
                if int(guess) == st.session_state.ns_answer:
                    st.session_state.ns_feedback = "correct"
                else:
                    st.session_state.ns_feedback = "incorrect"
            except:
                st.error("ใส่เฉพาะตัวเลขครับ")

    if st.session_state.ns_feedback == "correct":
        st.success("✅ ถูกต้อง!")
        if st.button("ข้อต่อไป", type="primary"):
            get_new_ns_question()
            st.rerun()
    elif st.session_state.ns_feedback == "incorrect":
        st.error("❌ ยังไม่ถูก")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 ข้ามข้อนี้"): get_new_ns_question(); st.rerun()
    with col2:
        if st.button("💡 ดูเฉลย"): st.session_state.ns_show_answer = True
    
    if st.session_state.ns_show_answer:
        st.info(f"**ตอบ: {st.session_state.ns_answer}** | {st.session_state.ns_logic}")


# ==========================================
# MODE 2: Symbol Addition (บวกเลขต่อเนื่อง)
# ==========================================
elif app_mode == "🔣 Symbol Addition (ใหม่)":
    if 'sym_seq' not in st.session_state:
        init_symbol_test()

    st.title("🔣 Continuous Addition (ถอดรหัสบวกเลข)")
    st.write("จำค่าสัญลักษณ์ด้านบน แล้วนำมา **บวกทบยอด** ลงมาเรื่อยๆ ทีละบรรทัด")
    
    # 1. แสดงตารางอ้างอิงสัญลักษณ์ (Legend) แบบจัดเรียงสวยงาม
    st.markdown("### 🔑 ค่าสัญลักษณ์ (เปลี่ยนใหม่ทุกรอบ)")
    cols = st.columns(len(SYMBOLS))
    for i, sym in enumerate(SYMBOLS):
        with cols[i]:
            st.markdown(f"<div style='text-align:center; font-size:24px;'>{sym}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center; font-size:18px; font-weight:bold;'>{st.session_state.sym_map[sym]}</div>", unsafe_allow_html=True)
    
    st.divider()

    col_q, col_timer = st.columns([2, 1])
    with col_timer:
        st.button("🔄 สุ่มโจทย์ใหม่", on_click=init_symbol_test, type="primary", use_container_width=True)
        timer_html = f"""
        <div id="t_sym_{st.session_state.timer_id}" style="font-size: 2.5rem; text-align:center; font-family: monospace; font-weight: bold; color: #1f77b4; margin-top: 20px;">45 วินาที</div>
        <script>
            (function() {{
                var t = 45, e = document.getElementById("t_sym_{st.session_state.timer_id}");
                var id = setInterval(function() {{
                    t--; if(t<=0) {{ clearInterval(id); e.innerHTML="⏰ หมดเวลา!"; e.style.color="red"; }}
                    else {{ e.innerHTML=t+" วินาที"; if(t<=10) e.style.color="orange"; }}
                }}, 1000);
            }})();
        </script>
        """
        # จับเวลา 45 วิ สำหรับหมวดนี้เพราะต้องพิมพ์หลายช่อง
        components.html(timer_html, height=100)

    with col_q:
        # 2. สร้างฟอร์มสำหรับเติมคำตอบ (ป้องกันเว็บ Refresh ระหว่างพิมพ์)
        with st.form("symbol_addition_form"):
            st.write("พิมพ์ยอดรวมสะสมลงในช่องว่าง (กด Tab เพื่อเลื่อนช่องถัดไป)")
            
            user_inputs = []
            # สร้างแถวสัญลักษณ์ พร้อมช่องกรอก
            for i, sym in enumerate(st.session_state.sym_seq):
                row_col1, row_col2 = st.columns([1, 4])
                with row_col1:
                    st.markdown(f"<div style='font-size:30px; text-align:right;'>{sym}</div>", unsafe_allow_html=True)
                with row_col2:
                    ans = st.text_input("ยอดรวม", key=f"sym_ans_{i}", label_visibility="collapsed")
                    user_inputs.append(ans)
            
            submitted = st.form_submit_button("ส่งคำตอบเพื่อตรวจ ⏎", use_container_width=True)

            if submitted:
                st.session_state.sym_submitted = True
                st.session_state.user_inputs = user_inputs

    # 3. ตรวจคำตอบหลังจากกด Submit
    if st.session_state.sym_submitted:
        st.header("📊 ตรวจคำตอบ")
        correct_running_sum = 0
        all_correct = True
        
        # สร้างตารางเฉลย
        res_cols = st.columns([1, 2, 2, 2])
        res_cols[0].write("**สัญลักษณ์**")
        res_cols[1].write("**ค่าของมัน**")
        res_cols[2].write("**คำตอบที่คุณตอบ**")
        res_cols[3].write("**ยอดรวมที่ถูกต้อง**")

        for i, sym in enumerate(st.session_state.sym_seq):
            val = st.session_state.sym_map[sym]
            correct_running_sum += val
            
            user_ans = st.session_state.user_inputs[i]
            user_val = int(user_ans) if user_ans.isdigit() else None
            
            is_correct = (user_val == correct_running_sum)
            if not is_correct: all_correct = False
            
            icon = "✅" if is_correct else "❌"
            
            r1, r2, r3, r4 = st.columns([1, 2, 2, 2])
            r1.write(f"### {sym}")
            r2.write(f"+ {val}")
            
            if is_correct:
                r3.success(f"{user_ans} {icon}")
            else:
                r3.error(f"{user_ans if user_ans else '-'} {icon}")
                
            r4.info(str(correct_running_sum))
            
        if all_correct:
            st.balloons()
            st.success("🎉 ถูกต้องทุกข้อ! สมาธิและความจำคุณนิ่งมากครับ")
        else:
            st.warning("มีจุดบวกพลาด ลองไล่ดูตรงเฉลยนะครับว่าเริ่มหลุดที่บรรทัดไหน")
