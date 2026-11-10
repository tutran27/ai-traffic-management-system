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
# DESIGN SYSTEM: Editorial Academic & Engineering Showcase (Clean Human-Designed)
# ==============================================================================
# Pure white background, authoritative Deep Navy (#0B192C) ink, elegant hairline
# structural rules, asymmetric whitespace, NO generic rounded cards or AI emojis.
# ==============================================================================

BG_WHITE = RGBColor(255, 255, 255)
INK_NAVY = RGBColor(11, 25, 44)         # #0B192C - Primary text, bold headers, formulas
INK_SLATE = RGBColor(71, 85, 105)       # #475569 - Secondary text, subtitles, captions
INK_LIGHT_NAVY = RGBColor(30, 58, 138)  # #1E3A8A - Highlight accents, step numbers
HAIRLINE = RGBColor(226, 232, 240)      # #E2E8F0 - Architectural hairline dividers
BORDER_BOX = RGBColor(203, 213, 225)    # #CBD5E1 - Precise image borders
TINT_SURFACE = RGBColor(248, 250, 252)  # #F8FAFC - Subtle full-zone architectural wash
TINT_BAR = RGBColor(241, 245, 249)      # #F1F5F9 - Subtle table header wash

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

FORMULA_DIR = "temp_formulas_editorial"
os.makedirs(FORMULA_DIR, exist_ok=True)

def render_formula(name, latex_code, fontsize=18, dpi=300):
    fig = plt.figure(figsize=(10, 1.4))
    plt.text(0.5, 0.5, latex_code, fontsize=fontsize, ha='center', va='center', color='#0B192C')
    plt.axis('off')
    path = os.path.join(FORMULA_DIR, f"{name}.png")
    plt.savefig(path, bbox_inches='tight', transparent=True, dpi=dpi)
    plt.close()
    return path

print("Rendering high-res formulas...")
f_loss_total = render_formula("loss_total", r'$\mathcal{L}_{\mathrm{total}} = 7.5 \cdot \mathcal{L}_{\mathrm{box}} + 0.5 \cdot \mathcal{L}_{\mathrm{cls}} + 1.5 \cdot \mathcal{L}_{\mathrm{dfl}}$', fontsize=21)
f_ciou = render_formula("ciou_loss", r'$\mathcal{L}_{\mathrm{box}} = 1 - \left(\mathrm{IoU} - \frac{\rho^2(\mathbf{b}, \mathbf{b}^{gt})}{c^2} - \alpha v\right)$', fontsize=15)
f_ciou_sub = render_formula("ciou_sub", r'$v = \frac{4}{\pi^2}\left(\arctan\frac{w^{gt}}{h^{gt}} - \arctan\frac{w}{h}\right)^2, \; \alpha = \frac{v}{(1-\mathrm{IoU})+v}$', fontsize=13.5)
f_bce = render_formula("bce_loss", r'$\mathcal{L}_{\mathrm{cls}} = -\frac{1}{N}\sum_{i=1}^N \sum_{k=1}^K [y_{i,k}\log \sigma(p_{i,k}) + (1-y_{i,k})\log(1-\sigma(p_{i,k}))]$', fontsize=14)
f_dfl = render_formula("dfl_loss", r'$\mathcal{L}_{\mathrm{dfl}}(S_l, S_r) = -[(y_r - y)\log(S_l) + (y - y_l)\log(S_r)]$', fontsize=15)
f_lr = render_formula("lr_sched", r'$\mathrm{Warmup:}\; \eta(t) = \eta_0 \frac{t}{3.0} \quad | \quad \mathrm{Linear:}\; \eta(t) = 0.01 \cdot \left[1 - \frac{t-3}{97} \cdot 0.99\right]$', fontsize=14)
f_kalman = render_formula("kalman", r'$\mathbf{x}_t = [X_c, Y_c, a, h, \dot{X}_c, \dot{Y}_c, \dot{a}, \dot{h}]^T, \quad \mathbf{P}_{t|t-1} = \mathbf{F}\mathbf{P}_{t-1|t-1}\mathbf{F}^T + \mathbf{Q}$', fontsize=14)
f_homography = render_formula("homography", r'$[X_w, Y_w, 1]^T \sim \mathbf{H} [u, v, 1]^T \Rightarrow X_w = \frac{h_{11}u + h_{12}v + h_{13}}{h_{31}u + h_{32}v + h_{33}}, \; Y_w = \frac{h_{21}u + h_{22}v + h_{23}}{h_{31}u + h_{32}v + h_{33}}$', fontsize=13.5)
f_speed = render_formula("speed", r'$\bar{v}(t) = \frac{1}{M}\sum_{m=0}^{M-1} \frac{\Delta d(t-m)}{\Delta t \cdot \Delta k} \quad (\bar{v} < 2.0\mathrm{\;m/s}, \; \tau \geq 2.0\mathrm{\;s})$', fontsize=14)
f_ema = render_formula("ema", r'$S_i(k) = 0.7 \cdot Q_i(k) + 0.3 \cdot S_i(k-1)$', fontsize=15)
f_grouping = render_formula("grouping", r'$\mathcal{U} = \{i \mid S_i(k) > 0\}, \quad \mathcal{S} = \{j \mid S_j(k) \leq 0\}$', fontsize=15)
f_redist = render_formula("redist", r'$R = \min\left(12.0\mathrm{s}, \sum_{j \in \mathcal{S}} \max(0, g_j - g_{\min})\right), \; g_i(k+1) = \min\left(g_{\max}, g_i(k) + R \cdot \frac{S_i}{\sum S_m}\right)$', fontsize=13.5)
f_alinea = render_formula("alinea", r'$r(k) = \operatorname{clamp}\left(r(k-1) + K_R \cdot (o^* - \hat{o}(k)), \; r_{\min}, \; r_{\max}\right)$', fontsize=14)
f_ramp_cycle = render_formula("ramp_cycle", r'$T_{\mathrm{cycle}}(k) = \frac{3600}{r(k)}, \quad t_{\mathrm{red}}(k) = \max\left(0, T_{\mathrm{cycle}}(k) - 3.0\mathrm{s}\right)$', fontsize=14)
f_preempt = render_formula("preempt", r'$D_d(J) \leftarrow D_d(J) + \Delta t_{\mathrm{preempt}}, \quad t_{\mathrm{comp}} = \min(D_{d^*}, 15.0\mathrm{s})$', fontsize=14)
f_hcm = render_formula("hcm", r'$d_i = \max(0, t_{\mathrm{dwell}} - t_{\mathrm{free\_flow}}), \quad \mathrm{Throughput} = \frac{N_{\mathrm{completed}} \times 60}{T_{\mathrm{sim}}}$', fontsize=14.5)
print("Formulas rendered successfully!")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = BG_WHITE

def add_header(slide, kicker, title, subtitle):
    # Kicker / Category tag
    k_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.28))
    tf_k = k_box.text_frame
    tf_k.word_wrap = True
    tf_k.margin_left = tf_k.margin_right = tf_k.margin_top = tf_k.margin_bottom = 0
    p_k = tf_k.paragraphs[0]
    p_k.text = kicker.upper()
    p_k.font.name = FONT_HEADING
    p_k.font.size = Pt(9.5)
    p_k.font.bold = True
    p_k.font.color.rgb = INK_LIGHT_NAVY

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.733), Inches(0.42))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = INK_NAVY

    # Subtitle / Executive Takeaway
    s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.12), Inches(11.733), Inches(0.28))
    tf_s = s_box.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle
    p_s.font.name = FONT_BODY
    p_s.font.size = Pt(11)
    p_s.font.color.rgb = INK_SLATE

    # Hairline divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = HAIRLINE
    line.line.fill.background()

def add_footer(slide, current_slide, total_slides=12):
    # Hairline divider
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = HAIRLINE
    line.line.fill.background()

    # Left note
    f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.14), Inches(8.0), Inches(0.26))
    tf_f = f_box.text_frame
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = "AI Traffic Management & Monitoring System — Báo cáo tiến độ kỹ thuật"
    p_f.font.name = FONT_BODY
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = INK_SLATE

    # Right slide number
    r_box = slide.shapes.add_textbox(Inches(9.533), Inches(7.14), Inches(3.0), Inches(0.26))
    tf_r = r_box.text_frame
    tf_r.margin_left = tf_r.margin_right = tf_r.margin_top = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.text = f"Slide {current_slide} / {total_slides}"
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.font.name = FONT_HEADING
    p_r.font.size = Pt(9)
    p_r.font.bold = True
    p_r.font.color.rgb = INK_NAVY

# ==============================================================================
# SLIDE 1: COVER & EXECUTIVE HIGHLIGHTS (Asymmetric Editorial Poster)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Left Column (Content & Hero Metrics)
k_box1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(6.5), Inches(0.3))
tf = k_box1.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "TECHNICAL PROGRESS REPORT  •  Q4 2026"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

t_box1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(6.5), Inches(1.3))
tf = t_box1.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "HỆ THỐNG ĐIỀU PHỐI & GIÁM SÁT GIAO THÔNG THÔNG MINH"
p.font.name = FONT_HEADING
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = INK_NAVY

s_box1 = s1.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(6.5), Inches(0.6))
tf = s_box1.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "Nền tảng Tối ưu hóa Luồng Giao thông Đô thị Thời gian Thực kết hợp Thị giác Máy tính YOLOv11m, Điều khiển Thích nghi Leftover-Queue, Cao tốc ALINEA & Mô phỏng Vi mô SUMO."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = INK_SLATE

# Hairline rule on left
line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.35), Inches(6.2), Inches(0.015))
line1.fill.solid()
line1.fill.fore_color.rgb = HAIRLINE
line1.line.fill.background()

# 2x2 Clean Metric Grid
metrics = [
    ("-54.0%", "Thời gian dừng chờ xe", "Giảm trễ trung bình trên toàn mạng lưới"),
    ("94.91%", "mAP@50 Đô thị", "YOLOv11m nhận diện 7 lớp phương tiện"),
    ("27.7 FPS", "Tốc độ Inference Biên", "Xử lý video camera độ phân giải cao"),
    ("100% Real-Time", "TraCI Socket Streaming", "Chu kỳ vi mô 10 Hz & Next.js 14 Dashboard")
]

for idx, (num, label, desc) in enumerate(metrics):
    row = idx // 2
    col = idx % 2
    m_left = Inches(0.8 + col * 3.25)
    m_top = Inches(3.6 + row * 1.5)
    
    mb = s1.shapes.add_textbox(m_left, m_top, Inches(3.2), Inches(1.3))
    tf_m = mb.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_right = tf_m.margin_top = tf_m.margin_bottom = 0
    
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

# Right Column: Aspect-Ratio Preserved Image Framing
hero_path = "docs/images/hero-banner.png"
if os.path.exists(hero_path):
    pic = s1.shapes.add_picture(hero_path, Inches(7.5), Inches(1.6), width=Inches(5.033))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    
    cap = s1.shapes.add_textbox(Inches(7.5), Inches(4.7), Inches(5.033), Inches(0.4))
    tf_c = cap.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]
    p.text = "Hình: Giao diện Trung tâm Điều hành & Giám sát Luồng Giao thông Thời gian Thực"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s1, 1)

# ==============================================================================
# SLIDE 2: KIẾN TRÚC PHÂN TẦNG ĐỘC LẬP (Continuous Pipeline & Columns)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "02 // KIẾN TRÚC TỔNG THỂ", "Kiến Trúc Phân Tầng Độc Lập Đã Triển Khai", "Hierarchical & Decoupled Architecture: Phân tách rõ ràng giữa Cảm biến, Điều khiển, Mô phỏng và Vận hành.")

# Top Pipeline Bar (Clean Non-redundant Axis)
pipe_box = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.35))
tf_p = pipe_box.text_frame
tf_p.word_wrap = True
tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
p = tf_p.paragraphs[0]
p.text = "01. CẢM BIẾN   ────────►   02. QUYẾT ĐỊNH   ────────►   03. MÔ PHỎNG   ────────►   04. ĐIỀU HÀNH"
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
    
    # Vertical hairline divider between columns
    if i > 0:
        div = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.1), Inches(2.1), Inches(0.015), Inches(4.3))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()

    # Column Box
    c_box = s2.shapes.add_textbox(c_left, Inches(2.1), col_w, Inches(4.3))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    
    # Title
    p1 = tf_c.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = INK_NAVY
    
    # Pkg
    p2 = tf_c.add_paragraph()
    p2.text = pkg
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9)
    p2.font.color.rgb = INK_LIGHT_NAVY
    p2.space_before = Pt(2)
    p2.space_after = Pt(10)
    
    # Items
    for lead, desc in items:
        pi = tf_c.add_paragraph()
        pi.text = f"• {lead}: {desc}"
        pi.font.name = FONT_BODY
        pi.font.size = Pt(9.8)
        pi.font.color.rgb = INK_NAVY
        pi.space_before = Pt(4)
        
    # Output tag
    po = tf_c.add_paragraph()
    po.text = f"► {out_text}"
    po.font.name = FONT_HEADING
    po.font.size = Pt(9)
    po.font.bold = True
    po.font.color.rgb = INK_LIGHT_NAVY
    po.space_before = Pt(14)

# Bottom architectural note
note_box = s2.shapes.add_textbox(Inches(0.8), Inches(6.52), Inches(11.733), Inches(0.35))
tf_n = note_box.text_frame
tf_n.word_wrap = True
tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
p = tf_n.paragraphs[0]
p.text = "NGUYÊN TẮC THIẾT KẾ DECOUPLED: Tách rời hoàn toàn cảm biến và điều khiển; sẵn sàng chuyển giao nguồn camera RTSP thực địa mà không phải chỉnh sửa giải thuật cốt lõi."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = INK_SLATE

add_footer(s2, 2)

# ==============================================================================
# SLIDE 3: THỊ GIÁC MÁY TÍNH & CARLA (Editorial 42/58 Split)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "03 // THỊ GIÁC MÁY TÍNH (COMPUTER VISION)", "Phân Hệ Thị Giác Máy Tính & Bộ Dữ Liệu CARLA", "Huấn luyện YOLOv11m trên 10,064 ảnh độ phân giải cao từ CARLA Simulator kết hợp cân bằng lớp Spawner.")

# Left Column (44% width = 5.15")
l_box3 = s3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.15), Inches(1.6))
tf3 = l_box3.text_frame
tf3.word_wrap = True
tf3.margin_left = tf3.margin_right = tf3.margin_top = tf3.margin_bottom = 0

p = tf3.paragraphs[0]
p.text = "DỮ LIỆU TỔNG HỢP CARLA & KỸ THUẬT CÂN BẰNG LỚP"
p.font.name = FONT_HEADING
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = INK_NAVY

p = tf3.add_paragraph()
p.text = "• Khắc phục triệt để mất cân bằng lớp dữ liệu cào web bằng kỹ thuật Spawner nhân tạo tỷ lệ xe buýt và xe ưu tiên lên gấp 2x - 3x.\n• 10,064 ảnh độ phân giải 1920x1080 qua 13 điều kiện thời tiết (Nắng gắt, Mưa lớn, Hoàng hôn, Ban đêm)."
p.font.name = FONT_BODY
p.font.size = Pt(10)
p.font.color.rgb = INK_NAVY
p.space_before = Pt(4)

# Publication Table (IEEE Style: 3 Horizontal Lines)
table_shape = s3.shapes.add_table(5, 3, Inches(0.8), Inches(3.25), Inches(5.15), Inches(2.2))
tbl = table_shape.table
tbl.columns[0].width = Inches(1.4)
tbl.columns[1].width = Inches(1.0)
tbl.columns[2].width = Inches(2.75)

headers = ["Chỉ số", "Kết quả", "Ý nghĩa kỹ thuật"]
for c, h in enumerate(headers):
    cell = tbl.cell(0, c)
    cell.fill.solid()
    cell.fill.fore_color.rgb = TINT_BAR
    cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
    cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.06)
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
        cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
        cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.05)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        if c == 1:
            p.font.bold = True
            p.font.color.rgb = INK_LIGHT_NAVY
        else:
            p.font.color.rgb = INK_NAVY

# Model Checkpoint specs at bottom left
cp_box = s3.shapes.add_textbox(Inches(0.8), Inches(5.75), Inches(5.15), Inches(0.9))
tf_cp = cp_box.text_frame
tf_cp.word_wrap = True
tf_cp.margin_left = tf_cp.margin_right = tf_cp.margin_top = tf_cp.margin_bottom = 0
p = tf_cp.paragraphs[0]
p.text = "THÔNG SỐ CHECKPOINT"
p.font.name = FONT_HEADING
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = INK_NAVY
p = tf_cp.add_paragraph()
p.text = "• Model: packages/cv-pipeline/models/best.pt\n• Dung lượng: 40.5 MB (20.06M tham số) | Huấn luyện 100 Epochs trên GPU NVIDIA L40S."
p.font.name = FONT_CODE
p.font.size = Pt(9)
p.font.color.rgb = INK_SLATE
p.space_before = Pt(2)

# Right Column (56% width = 6.25")
det_img_path = "docs/images/realworld-detections.png"
if os.path.exists(det_img_path):
    pic = s3.shapes.add_picture(det_img_path, Inches(6.35), Inches(1.6), width=Inches(6.183), height=Inches(4.8))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    
    cap = s3.shapes.add_textbox(Inches(6.35), Inches(6.48), Inches(6.183), Inches(0.35))
    tf_c = cap.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]
    p.text = "Hình 1: Kiểm thử nhận diện đồng thời 7 lớp xe trong điều kiện trời mưa và ánh sáng thực tế phức tạp"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s3, 3)

# ==============================================================================
# SLIDE 4: CÔNG THỨC TOÁN HỌC - HÀM MẤT MÁT (Academic Paper Layout)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "04 // CƠ SỞ TOÁN HỌC", "Công Thức Toán Học - Hàm Mất Mát Đa Nhiệm Thị Giác", "Tối ưu hóa đa nhiệm kết hợp CIoU Bounding Box Loss, BCE Classification và Distribution Focal Loss (DFL).")

# Master Objective Block (Clean Center Math with Breathing Room)
mb_box = s4.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.28))
tf_mb = mb_box.text_frame
tf_mb.margin_left = tf_mb.margin_right = tf_mb.margin_top = tf_mb.margin_bottom = 0
p = tf_mb.paragraphs[0]
p.text = "TỔNG HÀM MẤT MÁT ĐA NHIỆM HUẤN LUYỆN (MULTI-TASK OBJECTIVE FORMULATION)"
p.font.name = FONT_HEADING
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

s4.shapes.add_picture(f_loss_total, Inches(2.9), Inches(1.78), width=Inches(7.5))

# Hairline rule placed with proper margin below formula
div4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.78), Inches(11.733), Inches(0.015))
div4.fill.solid()
div4.fill.fore_color.rgb = HAIRLINE
div4.line.fill.background()

# 3 Columns for 3 Losses
col_w4 = Inches(3.7)
losses = [
    ("1. HỒI QUY VỊ TRÍ (CIoU LOSS)", f_ciou, f_ciou_sub, [
        ("Tối ưu diện tích", "Đo mức độ chồng lấn IoU giữa dự đoán và nhãn thực."),
        ("Khoảng cách tâm", "Phạt khoảng cách tâm Euclidean rho chuẩn hóa theo c."),
        ("Tỷ lệ co giãn", "Bù trừ tỷ lệ khung hình với hai hệ số v và alpha.")
    ]),
    ("2. PHÂN LOẠI (BCE WITH LOGITS)", f_bce, None, [
        ("Phân loại độc lập", "Xét độc lập K = 7 lớp xe, triệt tiêu áp chế xác suất."),
        ("Hàm Sigmoid", "Áp dụng hàm kích hoạt Sigmoid riêng biệt cho từng lớp."),
        ("Trọng số lỗi", "Gán trọng số lambda_cls = 0.5 để ưu tiên ổn định tọa độ.")
    ]),
    ("3. PHÂN PHỐI BIÊN TIÊU CỰ (DFL)", f_dfl, None, [
        ("Phân phối liên tục", "Học phân phối xác suất liên tục của biên thay cho Dirac."),
        ("Bù trừ che khuất", "Tăng độ nhạy khi phương tiện bị che khuất hoặc mờ nhòe."),
        ("Trọng số lỗi", "Gán trọng số lambda_dfl = 1.5 làm mịn tọa độ biên.")
    ])
]

for i, (l_title, f1, f2, points) in enumerate(losses):
    c_left = Inches(0.8 + i * (3.7 + 0.31))
    
    if i > 0:
        div = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.15), Inches(2.9), Inches(0.015), Inches(3.1))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()
        
    t_box = s4.shapes.add_textbox(c_left, Inches(2.88), col_w4, Inches(0.35))
    tf = t_box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = l_title
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    # Formula Picture
    s4.shapes.add_picture(f1, c_left, Inches(3.28), width=col_w4)
    if f2:
        s4.shapes.add_picture(f2, c_left, Inches(3.85), width=col_w4)
        desc_top = Inches(4.45)
    else:
        desc_top = Inches(3.98)
        
    d_box = s4.shapes.add_textbox(c_left, desc_top, col_w4, Inches(1.8))
    tf_d = d_box.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    for idx, (lead, txt) in enumerate(points):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.text = f"• {lead}: {txt}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(4)

# Bottom Hairline & Learning Rate Schedule
div_lr = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.015))
div_lr.fill.solid()
div_lr.fill.fore_color.rgb = HAIRLINE
div_lr.line.fill.background()

s4.shapes.add_picture(f_lr, Inches(4.0), Inches(6.15), width=Inches(6.2))
lbl_lr = s4.shapes.add_textbox(Inches(0.8), Inches(6.25), Inches(3.0), Inches(0.3))
tf_lr = lbl_lr.text_frame
tf_lr.margin_left = tf_lr.margin_right = tf_lr.margin_top = tf_lr.margin_bottom = 0
p = tf_lr.paragraphs[0]
p.text = "LỊCH TRÌNH TỐC ĐỘ HỌC (LR):"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

add_footer(s4, 4)

# ==============================================================================
# SLIDE 5: THEO DÕI ĐA ĐỐI TƯỢNG & HOMOGRAPHY (Editorial Split)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "05 // THEO DÕI & ĐO ĐẠC", "Theo Dõi Đa Đối Tượng & Chiếu Tọa Độ Thực", "ByteTrack 2 tầng duy trì ID phương tiện liên tục và ma trận Homography mặt đất xác định vận tốc thực.")

# Left Column: Theory & Equations (46% = 5.4")
sections_s5 = [
    ("1. THEO DÕI LIÊN TỤC VỚI BYTETRACK & KALMAN 8 TRẠNG THÁI", f_kalman,
     "Ghép nối Hungarian 2 tầng tận dụng cả các phát hiện có độ tin cậy thấp, duy trì ID liên tục qua các khung hình bị che khuất ngắn hạn."),
    ("2. MA TRẬN HOMOGRAPHY MẶT ĐẤT (GROUND-PLANE H)", f_homography,
     "Chiếu điểm tiếp đất bánh xe (u, v) sang tọa độ thực (X_w, Y_w, 0) trên mặt đường nhằm đo đạc cự ly và kích thước theo đơn vị mét chuẩn xác."),
    ("3. ƯỚC LƯỢNG VẬN TỐC & TIÊU CHUẨN XE CHỜ ĐÈN ĐỎ", f_speed,
     "Bộ lọc vận tốc trượt M = 5 frames. Xác nhận xe dừng chờ đèn đỏ khi v < 2.0 m/s duy trì trong khoảng thời gian tau >= 2.0 giây.")
]

y_pos = Inches(1.6)
for title, f_pic, desc in sections_s5:
    tb = s5.shapes.add_textbox(Inches(0.8), y_pos, Inches(5.4), Inches(0.3))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    s5.shapes.add_picture(f_pic, Inches(0.8), y_pos + Inches(0.3), width=Inches(5.4))
    
    db = s5.shapes.add_textbox(Inches(0.8), y_pos + Inches(0.95), Inches(5.4), Inches(0.55))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    p = tf_d.paragraphs[0]
    p.text = desc
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = INK_SLATE
    
    y_pos += Inches(1.65)

# Right Column: Visual Evidence (54% = 6.0")
col_img_path = "docs/images/collision-detection.png"
if os.path.exists(col_img_path):
    pic = s5.shapes.add_picture(col_img_path, Inches(6.5), Inches(1.6), width=Inches(6.033), height=Inches(4.8))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    
    cap = s5.shapes.add_textbox(Inches(6.5), Inches(6.48), Inches(6.033), Inches(0.35))
    tf_c = cap.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]
    p.text = "Hình 2: Trực quan hóa ID phương tiện, quỹ đạo di chuyển và cảnh báo xung đột giao cắt"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s5, 5)

# ==============================================================================
# SLIDE 6: THUẬT TOÁN THÍCH NGHI - LEFTOVER QUEUE (Horizontal 3-Step Flow)
# ==============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "06 // ĐIỀU KHIỂN THÍCH NGHI", "Thuật Toán Thích Nghi - Tái Phân Bổ Hàng Đợi Tồn Dư", "Leftover-Queue Actuated Signal Control: Cân bằng thời lượng xanh chu kỳ tại thời điểm chớm vàng.")

# 3 Step Progression Columns
steps_s6 = [
    ("BƯỚC 1: LÀM MỊN HÀNG ĐỢI TỒN", f_ema, [
        ("Ghi nhận Q_i(k)", "Đo số xe tồn đọng tại thời điểm chớm vàng."),
        ("Bộ lọc EMA", "Tham số alpha = 0.7 khử nhiễu ngẫu nhiên chu kỳ."),
        ("Phản ánh trung thực", "Nắm bắt chính xác nhu cầu lưu thông thực tế.")
    ]),
    ("BƯỚC 2: PHÂN NHÓM TRẠNG THÁI", f_grouping, [
        ("Nhóm U (Undersupplied)", "S_i(k) > 0: Vẫn còn tồn đọng xe sau pha xanh."),
        ("Nhóm S (Satisfied)", "S_j(k) <= 0: Đã giải phóng hết xe thông thoáng."),
        ("Ngân sách tái phân bổ", "Trích xuất tối đa R_max = 12.0s từ các nhánh dư thừa.")
    ]),
    ("BƯỚC 3: TÁI PHÂN BỔ CÓ RÀNG BUỘC", f_redist, [
        ("Bù thời gian xanh", "Cấp thêm thời gian xanh theo tỷ trọng w_i = S_i / sum(S)."),
        ("Bảo toàn chu kỳ", "Giữ nguyên tổng thời lượng chu kỳ đèn giao lộ."),
        ("Ràng buộc nghiêm ngặt", "Luôn tuân thủ biên an toàn [g_min, g_max].")
    ])
]

col_w6 = Inches(3.7)
for i, (stitle, f_pic, pts) in enumerate(steps_s6):
    c_left = Inches(0.8 + i * (3.7 + 0.31))
    
    if i > 0:
        div = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.15), Inches(1.7), Inches(0.015), Inches(4.3))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()
        
    tb = s6.shapes.add_textbox(c_left, Inches(1.7), col_w6, Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = stitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = INK_LIGHT_NAVY
    
    # Formula Picture
    s6.shapes.add_picture(f_pic, c_left, Inches(2.2), width=col_w6)
    
    # Points
    db = s6.shapes.add_textbox(c_left, Inches(3.2), col_w6, Inches(2.5))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    for idx, (lead, txt) in enumerate(pts):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.text = f"• {lead}: {txt}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.8)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)

# Bottom Hard Safety Constraints Strip (No emoji)
strip6 = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.15), Inches(11.733), Inches(0.7))
strip6.fill.solid()
strip6.fill.fore_color.rgb = TINT_SURFACE
strip6.line.color.rgb = BORDER_BOX
strip6.line.width = Pt(0.75)

tb_s6 = s6.shapes.add_textbox(Inches(1.0), Inches(6.22), Inches(11.333), Inches(0.55))
tf_s6 = tb_s6.text_frame
tf_s6.word_wrap = True
tf_s6.margin_left = tf_s6.margin_right = tf_s6.margin_top = tf_s6.margin_bottom = 0
p = tf_s6.paragraphs[0]
p.text = "RÀNG BUỘC AN TOÀN TUYỆT ĐỐI (HARD SAFETY CONSTRAINTS)"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_NAVY

p = tf_s6.add_paragraph()
p.text = "Thời lượng xanh tối thiểu g_min = 10.0 s (cho người đi bộ) | Thời lượng xanh tối đa g_max = 50.0 s | Biên độ thay đổi mỗi chu kỳ R_max = 12.0 s."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.color.rgb = INK_SLATE
p.space_before = Pt(2)

add_footer(s6, 6)

# ==============================================================================
# SLIDE 7: ĐIỀU TIẾT NHẬP LÀN CAO TỐC ALINEA (Comparative Deep Dive)
# ==============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "07 // ĐIỀU TIẾT CAO TỐC", "Điều Tiết Nhập Làn Cao Tốc ALINEA & Chống Tràn", "Luật điều khiển tích phân vòng kín Papageorgiou et al. giữ mật độ tuyến chính dưới điểm sụp đổ lưu lượng.")

# Left Column (5.6"): ALINEA Theory
tb7_l = s7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.35))
tf = tb7_l.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "1. LUẬT ĐIỀU KHIỂN HỒI TIẾP TÍCH PHÂN ALINEA"
p.font.name = FONT_HEADING
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = INK_NAVY

s7.shapes.add_picture(f_alinea, Inches(0.8), Inches(2.05), width=Inches(5.6))

db7_l = s7.shapes.add_textbox(Inches(0.8), Inches(2.85), Inches(5.6), Inches(1.3))
tf = db7_l.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "• K_R = 70.0 veh/h/%: Hệ số khuếch đại tích phân phản hồi.\n• o* = 20%: Mật độ chiếm dụng mục tiêu lý tưởng tại hạ lưu điểm hòa dòng.\n• [r_min, r_max] = [200, 1200] veh/h: Giới hạn lưu lượng cấp xe."
p.font.name = FONT_BODY
p.font.size = Pt(9.8)
p.font.color.rgb = INK_NAVY

tb7_l2 = s7.shapes.add_textbox(Inches(0.8), Inches(4.3), Inches(5.6), Inches(0.35))
tf = tb7_l2.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "QUY ĐỔI SANG THỜI LƯỢNG ĐÈN METERING"
p.font.name = FONT_HEADING
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

s7.shapes.add_picture(f_ramp_cycle, Inches(0.8), Inches(4.7), width=Inches(5.6))

db7_l3 = s7.shapes.add_textbox(Inches(0.8), Inches(5.45), Inches(5.6), Inches(1.2))
tf = db7_l3.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "• Thời lượng xanh cố định t_green = 2.0 s (cấp 1 xe nhập làn mỗi chu kỳ).\n• Thời lượng vàng cố định t_yellow = 1.0 s.\n• Thời lượng đỏ t_red(k) điều biến tự động theo chu kỳ T_cycle."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.color.rgb = INK_SLATE

# Vertical hairline divider
div7 = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.6), Inches(0.015), Inches(5.1))
div7.fill.solid()
div7.fill.fore_color.rgb = HAIRLINE
div7.line.fill.background()

# Right Column (5.6"): Spillback Override & Schematic
tb7_r = s7.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.6), Inches(0.35))
tf = tb7_r.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "2. CƠ CHẾ GHI ĐÈ CHỐNG TRÀN (SPILLBACK OVERRIDE)"
p.font.name = FONT_HEADING
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = INK_NAVY

sb7_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(2.05), Inches(5.633), Inches(0.85))
sb7_box.fill.solid()
sb7_box.fill.fore_color.rgb = TINT_SURFACE
sb7_box.line.color.rgb = BORDER_BOX
sb7_box.line.width = Pt(0.75)

tb_sb = s7.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.2), Inches(0.55))
tf = tb_sb.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "Nếu Q_ramp(k) >= 30 xe  ==>  r(k) = r_max (1200 veh/h)"
p.font.name = FONT_CODE
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

db7_r = s7.shapes.add_textbox(Inches(6.9), Inches(3.1), Inches(5.633), Inches(1.2))
tf = db7_r.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "• Ngăn dòng xe xếp hàng trên nhánh nối tràn ngược làm nghẽn đường đô thị.\n• Mở xả tối đa giải tỏa nhánh nhập làn khẩn cấp.\n• Tự động phục hồi luật hồi tiếp ALINEA khi hàng đợi đã giải phóng."
p.font.name = FONT_BODY
p.font.size = Pt(9.8)
p.font.color.rgb = INK_NAVY

# Highway Merge Schematic Box
tb7_s = s7.shapes.add_textbox(Inches(6.9), Inches(4.3), Inches(5.633), Inches(0.35))
tf = tb7_s.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & ON-RAMP METERING"
p.font.name = FONT_HEADING
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

diag_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.9), Inches(4.7), Inches(5.633), Inches(1.8))
diag_box.fill.solid()
diag_box.fill.fore_color.rgb = TINT_SURFACE
diag_box.line.color.rgb = BORDER_BOX
diag_box.line.width = Pt(0.75)

tb_diag = s7.shapes.add_textbox(Inches(7.1), Inches(4.85), Inches(5.2), Inches(1.5))
tf_d = tb_diag.text_frame
tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
p = tf_d.paragraphs[0]
p.text = "Tuyến chính cao tốc ────────[ Cảm biến ô(k) ]────────► Thông suốt\n                                  ▲ Điểm hòa dòng\nNhánh nối On-Ramp  ──────────[ Đèn Meter r(k) ]"
p.font.name = FONT_CODE
p.font.size = Pt(9.5)
p.font.color.rgb = INK_NAVY

p2 = tf_d.add_paragraph()
p2.text = "Cảm biến hạ lưu đo mật độ ô(k) hồi tiếp về bộ điều khiển ALINEA theo chu kỳ 10 giây."
p2.font.name = FONT_BODY
p2.font.size = Pt(9)
p2.font.italic = True
p2.font.color.rgb = INK_SLATE
p2.space_before = Pt(8)

add_footer(s7, 7)

# ==============================================================================
# SLIDE 8: CƠ CHẾ ƯU TIÊN XE KHẨN CẤP (3-Phase Incident Flow)
# ==============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "08 // ƯU TIÊN KHẨN CẤP", "Cơ Chế Ưu Tiên Xe Khẩn Cấp & Bù Trừ Nợ Xanh", "Phát hiện xe cứu thương, cứu hỏa, cảnh sát → Kích hoạt làn sóng xanh → Hoàn trả công nợ thời gian.")

phases_s8 = [
    ("GIAI ĐOẠN 1: KÍCH HOẠT ƯU TIÊN", "phi_J  <--  phi_EV(e) (Pha xanh tức thời)", [
        ("Phát hiện EV", "Camera / SUMO phát hiện Ambulance/Police."),
        ("Định hướng nút", "Xác định hướng di chuyển và nút giao J."),
        ("Dọn đường", "Kích hoạt ngay pha xanh dọn đường tức thời."),
        ("0s Chờ đợi", "Xe khẩn cấp vượt giao lộ trong 0s dừng chờ.")
    ]),
    ("GIAI ĐOẠN 2: TÍCH LŨY CÔNG NỢ", "D_d(J)  <--  D_d(J) + delta_t_preempt", [
        ("Ghi nhận thiệt hại", "Các hướng trực giao bị cắt quyền đi."),
        ("Tích lũy công nợ", "Tích lũy nợ thời gian suốt delta_t_preempt."),
        ("Sổ nợ giao lộ", "Ghi nhận vào sổ nợ giao lộ D_d(J)."),
        ("Tính minh bạch", "Đảm bảo tính minh bạch điều hành mạng lưới.")
    ]),
    ("GIAI ĐOẠN 3: BÙ NỢ CÔNG BẰNG", "t_comp = min(D_d*, 15.0 s)", [
        ("Rời khỏi nút", "Xe khẩn cấp vừa rời khỏi nút giao."),
        ("Tìm hướng nợ", "Tìm hướng chịu thiệt hại lớn nhất d*."),
        ("Cấp bù thời gian", "Cấp bù thời gian xanh t_comp cho d*."),
        ("Chống ùn tắc", "Tránh hiện tượng nghẽn lan tỏa dây chuyền.")
    ])
]

col_w8 = Inches(3.7)
for i, (ptitle, code_str, pts) in enumerate(phases_s8):
    c_left = Inches(0.8 + i * (3.7 + 0.31))
    
    if i > 0:
        div = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.15), Inches(1.7), Inches(0.015), Inches(4.0))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()
        
    tb = s8.shapes.add_textbox(c_left, Inches(1.7), col_w8, Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = ptitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    # Formula Tag Box
    c_box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(2.15), col_w8, Inches(0.65))
    c_box.fill.solid()
    c_box.fill.fore_color.rgb = TINT_SURFACE
    c_box.line.color.rgb = BORDER_BOX
    c_box.line.width = Pt(0.75)
    
    tb_c = s8.shapes.add_textbox(c_left + Inches(0.1), Inches(2.25), col_w8 - Inches(0.2), Inches(0.45))
    tf_c = tb_c.text_frame
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]
    p.text = code_str
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = INK_LIGHT_NAVY
    
    # Points
    db = s8.shapes.add_textbox(c_left, Inches(3.0), col_w8, Inches(2.5))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    for idx, (lead, txt) in enumerate(pts):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.text = f"• {lead}: {txt}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.8)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)

# Bottom Formula & Proof Strip with generous spacing
div8_b = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.015))
div8_b.fill.solid()
div8_b.fill.fore_color.rgb = HAIRLINE
div8_b.line.fill.background()

s8.shapes.add_picture(f_preempt, Inches(3.8), Inches(5.92), width=Inches(5.8))

lbl8_b = s8.shapes.add_textbox(Inches(0.8), Inches(6.62), Inches(11.733), Inches(0.32))
tf8_b = lbl8_b.text_frame
tf8_b.margin_left = tf8_b.margin_right = tf8_b.margin_top = tf8_b.margin_bottom = 0
p = tf8_b.paragraphs[0]
p.text = "✓ Kết quả thực nghiệm: Phương tiện khẩn cấp vượt giao lộ với 0 giây dừng chờ; các hướng trực giao được hoàn trả thời lượng, hồi phục cân bằng sau 1-2 chu kỳ."
p.font.name = FONT_BODY
p.font.size = Pt(9.2)
p.font.italic = True
p.font.color.rgb = INK_SLATE

add_footer(s8, 8)

# ==============================================================================
# SLIDE 9: MÔ PHỎNG VI MÔ SUMO (Triptych Showcase)
# ==============================================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "09 // MÔ PHỎNG VI MÔ", "Mô Phỏng Vi Mô SUMO & 3 Mạng Lưới Đã Xây Dựng", "Tích hợp TraCI Socket Protocol 10 Hz và 3 mô hình mạng lưới kiểm thử chuyên biệt.")

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

col_w9 = Inches(3.7)
for i, (ntitle, img_p, sub, pts) in enumerate(networks):
    c_left = Inches(0.8 + i * (3.7 + 0.31))
    
    if i > 0:
        div = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.15), Inches(1.6), Inches(0.015), Inches(4.7))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()
        
    tb = s9.shapes.add_textbox(c_left, Inches(1.6), col_w9, Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = ntitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    p_sub = tf.add_paragraph()
    p_sub.text = sub
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = INK_LIGHT_NAVY
    p_sub.space_before = Pt(1)
    
    # Image
    if os.path.exists(img_p):
        pic = s9.shapes.add_picture(img_p, c_left, Inches(2.3), width=col_w9, height=Inches(2.2))
        pic.line.color.rgb = BORDER_BOX
        pic.line.width = Pt(0.75)
        
    db = s9.shapes.add_textbox(c_left, Inches(4.65), col_w9, Inches(1.7))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    for idx, (lead, txt) in enumerate(pts):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.text = f"• {lead}: {txt}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(4)

# Bottom SUMO Specs (No emoji)
div9_b = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.45), Inches(11.733), Inches(0.015))
div9_b.fill.solid()
div9_b.fill.fore_color.rgb = HAIRLINE
div9_b.line.fill.background()

tb9_b = s9.shapes.add_textbox(Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.35))
tf9_b = tb9_b.text_frame
tf9_b.margin_left = tf9_b.margin_right = tf9_b.margin_top = tf9_b.margin_bottom = 0
p = tf9_b.paragraphs[0]
p.text = "THÔNG SỐ VI MÔ SUMO: TraCI Socket tần số 10 Hz (Delta_t = 0.1s) | Mô hình xe bám đuôi Krauss Car-Following | Cấu hình pha Dual-Ring Permissive Left Turn."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.color.rgb = INK_SLATE

add_footer(s9, 9)

# ==============================================================================
# SLIDE 10: NỀN TẢNG FULL-STACK & DASHBOARD (Showcase 58/42 Split)
# ==============================================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "10 // NỀN TẢNG FULL-STACK", "Nền Tảng Full-Stack: Backend & Operator Dashboard", "FastAPI Async WebSocket Engine và Next.js 14 Interactive Operator Dashboard.")

# Left (58% = 6.6"): Large Dashboard Image
dash_img_path = "docs/images/dashboard.png"
if os.path.exists(dash_img_path):
    pic = s10.shapes.add_picture(dash_img_path, Inches(0.8), Inches(1.6), width=Inches(6.6), height=Inches(4.7))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    
    cap = s10.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(6.6), Inches(0.4))
    tf_c = cap.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]
    p.text = "Hình: Giao diện Dashboard thời gian thực: Bản đồ nhiệt động học, thông số từng nút giao và telemetry vi mô"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

# Right (42% = 4.8"): 3 Architectural Strengths (Clean Numbered Headers)
strengths = [
    ("1. FASTAPI BACKEND HIGH-CONCURRENCY", [
        "Khử TCP Backpressure: Bọc lệnh gửi socket với timeout tau_ws <= 0.15 s tránh làm lag luồng mô phỏng vi mô.",
        "Nén Payload JSON: Giảm 45% kích thước gói tin tick-by-tick (từ 60 KB xuống còn 32 KB)."
    ]),
    ("2. PHÒNG THÍ NGHIỆM ĐUA CHÍNH SÁCH (LAB)", [
        "Chạy song song 2 phiên mô phỏng đối đầu (Fixed-Time vs Adaptive) cùng seed ngẫu nhiên 42.",
        "Quan sát trực tiếp sự phân hóa hàng đợi và thời gian chờ tích lũy ngay trên giao diện."
    ]),
    ("3. TRỢ LÝ GROQ LLM TRAFFIC COPILOT", [
        "Tích hợp LLM Groq giải thích nguyên nhân chuyển pha đèn bằng ngôn ngữ tự nhiên.",
        "Tự động sinh khuyến nghị điều phối khi phát hiện điểm nghẽn giao thông bất thường."
    ])
]

y_pos10 = Inches(1.6)
for stitle, bts in strengths:
    tb = s10.shapes.add_textbox(Inches(7.7), y_pos10, Inches(4.833), Inches(0.35))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = stitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    db = s10.shapes.add_textbox(Inches(7.7), y_pos10 + Inches(0.35), Inches(4.833), Inches(1.1))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    for idx, b in enumerate(bts):
        p = tf_d.paragraphs[0] if idx == 0 else tf_d.add_paragraph()
        p.text = f"• {b}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_SLATE
        if idx > 0:
            p.space_before = Pt(4)
            
    y_pos10 += Inches(1.65)

add_footer(s10, 10)

# ==============================================================================
# SLIDE 11: KẾT QUẢ ĐO KIỂM BENCHMARK (Quantitative Evidence Showcase)
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)
add_header(s11, "11 // KẾT QUẢ THỰC NGHIỆM", "Kết Quả Đo Kiểm Benchmark (Chuẩn HCM Metrics)", "Đánh giá định lượng trên 5,500 phương tiện qua 3 profile nhu cầu (Race Framework đối đầu).")

# Left Column (5.4"): Giant Hero Drops & HCM Formulas
metrics_s11 = [
    ("-40.5%", "Kịch bản Cân bằng (Balanced)", "Thời gian chờ: 65.4 s -> 38.9 s | Thông lượng mạng lưới: +14%"),
    ("-52.3%", "Kịch bản Lệch tải (Asymmetric)", "Thời gian chờ: 88.2 s -> 42.1 s | Thông lượng mạng lưới: +22%"),
    ("-54.0%", "Kịch bản Quá tải cực hạn (Extreme)", "Thời gian chờ: 124.6 s -> 57.3 s | Thông lượng mạng lưới: +28%")
]

for idx, (pct, sc, det) in enumerate(metrics_s11):
    m_top = Inches(1.6 + idx * 1.15)
    
    # Big Number Box
    nb = s11.shapes.add_textbox(Inches(0.8), m_top, Inches(1.6), Inches(0.8))
    tf_n = nb.text_frame
    tf_n.margin_left = tf_n.margin_right = tf_n.margin_top = tf_n.margin_bottom = 0
    p = tf_n.paragraphs[0]
    p.text = pct
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    # Label Box
    lb = s11.shapes.add_textbox(Inches(2.5), m_top + Inches(0.05), Inches(3.7), Inches(0.8))
    tf_l = lb.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_right = tf_l.margin_top = tf_l.margin_bottom = 0
    p1 = tf_l.paragraphs[0]
    p1.text = sc
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = INK_LIGHT_NAVY
    
    p2 = tf_l.add_paragraph()
    p2.text = det
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = INK_SLATE
    p2.space_before = Pt(2)

# Divider line on left
div11_l = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.1), Inches(5.4), Inches(0.015))
div11_l.fill.solid()
div11_l.fill.fore_color.rgb = HAIRLINE
div11_l.line.fill.background()

tb_hcm = s11.shapes.add_textbox(Inches(0.8), Inches(5.25), Inches(5.4), Inches(0.35))
tf = tb_hcm.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "TIÊU CHUẨN HIGHWAY CAPACITY MANUAL (HCM)"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

s11.shapes.add_picture(f_hcm, Inches(0.8), Inches(5.6), width=Inches(5.4))

db_hcm = s11.shapes.add_textbox(Inches(0.8), Inches(6.35), Inches(5.4), Inches(0.5))
tf = db_hcm.text_frame
tf_d.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "Control Delay đo thời gian hao phí thực tế so với lưu thông tự do vùng 50m; Throughput đo số chuyến đi hoàn thành thành công rời mạng lưới trên mỗi phút."
p.font.name = FONT_BODY
p.font.size = Pt(9)
p.font.italic = True
p.font.color.rgb = INK_SLATE

# Right Column (6.0"): Benchmark Chart
wait_img_path = "docs/images/waiting-time.png"
if os.path.exists(wait_img_path):
    pic = s11.shapes.add_picture(wait_img_path, Inches(6.6), Inches(1.6), width=Inches(5.933), height=Inches(4.6))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    
    cap = s11.shapes.add_textbox(Inches(6.6), Inches(6.35), Inches(5.933), Inches(0.4))
    tf_c = cap.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p = tf_c.paragraphs[0]
    p.text = "Biểu đồ phân phối thời gian chờ: Thuật toán Adaptive AI giải phóng mạng lưới nhanh hơn tới 54%"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s11, 11)

# ==============================================================================
# SLIDE 12: MA TRẬN TIẾN ĐỘ & ĐỊNH HƯỚNG CHIẾN LƯỢC (Two-Panel Horizon Architecture)
# ==============================================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)
add_header(s12, "12 // TỔNG KẾT & LỘ TRÌNH", "Ma Trận Tiến Độ Đã Hoàn Thành & Định Hướng", "Nghiệm thu 100% các khối AI cốt lõi và định hướng mở rộng hệ thống trong giai đoạn tiếp theo.")

# Left Panel (5.6"): Completed Modules (Checklist)
tb12_l = s12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.35))
tf = tb12_l.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "CÁC HẠNG MỤC ĐÃ HOÀN THÀNH 100% (DELIVERED CORE)"
p.font.name = FONT_HEADING
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = INK_NAVY

completed = [
    ("Thị giác YOLOv11m & CARLA 10k", "mAP50 = 94.91%, 7 classes phương tiện"),
    ("ByteTrack & Camera Homography H", "Ước lượng vận tốc thực & dừng chờ"),
    ("Thuật toán Leftover-Queue", "EMA smoothing, giảm 54% wait time"),
    ("ALINEA Freeway Ramp Metering", "Điều tiết cao tốc & chống tràn nhánh"),
    ("Emergency Preemption Wave", "Làn sóng xanh & bù nợ sau ưu tiên"),
    ("Mô phỏng SUMO vi mô", "3 mạng lưới: Arterial, Highway, Mix"),
    ("FastAPI Concurrency WebSocket", "Streaming 10 Hz, nén payload 45%"),
    ("Next.js 14 Dashboard & Lab", "Canvas Map, A/B race, Groq Copilot")
]

db12_l = s12.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7))
tf_c12 = db12_l.text_frame
tf_c12.word_wrap = True
tf_c12.margin_left = tf_c12.margin_right = tf_c12.margin_top = tf_c12.margin_bottom = 0
for idx, (lead, note) in enumerate(completed):
    p = tf_c12.paragraphs[0] if idx == 0 else tf_c12.add_paragraph()
    p.text = f"✓  {lead}: {note}"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = INK_NAVY
    if idx > 0:
        p.space_before = Pt(7)

# Vertical hairline divider
div12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.6), Inches(0.015), Inches(5.1))
div12.fill.solid()
div12.fill.fore_color.rgb = HAIRLINE
div12.line.fill.background()

# Right Panel (5.6"): Strategic Roadmap Horizons
tb12_r = s12.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.633), Inches(0.35))
tf = tb12_r.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "KẾ HOẠCH GIAI ĐOẠN TIẾP THEO (STRATEGIC ROADMAP)"
p.font.name = FONT_HEADING
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

horizons = [
    ("HORIZON 1: NÂNG CẤP REINFORCEMENT LEARNING (MARL)",
     "Tích hợp thuật toán học tăng cường sâu đa tác tử (Multi-Agent PPO) kết hợp cùng Leftover-Queue để tối ưu hóa phối hợp giữa các cụm nút giao phức tạp."),
    ("HORIZON 2: TRIỂN KHAI PHẦN CỨNG BIÊN (EDGE DEVICE)",
     "Biên dịch và tối ưu hóa mô hình YOLOv11m sang TensorRT (FP16 / INT8) để chạy trực tiếp trên các kit phần cứng nhúng NVIDIA Jetson Orin Nano / AGX tại cột đèn giao thông."),
    ("HORIZON 3: THỬ NGHIỆM NGUỒN VIDEO RTSP THỰC ĐỊA",
     "Mở rộng kết nối luồng camera giao thông công cộng qua giao thức RTSP phục vụ đánh giá năng lực chạy thực tế diện rộng (Field Pilot Test).")
]

y_pos12 = Inches(2.1)
for htitle, hdesc in horizons:
    tb = s12.shapes.add_textbox(Inches(6.9), y_pos12, Inches(5.633), Inches(0.3))
    tf = tb.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = htitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    db = s12.shapes.add_textbox(Inches(6.9), y_pos12 + Inches(0.32), Inches(5.633), Inches(1.0))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    tf_d.margin_left = tf_d.margin_right = tf_d.margin_top = tf_d.margin_bottom = 0
    p = tf_d.paragraphs[0]
    p.text = hdesc
    p.font.name = FONT_BODY
    p.font.size = Pt(9.8)
    p.font.color.rgb = INK_SLATE
    
    y_pos12 += Inches(1.55)

add_footer(s12, 12)

# ==============================================================================
# SAVE PRESENTATION
# ==============================================================================
output_pptx = "d:/ai-traffic-management-system/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully to: {output_pptx}")

artifact_path = "C:/Users/Admin/.gemini/antigravity/brain/0bd16718-e31e-4a30-ae40-69e42323aea0/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
shutil.copy2(output_pptx, artifact_path)
print(f"Copy saved to artifact directory: {artifact_path}")
