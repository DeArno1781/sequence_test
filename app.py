import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ==========================================
# 1. ฟังก์ชันตัวช่วยสร้าง HTML นาฬิกาจับเวลาพร้อมปุ่มควบคุม
# ==========================================
def render_timer(duration_sec, timer_id, auto_start=True):
    auto_js = "startTimer();" if auto_start else ""
    return f"""
    <div style="font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 10px; background: #f8f9fa; border-radius: 10px; border: 1px solid #e9ecef;">
        <div id="t_display" style="font-size: 2.5rem; font-weight: bold; color: #1f77b4; margin-bottom: 15px; font-family: monospace;">
            {duration_sec} วินาที
        </div>
        <div style="display: flex; gap: 10px;">
            <button onclick="startTimer()" style="padding: 8px 15px; border: none; border-radius: 5px; background: #28a745; color: white; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">▶ เริ่ม (Start)</button>
            <button onclick="pauseTimer()" style="padding: 8px 15px; border: none; border-radius: 5px; background: #dc3545; color: white; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">⏸ หยุด (Pause)</button>
            <button onclick="resetTimer()" style="padding: 8px 15px; border: none; border-radius: 5px; background: #6c757d; color: white; cursor: pointer; font-weight: bold; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">🔄 รีเซ็ต (Reset)</button>
        </div>
    </div>
    <script>
        var duration = {duration_sec};
        var timeLeft = duration;
        var timerId = null;
        var display = document.getElementById("t_display");

        function updateDisplay() {{
            if (timeLeft <= 0) {{
                display.innerHTML = "⏰ หมดเวลา!";
                display.style.color = "#dc3545"; // แดง
            }} else {{
                display.innerHTML = timeLeft + " วินาที";
                if (timeLeft <= 5) {{
                    display.style.color = "#ffc107"; // ส้ม
                }} else {{
                    display.style.color = "#1f77b4"; // ฟ้า
                }}
            }}
        }}

        function startTimer() {{
            if (timerId !== null) return; // ทำงานอยู่แล้ว
            if (timeLeft <= 0) return; // หมดเวลาไปแล้ว
            timerId = setInterval(function() {{
                timeLeft--;
                updateDisplay();
                if (timeLeft <= 0) clearInterval(timerId);
            }}, 1000);
        }}

        function pauseTimer() {{
            if (timerId !== null) {{
                clearInterval(timerId);
                timerId = null;
            }}
        }}

        function resetTimer() {{
            pauseTimer();
            timeLeft = duration;
            updateDisplay();
        }}

        // เริ่มอัตโนมัติเมื่อโหลดคอมโพเนนต์เสร็จ
        {auto_js}
    </script>
    """

# ==========================================
# 2. ฟังก์ชันสุ่มโจทย์ Number Series
# ==========================================
def gen_arithmetic():
    start = random.randint(5, 50)
    step = random.choice([-8, -7, -6, 6, 7, 8, 9, 12, 15])
    seq = [start + (step * i) for i in range(6)]
    ans = seq.pop()
    op = f"+ {step}" if step > 0 else f"- {abs(step)}"
    return seq, ans, f"อนุกรมพื้นฐาน: ขยับทีละ {op} เสมอ\nถัดไปคือ {seq[-1]} {op} = {ans}"

def gen_geometric():
    start = random.randint(2, 5)
    step = random.choice([2, 3, 4])
    seq = [start * (step ** i) for i in range(5)]
    ans = seq.pop()
    return seq, ans, f"อนุกรมคูณสะสม: คูณด้วย {step} เสมอ\nถัดไปคือ {seq[-1]} * {step} = {ans}"

def gen_interleaved():
    start1 = random.randint(10, 50)
    step1 = random.choice([-5, -4, 4, 5, 6])
    start2 = random.randint(10, 50)
    step2 = random.choice([-3, -2, 2, 3])
    seq = []
    for i in range(4):
        seq.append(start1 + (step1 * i))
        seq.append(start2 + (step2 * i))
    ans = seq.pop()
    return seq, ans, f"อนุกรมซ้อน 2 ชุด (สลับฟันปลา):\nชุดคี่ขยับ {step1}, ชุดคู่ขยับ {step2}\nถัดไปอยู่ชุดคู่: {ans - step2} + ({step2}) = {ans}"

def gen_exponential_basic():
    base = random.randint(2, 5)
    seq = [base ** i for i in range(1, 6)]
    ans = seq.pop()
    return seq, ans, f"เลขยกกำลังฐาน {base}:\nรูปแบบ {base}^1, {base}^2, {base}^3...\nถัดไปคือ {base}^5 = {ans}"

def gen_mixed_operations():
    start = random.randint(2, 10)
    mul = random.randint(2, 4)
    sub = random.randint(1, 5)
    seq = [start]
    current = start
    for i in range(6):
        current = current * mul if i % 2 == 0 else current - sub
        seq.append(current)
    ans = seq.pop()
    op_next = f"คูณ {mul}" if len(seq) % 2 == 0 else f"ลบ {sub}"
    return seq, ans, f"สลับเครื่องหมาย:\nรูปแบบ คูณ {mul} สลับกับ ลบ {sub}\nรอบถัดไปคือการ{op_next} -> {ans}"

def gen_prime_addition():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    start = random.randint(1, 15)
    idx = random.randint(0, 3)
    seq = [start]
    current = start
    for i in range(5):
        current += primes[idx + i]
        seq.append(current)
    ans = seq.pop()
    used_primes = primes[idx:idx+5]
    return seq, ans, f"ระยะห่างคือ จำนวนเฉพาะ (Prime Numbers):\nบวกเพิ่มทีละ {', '.join(map(str, used_primes[:-1]))}...\nถัดไปคือ {seq[-1]} + {used_primes[-1]} = {ans}"

def gen_fractional_multiplier():
    start = random.choice([4, 8, 12, 16])
    multiplier = 0.5
    seq = [start]
    current = float(start)
    for i in range(4):
        current *= multiplier
        seq.append(int(current) if current.is_integer() else current)
        multiplier += 0.5
    ans = seq.pop()
    return seq, ans, f"คูณด้วยทศนิยมที่เพิ่มขึ้นทีละ 0.5:\nรูปแบบ x0.5, x1.0, x1.5, x2.0...\nถัดไปคือ {seq[-1]} * {multiplier - 0.5} = {ans}"

def gen_digit_sum():
    start = random.randint(11, 25)
    seq = [start]
    current = start
    for i in range(4):
        digit_sum = sum(int(d) for d in str(current))
        current += digit_sum
        seq.append(current)
    ans = seq.pop()
    last_val = seq[-1]
    last_sum = sum(int(d) for d in str(last_val))
    return seq, ans, f"บวกด้วย ผลรวมของเลขโดดตัวมันเอง:\nเช่น {seq[0]} บวก ({'+'.join(str(seq[0]))}) = {seq[1]}\nถัดไปคือ {last_val} บวก ({'+'.join(str(last_val))}) = {ans}"

def gen_fibonacci_variant():
    seq = [random.randint(1, 3), random.randint(3, 6)]
    modifier = random.choice([-2, -1, 1, 2])
    for i in range(4):
        seq.append(seq[-1] + seq[-2] + modifier)
    ans = seq.pop()
    mod_str = f"+ {modifier}" if modifier > 0 else f"- {abs(modifier)}"
    return seq, ans, f"ฟีโบนัชชีประยุกต์ (บวก 2 ตัวหน้า แล้วชดเชยค่า):\nสูตร (ตัวที่ 1 + ตัวที่ 2) {mod_str} = ตัวที่ 3\nถัดไปคือ ({seq[-2]} + {seq[-1]}) {mod_str} = {ans}"

def gen_multiply_and_modify():
    start = random.randint(2, 5)
    multiplier = random.choice([2, 3])
    mod_start = random.choice([1, -1, 2, -2])
    mod_step = random.choice([1, -1])
    seq = [start]
    current = start
    current_mod = mod_start
    for i in range(4):
        current = (current * multiplier) + current_mod
        seq.append(current)
        current_mod += mod_step
    ans = seq.pop()
    mod_str_next = f"+ {current_mod}" if current_mod >= 0 else f"- {abs(current_mod)}"
    return seq, ans, f"Multiply & Modify (คูณแล้วบวกลบในสเต็ปเดียว):\nเอาค่าก่อนหน้า 'คูณ {multiplier}' แล้ว 'บวก/ลบด้วยเลขที่ขยับทีละ 1'\nสเต็ปถัดไป: ({seq[-1]} * {multiplier}) {mod_str_next} = {ans}"

def gen_power_differences():
    start = random.randint(2, 20)
    power = random.choice([2, 3])
    base_start = random.randint(1, 3)
    seq = [start]
    current = start
    for i in range(5):
        diff = (base_start + i) ** power
        current += diff
        seq.append(current)
    ans = seq.pop()
    diff_str = "ยกกำลังสอง" if power == 2 else "ยกกำลังสาม"
    return seq, ans, f"Power Differences (ระยะห่างเป็นเลข{diff_str}):\nส่วนต่างคือ {base_start}^{power}, {base_start+1}^{power}, {base_start+2}^{power}...\nถัดไปคือ {seq[-1]} + {(base_start+4)**power} = {ans}"

# ==========================================
# 3. Setup & State Initialization
# ==========================================
st.set_page_config(page_title="Aptitude Test Gym", layout="wide")

if 'ns_score' not in st.session_state:
    st.session_state.update({
        'ns_score': 0, 'ns_attempts': 0, 'ns_diff': 'ยาก (Hard)',
        'sym_score': 0, 'sym_attempts': 0,
        'app_mode': '🔢 Number Series'
    })

def get_new_ns_question():
    level = st.session_state.ns_diff
    if level == "ง่าย (Easy)":
        funcs = [gen_arithmetic, gen_geometric]
    elif level == "ปานกลาง (Medium)":
        funcs = [gen_interleaved, gen_exponential_basic]
    else:
        funcs = [gen_mixed_operations, gen_prime_addition, gen_fractional_multiplier, 
                 gen_digit_sum, gen_fibonacci_variant, gen_multiply_and_modify, gen_power_differences]
    
    seq, ans, logic = random.choice(funcs)()
    st.session_state.update({
        'ns_seq': seq, 'ns_ans': ans, 'ns_logic': logic,
        'ns_show_ans': False, 'ns_feedback': None, 'timer_id_ns': str(time.time())
    })

SYMBOLS = ['♒', '😃', '✌', '♌', '✈', '⌘', '◆', '💀', '⬤']
def init_symbol_test():
    st.session_state.update({
        'sym_map': {sym: random.randint(3, 25) for sym in SYMBOLS},
        'sym_seq': [random.choice(SYMBOLS) for _ in range(16)],
        'sym_submitted': False, 'timer_id_sym': str(time.time())
    })

if 'ns_seq' not in st.session_state: get_new_ns_question()
if 'sym_seq' not in st.session_state: init_symbol_test()

# ==========================================
# 4. Sidebar (Menu & Stats)
# ==========================================
with st.sidebar:
    st.title("🎯 เมนูฝึกซ้อม")
    st.session_state.app_mode = st.radio("เลือกโหมด:", ["🔢 Number Series", "🔣 Symbol Addition"])
    st.divider()
    
    st.header("📊 สถิติของคุณ")
    if st.session_state.app_mode == "🔢 Number Series":
        st.subheader("โหมดอนุกรมตัวเลข")
        c1, c2 = st.columns(2)
        c1.metric("คะแนน", st.session_state.ns_score)
        c2.metric("ทำไปแล้ว", st.session_state.ns_attempts)
        acc = (st.session_state.ns_score / max(1, st.session_state.ns_attempts)) * 100
        st.metric("ความแม่นยำ", f"{acc:.1f}%")
        if st.button("🗑️ รีเซ็ตสถิติอนุกรม", use_container_width=True):
            st.session_state.ns_score = 0; st.session_state.ns_attempts = 0; st.rerun()
            
    else:
        st.subheader("โหมดบวกเลขต่อเนื่อง")
        c1, c2 = st.columns(2)
        c1.metric("คะแนน (ข้อ)", st.session_state.sym_score)
        c2.metric("ทำไปแล้ว (รอบ)", st.session_state.sym_attempts)
        acc = (st.session_state.sym_score / max(1, st.session_state.sym_attempts*16)) * 100
        st.metric("ความแม่นยำรวม", f"{acc:.1f}%")
        if st.button("🗑️ รีเซ็ตสถิติสัญลักษณ์", use_container_width=True):
            st.session_state.sym_score = 0; st.session_state.sym_attempts = 0; st.rerun()

# ==========================================
# 5. Main App Logic (Number Series)
# ==========================================
if st.session_state.app_mode == "🔢 Number Series":
    st.title("🧠 Number Series Gym")
    
    # ควบคุมความยาก
    new_diff = st.radio("ความยาก:", ["ง่าย (Easy)", "ปานกลาง (Medium)", "ยาก (Hard)"], horizontal=True, index=["ง่าย (Easy)", "ปานกลาง (Medium)", "ยาก (Hard)"].index(st.session_state.ns_diff))
    if new_diff != st.session_state.ns_diff:
        st.session_state.ns_diff = new_diff
        get_new_ns_question()
        st.rerun()

    st.divider()
    
    # แสดงโจทย์และนาฬิกาควบคู่กัน
    col_q, col_timer = st.columns([2, 1])
    with col_q:
        st.header(f"Sequence: {', '.join(map(str, st.session_state.ns_seq))}, ?")
        st.write("")
        st.button("🔄 สุ่มโจทย์ใหม่และเริ่มเวลา", on_click=get_new_ns_question, type="primary")
        
    with col_timer:
        # ฝังนาฬิกาที่มีปุ่มควบคุมของตัวเอง (ตั้งเวลา 30 วินาที)
        html_code = render_timer(30, st.session_state.timer_id_ns, auto_start=True)
        components.html(html_code, height=140)

    # ช่องตอบคำถาม
    with st.form("ns_form", clear_on_submit=True):
        guess = st.text_input("พิมพ์คำตอบ:", placeholder="พิมพ์ตัวเลขแล้วกด Enter...")
        if st.form_submit_button("ส่งคำตอบ ⏎"):
            if guess.strip():
                try:
                    ans_val = float(guess) if '.' in guess else int(guess)
                    st.session_state.ns_attempts += 1
                    if ans_val == st.session_state.ns_ans:
                        st.session_state.ns_score += 1
                        st.session_state.ns_feedback = "correct"
                    else:
                        st.session_state.ns_feedback = "incorrect"
                except: 
                    st.error("ใส่เฉพาะตัวเลขเท่านั้นครับ")

    if st.session_state.ns_feedback == "correct":
        st.success("✅ ถูกต้อง! บวกคะแนนแล้ว")
    elif st.session_state.ns_feedback == "incorrect":
        st.error("❌ ยังไม่ถูก ลองคิดอีกที")

    c1, c2 = st.columns(2)
    with c1: 
        if st.button("💡 ดูเฉลย", use_container_width=True): 
            st.session_state.ns_show_ans = True
        
    if st.session_state.ns_show_ans:
        st.info(f"**ตอบ: {st.session_state.ns_ans}**\n\n**แนวคิด:**\n{st.session_state.ns_logic}")


# ==========================================
# 6. Main App Logic (Symbol Addition)
# ==========================================
elif st.session_state.app_mode == "🔣 Symbol Addition":
    st.title("🔣 Continuous Addition")
    st.write("โจทย์รอบละ 16 ข้อ ให้เวลาบวกเพียง **30 วินาที** (พิมพ์เสร็จกด Tab เลื่อนช่องได้เลย กล่องจะเลื่อนลงอัตโนมัติ)")
    
    # แสดงค่าสัญลักษณ์
    st.markdown("### 🔑 ค่าสัญลักษณ์")
    cols = st.columns(len(SYMBOLS))
    for i, sym in enumerate(SYMBOLS):
        cols[i].markdown(f"<div style='text-align:center;font-size:28px;'>{sym}</div><div style='text-align:center;font-weight:bold;font-size:22px;color:#1f77b4;'>{st.session_state.sym_map[sym]}</div>", unsafe_allow_html=True)
    
    st.divider()

    col_btn, col_timer = st.columns([1, 1])
    with col_btn:
        st.write("")
        st.write("")
        st.button("🔄 สุ่มโจทย์ใหม่และเริ่มเวลา", on_click=init_symbol_test, type="primary", use_container_width=True)
        
    with col_timer:
        # ฝังนาฬิกาที่มีปุ่มควบคุมของตัวเอง (ตั้งเวลา 30 วินาที)
        html_code = render_timer(30, st.session_state.timer_id_sym, auto_start=True)
        components.html(html_code, height=140)

    # กล่องโจทย์แบบ Scrollable Height=400 (เลื่อนช่องได้โดยตารางอ้างอิงและนาฬิกาไม่ขยับ)
    with st.container(height=400):
        with st.form("sym_form", clear_on_submit=False):
            user_inputs = []
            for i, sym in enumerate(st.session_state.sym_seq):
                r1, r2 = st.columns([1, 5])
                r1.markdown(f"<div style='font-size:28px;text-align:right;'>{sym}</div>", unsafe_allow_html=True)
                ans = r2.text_input("ยอด", key=f"s_{st.session_state.timer_id_sym}_{i}", label_visibility="collapsed")
                user_inputs.append(ans)
                
            if st.form_submit_button("ส่งคำตอบเพื่อตรวจ ⏎", use_container_width=True):
                st.session_state.sym_submitted = True
                st.session_state.user_inputs = user_inputs
                st.session_state.sym_attempts += 1 

    # ระบบตรวจคำตอบ
    if st.session_state.sym_submitted:
        st.header("📊 ตรวจคำตอบ")
        run_sum = 0
        round_score = 0
        
        r1, r2, r3, r4 = st.columns([1, 2, 2, 2])
        r1.write("**สัญลักษณ์**")
        r2.write("**ค่าของมัน**")
        r3.write("**คุณตอบ**")
        r4.write("**ยอดที่ถูกต้อง**")

        for i, sym in enumerate(st.session_state.sym_seq):
            val = st.session_state.sym_map[sym]
            run_sum += val
            ans = st.session_state.user_inputs[i]
            user_val = int(ans) if ans.isdigit() else None
            
            is_correct = (user_val == run_sum)
            if is_correct: round_score += 1
            icon = "✅" if is_correct else "❌"
            
            c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
            c1.write(f"### {sym}")
            c2.write(f"+ {val}")
            if is_correct: 
                c3.success(f"{ans} {icon}")
            else: 
                c3.error(f"{ans if ans else '-'} {icon}")
            c4.info(str(run_sum))
            
        st.session_state.sym_score += round_score
        if round_score == 16:
            st.balloons()
            st.success("🎉 สุดยอด! ทันเวลาและแม่นยำทุกข้อ (16/16)")
        else: 
            st.warning(f"ได้ {round_score}/16 คะแนนในรอบนี้ ไล่ดูจุดที่พลาดแล้วลุยใหม่ครับ!")
