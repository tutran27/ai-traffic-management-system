import os
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# DESIGN SYSTEM: Editorial Academic & Deep-Tech (Presentation-Ready Narrative)
# ==============================================================================
# 21 Slides strictly structured following user's requested storyline:
# Slide 1: Giới thiệu chủ đề
# Slide 2: Nội dung báo cáo (Agenda)
# Slide 3: Tổng quan đề tài & Kiến trúc phân tầng
# Slide 4: Dữ liệu tổng hợp CARLA 10k & Cân bằng lớp Spawner
# Slide 5: Mô hình YOLOv11m, Cấu hình train & Các hàm mất mát
# Slide 6: Kết quả đánh giá mô hình (CV Benchmark) & Visual Detection
# Slide 7: Tracking: Định danh liên tục với ByteTrack & Hungarian 2 tầng
# Slide 8: Bộ lọc Kalman 8 chiều khử nhiễu & Dự báo động học
# Slide 9: Hình học không gian: Ma trận Homography mặt đất H
# Slide 10: Ước lượng vận tốc thực & Tiêu chuẩn xe dừng chờ
# Slide 11: Điều khiển thích nghi: Nguyên lý Hàng đợi Tồn dư & Lọc EMA
# Slide 12: Điều khiển thích nghi: Tái phân bổ thời gian xanh & Biên an toàn
# Slide 13: Điều tiết cao tốc ALINEA & Kiểm soát điểm hòa dòng
# Slide 14: Cơ chế chống tràn nhánh nối (Spillback Override)
# Slide 15: Ưu tiên xe khẩn cấp: Làn sóng xanh tức thời (0s Delay)
# Slide 16: Cơ chế hoàn trả công nợ thời gian xanh công bằng
# Slide 17: Mô phỏng vi mô SUMO: 3 Mạng lưới đã xây dựng
# Slide 18: Nền tảng Backend: FastAPI Concurrency Engine & Khử backpressure
# Slide 19: Giao diện vận hành: Next.js 14 Dashboard & Groq Copilot
# Slide 20: Đánh giá thực nghiệm đối đầu: Chuẩn HCM Benchmark
# Slide 21: Ma trận nghiệm thu 100% khối lõi & Lộ trình phát triển
# ==============================================================================

BG_WHITE = RGBColor(255, 255, 255)
INK_NAVY = RGBColor(11, 25, 44)         # #0B192C - Primary ink
INK_SLATE = RGBColor(71, 85, 105)       # #475569 - Secondary text, subtitles, captions
INK_LIGHT_NAVY = RGBColor(30, 58, 138)  # #1E3A8A - Kicker, step badges, accents
HAIRLINE = RGBColor(226, 232, 240)      # #E2E8F0 - Architectural hairline dividers
BORDER_BOX = RGBColor(203, 213, 225)    # #CBD5E1 - Precise image & card borders
TINT_SURFACE = RGBColor(248, 250, 252)  # #F8FAFC - Formula pedestal & card fills
TINT_BAR = RGBColor(241, 245, 249)      # #F1F5F9 - Table headers / badge fills

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

FORMULA_DIR = "temp_formulas_narrative"
os.makedirs(FORMULA_DIR, exist_ok=True)

def render_formula(name, latex_code, fontsize=18, dpi=300):
    fig = plt.figure(figsize=(10, 1.4))
    plt.text(0.5, 0.5, latex_code, fontsize=fontsize, ha='center', va='center', color='#0B192C')
    plt.axis('off')
    path = os.path.join(FORMULA_DIR, f"{name}.png")
    plt.savefig(path, bbox_inches='tight', transparent=True, dpi=dpi)
    plt.close()
    return path

print("Rendering high-res formulas for narrative slides...")
F = {}
F['loss_total'] = render_formula("loss_total", r'$\mathcal{L}_{\mathrm{total}} = 7.5 \cdot \mathcal{L}_{\mathrm{box}} (\mathrm{CIoU}) + 0.5 \cdot \mathcal{L}_{\mathrm{cls}} (\mathrm{BCE}) + 1.5 \cdot \mathcal{L}_{\mathrm{dfl}} (\mathrm{DFL})$', fontsize=17)
F['ciou'] = render_formula("ciou", r'$\mathcal{L}_{\mathrm{box}} = 1 - \left(\mathrm{IoU} - \frac{\rho^2(\mathbf{b}, \mathbf{b}^{gt})}{c^2} - \alpha v\right)$', fontsize=17)
F['kalman'] = render_formula("kalman", r'$\mathbf{x}_t = [X_c, Y_c, a, h, \dot{X}_c, \dot{Y}_c, \dot{a}, \dot{h}]^T, \quad \mathbf{P}_{t|t-1} = \mathbf{F}\mathbf{P}_{t-1|t-1}\mathbf{F}^T + \mathbf{Q}$', fontsize=16)
F['homography'] = render_formula("homography", r'$[X_w, Y_w, 1]^T \sim \mathbf{H} [u, v, 1]^T \Rightarrow X_w = \frac{h_{11}u + h_{12}v + h_{13}}{h_{31}u + h_{32}v + h_{33}}, \quad Y_w = \frac{h_{21}u + h_{22}v + h_{23}}{h_{31}u + h_{32}v + h_{33}}$', fontsize=14.5)
F['speed'] = render_formula("speed", r'$\bar{v}(t) = \frac{1}{M}\sum_{m=0}^{M-1} \frac{\Delta d(t-m)}{\Delta t \cdot \Delta k}, \quad (\bar{v} < 2.0\mathrm{\;m/s}, \; \tau \geq 2.0\mathrm{\;s})$', fontsize=16)
F['ema'] = render_formula("ema", r'$S_i(k) = 0.7 \cdot Q_i(k) + 0.3 \cdot S_i(k-1)$', fontsize=18)
F['redist'] = render_formula("redist", r'$g_i(k+1) = \min\left(g_{\max}, \; g_i(k) + R \cdot \frac{S_i}{\sum_{m \in \mathcal{U}} S_m}\right), \quad g_i \in [10.0\mathrm{\;s}, 50.0\mathrm{\;s}]$', fontsize=15.5)
F['alinea'] = render_formula("alinea", r'$r(k) = \operatorname{clamp}\left(r(k-1) + 70.0 \cdot (0.20 - \hat{o}(k)), \; 200, \; 1200\right), \quad T_{\mathrm{cycle}}(k) = \frac{3600}{r(k)}$', fontsize=15)
F['spillback'] = render_formula("spillback", r'$Q_{\mathrm{ramp}}(k) \geq 30\mathrm{\;vehicles} \Rightarrow r(k) = r_{\max} = 1200\mathrm{\;veh/h}$', fontsize=17)
F['preempt'] = render_formula("preempt", r'$\mathrm{EV\;Detected:}\quad \phi(t) \leftarrow \phi_{\mathrm{EV}}(e), \quad t_{\mathrm{delay}} = 0\mathrm{\;s}$', fontsize=17)
F['debt'] = render_formula("debt", r'$D_d(J) \leftarrow D_d(J) + \Delta t_{\mathrm{preempt}}, \quad t_{\mathrm{comp}} = \min(D_{d^*}, \; 15.0\mathrm{\;s})$', fontsize=17)
F['hcm'] = render_formula("hcm", r'$d_i = \max(0, \; t_{\mathrm{dwell}} - t_{\mathrm{free\_flow}}), \quad \mathrm{Throughput} = \frac{N_{\mathrm{completed}} \times 60}{T_{\mathrm{sim}}}$', fontsize=16)
print("Formulas rendered successfully!")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]
TOTAL_SLIDES = 21

def set_bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG_WHITE

def add_header(slide, kicker, title, subtitle):
    # Kicker
    k_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.28))
    tf_k = k_box.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p = tf_k.paragraphs[0]
    p.text = kicker.upper()
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = INK_LIGHT_NAVY

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.42))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p = tf_t.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY

    # Subtitle
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.12), Inches(11.733), Inches(0.28))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p = tf_s.paragraphs[0]
    p.text = subtitle
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = INK_SLATE

    # Hairline divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = HAIRLINE
    line.line.fill.background()

def add_footer(slide, current_slide):
    # Hairline divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = HAIRLINE
    line.line.fill.background()

    # Left note
    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.14), Inches(8.0), Inches(0.26))
    tf_f = f_box.text_frame
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p = tf_f.paragraphs[0]
    p.text = "AI-Based Traffic Management & Monitoring System — Báo cáo tiến độ kỹ thuật"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = INK_SLATE

    # Right slide number
    r_box = slide.shapes.add_textbox(Inches(9.533), Inches(7.14), Inches(3.0), Inches(0.26))
    tf_r = r_box.text_frame
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p = tf_r.paragraphs[0]
    p.text = f"Slide {current_slide} / {TOTAL_SLIDES}"
    p.alignment = PP_ALIGN.RIGHT
    p.font.name = FONT_HEADING
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY

def create_formula_slide_2col(slide_num, kicker, title, subtitle, formula_key, eq_label, col1_data, col2_data):
    """Layout for deep-dive technical slides with large formula + 2 clean structured columns."""
    s = prs.slides.add_slide(blank_layout)
    set_bg(s)
    add_header(s, kicker, title, subtitle)
    
    # Formula Stage
    stage = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.35))
    stage.fill.solid()
    stage.fill.fore_color.rgb = TINT_SURFACE
    stage.line.color.rgb = BORDER_BOX
    stage.line.width = Pt(0.75)
    
    s.shapes.add_picture(F[formula_key], Inches(1.2), Inches(1.78), width=Inches(9.5))
    
    eq_b = s.shapes.add_textbox(Inches(10.8), Inches(1.75), Inches(1.5), Inches(0.3))
    p = eq_b.text_frame.paragraphs[0]
    p.text = eq_label
    p.font.name = FONT_CODE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_LIGHT_NAVY
    p.alignment = PP_ALIGN.RIGHT
    
    # 2 Columns
    c_w = Inches(5.7)
    cols = [col1_data, col2_data]
    for i, (ctitle, items) in enumerate(cols):
        c_left = Inches(0.8 + i * (5.7 + 0.33))
        card = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(3.2), c_w, Inches(3.65))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_WHITE
        card.line.color.rgb = BORDER_BOX
        card.line.width = Pt(0.75)
        
        strip = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(3.2), c_w, Inches(0.42))
        strip.fill.solid()
        strip.fill.fore_color.rgb = TINT_BAR
        strip.line.fill.background()
        
        tb = s.shapes.add_textbox(c_left + Inches(0.15), Inches(3.28), c_w - Inches(0.3), Inches(0.3))
        p = tb.text_frame.paragraphs[0]
        p.text = ctitle
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = INK_NAVY
        
        tb_b = s.shapes.add_textbox(c_left + Inches(0.18), Inches(3.72), c_w - Inches(0.36), Inches(3.0))
        tf = tb_b.text_frame
        tf.word_wrap = True
        for idx, (lead, body) in enumerate(items):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.text = f"• {lead}: {body}"
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = INK_NAVY
            if idx > 0:
                p.space_before = Pt(6)
                
    add_footer(s, slide_num)
    return s

# ==============================================================================
# SLIDE 1: GIỚI THIỆU CHỦ ĐỀ (Title & Executive Overview)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_bg(s1)

k1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(6.5), Inches(0.3))
p = k1.text_frame.paragraphs[0]
p.text = "TECHNICAL PROGRESS REPORT  •  Q4 2026"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(6.5), Inches(1.3))
tf = t1.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "HỆ THỐNG ĐIỀU PHỐI & GIÁM SÁT GIAO THÔNG THÔNG MINH"
p.font.name = FONT_HEADING
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = INK_NAVY

s1_sub = s1.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(6.5), Inches(0.6))
tf = s1_sub.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Nền tảng Tối ưu hóa Luồng Giao thông Đô thị Thời gian Thực kết hợp Thị giác YOLOv11m, Điều khiển Thích nghi Leftover-Queue, Cao tốc ALINEA & SUMO Engine."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = INK_SLATE

line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.35), Inches(6.2), Inches(0.015))
line1.fill.solid()
line1.fill.fore_color.rgb = HAIRLINE
line1.line.fill.background()

metrics = [
    ("-54.0%", "Thời gian dừng chờ xe", "Giảm trễ trung bình toàn mạng lưới (HCM)"),
    ("94.91%", "mAP@50 Đô thị", "YOLOv11m nhận diện 7 lớp phương tiện"),
    ("27.7 FPS", "Tốc độ Inference Biên", "Xử lý video camera độ phân giải cao"),
    ("100% Real-Time", "TraCI Socket Streaming", "Chu kỳ vi mô 10 Hz & Next.js 14 Dashboard")
]

for idx, (num, label, desc) in enumerate(metrics):
    row, col = idx // 2, idx % 2
    mb = s1.shapes.add_textbox(Inches(0.8 + col * 3.25), Inches(3.6 + row * 1.5), Inches(3.2), Inches(1.3))
    tf_m = mb.text_frame
    tf_m.word_wrap = True
    p1 = tf_m.paragraphs[0]
    p1.text = num
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(27)
    p1.font.bold = True
    p1.font.color.rgb = INK_NAVY
    p2 = tf_m.add_paragraph()
    p2.text = label
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = INK_LIGHT_NAVY
    p2.space_before = Pt(3)
    p3 = tf_m.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = INK_SLATE
    p3.space_before = Pt(2)

hero_path = "docs/images/hero-banner.png"
if os.path.exists(hero_path):
    pic = s1.shapes.add_picture(hero_path, Inches(7.5), Inches(1.6), width=Inches(5.033))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s1.shapes.add_textbox(Inches(7.5), Inches(4.7), Inches(5.033), Inches(0.4))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Giao diện Trung tâm Điều hành & Giám sát Luồng Giao thông Thời gian Thực"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s1, 1)

# ==============================================================================
# SLIDE 2: NỘI DUNG BÁO CÁO (AGENDA)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_bg(s2)
add_header(s2, "MỤC LỤC BÁO CÁO", "Nội Dung Báo Cáo Kỹ Thuật Đề Tài", "Cấu trúc báo cáo tiến độ kỹ thuật từ thu thập dữ liệu, thị giác, thuật toán đến nền tảng vận hành.")

agenda_pillars = [
    ("PHẦN 1: TỔNG QUAN & THỊ GIÁC (03-06)", [
        ("01. Tổng quan đề tài", "Bối cảnh nghiên cứu và kiến trúc 4 phân tầng độc lập (Decoupled Architecture)."),
        ("02. Dữ liệu CARLA 10k", "Bộ dữ liệu 10,064 ảnh qua 13 điều kiện thời tiết & kỹ thuật Spawner cân bằng lớp."),
        ("03. Mô hình YOLOv11m", "Cấu hình huấn luyện, hàm mất mát đa nhiệm (CIoU, BCE, DFL) & LR scheduler."),
        ("04. Kết quả đánh giá", "Chỉ số kiểm định Precision, Recall, mAP@50 (94.91%) và tốc độ 27.7 FPS.")
    ]),
    ("PHẦN 2: THEO DÕI & HÌNH HỌC (07-10)", [
        ("05. Định danh ByteTrack", "Theo dõi đa đối tượng liên tục với cơ chế ghép nối Hungarian 2 tầng khử che khuất."),
        ("06. Bộ lọc Kalman 8D", "Vector trạng thái 8 chiều, làm mịn quỹ đạo và dự báo động học phương tiện."),
        ("07. Homography mặt đất H", "Phép chiếu phối cảnh chuyển đổi tọa độ điểm ảnh 2D sang cự ly mét thực tế."),
        ("08. Ước lượng vận tốc thực", "Cửa sổ trượt 5 frames và tiêu chuẩn kép nhận diện xe dừng chờ đèn đỏ (Queue).")
    ]),
    ("PHẦN 3: ĐIỀU TIẾT & NỀN TẢNG (11-21)", [
        ("09. Thích nghi Leftover-Queue", "Cân bằng chu kỳ đèn thích nghi theo hàng đợi tồn dư tại thời điểm chớm vàng."),
        ("10. Cao tốc ALINEA & Chống tràn", "Điều tiết nhập làn cao tốc và cơ chế xả trạm khẩn cấp (Spillback Override)."),
        ("11. Làn sóng xanh EV & Bù nợ", "Ưu tiên xe khẩn cấp 0s delay và thuật toán hoàn trả công nợ thời gian xanh."),
        ("12. Nền tảng Full-Stack & HCM", "Mô phỏng vi mô SUMO 10 Hz, Dashboard Next.js 14, Groq Copilot & Đo kiểm đối đầu.")
    ])
]

col_w2 = Inches(3.75)
for i, (atitle, items) in enumerate(agenda_pillars):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col_w2, Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), col_w2, Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s2.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), col_w2 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = atitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s2.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), col_w2 - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"{lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)

add_footer(s2, 2)

# ==============================================================================
# SLIDE 3: TỔNG QUAN ĐỀ TÀI & KIẾN TRÚC PHÂN TẦNG (PIPELINE)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_bg(s3)
add_header(s3, "01 // TỔNG THỂ HỆ THỐNG", "Kiến Trúc Phân Tầng Độc Lập Đã Triển Khai", "Phân tách rõ ràng giữa 4 phân tầng: Cảm biến, Điều khiển, Mô phỏng và Vận hành liên lạc qua Interface chuẩn.")

pipe_box = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.35))
p = pipe_box.text_frame.paragraphs[0]
p.text = "01. CẢM BIẾN (CAMERA)   ────────►   02. RA QUYẾT ĐỊNH (POLICY)   ────────►   03. MÔ PHỎNG (SUMO)   ────────►   04. VẬN HÀNH (DASHBOARD)"
p.font.name = FONT_HEADING
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

layers = [
    ("Phân Hệ Cảm Biến", "packages/cv-pipeline", [
        ("YOLOv11m", "Nhận diện 7 lớp phương tiện đô thị (mAP50 = 94.91%)."),
        ("ByteTrack 8D", "Theo dõi đa đối tượng liên tục, bù trừ che khuất tạm thời."),
        ("Homography H", "Ma trận chuyển đổi pixel sang tọa độ mét thực tế."),
        ("Đo lường", "Ước lượng vận tốc thực & phát hiện xe dừng chờ (Queue).")
    ], "Dữ liệu ra: Q_i, v_avg, EV alerts"),

    ("Chính Sách Điều Khiển", "packages/adaptive-policy", [
        ("Leftover-Queue", "Cân bằng chu kỳ đèn thích nghi theo hàng đợi tồn dư."),
        ("ALINEA Ramp", "Điều tiết nhập làn cao tốc & cơ chế chống tràn nhánh."),
        ("Làn sóng xanh", "Ưu tiên xe khẩn cấp tức thời (0s delay dọn đường)."),
        ("Bù nợ xanh", "Hoàn trả thời lượng công bằng cho các hướng bị cắt.")
    ], "Lệnh pha: SignalCommands(phase, dur)"),

    ("Động Cơ Mô Phỏng", "packages/sumo-engine", [
        ("TraCI Protocol", "Giao tiếp Socket tần số 10 Hz (Delta_t = 0.1s)."),
        ("3 Mạng lưới", "Kiểm thử Arterial Grid 3x2, Highway Corridor, Mix."),
        ("Động học xe", "Mô hình Krauss Car-Following & Dual-Ring rẽ trái."),
        ("Đo kiểm HCM", "Thu thập độ trễ Control Delay và thông lượng (Throughput).")
    ], "Dòng telemetry: TickData (10 Hz)"),

    ("Nền Tảng Vận Hành", "backend & frontend", [
        ("FastAPI Engine", "Bọc timeout socket khử TCP backpressure, nén 45% JSON."),
        ("Next.js 14 Canvas", "Bản đồ nhiệt trực quan, render telemetry thời gian thực."),
        ("Simulation Lab", "Đua chính sách đối đầu song song (Fixed vs Adaptive)."),
        ("Groq Copilot", "Trợ lý LLM giải trình nguyên nhân chuyển pha đèn.")
    ], "UX: Giám sát & Điều hành tức thời")
]

col_w = Inches(2.78)
for i, (title, pkg, items, out_text) in enumerate(layers):
    c_left = Inches(0.8 + i * (2.78 + 0.2))
    if i > 0:
        div = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.1), Inches(2.1), Inches(0.015), Inches(4.3))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()

    c_box = s3.shapes.add_textbox(c_left, Inches(2.1), col_w, Inches(4.3))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True
    p1 = tf_c.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = INK_NAVY
    p2 = tf_c.add_paragraph()
    p2.text = pkg
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9)
    p2.font.color.rgb = INK_LIGHT_NAVY
    p2.space_before = Pt(2)
    p2.space_after = Pt(10)
    for lead, desc in items:
        pi = tf_c.add_paragraph()
        pi.text = f"• {lead}: {desc}"
        pi.font.name = FONT_BODY
        pi.font.size = Pt(9.8)
        pi.font.color.rgb = INK_NAVY
        pi.space_before = Pt(4)
    po = tf_c.add_paragraph()
    po.text = f"► {out_text}"
    po.font.name = FONT_HEADING
    po.font.size = Pt(9)
    po.font.bold = True
    po.font.color.rgb = INK_LIGHT_NAVY
    po.space_before = Pt(14)

note_box = s3.shapes.add_textbox(Inches(0.8), Inches(6.52), Inches(11.733), Inches(0.35))
p = note_box.text_frame.paragraphs[0]
p.text = "NGUYÊN TẮC THIẾT KẾ DECOUPLED: Tách rời hoàn toàn cảm biến và điều khiển; sẵn sàng chuyển giao nguồn camera RTSP thực địa mà không phải chỉnh sửa giải thuật cốt lõi."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = INK_SLATE

add_footer(s3, 3)

# ==============================================================================
# SLIDE 4: DỮ LIỆU TỔNG HỢP CARLA 10K & CÂN BẰNG LỚP
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_bg(s4)
add_header(s4, "02 // THỊ GIÁC MÁY TÍNH", "Bộ Dữ Liệu Tổng Hợp CARLA 10k & Cân Bằng Lớp", "Khắc phục triệt để Domain Shift và mất cân bằng lớp dữ liệu cào web bằng Simulator 3D.")

ds_cards = [
    ("QUY MÔ DỮ LIỆU & ĐỘ PHÂN GIẢI", [
        ("Tổng số lượng ảnh", "10,064 ảnh chất lượng cao photorealistic trích xuất từ CARLA 0.9.16."),
        ("Độ phân giải chuẩn", "1920x1080 Full HD với ground-truth bounding box 2D và 3D."),
        ("Độ bao phủ đô thị", "Bao trùm các ngã tư, bùng binh, đường cao tốc và nhánh nối On-Ramp.")
    ]),
    ("ĐA DẠNG HÓA 13 ĐIỀU KIỆN THỜI TIẾT", [
        ("Thời gian trong ngày", "Ban ngày nắng gắt, hoàng hôn, chập tối và ban đêm ánh sáng đèn đường."),
        ("Hiện tượng thời tiết", "Trời quang, mưa nhỏ, mưa rào ngập mặt đường, sương mù dày đặc."),
        ("Độ bền bỉ mô hình", "Giúp mạng neural nhận diện chuẩn xác khi camera thực địa bị mờ nhòe nước mưa.")
    ]),
    ("KỸ THUẬT CÂN BẰNG LỚP (SPAWNER)", [
        ("Vấn đề dữ liệu cào", "Xe buýt, xe cứu thương, xe cảnh sát chỉ chiếm < 2% tần suất tự nhiên."),
        ("Giải pháp Spawner", "Cấu hình bộ sinh xe nhân tạo tăng tỷ lệ xe hiếm lên gấp 2x - 3x."),
        ("Kết quả thực nghiệm", "Recall nhận diện xe buýt tăng vọt từ 5.9% lên mức 92.0%.")
    ])
]

# Metrics ribbon on top
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
            p.space_before = Pt(6)

add_footer(s4, 4)

# ==============================================================================
# SLIDE 5: MÔ HÌNH YOLOV11M & HÀM MẤT MÁT ĐA NHIỆM
# ==============================================================================
create_formula_slide_2col(
    slide_num=5,
    kicker="02 // THỊ GIÁC MÁY TÍNH",
    title="Mô Hình YOLOv11m, Cấu Hình Huấn Luyện & Hàm Mất Mát",
    subtitle="Huấn luyện 100 epochs trên GPU NVIDIA L40S với hàm mục tiêu đa nhiệm kết hợp CIoU, BCE và DFL.",
    formula_key="loss_total",
    eq_label="[Eq. 01]",
    col1_data=("CẤU HÌNH HUẤN LUYỆN (TRAINING CONFIG)", [
        ("Mô hình kiến trúc", "YOLOv11m (Medium) với 20.06M tham số, checkpoint dung lượng 40.5 MB."),
        ("Phần cứng huấn luyện", "GPU NVIDIA L40S (48GB VRAM), huấn luyện 100 Epochs hoàn chỉnh."),
        ("Lịch trình tốc độ học (LR)", "Warmup 3 epochs đầu (từ 0 lên eta_0), sau đó giảm tuyến tính (Linear Decay)."),
        ("Tối ưu hóa bộ nhớ", "Kỹ thuật Mixed Precision FP16 và Optimizer AdamW (Weight Decay 0.0005).")
    ]),
    col2_data=("3 HÀM MẤT MÁT THÀNH PHẦN (LOSS FORMULATION)", [
        ("CIoU Loss (Trọng số 7.5)", "Tối ưu hóa diện tích IoU, phạt khoảng cách tâm Euclid và sai lệch tỷ lệ khung hình."),
        ("BCE with Logits (Trọng số 0.5)", "Phân loại độc lập cho K = 7 lớp xe, triệt tiêu hiện tượng áp chế xác suất giữa các lớp."),
        ("DFL Loss (Trọng số 1.5)", "Học phân phối xác suất liên tục của biên hộp bao, bù trừ hiện tượng xe bị che khuất."),
        ("Cân bằng gradient", "Bộ 3 trọng số [7.5, 0.5, 1.5] giúp mạng nơ-ron định vị hộp bao cực kỳ chuẩn xác.")
    ])
)

# ==============================================================================
# SLIDE 6: KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH (CV BENCHMARK) & VISUAL
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_bg(s6)
add_header(s6, "02 // THỊ GIÁC MÁY TÍNH", "Kết Quả Đánh Giá Mô Hình & Kiểm Thử Thị Giác", "Đạt mAP@50 = 94.91% trên 7 lớp xe đô thị và tốc độ 27.7 FPS đáp ứng hoàn toàn điều kiện thời gian thực.")

# Left (44%): Table & Checkpoint
t_box = s6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.15), Inches(0.35))
p = t_box.text_frame.paragraphs[0]
p.text = "KẾT QUẢ ĐO KIỂM MÔ HÌNH (CV BENCHMARK METRICS)"
p.font.name = FONT_HEADING
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = INK_NAVY

table_shape = s6.shapes.add_table(5, 3, Inches(0.8), Inches(2.05), Inches(5.15), Inches(2.4))
tbl = table_shape.table
tbl.columns[0].width = Inches(1.4)
tbl.columns[1].width = Inches(1.0)
tbl.columns[2].width = Inches(2.75)

headers = ["Chỉ số", "Kết quả", "Ý nghĩa kỹ thuật"]
for c, h in enumerate(headers):
    cell = tbl.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = TINT_BAR
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY

rows_data = [
    ("Precision (P)", "96.98%", "Triệt tiêu tối đa báo động giả"),
    ("Recall (R)", "89.67%", "Recall xe buýt tăng từ 5.9% lên 92.0%"),
    ("mAP@50", "94.91%", "7 lớp phương tiện giao thông đô thị"),
    ("mAP@50-95", "86.49%", "Định vị hộp bao (Bounding Box) cực chuẩn")
]

for r, (metric, val, note) in enumerate(rows_data, start=1):
    for c, text in enumerate([metric, val, note]):
        cell = tbl.cell(r, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BG_WHITE if r % 2 == 0 else TINT_SURFACE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        if c == 1:
            p.font.bold = True
            p.font.color.rgb = INK_LIGHT_NAVY
        else:
            p.font.color.rgb = INK_NAVY

cp_box = s6.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(5.15), Inches(1.9))
tf = cp_box.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THÔNG SỐ MÔ HÌNH VÀ CHECKPOINT"
p.font.name = FONT_HEADING
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = INK_NAVY
specs = [
    ("Checkpoint Path", "packages/cv-pipeline/models/best.pt"),
    ("Dung lượng file", "40.5 MB (20.06M tham số mô hình)"),
    ("Huấn luyện", "100 Epochs trên GPU NVIDIA L40S (48GB VRAM)"),
    ("Tốc độ xử lý", "27.7 FPS tại độ phân giải 1920x1080 (đạt chuẩn Real-Time)")
]
for idx, (k, v) in enumerate(specs):
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = INK_SLATE
    p.space_before = Pt(3)

# Right (56%): Real-world detection image
det_img_path = "docs/images/realworld-detections.png"
if os.path.exists(det_img_path):
    pic = s6.shapes.add_picture(det_img_path, Inches(6.35), Inches(1.6), width=Inches(6.183), height=Inches(4.8))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s6.shapes.add_textbox(Inches(6.35), Inches(6.48), Inches(6.183), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Kiểm thử nhận diện đồng thời 7 lớp xe trong điều kiện trời mưa và ánh sáng thực tế phức tạp"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s6, 6)

# ==============================================================================
# SLIDE 7: TRACKING: ĐỊNH DANH LIÊN TỤC VỚI BYTETRACK
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_bg(s7)
add_header(s7, "03 // THEO DÕI ĐA ĐỐI TƯỢNG", "Tracking: Định Danh Liên Tục Với ByteTrack", "Khắc phục triệt để hiện tượng nhảy ID (ID Switches) bằng kỹ thuật ghép nối Hungarian 2 tầng.")

# 3 Pipeline Step Cards
track_steps = [
    ("BƯỚC 1: PHÂN LOẠI ĐỘ TIN CẬY", [
        ("Bộ phát hiện YOLOv11m", "Xuất ra danh sách Bounding Boxes kèm điểm tin cậy (Confidence Score)."),
        ("Tách ngưỡng High/Low Score", "Phân chia hộp bao thành 2 tập hợp: Điểm cao (score >= 0.5) và Điểm thấp (score < 0.5)."),
        ("Không loại bỏ sớm", "Khác biệt cốt lõi: Không vứt bỏ các detection điểm thấp bị mờ nhòe như thuật toán SORT truyền thống.")
    ]),
    ("BƯỚC 2: GHÉP TẦNG 1 (HIGH-SCORE)", [
        ("Ghép nối ưu tiên", "Ghép các phát hiện rõ nét (score >= 0.5) với các vệt theo dõi (Tracks) đang hoạt động."),
        ("Ma trận khoảng cách IoU", "Tính toán mức độ trùng khớp không gian giữa vị trí dự báo Kalman và hộp bao phát hiện."),
        ("Khởi tạo vệt mới", "Các detection điểm cao chưa ghép được sẽ được khởi tạo thành các ứng viên theo dõi mới.")
    ]),
    ("BƯỚC 3: GHÉP TẦNG 2 (LOW-SCORE)", [
        ("Cứu vãn đối tượng bị che khuất", "Lấy các vệt theo dõi chưa tìm được cặp ghép tiếp với tập detection điểm thấp."),
        ("Duy trì ID xuyên suốt", "Giúp xe máy đi sau xe tải hoặc xe đi qua bóng cây râm vẫn giữ nguyên vẹn ID."),
        ("Kết quả thực nghiệm", "Giảm hơn 80% hiện tượng nhảy ID khi xe dừng chờ san sát nhau tại nút giao.")
    ])
]

# Top pipeline sequence bar with clean background box
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
            p.space_before = Pt(7)

add_footer(s7, 7)

# ==============================================================================
# SLIDE 8: BỘ LỌC KALMAN 8 CHIỀU KHỬ NHIỄU & DỰ BÁO ĐỘNG HỌC
# ==============================================================================
create_formula_slide_2col(
    slide_num=8,
    kicker="03 // THEO DÕI ĐA ĐỐI TƯỢNG",
    title="Bộ Lọc Kalman 8 Chiều: Lọc Nhiễu Quỹ Đạo & Dự Báo Động Học",
    subtitle="Mô hình chuyển động vận tốc không đổi (Constant Velocity) với vector trạng thái 8 chiều làm mịn quỹ đạo xe.",
    formula_key="kalman",
    eq_label="[Eq. 02]",
    col1_data=("VECTOR TRẠNG THÁI 8 CHIỀU (x_t)", [
        ("Tọa độ tâm hình học (X_c, Y_c)", "Xác định vị trí trung tâm của phương tiện trên mặt phẳng hình ảnh."),
        ("Kích thước hình học (a, h)", "a là tỷ lệ khung hình (w/h), h là chiều cao của hộp bao Bounding Box."),
        ("Vận tốc biến thiên (X_dot, Y_dot, a_dot, h_dot)", "Đạo hàm bậc nhất thể hiện hướng và tốc độ dịch chuyển của phương tiện."),
        ("Mô hình chuyển động tuyến tính", "Ma trận chuyển trạng thái F dự báo vị trí xe ở khung hình t+1 trước khi nhận kết quả dò.")
    ]),
    col2_data=("CƠ CHẾ DỰ BÁO VÀ LỌC NHIỄU CẢM BIẾN", [
        ("Làm mịn quỹ đạo di chuyển", "Triệt tiêu hiện tượng rung giật Bounding Box phát sinh do nhiễu cảm biến hình ảnh."),
        ("Dự báo khi mất dấu tạm thời", "Nếu xe bị che khuất trong 1-3 frames, Kalman tiếp tục dự báo vị trí theo quán tính vận tốc."),
        ("Ma trận hiệp phương sai sai số P", "Tự động điều chỉnh độ lợi Kalman Gain K_t dựa trên độ tin cậy của phép đo thực tế."),
        ("Cơ sở dữ liệu quỹ đạo", "Cung cấp chuỗi tọa độ liên tục phục vụ tính toán vận tốc km/h và hướng rẽ.")
    ])
)

# ==============================================================================
# SLIDE 9: HÌNH HỌC KHÔNG GIAN: MA TRẬN HOMOGRAPHY MẶT ĐẤT H
# ==============================================================================
create_formula_slide_2col(
    slide_num=9,
    kicker="04 // HÌNH HỌC & ĐO ĐẠC",
    title="Hình Học Không Gian: Ma Trận Homography Mặt Đất H",
    subtitle="Chiếu phối cảnh từ không gian điểm ảnh 2D (u, v) sang tọa độ phẳng thế giới thực (X_w, Y_w) theo đơn vị mét.",
    formula_key="homography",
    eq_label="[Eq. 03]",
    col1_data=("NGUYÊN LÝ HÌNH HỌC PHỐI CẢNH (PERSPECTIVE)", [
        ("Hiện tượng méo phối cảnh", "Điểm ảnh pixel không đồng đều: 10 pixel ở gần bằng 0.5m, nhưng ở xa có thể bằng 5.0m."),
        ("Mặt phẳng mặt đường (Z_w = 0)", "Giả định toàn bộ điểm tiếp xúc bánh xe của phương tiện đều nằm trên mặt phẳng lòng đường."),
        ("Phép biến đổi xạ ảnh 1-1", "Ánh xạ trực tiếp từ tọa độ pixel (u, v) sang tọa độ thực địa (X_w, Y_w) không phụ thuộc góc máy."),
        ("Hiệu chuẩn 4 điểm mốc", "Ma trận H 3x3 gồm 8 bậc tự do được xác định chính xác qua 4 điểm đo thực địa đã biết cự ly.")
    ]),
    col2_data=("ỨNG DỤNG ĐO ĐẠC GIAO THÔNG CHUẨN XÁC", [
        ("Đo cự ly vật lý (Headway)", "Đo khoảng cách vật lý chuẩn xác theo mét giữa hai xe liên tiếp trên làn đường."),
        ("Tính toán vận tốc tuyệt đối", "Cơ sở toán học duy nhất để đổi quãng đường dịch chuyển pixel sang vận tốc km/h."),
        ("Phát hiện xung đột ngã tư", "Xác định nguy cơ va chạm dựa trên khoảng cách mét thực giữa các luồng xe giao cắt."),
        ("Độc lập với vị trí đặt camera", "Cho phép hoán đổi vị trí camera cột đèn mà chỉ cần hiệu chuẩn lại ma trận H.")
    ])
)

# ==============================================================================
# SLIDE 10: ƯỚC LƯỢNG VẬN TỐC THỰC & TIÊU CHUẨN XE CHỜ ĐÈN ĐỎ
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_bg(s10)
add_header(s10, "04 // HÌNH HỌC & ĐO ĐẠC", "Ước Lượng Vận Tốc Thực & Tiêu Chuẩn Xe Chờ Đèn Đỏ", "Bộ lọc trượt M = 5 frames và tiêu chuẩn kép (Vận tốc < 2.0 m/s trong thời gian tau >= 2.0s) phát hiện hàng đợi.")

stage10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.35))
stage10.fill.solid()
stage10.fill.fore_color.rgb = TINT_SURFACE
stage10.line.color.rgb = BORDER_BOX
stage10.line.width = Pt(0.75)

s10.shapes.add_picture(F['speed'], Inches(1.5), Inches(1.78), width=Inches(9.0))

eq_b = s10.shapes.add_textbox(Inches(10.8), Inches(1.75), Inches(1.5), Inches(0.3))
p = eq_b.text_frame.paragraphs[0]
p.text = "[Eq. 04]"
p.font.name = FONT_CODE
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY
p.alignment = PP_ALIGN.RIGHT

# Left (46%): 2 Cards
c_w10 = Inches(5.4)
cards10 = [
    ("BỘ LỌC VẬN TỐC TRƯỢT M = 5 FRAMES", [
        ("Lấy mẫu liên tục", "Tính quãng đường dịch chuyển Delta_d trên mặt phẳng Homography qua từng frame ảnh."),
        ("Trung bình động trượt", "Lấy trung bình vận tốc trên cửa sổ M = 5 frames để khử nhiễu rung giật Bounding Box."),
        ("Chuẩn hóa thời gian", "Chia cho khoảng thời gian Delta_t * Delta_k đảm bảo vận tốc chính xác theo đơn vị m/s.")
    ]),
    ("TIÊU CHUẨN KÉP XÁC NHẬN XE DỪNG CHỜ (QUEUE)", [
        ("Ngưỡng vận tốc v < 2.0 m/s", "Phương tiện giảm tốc độ xuống dưới 7.2 km/h được đưa vào diện nghi vấn chờ."),
        ("Ngưỡng thời gian tau >= 2.0 s", "Phải duy trì trạng thái chậm liên tục ít nhất 2 giây để tránh báo động giả."),
        ("Khử báo động giả", "Loại trừ chính xác các trường hợp xe chỉ giảm tốc độ để tránh người đi bộ hoặc rẽ.")
    ])
]

y_pos10 = Inches(3.2)
for title, items in cards10:
    card = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos10, c_w10, Inches(1.75))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos10, c_w10, Inches(0.38))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s10.shapes.add_textbox(Inches(0.95), y_pos10 + Inches(0.06), c_w10 - Inches(0.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s10.shapes.add_textbox(Inches(0.95), y_pos10 + Inches(0.45), c_w10 - Inches(0.3), Inches(1.2))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.2)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(3)
    y_pos10 += Inches(1.9)

# Right (54%): Visual Figure
col_img_path = "docs/images/collision-detection.png"
if os.path.exists(col_img_path):
    pic = s10.shapes.add_picture(col_img_path, Inches(6.5), Inches(3.2), width=Inches(6.033), height=Inches(3.5))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s10.shapes.add_textbox(Inches(6.5), Inches(6.75), Inches(6.033), Inches(0.3))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Nhận diện xe dừng chờ đèn đỏ và phát hiện nguy cơ va chạm giao cắt tức thời"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s10, 10)

# ==============================================================================
# SLIDE 11: ĐIỀU KHIỂN THÍCH NGHI: HÀNG ĐỢI TỒN DƯ & LỌC EMA
# ==============================================================================
create_formula_slide_2col(
    slide_num=11,
    kicker="05 // ĐIỀU KHIỂN THÍCH NGHI",
    title="Điều Khiển Thích Nghi: Nguyên Lý Hàng Đợi Tồn Dư & Bộ Lọc EMA",
    subtitle="Leftover-Queue Actuated Control: Đo lượng xe tồn đọng tại thời điểm chớm vàng để san sẻ thời gian xanh.",
    formula_key="ema",
    eq_label="[Eq. 05]",
    col1_data=("NGUYÊN LÝ ĐO LƯỜNG TẠI THỜI ĐIỂM CHỚM VÀNG", [
        ("Thời điểm đo đạc then chốt", "Số lượng xe dừng chờ Q_i(k) được chốt chính xác tại khoảnh khắc đèn chuyển từ Xanh sang Vàng."),
        ("Ý nghĩa vật lý dòng xe", "Đại diện cho lượng nhu cầu giao thông chưa được giải tỏa hết trong pha xanh vừa kết thúc."),
        ("Không phụ thuộc dự báo xa", "Loại bỏ hoàn toàn sự phụ thuộc vào các mô hình dự báo lưu lượng dài hạn thiếu chính xác."),
        ("Phản ứng tức thời theo chu kỳ", "Nhận biết ngay lập tức nhánh giao thông nào đang bị quá tải để xử lý trong chu kỳ kế tiếp.")
    ]),
    col2_data=("BỘ LỌC THÔNG THẤP EMA (ALPHA = 0.7)", [
        ("Trọng số hiện tại (70%)", "Phản ứng nhạy bén với sự gia tăng đột biến của dòng phương tiện trong chu kỳ vừa qua."),
        ("Trọng số lịch sử (30%)", "Kế thừa trạng thái hàng đợi tích lũy từ chu kỳ k-1 nhằm duy trì tính ổn định của hệ thống."),
        ("Khử nhiễu ngẫu nhiên", "Ngăn chặn thuật toán phản ứng quá mức với một chiếc xe đi chậm hoặc sự cố tạm thời."),
        ("Độ ổn định chu kỳ", "Giúp hệ số dao động thời lượng xanh giảm hơn 65% so với việc dùng trực tiếp số đo thô Q_i.")
    ])
)

# ==============================================================================
# SLIDE 12: ĐIỀU KHIỂN THÍCH NGHI: TÁI PHÂN BỔ & RÀNG BUỘC AN TOÀN
# ==============================================================================
create_formula_slide_2col(
    slide_num=12,
    kicker="05 // ĐIỀU KHIỂN THÍCH NGHI",
    title="Điều Khiển Thích Nghi: Tái Phân Bổ Thời Gian Xanh & Khung An Toàn",
    subtitle="Bù thời gian xanh theo tỷ trọng tồn dư và tuân thủ tuyệt đối khung an toàn cho người đi bộ.",
    formula_key="redist",
    eq_label="[Eq. 06]",
    col1_data=("PHÂN NHÓM TRẠNG THÁI & TÁI PHÂN BỔ THEO TỶ TRỌNG", [
        ("Nhóm thiếu (Undersupplied U)", "Gồm các pha có hàng đợi tồn dư S_i(k) > 0 (vẫn còn xe kẹt sau khi hết đèn xanh)."),
        ("Nhóm thỏa mãn (Satisfied S)", "Gồm các pha có hàng đợi tồn dư S_j(k) <= 0 (đã giải phóng hết xe thông thoáng)."),
        ("Trích xuất ngân sách R", "Rút phần thời gian xanh dư thừa từ nhóm S (tối đa R_max = 12.0s mỗi chu kỳ)."),
        ("Tái phân bổ theo trọng số w_i", "Nhánh nào kẹt nặng hơn nhận thêm nhiều thời gian hơn: w_i = S_i / sum(S_m).")
    ]),
    col2_data=("RÀNG BUỘC AN TOÀN TUYỆT ĐỐI (SAFETY CONSTRAINTS)", [
        ("Thời lượng tối thiểu g_min = 10.0s", "Đảm bảo tuyệt đối thời gian cho người đi bộ qua đường an toàn theo quy chuẩn kỹ thuật."),
        ("Thời lượng tối đa g_max = 50.0s", "Ngăn chặn tình trạng một nhánh giao thông độc quyền đèn xanh gây nghẽn các hướng khác."),
        ("Bảo toàn chu kỳ giao lộ", "Tổng thời lượng phân bổ lại bằng đúng thời gian thu hồi, bảo toàn tổng chu kỳ điều khiển."),
        ("Hiệu quả thực nghiệm", "Giảm tới 54% thời gian dừng chờ xe và tăng 28% thông lượng mạng lưới.")
    ])
)

# ==============================================================================
# SLIDE 13: ĐIỀU TIẾT CAO TỐC ALINEA
# ==============================================================================
create_formula_slide_2col(
    slide_num=13,
    kicker="06 // ĐIỀU TIẾT CAO TỐC",
    title="Điều Tiết Cao Tốc: Luật Hồi Tiếp Tích Phân ALINEA",
    subtitle="Duy trì mật độ tuyến chính dưới điểm sụp đổ thông lượng (Capacity Drop) bằng đèn tín hiệu On-Ramp Metering.",
    formula_key="alinea",
    eq_label="[Eq. 07]",
    col1_data=("NGUYÊN LÝ ĐIỀU KHIỂN HỒI TIẾP VÒNG KÍN", [
        ("Mật độ mục tiêu o* = 20%", "Điểm mật độ chiếm dụng lý tưởng giữ cho tuyến chính cao tốc đạt thông lượng tối đa."),
        ("Cảm biến hạ lưu ô(k)", "Đo mật độ thực tế tại hạ lưu điểm hòa dòng và hồi tiếp về bộ điều khiển sau mỗi 10 giây."),
        ("Cơ chế tích phân (I-Controller)", "Tự động bù trừ sai lệch mật độ mà không để lại sai số xác lập (zero steady-state error)."),
        ("Hệ số khuếch đại K_R = 70.0", "Hệ số chuẩn quốc tế đảm bảo hệ thống phản ứng nhanh nhưng không bị dao động kích động.")
    ]),
    col2_data=("QUY ĐỔI SANG THỜI LƯỢNG ĐÈN METERING", [
        ("Biên độ điều tiết [200, 1200] veh/h", "Không đóng hoàn toàn nhánh nối (tối thiểu 200) và không cấp quá năng lực 1 làn (tối đa 1200)."),
        ("Quy đổi chu kỳ T_cycle = 3600 / r(k)", "Tính toán chu kỳ đèn để cấp đúng số lượng xe nhập làn mong muốn."),
        ("Cố định thời lượng xanh 2.0s", "Chỉ cho phép duy nhất 1 xe nhập làn trong mỗi chu kỳ (One vehicle per green rule)."),
        ("Thời lượng đỏ điều biến", "Thời gian đỏ t_red co giãn tự động để giãn cách phương tiện trước khi hòa vào dòng chính.")
    ])
)

# ==============================================================================
# SLIDE 14: CƠ CHẾ CHỐNG TRÀN NHÁNH NỐI (SPILLBACK OVERRIDE)
# ==============================================================================
s14 = prs.slides.add_slide(blank_layout)
set_bg(s14)
add_header(s14, "06 // ĐIỀU TIẾT CAO TỐC", "Điều Tiết Cao Tốc: Cơ Chế Chống Tràn Nhánh Nối (Spillback)", "Mở xả trạm tối đa khi hàng đợi nhánh nối vượt quá 30 xe nhằm ngăn chặn nghẽn lan tỏa vào nội đô.")

stage14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.3))
stage14.fill.solid()
stage14.fill.fore_color.rgb = TINT_SURFACE
stage14.line.color.rgb = BORDER_BOX
stage14.line.width = Pt(0.75)

s14.shapes.add_picture(F['spillback'], Inches(1.5), Inches(1.78), width=Inches(9.0))

eq_b = s14.shapes.add_textbox(Inches(10.8), Inches(1.75), Inches(1.5), Inches(0.3))
p = eq_b.text_frame.paragraphs[0]
p.text = "[Rule. 01]"
p.font.name = FONT_CODE
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY
p.alignment = PP_ALIGN.RIGHT

# Left (48%): Cards
cards14 = [
    ("NGUY CƠ NGHẼN TRÀN NGƯỢC (SPILLBACK RISK)", [
        ("Nghẽn tắc đô thị phụ cận", "Khi đèn Metering giữ đỏ quá lâu, hàng xe xếp dài trên nhánh nối tràn ra các giao lộ nội đô lân cận."),
        ("Gây tê liệt dây chuyền", "Làm mất khả năng thông hành của đường gom và ngã tư đèn tín hiệu dẫn vào cao tốc."),
        ("Cần cơ chế ghi đè khẩn cấp", "Phải ưu tiên giải tỏa nhánh nối khi chiều dài hàng đợi chạm ngưỡng nguy hiểm.")
    ]),
    ("CƠ CHẾ GHI ĐÈ KHẨN CẤP (OVERRIDE)", [
        ("Ngưỡng kích hoạt Q_ramp >= 30 xe", "Cảm biến nhánh nối phát hiện số xe dừng chờ vượt quá 30 phương tiện."),
        ("Ghi đè lưu lượng r_max = 1200 veh/h", "Tạm thời vô hiệu hóa luật ALINEA, mở đèn xanh tối đa để xả nhanh dòng xe."),
        ("Tự động phục hồi", "Khi hàng đợi giảm xuống dưới mức an toàn, hệ thống tự động trả quyền điều khiển về cho ALINEA.")
    ])
]

y_pos14 = Inches(3.15)
for title, items in cards14:
    card = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos14, Inches(5.6), Inches(1.75))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos14, Inches(5.6), Inches(0.38))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s14.shapes.add_textbox(Inches(0.95), y_pos14 + Inches(0.06), Inches(5.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s14.shapes.add_textbox(Inches(0.95), y_pos14 + Inches(0.45), Inches(5.3), Inches(1.2))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.2)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(3)
    y_pos14 += Inches(1.9)

# Right (52%): Native Graphic Box
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
p.text = "• Bình thường: ALINEA xiết van đèn đỏ khi mật độ ô(k) cao chống sụp đổ lưu lượng tuyến chính.\n• Khi kẹt nhánh nối: Tự động ghi đè xả trạm để cứu mạng lưới giao lộ nội đô lân cận."
p.font.name = FONT_BODY
p.font.size = Pt(8.6)
p.font.italic = True
p.font.color.rgb = INK_SLATE

add_footer(s14, 14)

# ==============================================================================
# SLIDE 15: CƠ CHẾ ƯU TIÊN XE KHẨN CẤP: LÀN SÓNG XANH TỨC THỜI
# ==============================================================================
create_formula_slide_2col(
    slide_num=15,
    kicker="07 // ƯU TIÊN KHẨN CẤP",
    title="Cơ Chế Ưu Tiên Xe Khẩn Cấp: Làn Sóng Xanh Tức Thời (0s Delay)",
    subtitle="Emergency Vehicle Preemption: Nhận diện phương tiện ưu tiên và cưỡng bức chuyển pha dọn đường tức thời.",
    formula_key="preempt",
    eq_label="[Rule. 02]",
    col1_data=("CƠ CHẾ KÍCH HOẠT LÀN SÓNG XANH TỨC THỜI", [
        ("Nguồn phát hiện đa kênh", "Nhận diện từ camera AI YOLOv11m (Ambulance, Fire Truck, Police) hoặc tín hiệu GPS/TraCI."),
        ("Xác định hướng di chuyển", "Hệ thống tự động tra cứu lộ trình và nút giao mục tiêu J nằm trên đường đi của xe."),
        ("Cưỡng bức chuyển pha phi_EV", "Ngay lập tức cắt ngắn pha đèn hiện tại để chuyển sang pha xanh phục vụ xe ưu tiên."),
        ("Độ trễ bằng 0 giây", "Xe khẩn cấp lưu thông qua nút giao với vận tốc tối đa mà không phải giảm tốc hoặc dừng chờ.")
    ]),
    col2_data=("QUY TRÌNH DỌN ĐƯỜNG AN TOÀN", [
        ("Thời gian vàng tối thiểu", "Vẫn duy trì khoảng đệm vàng 3.0s cho các luồng xe trực giao kịp dừng lại an toàn."),
        ("Dọn sạch hàng xe phía trước", "Bật đèn xanh sớm trước khi xe đến để xả hết các phương tiện đang dừng chắn lối."),
        ("Khóa hướng rẽ xung đột", "Khóa cứng các hướng rẽ cắt ngang hành lang di chuyển của xe khẩn cấp."),
        ("Theo dõi thoát nút", "Giữ pha xanh dọn đường cho đến khi xe ưu tiên vừa thoát khỏi tâm nút giao.")
    ])
)

# ==============================================================================
# SLIDE 16: HOÀN TRẢ CÔNG NỢ THỜI GIAN XANH CÔNG BẰNG
# ==============================================================================
create_formula_slide_2col(
    slide_num=16,
    kicker="07 // ƯU TIÊN KHẨN CẤP",
    title="Cơ Chế Hoàn Trả Công Nợ Thời Gian Xanh Công Bằng",
    subtitle="Starvation Debt Compensation: Tích lũy thiệt hại của các hướng bị cắt và cấp bù thời gian xanh sau sự cố.",
    formula_key="debt",
    eq_label="[Eq. 08]",
    col1_data=("SỔ NỢ THỜI GIAN GIAO LỘ D_d(J)", [
        ("Thiệt hại các hướng trực giao", "Các luồng xe bị cưỡng bức dừng đèn đỏ đột ngột trong suốt thời gian ưu tiên Delta_t_preempt."),
        ("Tích lũy công nợ toán học", "Hệ thống ghi nhận chính xác từng giây bị tước quyền ưu tiên vào biến nợ D_d(J)."),
        ("Tính minh bạch điều hành", "Đảm bảo mọi hướng giao thông bị ảnh hưởng đều được hệ thống ghi nhận công bằng."),
        ("Tránh bỏ quên nhánh phụ", "Ngăn chặn tình trạng nhánh đường phụ bị bỏ đói dẫn đến ùn tắc kéo dài hàng giờ.")
    ]),
    col2_data=("THUẬT TOÁN BÙ NỢ CÔNG BẰNG t_comp", [
        ("Xác định hướng chịu thiệt hại lớn nhất d*", "Quét toàn bộ giao lộ để tìm hướng có chỉ số công nợ tích lũy cao nhất."),
        ("Cấp thời lượng bù t_comp = min(D_d*, 15.0s)", "Giới hạn trần bù 15.0 giây để tránh việc bù quá mức gây sốc ngược chu kỳ."),
        ("Giải tỏa ùn ứ tức thì", "Nhanh chóng xả sạch hàng đợi tồn đọng phát sinh trong thời gian phục vụ xe ưu tiên."),
        ("Khôi phục cân bằng 1-2 chu kỳ", "Mạng lưới nút giao trở lại trạng thái lưu thông bình thường chỉ sau 1 đến 2 chu kỳ đèn.")
    ])
)

# ==============================================================================
# SLIDE 17: MÔ PHỎNG VI MÔ SUMO & 3 MẠNG LƯỚI ĐÃ XÂY DỰNG
# ==============================================================================
s17 = prs.slides.add_slide(blank_layout)
set_bg(s17)
add_header(s17, "08 // MÔ PHỎNG VI MÔ SUMO", "Mô Phỏng Vi Mô SUMO & 3 Mạng Lưới Đã Xây Dựng", "Tích hợp TraCI Socket Protocol 10 Hz và 3 mô hình mạng lưới kiểm thử chuyên biệt.")

networks = [
    ("1. MẠNG ARTERIAL GRID (3x2)", "docs/images/arterial-grid.png", "6 Nút giao liên hoàn", [
        ("Mục tiêu kiểm thử", "Kiểm thử điều phối đèn đa nút giao liên hoàn."),
        ("Xung đột rẽ trái", "Giải quyết xung đột rẽ trái pha bảo hộ (Protected)."),
        ("Đồng bộ chu kỳ", "Đồng bộ tín hiệu Dual-Ring 2 chiều giao thông.")
    ]),
    ("2. MẠNG HIGHWAY CORRIDOR", "docs/images/highway-corridor.png", "Cao tốc 3 làn & 2 On-Ramp", [
        ("Mục tiêu kiểm thử", "Kiểm thử giải thuật ALINEA điều tiết nhập làn."),
        ("Chống nghẽn tắc", "Ngăn chặn tắc nghẽn sụp đổ lưu lượng tuyến chính."),
        ("Khai thác luồng", "Khai thác tối đa năng lực thông hành điểm hòa dòng.")
    ]),
    ("3. MẠNG KẾT HỢP (COMBINED)", "docs/images/combined-network.png", "Hệ thống đô thị tích hợp", [
        ("Nội đô - Cao tốc", "Mô hình kết nối hoàn chỉnh đô thị ra tuyến cao tốc."),
        ("Kiểm thử toàn tải", "Kiểm thử chịu tải toàn diện End-to-End quy mô lớn."),
        ("Dòng xe hỗn hợp", "Mô hình hóa chính xác lưu thông phương tiện hỗn hợp.")
    ])
]

col_w17 = Inches(3.7)
for i, (ntitle, img_p, sub, pts) in enumerate(networks):
    c_left = Inches(0.8 + i * (3.7 + 0.31))
    if i > 0:
        div = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.15), Inches(1.6), Inches(0.015), Inches(4.7))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()
        
    tb = s17.shapes.add_textbox(c_left, Inches(1.6), col_w17, Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = ntitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    p_sub = tb.text_frame.add_paragraph()
    p_sub.text = sub
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = INK_LIGHT_NAVY
    p_sub.space_before = Pt(1)
    
    if os.path.exists(img_p):
        pic = s17.shapes.add_picture(img_p, c_left, Inches(2.3), width=col_w17, height=Inches(2.2))
        pic.line.color.rgb = BORDER_BOX
        pic.line.width = Pt(0.75)
        
    db = s17.shapes.add_textbox(c_left, Inches(4.65), col_w17, Inches(1.7))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    for idx, (lead, txt) in enumerate(pts):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.text = f"• {lead}: {txt}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(4)

div17_b = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.015))
div17_b.fill.solid()
div17_b.fill.fore_color.rgb = HAIRLINE
div17_b.line.fill.background()

tb17_b = s17.shapes.add_textbox(Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.35))
p = tb17_b.text_frame.paragraphs[0]
p.text = "THÔNG SỐ VI MÔ SUMO: TraCI Socket tần số 10 Hz (Delta_t = 0.1s) | Mô hình xe bám đuôi Krauss Car-Following | Cấu hình pha Dual-Ring Permissive Left Turn."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.color.rgb = INK_SLATE

add_footer(s17, 17)

# ==============================================================================
# SLIDE 18: NỀN TẢNG BACKEND: FASTAPI CONCURRENCY & KHỬ BACKPRESSURE
# ==============================================================================
s18 = prs.slides.add_slide(blank_layout)
set_bg(s18)
add_header(s18, "09 // NỀN TẢNG FULL-STACK", "Nền Tảng Backend: FastAPI WebSocket Engine", "Khử triệt để TCP Backpressure và tối ưu hóa nén JSON payload phục vụ truyền phát dữ liệu 10 Hz.")

be_cards = [
    ("KHỬ TCP BACKPRESSURE VỚI TIMEOUT", [
        ("Vấn đề nghẽn cổ chai mạng", "Khi client (trình duyệt) xử lý chậm, bộ đệm TCP bị đầy làm nghẽn ngược luồng mô phỏng SUMO."),
        ("Bọc Socket Timeout tau_ws <= 0.15s", "Nếu client không nhận kịp trong 0.15s, backend chủ động hủy gói tin trễ (drop-stale)."),
        ("Bảo toàn chu kỳ thời gian thực", "Đảm bảo luồng mô phỏng động học luôn duy trì chính xác tần số vi mô 10 Hz.")
    ]),
    ("TỐI ƯU HÓA NÉN PAYLOAD JSON (-45%)", [
        ("Gói tin tick-by-tick khổng lồ", "Mỗi chu kỳ 0.1s gửi hàng trăm tọa độ xe, thông số đèn và telemetry khiến dung lượng ban đầu là 60 KB."),
        ("Rút gọn cấu trúc dữ liệu", "Lược bỏ trường thừa, dùng mảng nén và mã hóa định danh ngắn gọn."),
        ("Dung lượng còn 32 KB", "Giảm 45% băng thông mạng, giảm tải tiêu thụ CPU và render của trình duyệt web.")
    ]),
    ("KIẾN TRÚC BẤT ĐỒNG BỘ ASYNCIO", [
        ("Non-blocking I/O", "Tách riêng luồng điều khiển TraCI Socket của SUMO và luồng phát WebSocket cho người dùng."),
        ("Hỗ trợ đa người dùng (Multi-client)", "Nhiều kỹ sư vận hành có thể cùng mở Dashboard giám sát mà không làm tụt xung nhịp hệ thống."),
        ("Độ trễ truyền dẫn cực thấp", "Độ trễ từ khi mô phỏng tính toán đến khi hiển thị trên màn hình chỉ dưới 15 mili-giây.")
    ])
]

col_w18 = Inches(3.75)
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
    p.alignment = PP_ALIGN.CENTER

add_footer(s18, 18)

# ==============================================================================
# SLIDE 19: GIAO DIỆN VẬN HÀNH: NEXT.JS 14 DASHBOARD & GROQ COPILOT
# ==============================================================================
s19 = prs.slides.add_slide(blank_layout)
set_bg(s19)
add_header(s19, "09 // NỀN TẢNG FULL-STACK", "Giao Diện Vận Hành: Next.js 14 Dashboard & Groq Copilot", "Bản đồ nhiệt trực quan 60 FPS, phòng thí nghiệm đua chính sách đối đầu và trợ lý Groq LLM Copilot.")

dash_img_path = "docs/images/dashboard.png"
if os.path.exists(dash_img_path):
    pic = s19.shapes.add_picture(dash_img_path, Inches(0.8), Inches(1.6), width=Inches(6.6), height=Inches(4.7))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s19.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(6.6), Inches(0.4))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Giao diện Dashboard điều hành: Bản đồ nhiệt trực tiếp, thông số từng nút giao và telemetry vi mô"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

cards19 = [
    ("1. BẢN ĐỒ NHIỆT ĐỘNG HỌC CANVAS", [
        "Render mượt mà hàng nghìn xe và pha tín hiệu đèn ở tốc độ 60 FPS.",
        "Màu sắc trực quan thể hiện mức độ ùn ứ theo thời gian thực (Xanh - Vàng - Đỏ)."
    ]),
    ("2. PHÒNG THÍ NGHIỆM ĐUA CHÍNH SÁCH (LAB)", [
        "Chạy song song 2 phiên mô phỏng đối đầu (Fixed-Time vs Adaptive) cùng seed ngẫu nhiên 42.",
        "Quan sát trực tiếp sự phân hóa hàng đợi và thời gian dừng chờ tích lũy ngay trên màn hình."
    ]),
    ("3. TRỢ LÝ GROQ LLM TRAFFIC COPILOT", [
        "Tích hợp LLM Groq giải thích nguyên nhân chuyển pha đèn bằng ngôn ngữ tự nhiên.",
        "Tự động sinh cảnh báo và khuyến nghị điều phối khi phát hiện điểm nghẽn giao thông bất thường."
    ])
]

y_pos19 = Inches(1.6)
for title, bts in cards19:
    tb = s19.shapes.add_textbox(Inches(7.7), y_pos19, Inches(4.833), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    db = s19.shapes.add_textbox(Inches(7.7), y_pos19 + Inches(0.35), Inches(4.833), Inches(1.1))
    tf = db.text_frame
    tf.word_wrap = True
    for idx, b in enumerate(bts):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {b}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_SLATE
        if idx > 0:
            p.space_before = Pt(4)
    y_pos19 += Inches(1.65)

add_footer(s19, 19)

# ==============================================================================
# SLIDE 20: ĐÁNH GIÁ THỰC NGHIỆM ĐỐI ĐẦU: CHUẨN HCM BENCHMARK
# ==============================================================================
s20 = prs.slides.add_slide(blank_layout)
set_bg(s20)
add_header(s20, "10 // ĐO KIỂM THỰC NGHIỆM", "Kết Quả Thực Nghiệm Đối Đầu: Chuẩn HCM Benchmark", "Đánh giá định lượng trên 5,500 phương tiện: Adaptive AI giảm tới 54% thời gian chờ và tăng 28% thông lượng.")

metrics_s20 = [
    ("-40.5%", "Kịch Bản Cân Bằng (Balanced)", [
        "Thời gian dừng chờ: 65.4 s  ──►  38.9 s",
        "Thông lượng mạng lưới: Cải thiện +14%"
    ]),
    ("-52.3%", "Kịch Bản Lệch Tải (Asymmetric)", [
        "Thời gian dừng chờ: 88.2 s  ──►  42.1 s",
        "Thông lượng mạng lưới: Cải thiện +22%"
    ]),
    ("-54.0%", "Kịch Bản Quá Tải Cực Hạn (Extreme)", [
        "Thời gian dừng chờ: 124.6 s ──►  57.3 s",
        "Thông lượng mạng lưới: Cải thiện +28%"
    ])
]

y_pos20 = Inches(1.8)
for pct, sc_title, details in metrics_s20:
    card = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos20, Inches(5.4), Inches(1.4))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    nb = s20.shapes.add_textbox(Inches(1.0), y_pos20 + Inches(0.2), Inches(1.8), Inches(0.9))
    p = nb.text_frame.paragraphs[0]
    p.text = pct
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb = s20.shapes.add_textbox(Inches(2.8), y_pos20 + Inches(0.18), Inches(3.2), Inches(1.1))
    tf = tb.text_frame
    p1 = tf.paragraphs[0]
    p1.text = sc_title
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = INK_LIGHT_NAVY
    
    for d in details:
        p = tf.add_paragraph()
        p.text = f"• {d}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.2)
        p.font.color.rgb = INK_SLATE
        p.space_before = Pt(2)
        
    y_pos20 += Inches(1.6)

wait_img_path = "docs/images/waiting-time.png"
if os.path.exists(wait_img_path):
    pic = s20.shapes.add_picture(wait_img_path, Inches(6.5), Inches(1.8), width=Inches(6.033), height=Inches(4.6))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s20.shapes.add_textbox(Inches(6.5), Inches(6.5), Inches(6.033), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Biểu đồ phân phối thời gian chờ: Thuật toán Adaptive AI giải phóng mạng lưới nhanh hơn tới 54%"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s20, 20)

# ==============================================================================
# SLIDE 21: MA TRẬN TIẾN ĐỘ 100% & ĐỊNH HƯỚNG 3 HORIZON
# ==============================================================================
s21 = prs.slides.add_slide(blank_layout)
set_bg(s21)
add_header(s21, "11 // TỔNG KẾT & LỘ TRÌNH", "Ma Trận Nghiệm Thu 100% Khối Lõi & Lộ Trình Chiến Lược", "Nghiệm thu toàn bộ 8 khối công nghệ cốt lõi và định hình lộ trình mở rộng hệ thống trong giai đoạn tiếp theo.")

tb21_l = s21.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.35))
p = tb21_l.text_frame.paragraphs[0]
p.text = "CÁC HẠNG MỤC ĐÃ HOÀN THÀNH 100% (DELIVERED CORE)"
p.font.name = FONT_HEADING
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = INK_NAVY

completed = [
    ("Thị giác YOLOv11m & CARLA 10k", "mAP50 = 94.91%, nhận diện chuẩn xác 7 classes"),
    ("ByteTrack 8D & Homography H", "Duy trì ID liên tục, đo vận tốc và dừng chờ mét thực"),
    ("Thuật toán Leftover-Queue", "EMA smoothing, giảm 54% thời gian dừng chờ xe"),
    ("ALINEA Freeway Ramp Metering", "Điều tiết nhập làn cao tốc & cơ chế chống tràn nhánh"),
    ("Emergency Preemption Wave", "Mở làn sóng xanh tức thời & bù công nợ xanh công bằng"),
    ("Mô phỏng SUMO vi mô 10 Hz", "Xây dựng hoàn chỉnh 3 mạng lưới Arterial, Highway, Mix"),
    ("FastAPI Concurrency WebSocket", "Khử TCP backpressure, nén 45% payload tick-by-tick"),
    ("Next.js 14 Dashboard & Lab", "Canvas Map thời gian thực, A/B race, Groq LLM Copilot")
]

db21_l = s21.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7))
tf = db21_l.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
for idx, (lead, note) in enumerate(completed):
    p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
    p.text = f"✓  {lead}: {note}"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = INK_NAVY
    if idx > 0:
        p.space_before = Pt(7)

div21 = s21.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.6), Inches(0.015), Inches(5.1))
div21.fill.solid()
div21.fill.fore_color.rgb = HAIRLINE
div21.line.fill.background()

tb21_r = s21.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.633), Inches(0.35))
p = tb21_r.text_frame.paragraphs[0]
p.text = "KẾ HOẠCH GIAI ĐOẠN TIẾP THEO (STRATEGIC ROADMAP)"
p.font.name = FONT_HEADING
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

horizons = [
    ("HORIZON 1: NÂNG CẤP REINFORCEMENT LEARNING (MARL)",
     "Tích hợp mô hình học tăng cường sâu đa tác tử (Multi-Agent PPO) phối hợp với Leftover-Queue để tối ưu hóa phối hợp cụm nút giao quy mô lớn."),
    ("HORIZON 2: TRIỂN KHAI PHẦN CỨNG BIÊN (EDGE DEVICE)",
     "Biên dịch và tối ưu hóa mô hình YOLOv11m sang TensorRT (FP16 / INT8) để chạy trực tiếp trên các kit phần cứng nhúng NVIDIA Jetson Orin Nano / AGX tại cột đèn giao thông."),
    ("HORIZON 3: THỬ NGHIỆM NGUỒN VIDEO RTSP THỰC ĐỊA",
     "Mở rộng kết nối luồng camera giao thông công cộng qua giao thức RTSP phục vụ đánh giá năng lực chạy thực tế diện rộng (Field Pilot Test).")
]

y_pos21 = Inches(2.1)
for htitle, hdesc in horizons:
    tb = s21.shapes.add_textbox(Inches(6.9), y_pos21, Inches(5.633), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = htitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    db = s21.shapes.add_textbox(Inches(6.9), y_pos21 + Inches(0.32), Inches(5.633), Inches(1.0))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = hdesc
    p.font.name = FONT_BODY
    p.font.size = Pt(9.8)
    p.font.color.rgb = INK_SLATE
    
    y_pos21 += Inches(1.55)

add_footer(s21, 21)

# ==============================================================================
# SAVE PRESENTATION
# ==============================================================================
output_pptx = "d:/ai-traffic-management-system/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully with 21 narrative slides to: {output_pptx}")

artifact_path = "C:/Users/Admin/.gemini/antigravity/brain/0bd16718-e31e-4a30-ae40-69e42323aea0/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
shutil.copy2(output_pptx, artifact_path)
print(f"Copy saved to artifact directory: {artifact_path}")
