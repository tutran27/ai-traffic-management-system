with open('scripts/build_pptx_narrative.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Slide 7: Refine step titles and add background banner to pipe_box7
old_s7_block = '''# Top pipeline sequence bar
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

new_s7_block = '''# Top pipeline sequence bar with clean background box
pipe_bg7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.48))
pipe_bg7.fill.solid()
pipe_bg7.fill.fore_color.rgb = TINT_SURFACE
pipe_bg7.line.color.rgb = BORDER_BOX
pipe_bg7.line.width = Pt(0.75)

pipe_box7 = s7.shapes.add_textbox(Inches(0.9), Inches(1.72), Inches(11.533), Inches(0.35))
tf = pipe_box7.text_frame
p = tf.paragraphs[0]
p.text = "YOLOv11m Detections  ──►  Tách ngưỡng Score (0.5)  ──►  Ghép Tầng 1 (High-Score)  ──►  Ghép Tầng 2 (Low-Score)  ──►  ID Quỹ đạo bền vững"
p.font.name = FONT_CODE
p.font.size = Pt(9.2)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY
p.alignment = PP_ALIGN.CENTER

col_w7 = Inches(3.75)
for i, (stitle, items) in enumerate(track_steps):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.32), col_w7, Inches(4.25))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.32), col_w7, Inches(0.42))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s7.shapes.add_textbox(c_left + Inches(0.12), Inches(2.39), col_w7 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = stitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s7.shapes.add_textbox(c_left + Inches(0.15), Inches(2.85), col_w7 - Inches(0.3), Inches(3.6))
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

assert old_s7_block in c, 'old_s7_block not found'
c = c.replace(old_s7_block, new_s7_block)

# Also shorten the step titles in Slide 7
c = c.replace('"BƯỚC 1: PHÁT HIỆN & PHÂN LOẠI ĐỘ TIN CẬY"', '"BƯỚC 1: PHÂN LOẠI ĐỘ TIN CẬY"')
c = c.replace('"BƯỚC 2: GHÉP NỐI HUNGARIAN TẦNG 1 (HIGH-SCORE)"', '"BƯỚC 2: GHÉP TẦNG 1 (HIGH-SCORE)"')
c = c.replace('"BƯỚC 3: GHÉP NỐI HUNGARIAN TẦNG 2 (LOW-SCORE)"', '"BƯỚC 3: GHÉP TẦNG 2 (LOW-SCORE)"')

# 2. Slide 14: Replace ASCII box with native visual layout
old_s14_block = '''# Right (52%): Schematic
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

new_s14_block = '''# Right (52%): Native Graphic Box
diag_box = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.15), Inches(5.733), Inches(3.65))
diag_box.fill.solid()
diag_box.fill.fore_color.rgb = BG_WHITE
diag_box.line.color.rgb = BORDER_BOX
diag_box.line.width = Pt(0.75)

strip14_r = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.15), Inches(5.733), Inches(0.38))
strip14_r.fill.solid()
strip14_r.fill.fore_color.rgb = TINT_BAR
strip14_r.line.fill.background()

tb_dh = s14.shapes.add_textbox(Inches(6.95), Inches(3.21), Inches(5.4), Inches(0.3))
p = tb_dh.text_frame.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & CƠ CHẾ GHI ĐÈ"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_NAVY

# 3 visual flow rows inside
flow_rows = [
    ("LUỒNG TUYẾN CHÍNH", "Tuyến chính cao tốc ──► Cảm biến mật độ ô(k) ──► Dòng xe thông suốt"),
    ("ĐIỀU TIẾT NHẬP LÀN", "Nhánh nối On-Ramp ──► Đèn tín hiệu Meter r(k) ──► Hòa dòng an toàn"),
    ("GHI ĐÈ KHẨN CẤP", "Hàng đợi Q_ramp >= 30 xe ──► GHI ĐÈ xả trạm r_max = 1200 veh/h")
]

for idx, (fhead, fbody) in enumerate(flow_rows):
    y_r = Inches(3.68 + idx * 0.72)
    bg_sub = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), y_r, Inches(5.333), Inches(0.62))
    bg_sub.fill.solid()
    bg_sub.fill.fore_color.rgb = TINT_SURFACE if idx < 2 else RGBColor(254, 243, 199) # subtle amber for override
    bg_sub.line.color.rgb = BORDER_BOX if idx < 2 else RGBColor(245, 158, 11)
    bg_sub.line.width = Pt(0.75)
    
    tb_sub = s14.shapes.add_textbox(Inches(7.1), y_r + Inches(0.04), Inches(5.133), Inches(0.54))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    p1 = tf_s.paragraphs[0]
    p1.text = fhead
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(8.5)
    p1.font.bold = True
    p1.font.color.rgb = INK_NAVY if idx < 2 else RGBColor(180, 83, 9)
    
    p2 = tf_s.add_paragraph()
    p2.text = fbody
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.2)
    p2.font.bold = (idx == 2)
    p2.font.color.rgb = INK_LIGHT_NAVY if idx < 2 else RGBColor(146, 64, 14)

# Bottom note
tb_note = s14.shapes.add_textbox(Inches(7.0), Inches(5.95), Inches(5.333), Inches(0.75))
tf_n = tb_note.text_frame
tf_n.word_wrap = True
p = tf_n.paragraphs[0]
p.text = "• Bình thường: ALINEA xiết van đèn đỏ khi mật độ ô(k) cao chống sụp đổ lưu lượng tuyến chính.\\n• Khi kẹt nhánh nối: Tự động ghi đè xả trạm để cứu mạng lưới giao lộ nội đô lân cận."
p.font.name = FONT_BODY
p.font.size = Pt(8.6)
p.font.italic = True
p.font.color.rgb = INK_SLATE'''

assert old_s14_block in c, 'old_s14_block not found'
c = c.replace(old_s14_block, new_s14_block)

with open('scripts/build_pptx_narrative.py', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated build_pptx_narrative.py successfully!')
