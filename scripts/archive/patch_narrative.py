import re

with open('scripts/build_pptx_narrative.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Slide 2: Update Agenda column headers
old_s2_1 = '("PHẦN 1: TỔNG QUAN & THỊ GIÁC MÁY TÍNH", ['
new_s2_1 = '("PHẦN 1: TỔNG QUAN & THỊ GIÁC (03-06)", ['
old_s2_2 = '("PHẦN 2: ĐỊNH DANH, LỌC & ĐO ĐẠC ĐỘNG HỌC", ['
new_s2_2 = '("PHẦN 2: THEO DÕI & HÌNH HỌC (07-10)", ['
old_s2_3 = '("PHẦN 3: ĐIỀU PHỐI, MÔ PHỎNG & VẬN HÀNH", ['
new_s2_3 = '("PHẦN 3: ĐIỀU TIẾT & NỀN TẢNG (11-21)", ['
assert old_s2_1 in c, 'old_s2_1 not found'
assert old_s2_2 in c, 'old_s2_2 not found'
assert old_s2_3 in c, 'old_s2_3 not found'
c = c.replace(old_s2_1, new_s2_1).replace(old_s2_2, new_s2_2).replace(old_s2_3, new_s2_3)

# 2. Slide 4: Enhance with top metric ribbon
old_s4 = '''for i, (ctitle, items) in enumerate(ds_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), Inches(3.75), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), Inches(3.75), Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s4.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), Inches(3.75) - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s4.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), Inches(3.75) - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.8)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)'''

new_s4 = '''# Metrics ribbon on top
s4_metrics = [
    ("10,064", "Ảnh CARLA 1080p"),
    ("13", "Điều kiện thời tiết"),
    ("7 Lớp", "Đối tượng đô thị"),
    ("92.0%", "Recall xe buýt (từ 5.9%)")
]
rib_w = Inches(2.78)
for i, (num, lbl) in enumerate(s4_metrics):
    r_left = Inches(0.8 + i * (2.78 + 0.2))
    rb = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, r_left, Inches(1.65), rib_w, Inches(0.82))
    rb.fill.solid()
    rb.fill.fore_color.rgb = TINT_SURFACE
    rb.line.color.rgb = BORDER_BOX
    rb.line.width = Pt(0.75)
    
    tb_n = s4.shapes.add_textbox(r_left, Inches(1.7), rib_w, Inches(0.42))
    p = tb_n.text_frame.paragraphs[0]
    p.text = num
    p.font.name = FONT_HEADING
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    p.alignment = PP_ALIGN.CENTER
    
    tb_l = s4.shapes.add_textbox(r_left, Inches(2.12), rib_w, Inches(0.3))
    p = tb_l.text_frame.paragraphs[0]
    p.text = lbl
    p.font.name = FONT_BODY
    p.font.size = Pt(8.8)
    p.font.color.rgb = INK_SLATE
    p.alignment = PP_ALIGN.CENTER

for i, (ctitle, items) in enumerate(ds_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.65), Inches(3.75), Inches(3.9))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.65), Inches(3.75), Inches(0.42))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s4.shapes.add_textbox(c_left + Inches(0.12), Inches(2.72), Inches(3.75) - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s4.shapes.add_textbox(c_left + Inches(0.15), Inches(3.18), Inches(3.75) - Inches(0.3), Inches(3.2))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.2)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(6)'''

assert old_s4 in c, 'old_s4 not found'
c = c.replace(old_s4, new_s4)

# 3. Slide 7: Add top pipeline ribbon
old_s7 = '''col_w7 = Inches(3.75)
for i, (stitle, items) in enumerate(track_steps):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col_w7, Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col_w7, Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s7.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), col_w7 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = stitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s7.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), col_w7 - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)'''

new_s7 = '''# Top pipeline sequence bar
pipe_box7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.45))
tf = pipe_box7.text_frame
p = tf.paragraphs[0]
p.text = "YOLOv11m Detections  ──►  Phân loại ngưỡng Score (0.5)  ──►  Ghép nối Tầng 1 (High-Score)  ──►  Ghép nối Tầng 2 (Low-Score)  ──►  ID Quỹ đạo bền vững"
p.font.name = FONT_CODE
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

col_w7 = Inches(3.75)
for i, (stitle, items) in enumerate(track_steps):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.25), col_w7, Inches(4.3))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.25), col_w7, Inches(0.42))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s7.shapes.add_textbox(c_left + Inches(0.12), Inches(2.32), col_w7 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = stitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s7.shapes.add_textbox(c_left + Inches(0.15), Inches(2.8), col_w7 - Inches(0.3), Inches(3.6))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.2)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(7)'''

assert old_s7 in c, 'old_s7 not found'
c = c.replace(old_s7, new_s7)

# 4. Slide 14: Fix right column word wrapping
old_s14 = '''# Right (52%): Schematic
diag_box = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.15), Inches(5.733), Inches(3.65))
diag_box.fill.solid()
diag_box.fill.fore_color.rgb = TINT_SURFACE
diag_box.line.color.rgb = BORDER_BOX
diag_box.line.width = Pt(0.75)

tb_diag = s14.shapes.add_textbox(Inches(7.1), Inches(3.4), Inches(5.2), Inches(3.2))
tf = tb_diag.text_frame
p = tf.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & ON-RAMP METERING"
p.font.name = FONT_HEADING
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

p2 = tf.add_paragraph()
p2.text = (
    "\\n[ TUYẾN CHÍNH ] ──► [ Cảm biến ô(k) ] ──► Thông suốt\\n"
    "                         ▲ Điểm hòa dòng\\n"
    "[ NHÁNH NỐI ] ────► [ Đèn Meter r(k) ]\\n"
    "  ▲\\n"
    "  └── Q_ramp >= 30 xe ──► [ GHI ĐÈ XẢ TRẠM r_max ]"
)
p2.font.name = FONT_CODE
p2.font.size = Pt(8.5)
p2.font.color.rgb = INK_NAVY
p2.space_before = Pt(10)

p3 = tf.add_paragraph()
p3.text = "\\nGiải thích cơ chế vận hành:\\n• Khi mật độ ô(k) cao nhưng hàng đợi nhánh nối nhỏ: ALINEA xiết van đèn đỏ.\\n• Khi hàng đợi nhánh nối chạm ngưỡng 30 xe: Ghi đè xả trạm ngay lập tức để giải cứu đường nội đô lân cận."
p3.font.name = FONT_BODY
p3.font.size = Pt(9.5)
p3.font.italic = True
p3.font.color.rgb = INK_SLATE
p3.space_before = Pt(10)'''

new_s14 = '''# Right (52%): Schematic
diag_box = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.15), Inches(5.733), Inches(3.65))
diag_box.fill.solid()
diag_box.fill.fore_color.rgb = TINT_SURFACE
diag_box.line.color.rgb = BORDER_BOX
diag_box.line.width = Pt(0.75)

tb_diag = s14.shapes.add_textbox(Inches(6.95), Inches(3.25), Inches(5.4), Inches(3.45))
tf = tb_diag.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & ON-RAMP METERING"
p.font.name = FONT_HEADING
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

p2 = tf.add_paragraph()
p2.text = (
    "\\n[ TUYẾN CHÍNH ] ──► [ Cảm biến ô(k) ] ──► Thông suốt\\n"
    "                         ▲ Điểm hòa dòng\\n"
    "[ NHÁNH NỐI ] ────► [ Đèn Meter r(k) ]\\n"
    "  ▲\\n"
    "  └── Q_ramp >= 30 xe ──► [ GHI ĐÈ XẢ TRẠM r_max ]"
)
p2.font.name = FONT_CODE
p2.font.size = Pt(8.0)
p2.font.color.rgb = INK_NAVY
p2.space_before = Pt(6)

p3 = tf.add_paragraph()
p3.text = (
    "\\nGiải thích cơ chế vận hành:\\n"
    "• Khi mật độ ô(k) cao nhưng nhánh nối ngắn: ALINEA xiết van đèn đỏ để bảo vệ tuyến chính.\\n"
    "• Khi hàng đợi nhánh nối chạm ngưỡng 30 xe: Ghi đè r_max = 1200 veh/h giải phóng dòng chờ, chống tràn ngược vào nội đô."
)
p3.font.name = FONT_BODY
p3.font.size = Pt(9.0)
p3.font.italic = True
p3.font.color.rgb = INK_SLATE
p3.space_before = Pt(8)'''

assert old_s14 in c, 'old_s14 not found'
c = c.replace(old_s14, new_s14)

# 5. Slide 18: Add bottom engineering metrics ribbon
old_s18 = '''col_w18 = Inches(3.75)
for i, (ctitle, items) in enumerate(be_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col_w18, Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col_w18, Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s18.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), col_w18 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s18.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), col_w18 - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)'''

new_s18 = '''col_w18 = Inches(3.75)
for i, (ctitle, items) in enumerate(be_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.65), col_w18, Inches(3.9))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.65), col_w18, Inches(0.42))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s18.shapes.add_textbox(c_left + Inches(0.12), Inches(1.72), col_w18 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s18.shapes.add_textbox(c_left + Inches(0.15), Inches(2.18), col_w18 - Inches(0.3), Inches(3.2))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.2)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(6)

# Bottom engineering metrics ribbon
be_metrics = [
    ("tau_ws <= 0.15s", "Bọc timeout khử treo mạng"),
    ("-45% Payload", "32 KB tick-by-tick tối ưu"),
    ("10 Hz TraCI", "Chu kỳ vi mô 0.1s thời gian thực"),
    ("< 15 ms", "Độ trễ truyền dẫn từ mô phỏng đến UI")
]
rib_w18 = Inches(2.78)
for i, (num, lbl) in enumerate(be_metrics):
    r_left = Inches(0.8 + i * (2.78 + 0.2))
    rb = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, r_left, Inches(5.72), rib_w18, Inches(0.82))
    rb.fill.solid()
    rb.fill.fore_color.rgb = TINT_SURFACE
    rb.line.color.rgb = BORDER_BOX
    rb.line.width = Pt(0.75)
    
    tb_n = s18.shapes.add_textbox(r_left, Inches(5.77), rib_w18, Inches(0.42))
    p = tb_n.text_frame.paragraphs[0]
    p.text = num
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    p.alignment = PP_ALIGN.CENTER
    
    tb_l = s18.shapes.add_textbox(r_left, Inches(6.18), rib_w18, Inches(0.3))
    p = tb_l.text_frame.paragraphs[0]
    p.text = lbl
    p.font.name = FONT_BODY
    p.font.size = Pt(8.8)
    p.font.color.rgb = INK_SLATE
    p.alignment = PP_ALIGN.CENTER'''

assert old_s18 in c, 'old_s18 not found'
c = c.replace(old_s18, new_s18)

with open('scripts/build_pptx_narrative.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated build_pptx_narrative.py successfully!')
