import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ==========================================
# 1. ฟังก์ชันนาฬิกาจับเวลา (อิสระ + Auto Submit + Default Pause)
# ==========================================
def render_timer(duration_sec, timer_id, auto_start=False, is_sym_mode=False):
    # ปิด auto_start เป็น False ตามค่าเริ่มต้น เพื่อให้นาฬิการอผู้ใช้กดเริ่มเอง
    auto_js = "startTimer();" if auto_start else ""
    
    submit_js = """
        var btns = window.parent.document.querySelectorAll('button');
        btns.forEach(function(btn) {
            if(btn.innerText.includes('ส่งคำตอบเพื่อตรวจ')) {
                btn.click();
            }
        });
    """ if is_sym_mode else ""

    return f"""
    <div style="font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 5px; background: #f8f9fa; border-radius: 8px; border: 1px solid #e9ecef;">
        <div id="t_display" style="font-size: 1.8rem; font-weight: bold; color: #1f77b4; margin-bottom: 5px; font-family: monospace;">
            {duration_sec} วินาที
        </div>
        <div style="display: flex; gap: 8px;">
            <button onclick="startTimer()" style="padding: 5px 10px; border: none; border-radius: 4px; background: #28a745; color: white; cursor: pointer; font-weight: bold; font-size: 12px;">▶ เริ่ม</button>
            <button onclick="pauseTimer()" style="padding: 5px 10px; border: none; border-radius: 4px; background: #dc3545; color: white; cursor: pointer; font-weight: bold; font-size: 12px;">⏸ หยุด</button>
            <button onclick="resetTimer()" style="padding: 5px 10px; border: none; border-radius: 4px; background: #6c757d; color: white; cursor: pointer; font-weight: bold; font-size: 12px;">🔄 รีเซ็ต</button>
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
                display.style.color = "#dc3545"; 
                {submit_js} 
            }} else {{
                display.innerHTML = timeLeft + " วินาที";
                if (timeLeft <= 5) display.style.color = "#dc3545"; 
                else if (timeLeft <= 10) display.style.color = "#ffc107"; 
                else display.style.color = "#1f77b4"; 
            }}
        }}

        function startTimer() {{
            if (timerId !== null) return; 
            if (timeLeft <= 0) return; 
            timerId = setInterval(function() {{
                timeLeft--; updateDisplay();
                if (timeLeft <= 0) clearInterval(timerId);
            }}, 1000);
        }}

        function pauseTimer() {{
            if (timerId !== null) {{ clearInterval(timerId); timerId = null; }}
        }}

        function resetTimer() {{
            pauseTimer(); timeLeft = duration; updateDisplay();
        }}
        {auto_js}
    </script>
    """

# ==========================================
# 2. ฟังก์ชันสุ่มโจทย์ Number Series (ครบ 11 รูปแบบ)
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
st.set_page_config(page_title="AVMED Aptitude Gym", layout="centered")

if 'ns_score' not in st.session_state:
    st.session_state.update({
        'ns_score': 0, 'ns_attempts': 0, 'ns_diff': 'สุ่มรวมทุกระดับ (Mixed)', 
        'sym_score': 0, 'sym_attempts': 0, 'app_mode': '🔢 Number Series',
        'sym_col_idx': 0, 'sym_round_scores': [], 'sym_columns': []
    })

def get_new_ns_question():
    level = st.session_state.ns_diff
    funcs_easy = [gen_arithmetic, gen_geometric]
    funcs_med = [gen_interleaved, gen_exponential_basic]
    funcs_hard = [gen_mixed_operations, gen_prime_addition, gen_fractional_multiplier, gen_digit_sum, gen_fibonacci_variant, gen_multiply_and_modify, gen_power_differences]
    
    if level == "ง่าย (Easy)": funcs = funcs_easy
    elif level == "ปานกลาง (Medium)": funcs = funcs_med
    elif level == "ยาก (Hard)": funcs = funcs_hard
    else: funcs = funcs_easy + funcs_med + funcs_hard
    
    seq, ans, logic = random.choice(funcs)()
    st.session_state.update({'ns_seq': seq, 'ns_ans': ans, 'ns_logic': logic, 'ns_show_ans': False, 'ns_feedback': None, 'timer_id_ns': str(time.time())})

# สัญลักษณ์คลาสสิก ดำ-เทา
SYMBOLS = ['★', '☺\uFE0E', '✌\uFE0E', '▲', '✈\uFE0E', '⌘', '◆', '☠\uFE0E', '⬤']

def init_symbol_test():
    sym_cols = []
    # สร้างโจทย์ 8 คอลัมน์ โดยบังคับไม่ให้สัญลักษณ์ติดกันซ้ำกัน
    for _ in range(8):
        seq = [random.choice(SYMBOLS)]
        for _ in range(15): # สุ่มอีก 15 ตัว
            # เลือกเฉพาะสัญลักษณ์ที่ไม่ซ้ำกับตัวก่อนหน้า (seq[-1])
            choices = [s for s in SYMBOLS if s != seq[-1]]
            seq.append(random.choice(choices))
        sym_cols.append(seq)

    st.session_state.update({
        'sym_map': {sym: random.randint(3, 25) for sym in SYMBOLS},
        'sym_columns': sym_cols,
        'sym_col_idx': 0,
        'sym_round_scores': [],
        'sym_submitted': False, 
        'timer_id_sym': str(time.time())
    })

if 'ns_seq' not in st.session_state: get_new_ns_question()
if not st.session_state.sym_columns: init_symbol_test()

# ==========================================
# 4. Sidebar (Menu, Settings & Stats)
# ==========================================
with st.sidebar:
    st.title("🎯 เมนูฝึกซ้อม")
    st.session_state.app_mode = st.radio("เลือกโหมด:", ["🔢 Number Series", "🔣 Symbol Addition"])
    st.divider()
    
    # --- ตั้งค่าระยะเวลาปรับได้ตามใจชอบ ---
    st.header("⚙️ ตั้งค่าเวลา")
    timer_duration = st.number_input("เวลาจับต่อรอบ (วินาที)", min_value=5, max_value=300, value=30, step=1)
    st.divider()
    
    st.header("📊 สถิติของคุณ")
    if st.session_state.app_mode == "🔢 Number Series":
        c1, c2 = st.columns(2)
        c1.metric("คะแนน", st.session_state.ns_score)
        c2.metric("ทำไปแล้ว", st.session_state.ns_attempts)
        acc = (st.session_state.ns_score / max(1, st.session_state.ns_attempts)) * 100
        st.metric("ความแม่นยำ", f"{acc:.1f}%")
        if st.button("🗑️ รีเซ็ตสถิติ", use_container_width=True):
            st.session_state.ns_score = 0; st.session_state.ns_attempts = 0; st.rerun()
    else:
        c1, c2 = st.columns(2)
        c1.metric("คะแนน (ข้อ)", st.session_state.sym_score)
        c2.metric("ทำไปแล้ว (ด่าน)", st.session_state.sym_attempts)
        acc = (st.session_state.sym_score / max(1, st.session_state.sym_attempts*16)) * 100
        st.metric("ความแม่นยำรวม", f"{acc:.1f}%")
        if st.button("🗑️ รีเซ็ตสถิติ", use_container_width=True):
            st.session_state.sym_score = 0; st.session_state.sym_attempts = 0; st.rerun()

# ==========================================
# 5. Main App Logic (Number Series)
# ==========================================
if st.session_state.app_mode == "🔢 Number Series":
    st.title("🧠 Number Series Gym")
    diff_options = ["ง่าย (Easy)", "ปานกลาง (Medium)", "ยาก (Hard)", "สุ่มรวมทุกระดับ (Mixed)"]
    new_diff = st.radio("เลือกระดับโจทย์:", diff_options, horizontal=True, index=diff_options.index(st.session_state.ns_diff))
    if new_diff != st.session_state.ns_diff:
        st.session_state.ns_diff = new_diff
        get_new_ns_question(); st.rerun()

    st.divider()
    col_q, col_timer = st.columns([5, 3])
    with col_q:
        st.header(f"Sequence: {', '.join(map(str, st.session_state.ns_seq))}, ?")
        st.button("🔄 สุ่มโจทย์ใหม่", on_click=get_new_ns_question, type="primary")
    with col_timer:
        # ใช้ timer_duration จาก Sidebar และปิด auto_start (รอให้ผู้ใช้กดเริ่มเอง)
        components.html(render_timer(timer_duration, st.session_state.timer_id_ns, auto_start=False, is_sym_mode=False), height=95)

    with st.form("ns_form", clear_on_submit=True):
        guess = st.text_input("พิมพ์คำตอบ:", placeholder="พิมพ์ตัวเลขแล้วกด Enter...", autocomplete="off")
        if st.form_submit_button("ส่งคำตอบ ⏎"):
            if guess.strip():
                try:
                    ans_val = float(guess) if '.' in guess else int(guess)
                    st.session_state.ns_attempts += 1
                    if ans_val == st.session_state.ns_ans:
                        st.session_state.ns_score += 1; st.session_state.ns_feedback = "correct"
                    else: st.session_state.ns_feedback = "incorrect"
                except: st.error("ใส่เฉพาะตัวเลขเท่านั้นครับ")

    if st.session_state.ns_feedback == "correct": st.success("✅ ถูกต้อง! บวกคะแนนแล้ว")
    elif st.session_state.ns_feedback == "incorrect": st.error("❌ ยังไม่ถูก ลองคิดอีกที")

    if st.button("💡 ดูเฉลย", use_container_width=True): st.session_state.ns_show_ans = True
    if st.session_state.ns_show_ans:
        st.info(f"**ตอบ: {st.session_state.ns_ans}**\n\n**แนวคิด:**\n{st.session_state.ns_logic}")

# ==========================================
# 6. Main App Logic (Symbol Addition - AVMED)
# ==========================================
elif st.session_state.app_mode == "🔣 Symbol Addition":
    # ปรับหัวข้อให้เปลี่ยนตามเวลาที่ผู้ใช้ตั้ง
    st.markdown(f"### 🔣 AVMED Addition (8 คอลัมน์, คอลัมน์ละ {timer_duration} วินาที)")
    
    cols = st.columns(len(SYMBOLS))
    for i, sym in enumerate(SYMBOLS):
        cols[i].markdown(f"<div style='text-align:center;font-size:24px;line-height:1.2;color:#333;'>{sym}</div><div style='text-align:center;font-weight:bold;font-size:16px;color:#1f77b4;'>{st.session_state.sym_map[sym]}</div>", unsafe_allow_html=True)
    st.write("") 

    col_btn, col_timer = st.columns([1, 1])
    with col_btn:
        st.info(f"📍 **กำลังทำคอลัมน์ที่ {st.session_state.sym_col_idx + 1} จาก 8** (ใช้ค่าด้านบนตลอด 8 คอลัมน์)")
        st.button("🔄 รีเซ็ตและสุ่มชุดใหม่ 8 คอลัมน์", on_click=init_symbol_test, type="secondary", use_container_width=True)
    
    with col_timer:
        if not st.session_state.sym_submitted:
            # ใช้ timer_duration จาก Sidebar และปิด auto_start
            components.html(render_timer(timer_duration, st.session_state.timer_id_sym, auto_start=False, is_sym_mode=True), height=95)

    if not st.session_state.sym_submitted:
        with st.container(height=300):
            with st.form("sym_form", clear_on_submit=False):
                user_inputs = []
                current_seq = st.session_state.sym_columns[st.session_state.sym_col_idx]
                for i, sym in enumerate(current_seq):
                    r1, r2 = st.columns([1, 6])
                    r1.markdown(f"<div style='font-size:20px;text-align:right;color:#333;'>{sym}</div>", unsafe_allow_html=True)
                    ans = r2.text_input("ยอด", key=f"s_{st.session_state.timer_id_sym}_{i}", label_visibility="collapsed", autocomplete="off")
                    user_inputs.append(ans)
                    
                if st.form_submit_button("ส่งคำตอบเพื่อตรวจ ⏎", use_container_width=True):
                    st.session_state.sym_submitted = True
                    st.session_state.user_inputs = user_inputs
                    st.rerun()

    if st.session_state.sym_submitted:
        st.header(f"📊 ตรวจคำตอบ (คอลัมน์ที่ {st.session_state.sym_col_idx + 1}/8)")
        run_sum = 0
        round_score = 0
        current_seq = st.session_state.sym_columns[st.session_state.sym_col_idx]
        
        r1, r2, r3, r4 = st.columns([1, 2, 2, 2])
        r1.write("**สัญลักษณ์**"); r2.write("**ค่า**"); r3.write("**คุณตอบ**"); r4.write("**เฉลย**")

        for i, sym in enumerate(current_seq):
            val = st.session_state.sym_map[sym]
            run_sum += val
            ans = st.session_state.user_inputs[i]
            user_val = int(ans) if ans.isdigit() else None
            
            is_correct = (user_val == run_sum)
            if is_correct: round_score += 1
            icon = "✅" if is_correct else "❌"
            
            c1, c2, c3, c4 = st.columns([1, 2, 2, 2])
            c1.write(f"#### <span style='color:#333;'>{sym}</span>", unsafe_allow_html=True); c2.write(f"+ {val}")
            if is_correct: c3.success(f"{ans} {icon}")
            else: c3.error(f"{ans if ans else '-'} {icon}")
            c4.info(str(run_sum))
            
        if len(st.session_state.sym_round_scores) == st.session_state.sym_col_idx:
            st.session_state.sym_score += round_score
            st.session_state.sym_attempts += 1
            st.session_state.sym_round_scores.append(round_score)
            
        st.divider()
        if st.session_state.sym_col_idx < 7:
            st.warning(f"คอลัมน์นี้คุณได้ {round_score}/16 คะแนน พักหายใจแล้วเตรียมลุยต่อ!")
            def go_next_col():
                st.session_state.sym_col_idx += 1
                st.session_state.sym_submitted = False
                st.session_state.timer_id_sym = str(time.time())
            st.button(f"▶ ไปคอลัมน์ที่ {st.session_state.sym_col_idx + 2}", on_click=go_next_col, type="primary", use_container_width=True)
        else:
            st.balloons()
            st.success(f"🎉 ยอดเยี่ยม! จบการทดสอบทั้ง 8 คอลัมน์\n\n**คะแนนรวมของคุณคือ: {sum(st.session_state.sym_round_scores)} / 128 คะแนน**")
            st.button("🔄 สร้างข้อสอบชุดใหม่ (เปลี่ยนค่าสัญลักษณ์)", on_click=init_symbol_test, type="primary", use_container_width=True)
