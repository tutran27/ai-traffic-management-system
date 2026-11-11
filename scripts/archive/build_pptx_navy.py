import os
import matplotlib.pyplot as plt
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# COLOR SYSTEM: 100% DEEP NAVY TEXT EVERYWHERE
# ==============================================================================
NAVY = RGBColor(11, 25, 44)           # #0B192C - Deep Navy (Used for ALL text)
NAVY_HEX = '#0B192C'

# Modern Executive Surfaces & Delicate Framing
WHITE = RGBColor(255, 255, 255)
CARD_BG = RGBColor(255, 255, 255)      # Pure White surface
CARD_TINT = RGBColor(241, 246, 254)    # Ice Blue / Very Soft Navy Tint
CARD_TINT_ALT = RGBColor(248, 250, 253)
BORDER_MAIN = RGBColor(186, 204, 226)  # Subtle Slate-Navy Border (1.2 pt)
BORDER_SUBTLE = RGBColor(215, 225, 238)
BORDER_DIVIDER = RGBColor(226, 232, 240)

FORMULA_DIR = "temp_formulas_navy"
os.makedirs(FORMULA_DIR, exist_ok=True)

# ==============================================================================
# 1. RENDER FORMULA IMAGES IN DEEP NAVY COLOR
# ==============================================================================
formulas = {
    'loss_total': (r'$\mathcal{L}_{\mathrm{total}} = 7.5 \cdot \mathcal{L}_{\mathrm{box}} + 0.5 \cdot \mathcal{L}_{\mathrm{cls}} + 1.5 \cdot \mathcal{L}_{\mathrm{dfl}}$', 16.5),
    'ciou': (r'$\mathcal{L}_{\mathrm{box}} = 1 - \left( \mathrm{IoU} - \frac{\rho^2(\mathbf{b}, \mathbf{b}^{gt})}{c^2} - \alpha v \right)$', 15),
    'ciou_v': (r'$v = \frac{4}{\pi^2} \left( \arctan\frac{w^{gt}}{h^{gt}} - \arctan\frac{w}{h} \right)^2, \; \alpha = \frac{v}{(1 - \mathrm{IoU}) + v}$', 13.5),
    'cls': (r'$\mathcal{L}_{\mathrm{cls}} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} [ y_{i,k} \log \sigma(p_{i,k}) + (1 - y_{i,k}) \log(1 - \sigma(p_{i,k})) ]$', 14.5),
    'dfl': (r'$\mathcal{L}_{\mathrm{dfl}}(S_l, S_r) = - [ (y_r - y) \log(S_l) + (y - y_l) \log(S_r) ]$', 14.5),
    'lr': (r'$\mathrm{Warmup: } \eta(t) = \eta_0 \frac{t}{3.0} \quad | \quad \mathrm{Linear: } \eta(t) = 0.01 \cdot [ 1 - \frac{t - 3}{97} \cdot 0.99 ]$', 13),
    'kalman': (r'$\mathbf{x}_t = [x_c, y_c, a, h, \dot{x}_c, \dot{y}_c, \dot{a}, \dot{h}]^T, \quad \mathbf{P}_{t|t-1} = \mathbf{F} \mathbf{P}_{t-1|t-1} \mathbf{F}^T + \mathbf{Q}$', 14.5),
    'homography': (r'$[X_w, Y_w, 1]^T \sim \mathbf{H} [u, v, 1]^T \Rightarrow X_w = \frac{h_{11}u + h_{12}v + h_{13}}{h_{31}u + h_{32}v + h_{33}}, \; Y_w = \frac{h_{21}u + h_{22}v + h_{23}}{h_{31}u + h_{32}v + h_{33}}$', 13.5),
    'speed': (r'$\bar{v}(t) = \frac{1}{M} \sum_{m=0}^{M-1} \frac{\Delta d(t-m)}{\Delta t \cdot \Delta k} \quad (\bar{v} < 2.0\mathrm{ m/s}, \; \tau \geq 2.0\mathrm{ s})$', 14.5),
    'ema': (r'$S_i(k) = 0.7 \cdot Q_i(k) + 0.3 \cdot S_i(k-1)$', 15.5),
    'redistribution': (r'$R = \min\left(12.0\mathrm{ s}, \sum_{j \in \mathcal{S}} \max(0, g_j - g_{\min})\right), \; g_i(k+1) = \min\left(g_{\max}, g_i(k) + R \cdot \frac{S_i}{\sum S_m}\right)$', 13),
    'alinea': (r'$r(k) = \mathrm{clamp}\left( r(k-1) + K_R \cdot (o^* - \hat{o}(k)), \; r_{\min}, \; r_{\max} \right)$', 15),
    'ramp_cycle': (r'$T_{\mathrm{cycle}}(k) = \frac{3600}{r(k)}, \quad t_{\mathrm{red}}(k) = \max\left( 0, T_{\mathrm{cycle}}(k) - t_{\mathrm{green}} - t_{\mathrm{yellow}} \right)$', 14),
    'preempt': (r'$D_d(J) \leftarrow D_d(J) + \Delta t_{\mathrm{preempt}}, \quad t_{\mathrm{comp}} = \min(D_{d^*}, 15.0\mathrm{ s})$', 14.5),
    'hcm': (r'$d_i = \max(0, t_{\mathrm{dwell}} - t_{\mathrm{free\_flow}}), \quad \mathrm{Throughput} = \frac{N_{\mathrm{completed}} \times 60}{T_{\mathrm{sim}}}$', 14.5)
}

print("Rendering formulas with balanced fonts...")
for name, (latex, fsize) in formulas.items():
    fig = plt.figure(figsize=(8.5, 1.0))
    plt.axis('off')
    plt.text(0.5, 0.5, latex, fontsize=fsize, ha='center', va='center', color=NAVY_HEX)
    plt.savefig(f'{FORMULA_DIR}/{name}.png', bbox_inches='tight', transparent=True, dpi=300)
    plt.close()

# ==============================================================================
# 2. PRESENTATION INITIALIZATION
# ==============================================================================
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def init_slide():
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = WHITE
    return slide

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_MAIN):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape

def add_header(slide, tag_text, title_text, subtitle_text=""):
    # Tag Pill Box
    tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(3.6), Inches(0.32))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = CARD_TINT
    tag_box.line.color.rgb = BORDER_MAIN
    tag_box.line.width = Pt(1)
    tf = tag_box.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = tag_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    # Title Box
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.5))
    tf = title_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Subtitle Box
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.24), Inches(11.733), Inches(0.35))
        tf = sub_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = subtitle_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = NAVY

    # Top separator line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.64), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_DIVIDER
    line.line.fill.background()

def add_footer(slide, current_slide, total_slides=12):
    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.02), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER_DIVIDER
    line.line.fill.background()

    # Left text
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.06), Inches(8.0), Inches(0.3))
    tf = tx_box.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "AI Traffic Management & Monitoring System — Báo cáo tiến độ dự án"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY

    # Right slide number
    tx_box2 = slide.shapes.add_textbox(Inches(10.533), Inches(7.06), Inches(2.0), Inches(0.3))
    tf2 = tx_box2.text_frame
    tf2.margin_left = tf2.margin_right = tf2.margin_top = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = f"Slide {current_slide} / {total_slides}"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = NAVY
    p2.alignment = PP_ALIGN.RIGHT

# ==============================================================================
# SLIDE 1: COVER & OVERVIEW
# ==============================================================================
slide1 = init_slide()

# Top pill
badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(0.55), Inches(3.933), Inches(0.35))
badge.fill.solid()
badge.fill.fore_color.rgb = CARD_TINT
badge.line.color.rgb = BORDER_MAIN
badge.line.width = Pt(1)
p = badge.text_frame.paragraphs[0]
p.text = "BÁO CÁO TIẾN ĐỘ KỸ THUẬT (PROGRESS REPORT)"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Main Title
title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.05), Inches(11.333), Inches(0.75))
tf = title_box.text_frame
p = tf.paragraphs[0]
p.text = "HỆ THỐNG ĐIỀU PHỐI & GIÁM SÁT GIAO THÔNG THÔNG MINH"
p.font.name = "Segoe UI"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

sub_box = slide1.shapes.add_textbox(Inches(1.5), Inches(1.78), Inches(10.333), Inches(0.4))
tf = sub_box.text_frame
p = tf.paragraphs[0]
p.text = "AI-Based Traffic Management & Monitoring System (YOLOv11m • Leftover-Queue • ALINEA • Next.js 14)"
p.font.name = "Segoe UI"
p.font.size = Pt(11.5)
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Hero Image (Centered with crisp navy border)
hero_img_path = "docs/images/hero-banner.png"
if os.path.exists(hero_img_path):
    pic = slide1.shapes.add_picture(hero_img_path, Inches(2.25), Inches(2.35), width=Inches(8.833))
    pic.line.color.rgb = BORDER_MAIN
    pic.line.width = Pt(1.2)

# 4 Metric Cards (Balanced Grid)
metrics = [
    ("-40.5% ~ -54%", "Giảm thời gian chờ xe"),
    ("94.91%", "YOLOv11m mAP50 (7 Lớp)"),
    ("27.7 FPS", "Tốc độ Edge Inference"),
    ("100% Real-Time", "WebSocket Streaming (10 Hz)")
]

for i, (val, label) in enumerate(metrics):
    left = Inches(0.8 + i * 3.0)
    card = add_card(slide1, left, Inches(5.72), Inches(2.733), Inches(1.15), bg_color=CARD_TINT, border_color=BORDER_MAIN)
    tf = card.text_frame
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.12)
    p1 = tf.paragraphs[0]
    p1.text = val
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = NAVY
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = NAVY
    p2.alignment = PP_ALIGN.CENTER

add_footer(slide1, 1)

# ==============================================================================
# SLIDE 2: ARCHITECTURE (BALANCED PILLARS)
# ==============================================================================
slide2 = init_slide()
add_header(slide2, "TỔNG THỂ HỆ THỐNG", "02. Kiến Trúc Phân Tầng Độc Lập Đã Triển Khai", "Hierarchical & Distributed AI Architecture: Cảm biến → Ra quyết định → Mô phỏng → Nền tảng điều hành")

layers = [
    ("TẦNG 1: PERCEPTION", "packages/cv-pipeline", [
        "• YOLOv11m Detect 7 lớp xe",
        "• ByteTrack Multi-Object Tracker",
        "• Camera Homography Matrix H",
        "• Đo vận tốc thực & Hàng đợi dừng"
    ], "Output: Q_i, v_avg, EV alerts"),
    
    ("TẦNG 2: DECISION & POLICY", "packages/adaptive-policy", [
        "• Leftover-Queue Redistribution",
        "• ALINEA Freeway Ramp Metering",
        "• Emergency Preemption Wave",
        "• Starvation Debt Compensation"
    ], "Output: SignalCommands (phase, dur)"),
    
    ("TẦNG 3: SIMULATION", "packages/sumo-engine", [
        "• SUMO TraCI Engine (10 Hz)",
        "• 3 Mạng lưới (Arterial, Highway, Mix)",
        "• Krauss Car-Following Model",
        "• HCM Control Delay & Throughput"
    ], "Output: Telemetry TickData"),
    
    ("TẦNG 4: FULL-STACK PLATFORM", "backend & frontend", [
        "• FastAPI Async WebSocket Stream",
        "• Next.js 14 Canvas Live Map",
        "• Simulation Lab (A/B Policy Race)",
        "• Groq LLM Traffic Copilot"
    ], "UX: Giám sát & Điều hành tức thì")
]

for i, (title, pkg, items, out_text) in enumerate(layers):
    left = Inches(0.8 + i * 3.0)
    card = add_card(slide2, left, Inches(1.82), Inches(2.733), Inches(4.35), bg_color=WHITE, border_color=BORDER_MAIN)
    
    # Sub-header pill inside card
    sub_pill = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(1.97), Inches(2.433), Inches(0.62))
    sub_pill.fill.solid()
    sub_pill.fill.fore_color.rgb = CARD_TINT
    sub_pill.line.color.rgb = BORDER_SUBTLE
    tf_p = sub_pill.text_frame
    tf_p.margin_top = Inches(0.06)
    p = tf_p.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    p_pkg = tf_p.add_paragraph()
    p_pkg.text = pkg
    p_pkg.font.name = "Consolas"
    p_pkg.font.size = Pt(8.5)
    p_pkg.font.color.rgb = NAVY
    p_pkg.alignment = PP_ALIGN.CENTER

    # Bullets inside card (Proper spacing & fill)
    tx = slide2.shapes.add_textbox(left + Inches(0.15), Inches(2.75), Inches(2.433), Inches(2.6))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for it in items:
        p = tf.add_paragraph()
        p.text = it
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.color.rgb = NAVY
        p.space_after = Pt(10)

    # Bottom output box inside card
    out_box = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(5.5), Inches(2.433), Inches(0.52))
    out_box.fill.solid()
    out_box.fill.fore_color.rgb = CARD_TINT
    out_box.line.color.rgb = BORDER_SUBTLE
    tf_o = out_box.text_frame
    tf_o.margin_top = Inches(0.08)
    p_o = tf_o.paragraphs[0]
    p_o.text = f"✓ {out_text}"
    p_o.font.name = "Segoe UI"
    p_o.font.size = Pt(8.5)
    p_o.font.bold = True
    p_o.font.color.rgb = NAVY
    p_o.alignment = PP_ALIGN.CENTER

# Bottom Summary Card
bot_card = add_card(slide2, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.6), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf = bot_card.text_frame
tf.margin_left = Inches(0.2)
tf.margin_top = Inches(0.1)
p = tf.paragraphs[0]
p.text = "💡 Điểm nhấn kiến trúc: Thiết kế phân tách ghép lỏng (Decoupled Architecture) — Sẵn sàng chuyển giao sang nguồn camera thực địa RTSP mà không phải chỉnh sửa tầng giải thuật điều khiển."
p.font.name = "Segoe UI"
p.font.size = Pt(9.5)
p.font.color.rgb = NAVY

add_footer(slide2, 2)

# ==============================================================================
# SLIDE 3: YOLOv11m & CARLA DATASET
# ==============================================================================
slide3 = init_slide()
add_header(slide3, "THỊ GIÁC MÁY TÍNH", "03. Phân Hệ Thị Giác Máy Tính & Dữ Liệu CARLA", "Huấn luyện YOLOv11m trên 10,064 ảnh độ chân thực cao từ CARLA Simulator kết hợp cân bằng lớp")

# Left Column (5.68 in)
# 1. Dataset Card
c1 = add_card(slide3, Inches(0.8), Inches(1.82), Inches(5.68), Inches(1.5), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf = c1.text_frame
tf.margin_left = Inches(0.2)
tf.margin_top = Inches(0.12)
p = tf.paragraphs[0]
p.text = "DỮ LIỆU TỔNG HỢP CARLA 0.9.16 (SYNTHETIC PHOTOREALISTIC)"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY
p.space_after = Pt(4)

p2 = tf.add_paragraph()
p2.text = "• Khắc phục triệt để lệch miền (Domain Shift) và mất cân bằng lớp của dữ liệu cào web.\n• 10,064 ảnh độ phân giải 1920x1080 qua 13 điều kiện thời tiết (Nắng, Mưa, Hoàng hôn, Đêm).\n• Tăng cường sinh Spawner: Tỷ lệ xe buýt, xe ưu tiên được nhân tạo gấp 2x - 3x."
p2.font.name = "Segoe UI"
p2.font.size = Pt(9.2)
p2.font.color.rgb = NAVY

# 2. Table Card (Centered & Well Balanced)
c_tbl = add_card(slide3, Inches(0.8), Inches(3.45), Inches(5.68), Inches(2.2), bg_color=WHITE, border_color=BORDER_MAIN)
table_shape = slide3.shapes.add_table(5, 3, Inches(0.95), Inches(3.55), Inches(5.38), Inches(2.0))
table = table_shape.table
table.columns[0].width = Inches(1.8)
table.columns[1].width = Inches(1.3)
table.columns[2].width = Inches(2.28)

headers = ["Chỉ số kiểm định", "Kết quả", "Ý nghĩa kỹ thuật"]
for col_idx, h in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = CARD_TINT
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY

rows_data = [
    ("Precision (P)", "96.98%", "Triệt tiêu tối đa báo động giả"),
    ("Recall (R)", "89.67%", "Recall xe buýt: 92.0% (trước: 5.9%)"),
    ("mAP@50", "94.91%", "7 lớp phương tiện đô thị"),
    ("mAP@50-95", "86.49%", "Định vị hộp bao cực kỳ chuẩn xác")
]

for row_idx, (m, val, note) in enumerate(rows_data):
    for col_idx, text in enumerate([m, val, note]):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else CARD_TINT_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = NAVY
        if col_idx == 1:
            p.font.bold = True

# 3. Checkpoint Info Card
chk = add_card(slide3, Inches(0.8), Inches(5.78), Inches(5.68), Inches(1.05), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf = chk.text_frame
tf.margin_left = Inches(0.2)
tf.margin_top = Inches(0.12)
p = tf.paragraphs[0]
p.text = "Checkpoint: packages/cv-pipeline/models/best.pt"
p.font.name = "Consolas"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = NAVY
p2 = tf.add_paragraph()
p2.text = "Dung lượng 40.5 MB | 20.06M tham số | 100 Epochs trên GPU NVIDIA L40S (48GB VRAM)"
p2.font.name = "Segoe UI"
p2.font.size = Pt(9)
p2.font.color.rgb = NAVY

# Right Column Image Card (Symmetric)
r_img_path = "docs/images/realworld-detections.png"
if os.path.exists(r_img_path):
    add_card(slide3, Inches(6.853), Inches(1.82), Inches(5.68), Inches(5.01), bg_color=WHITE, border_color=BORDER_MAIN)
    slide3.shapes.add_picture(r_img_path, Inches(6.95), Inches(1.92), width=Inches(5.486))
    
    cap = slide3.shapes.add_textbox(Inches(6.853), Inches(6.45), Inches(5.68), Inches(0.35))
    tf_c = cap.text_frame
    p = tf_c.paragraphs[0]
    p.text = "Ảnh kiểm thử: Nhận diện đồng thời 7 lớp xe trong điều kiện giao thông phức tạp"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

add_footer(slide3, 3)

# ==============================================================================
# SLIDE 4: MATHEMATICAL LOSS FUNCTIONS (BALANCED & PROPORTIONAL)
# ==============================================================================
slide4 = init_slide()
add_header(slide4, "CƠ SỞ TOÁN HỌC", "04. Công Thức Toán Học - Hàm Mất Mát Thị Giác", "Tối ưu hóa đa nhiệm kết hợp CIoU Bounding Box Loss, BCE Classification và Distribution Focal Loss (DFL)")

# Total loss banner (Width 11.733)
banner = add_card(slide4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.05), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf_b = banner.text_frame
tf_b.margin_top = Inches(0.08)
p_b = tf_b.paragraphs[0]
p_b.text = "TỔNG HÀM MẤT MÁT ĐA NHIỆM HUẤN LUYỆN (MULTI-TASK OBJECTIVE)"
p_b.font.name = "Segoe UI"
p_b.font.size = Pt(9.5)
p_b.font.bold = True
p_b.font.color.rgb = NAVY
p_b.alignment = PP_ALIGN.CENTER

slide4.shapes.add_picture(f"{FORMULA_DIR}/loss_total.png", Inches(3.4), Inches(2.18), width=Inches(6.5))

# 3 Loss Cards (Width 3.68, Gap 0.34)
losses = [
    ("1. HỒI QUY VỊ TRÍ (CIoU LOSS)", "ciou", "ciou_v", [
        "• Tối ưu hóa diện tích giao IoU",
        "• Phạt khoảng cách tâm Euclidean rho",
        "• Bù trừ tỷ lệ co dãn hai chiều v và alpha"
    ]),
    ("2. PHÂN LOẠI (BCE WITH LOGITS)", "cls", None, [
        "• Phân loại độc lập cho K = 7 lớp xe",
        "• Triệt tiêu áp chế xác suất giữa các lớp",
        "• Trọng số phạt lỗi phân loại: lambda = 0.5"
    ]),
    ("3. PHÂN PHỐI BIÊN TIÊU CỰ (DFL)", "dfl", None, [
        "• Học phân phối xác suất liên tục biên",
        "• Thay thế điểm cứng Dirac delta",
        "• Tăng độ nhạy khi xe bị mờ hoặc che khuất"
    ])
]

for i, (title, f_name, f_sub, bullets) in enumerate(losses):
    left = Inches(0.8 + i * 4.02)
    card = add_card(slide4, left, Inches(3.0), Inches(3.68), Inches(2.95), bg_color=WHITE, border_color=BORDER_MAIN)
    
    # Title inside card
    t_box = slide4.shapes.add_textbox(left + Inches(0.15), Inches(3.1), Inches(3.38), Inches(0.35))
    tf = t_box.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Sub-card for formula image (Balanced heights)
    f_subcard = add_card(slide4, left + Inches(0.15), Inches(3.5), Inches(3.38), Inches(1.15), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
    
    if f_sub:
        slide4.shapes.add_picture(f"{FORMULA_DIR}/{f_name}.png", left + Inches(0.25), Inches(3.55), width=Inches(3.18))
        slide4.shapes.add_picture(f"{FORMULA_DIR}/{f_sub}.png", left + Inches(0.25), Inches(4.1), width=Inches(3.18))
    else:
        slide4.shapes.add_picture(f"{FORMULA_DIR}/{f_name}.png", left + Inches(0.25), Inches(3.78), width=Inches(3.18))

    # Bullets below formula (Evenly distributed)
    tx_b = slide4.shapes.add_textbox(left + Inches(0.15), Inches(4.78), Inches(3.38), Inches(1.05))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    for b in bullets:
        p = tf_b.add_paragraph()
        p.text = b
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = NAVY
        p.space_after = Pt(4)

# Learning rate scheduler bar (Scaled nicely to fit inside box without overflowing)
lr_card = add_card(slide4, Inches(0.8), Inches(6.04), Inches(11.733), Inches(0.85), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf_l = lr_card.text_frame
tf_l.margin_top = Inches(0.06)
p_l = tf_l.paragraphs[0]
p_l.text = "LỊCH TRÌNH TỐC ĐỘ HỌC (LEARNING RATE SCHEDULER)"
p_l.font.name = "Segoe UI"
p_l.font.size = Pt(9)
p_l.font.bold = True
p_l.font.color.rgb = NAVY
p_l.alignment = PP_ALIGN.CENTER

slide4.shapes.add_picture(f"{FORMULA_DIR}/lr.png", Inches(4.0), Inches(6.32), width=Inches(5.333))

add_footer(slide4, 4)

# ==============================================================================
# SLIDE 5: BYTETRACK & HOMOGRAPHY
# ==============================================================================
slide5 = init_slide()
add_header(slide5, "THEO DÕI & ĐO ĐẠC", "05. Theo Dõi Đa Đối Tượng & Chiếu Tọa Độ Thực", "ByteTrack 2 tầng duy trì ID phương tiện liên tục và ma trận Homography mặt đất xác định vận tốc")

# Left Column (5.68 in)
# Card 1: Kalman
c1 = add_card(slide5, Inches(0.8), Inches(1.82), Inches(5.68), Inches(1.52), bg_color=WHITE, border_color=BORDER_MAIN)
t_b1 = slide5.shapes.add_textbox(Inches(0.95), Inches(1.92), Inches(5.38), Inches(0.3))
p = t_b1.text_frame.paragraphs[0]
p.text = "1. THEO DÕI LIÊN TỤC VỚI BYTETRACK & KALMAN 8 TRẠNG THÁI"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

f1 = add_card(slide5, Inches(0.95), Inches(2.25), Inches(5.38), Inches(0.65), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
slide5.shapes.add_picture(f"{FORMULA_DIR}/kalman.png", Inches(1.1), Inches(2.29), width=Inches(5.08))

tx1 = slide5.shapes.add_textbox(Inches(0.95), Inches(2.94), Inches(5.38), Inches(0.35))
p = tx1.text_frame.paragraphs[0]
p.text = "Ghép nối 2 tầng (Two-Stage Hungarian) phục hồi đối tượng bị che khuất tạm thời."
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.color.rgb = NAVY

# Card 2: Homography
c2 = add_card(slide5, Inches(0.8), Inches(3.46), Inches(5.68), Inches(1.62), bg_color=WHITE, border_color=BORDER_MAIN)
t_b2 = slide5.shapes.add_textbox(Inches(0.95), Inches(3.56), Inches(5.38), Inches(0.3))
p = t_b2.text_frame.paragraphs[0]
p.text = "2. MA TRẬN HOMOGRAPHY MẶT ĐẤT (GROUND-PLANE H)"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

f2 = add_card(slide5, Inches(0.95), Inches(3.9), Inches(5.38), Inches(0.68), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
slide5.shapes.add_picture(f"{FORMULA_DIR}/homography.png", Inches(1.05), Inches(3.94), width=Inches(5.18))

tx2 = slide5.shapes.add_textbox(Inches(0.95), Inches(4.62), Inches(5.38), Inches(0.4))
p = tx2.text_frame.paragraphs[0]
p.text = "Chiếu điểm tiếp đất bánh xe (u_ref, v_ref) sang hệ tọa độ thực tế (X_w, Y_w) với Z_w = 0."
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.color.rgb = NAVY

# Card 3: Speed & Queue
c3 = add_card(slide5, Inches(0.8), Inches(5.2), Inches(5.68), Inches(1.62), bg_color=WHITE, border_color=BORDER_MAIN)
t_b3 = slide5.shapes.add_textbox(Inches(0.95), Inches(5.3), Inches(5.38), Inches(0.3))
p = t_b3.text_frame.paragraphs[0]
p.text = "3. ƯỚC LƯỢNG VẬN TỐC THỰC & TIÊU CHUẨN XE CHỜ ĐÈN ĐỎ"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

f3 = add_card(slide5, Inches(0.95), Inches(5.62), Inches(5.38), Inches(0.65), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
slide5.shapes.add_picture(f"{FORMULA_DIR}/speed.png", Inches(1.15), Inches(5.66), width=Inches(4.98))

tx3 = slide5.shapes.add_textbox(Inches(0.95), Inches(6.3), Inches(5.38), Inches(0.45))
p = tx3.text_frame.paragraphs[0]
p.text = "Lọc vận tốc trượt M = 5 frames. Xác nhận xe chờ khi v < 2.0 m/s trong >= 2.0 giây."
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.color.rgb = NAVY

# Right Column Image Card (Symmetric)
col_img_path = "docs/images/collision-detection.png"
if os.path.exists(col_img_path):
    add_card(slide5, Inches(6.853), Inches(1.82), Inches(5.68), Inches(5.0), bg_color=WHITE, border_color=BORDER_MAIN)
    slide5.shapes.add_picture(col_img_path, Inches(6.95), Inches(1.92), width=Inches(5.486))

    cap = slide5.shapes.add_textbox(Inches(6.853), Inches(6.45), Inches(5.68), Inches(0.35))
    tf_c = cap.text_frame
    p = tf_c.paragraphs[0]
    p.text = "Trực quan: Khung theo dõi ID phương tiện, quỹ đạo di chuyển và cảnh báo xung đột"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

add_footer(slide5, 5)

# ==============================================================================
# SLIDE 6: LEFTOVER-QUEUE REDISTRIBUTION (WELL-BALANCED FRAMES)
# ==============================================================================
slide6 = init_slide()
add_header(slide6, "ĐIỀU KHIỂN THÍCH NGHI", "06. Thuật Toán Thích Nghi - Tái Phân Bổ Hàng Đợi Tồn Dư", "Leftover-Queue Actuated Signal Control: Cân bằng thời lượng xanh chu kỳ tại thời điểm chớm vàng")

# Top Principle Banner
p_banner = add_card(slide6, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.55), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf_p = p_banner.text_frame
tf_p.margin_left = Inches(0.2)
tf_p.margin_top = Inches(0.12)
p = tf_p.paragraphs[0]
p.text = "💡 Nguyên lý điều khiển: Không phụ thuộc vào lưu lượng dự báo xa; thuật toán đo số xe còn đọng lại tại thời điểm chớm vàng để san sẻ thời gian xanh giữa các hướng."
p.font.name = "Segoe UI"
p.font.size = Pt(9.5)
p.font.color.rgb = NAVY

# 3 Steps Cards (Height 3.48, fully balanced)
steps = [
    ("BƯỚC 1: LÀM MỊN HÀNG ĐỢI TỒN", "Lọc qua bộ lọc EMA với alpha = 0.7 để khử nhiễu:", "ema", [
        "• Ghi nhận Q_i(k) tại thời điểm chớm vàng",
        "• Khử dao động ngẫu nhiên giữa các chu kỳ",
        "• Phản ánh trung thực nhu cầu dòng xe thực",
        "• Cơ sở tính toán tái phân bổ ổn định"
    ], "Lọc thông thấp EMA (alpha = 0.7)"),
    
    ("BƯỚC 2: PHÂN NHÓM TRẠNG THÁI", "Chia các nhóm pha thành hai tập rời rạc:", None, [
        "• Nhóm U (Undersupplied): S_i > 0 (Còn tồn)",
        "• Nhóm S (Satisfied): S_j <= 0 (Đã thông thoáng)",
        "• Trích ngân sách thời gian từ nhóm S",
        "• Giới hạn trích xuất tối đa R_max = 12.0 s"
    ], "Phân tách rời rạc U và S"),
    
    ("BƯỚC 3: TÁI PHÂN PHỐI CÓ RÀNG BUỘC", "Cấp thêm thời gian theo tỷ trọng thiếu hụt:", "redistribution", [
        "• Giảm thời gian xanh ở các hướng thỏa mãn",
        "• Bù cho hướng thiếu theo w_i = S_i / sum S_m",
        "• Bảo toàn tổng chu kỳ điều khiển giao lộ",
        "• Tuân thủ nghiêm ngặt biên an toàn [10s, 50s]"
    ], "Tái phân bổ theo tỷ trọng w_i")
]

for i, (stitle, sdesc, sfname, sbullets, sfoot) in enumerate(steps):
    left = Inches(0.8 + i * 4.02)
    card = add_card(slide6, left, Inches(2.48), Inches(3.68), Inches(3.48), bg_color=WHITE, border_color=BORDER_MAIN)
    
    # Title inside card
    t_box = slide6.shapes.add_textbox(left + Inches(0.15), Inches(2.58), Inches(3.38), Inches(0.32))
    tf = t_box.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = stitle
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = NAVY

    # Subhead inside card
    d_box = slide6.shapes.add_textbox(left + Inches(0.15), Inches(2.9), Inches(3.38), Inches(0.3))
    tf_d = d_box.text_frame
    tf_d.margin_left = tf_d.margin_top = 0
    p = tf_d.paragraphs[0]
    p.text = sdesc
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY

    # Sub-card for formula
    if sfname:
        f_card = add_card(slide6, left + Inches(0.15), Inches(3.22), Inches(3.38), Inches(0.72), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
        slide6.shapes.add_picture(f"{FORMULA_DIR}/{sfname}.png", left + Inches(0.25), Inches(3.26), width=Inches(3.18))
    else:
        # Step 2 visual box
        def_card = add_card(slide6, left + Inches(0.15), Inches(3.22), Inches(3.38), Inches(0.72), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
        tf_def = def_card.text_frame
        tf_def.margin_left = Inches(0.1)
        tf_def.margin_top = Inches(0.06)
        p1 = tf_def.paragraphs[0]
        p1.text = "U = { i | S_i(k) > 0 }  (Thiếu thời gian xanh)"
        p1.font.name = "Consolas"
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p2 = tf_def.add_paragraph()
        p2.text = "S = { j | S_j(k) <= 0 } (Đã giải phóng hết xe)"
        p2.font.name = "Consolas"
        p2.font.size = Pt(8)
        p2.font.bold = True
        p2.font.color.rgb = NAVY

    # Bullets (Fills the middle gracefully)
    tx_b = slide6.shapes.add_textbox(left + Inches(0.15), Inches(4.02), Inches(3.38), Inches(1.4))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    for b in sbullets:
        p = tf_b.add_paragraph()
        p.text = b
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.8)
        p.font.color.rgb = NAVY
        p.space_after = Pt(3)

    # Bottom pill inside card
    foot_pill = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(5.48), Inches(3.38), Inches(0.36))
    foot_pill.fill.solid()
    foot_pill.fill.fore_color.rgb = CARD_TINT
    foot_pill.line.color.rgb = BORDER_SUBTLE
    tf_fp = foot_pill.text_frame
    tf_fp.margin_top = Inches(0.06)
    p_fp = tf_fp.paragraphs[0]
    p_fp.text = f"✓ {sfoot}"
    p_fp.font.name = "Segoe UI"
    p_fp.font.size = Pt(8.5)
    p_fp.font.bold = True
    p_fp.font.color.rgb = NAVY
    p_fp.alignment = PP_ALIGN.CENTER

# Bottom Safety Box
safe_card = add_card(slide6, Inches(0.8), Inches(6.08), Inches(11.733), Inches(0.78), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf_s = safe_card.text_frame
tf_s.margin_left = Inches(0.2)
tf_s.margin_top = Inches(0.08)
p = tf_s.paragraphs[0]
p.text = "🛡️ RÀNG BUỘC AN TOÀN TUYỆT ĐỐI (HARD SAFETY CONSTRAINTS)"
p.font.name = "Segoe UI"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = NAVY
p2 = tf_s.add_paragraph()
p2.text = "Thời lượng xanh tối thiểu g_min = 10.0 s (cho người đi bộ qua đường) | Thời lượng xanh tối đa g_max = 50.0 s | Biên độ thay đổi mỗi chu kỳ R_max = 12.0 s"
p2.font.name = "Segoe UI"
p2.font.size = Pt(9)
p2.font.color.rgb = NAVY

add_footer(slide6, 6)

# ==============================================================================
# SLIDE 7: ALINEA RAMP METERING (HARMONIOUS 4 BOXES)
# ==============================================================================
slide7 = init_slide()
add_header(slide7, "ĐIỀU TIẾT CAO TỐC", "07. Điều Tiết Nhập Làn Cao Tốc ALINEA & Chống Tràn", "Luật điều khiển tích phân vòng kín Papageorgiou et al. giữ mật độ tuyến chính dưới điểm sụp đổ lưu lượng")

# All 4 cards have matching structure: WHITE background, BORDER_MAIN, CARD_TINT sub-box!
# Top Left: ALINEA Law
c1 = add_card(slide7, Inches(0.8), Inches(1.82), Inches(5.68), Inches(2.42), bg_color=WHITE, border_color=BORDER_MAIN)
t_b1 = slide7.shapes.add_textbox(Inches(0.95), Inches(1.92), Inches(5.38), Inches(0.3))
p = t_b1.text_frame.paragraphs[0]
p.text = "1. LUẬT ĐIỀU KHIỂN HỒI TIẾP TÍCH PHÂN ALINEA"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

f1 = add_card(slide7, Inches(0.95), Inches(2.26), Inches(5.38), Inches(0.68), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
slide7.shapes.add_picture(f"{FORMULA_DIR}/alinea.png", Inches(1.1), Inches(2.3), width=Inches(5.08))

tx1 = slide7.shapes.add_textbox(Inches(0.95), Inches(3.04), Inches(5.38), Inches(1.1))
tf = tx1.text_frame
tf.margin_left = tf.margin_top = 0
for b in [
    "• K_R = 70.0 veh/h/%: Hệ số khuếch đại tích phân",
    "• o* = 20%: Mật độ chiếm dụng mục tiêu lý tưởng tại hạ lưu",
    "• [r_min, r_max] = [200, 1200] veh/h: Giới hạn lưu lượng cấp xe"
]:
    p = tf.add_paragraph()
    p.text = b
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY
    p.space_after = Pt(2)

# Bottom Left: Cycle Conversion
c2 = add_card(slide7, Inches(0.8), Inches(4.38), Inches(5.68), Inches(2.45), bg_color=WHITE, border_color=BORDER_MAIN)
t_b2 = slide7.shapes.add_textbox(Inches(0.95), Inches(4.48), Inches(5.38), Inches(0.3))
p = t_b2.text_frame.paragraphs[0]
p.text = "2. QUY ĐỔI SANG THỜI LƯỢNG ĐÈN METERING"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

f2 = add_card(slide7, Inches(0.95), Inches(4.82), Inches(5.38), Inches(0.68), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
slide7.shapes.add_picture(f"{FORMULA_DIR}/ramp_cycle.png", Inches(1.1), Inches(4.86), width=Inches(5.08))

tx2 = slide7.shapes.add_textbox(Inches(0.95), Inches(5.6), Inches(5.38), Inches(1.1))
tf = tx2.text_frame
tf.margin_left = tf.margin_top = 0
for b in [
    "• Thời lượng xanh cố định t_green = 2.0 s (cấp 1 xe nhập làn mỗi chu kỳ)",
    "• Thời lượng vàng cố định t_yellow = 1.0 s",
    "• Thời lượng đỏ t_red(k) điều biến tự động theo chu kỳ T_cycle"
]:
    p = tf.add_paragraph()
    p.text = b
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY
    p.space_after = Pt(2)

# Top Right: Spillback Override
c3 = add_card(slide7, Inches(6.853), Inches(1.82), Inches(5.68), Inches(2.42), bg_color=WHITE, border_color=BORDER_MAIN)
t_b3 = slide7.shapes.add_textbox(Inches(7.0), Inches(1.92), Inches(5.38), Inches(0.3))
p = t_b3.text_frame.paragraphs[0]
p.text = "⚠️ CƠ CHẾ GHI ĐÈ CHỐNG TRÀN NHÁNH NỐI (SPILLBACK OVERRIDE)"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

ov_box = add_card(slide7, Inches(7.0), Inches(2.26), Inches(5.38), Inches(0.68), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
tf_ov = ov_box.text_frame
tf_ov.margin_top = Inches(0.12)
p = tf_ov.paragraphs[0]
p.text = "Nếu Q_ramp(k) >= 30 xe ⇒ r(k) = r_max (1200 veh/h)"
p.font.name = "Consolas"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

tx3 = slide7.shapes.add_textbox(Inches(7.0), Inches(3.04), Inches(5.38), Inches(1.1))
tf = tx3.text_frame
tf.margin_left = tf.margin_top = 0
for b in [
    "• Ngăn dòng xe xếp hàng trên nhánh nối tràn ngược làm nghẽn đường đô thị",
    "• Mở xả tối đa giải tỏa nhánh nhập làn khẩn cấp",
    "• Tự động phục hồi luật hồi tiếp ALINEA khi hàng đợi đã giải phóng"
]:
    p = tf.add_paragraph()
    p.text = b
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY
    p.space_after = Pt(2)

# Bottom Right: Physical Schema
c4 = add_card(slide7, Inches(6.853), Inches(4.38), Inches(5.68), Inches(2.45), bg_color=WHITE, border_color=BORDER_MAIN)
t_b4 = slide7.shapes.add_textbox(Inches(7.0), Inches(4.48), Inches(5.38), Inches(0.3))
p = t_b4.text_frame.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & ON-RAMP METERING"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

d_box = add_card(slide7, Inches(7.0), Inches(4.82), Inches(5.38), Inches(1.15), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
tf_d = d_box.text_frame
tf_d.margin_left = Inches(0.15)
tf_d.margin_top = Inches(0.1)
p = tf_d.paragraphs[0]
p.text = "Tuyến chính cao tốc ═════[ Cảm biến ô(k) ]═════▶ Thông suốt\n                                      ▲ Điểm hòa dòng\nNhánh nối On-Ramp ───────[ Đèn Meter r(k) ]"
p.font.name = "Consolas"
p.font.size = Pt(8.5)
p.font.color.rgb = NAVY

tx4 = slide7.shapes.add_textbox(Inches(7.0), Inches(6.05), Inches(5.38), Inches(0.7))
tf = tx4.text_frame
tf.margin_left = tf.margin_top = 0
p = tf.paragraphs[0]
p.text = "Cảm biến hạ lưu đo mật độ ô(k) hồi tiếp về bộ điều khiển ALINEA theo chu kỳ 10 giây."
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.color.rgb = NAVY

add_footer(slide7, 7)

# ==============================================================================
# SLIDE 8: EMERGENCY PREEMPTION (BALANCED CARDS)
# ==============================================================================
slide8 = init_slide()
add_header(slide8, "ƯU TIÊN KHẨN CẤP", "08. Cơ Chế Ưu Tiên Xe Khẩn Cấp & Bù Trừ Nợ Xanh", "Phát hiện xe cứu thương, cứu hỏa, cảnh sát → Kích hoạt làn sóng xanh → Hoàn trả công nợ thời gian")

stages = [
    ("GIAI ĐOẠN 1: KÍCH HOẠT ƯU TIÊN", "Nhận diện phương tiện khẩn cấp:", "phi_J ← phi_EV(e) (Pha xanh tức thời)", [
        "• Camera/SUMO phát hiện Ambulance/Police",
        "• Xác định hướng di chuyển và nút giao J",
        "• Kích hoạt ngay pha xanh dọn đường",
        "• Xe khẩn cấp vượt giao lộ trong 0s chờ"
    ], "Kích hoạt tức thời (0s delay)"),
    
    ("GIAI ĐOẠN 2: TÍCH LŨY CÔNG NỢ", "Ghi nhận thiệt hại các hướng khác:", "D_d(J) ← D_d(J) + delta_t_preempt", [
        "• Các hướng trực giao bị cắt quyền đi",
        "• Tích lũy công nợ thời gian suốt delta_t",
        "• Ghi nhận vào sổ nợ giao lộ D_d(J)",
        "• Đảm bảo tính minh bạch điều hành"
    ], "Ghi nhận nợ giao lộ D_d(J)"),
    
    ("GIAI ĐOẠN 3: BÙ NỢ CÔNG BẰNG", "Hoàn trả thời gian sau ưu tiên:", "t_comp = min( D_d*, 15.0 s )", [
        "• Xe khẩn cấp vừa rời khỏi nút giao",
        "• Tìm hướng chịu thiệt hại lớn nhất d*",
        "• Cấp bù thời gian xanh t_comp cho d*",
        "• Tránh hiện tượng nghẽn lan tỏa"
    ], "Hoàn trả nợ công bằng")
]

for i, (stitle, sdesc, scond, sbullets, sfoot) in enumerate(stages):
    left = Inches(0.8 + i * 4.02)
    card = add_card(slide8, left, Inches(1.82), Inches(3.68), Inches(3.38), bg_color=WHITE, border_color=BORDER_MAIN)
    
    t_box = slide8.shapes.add_textbox(left + Inches(0.15), Inches(1.92), Inches(3.38), Inches(0.32))
    tf = t_box.text_frame
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = stitle
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY

    d_box = slide8.shapes.add_textbox(left + Inches(0.15), Inches(2.24), Inches(3.38), Inches(0.28))
    tf_d = d_box.text_frame
    tf_d.margin_left = tf_d.margin_top = 0
    p = tf_d.paragraphs[0]
    p.text = sdesc
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY

    c_box = add_card(slide8, left + Inches(0.15), Inches(2.54), Inches(3.38), Inches(0.55), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
    tf_c = c_box.text_frame
    tf_c.margin_top = Inches(0.06)
    p = tf_c.paragraphs[0]
    p.text = scond
    p.font.name = "Consolas"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

    tx_b = slide8.shapes.add_textbox(left + Inches(0.15), Inches(3.18), Inches(3.38), Inches(1.4))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    for b in sbullets:
        p = tf_b.add_paragraph()
        p.text = b
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.8)
        p.font.color.rgb = NAVY
        p.space_after = Pt(2.5)

    # Bottom pill
    foot_pill = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(4.72), Inches(3.38), Inches(0.36))
    foot_pill.fill.solid()
    foot_pill.fill.fore_color.rgb = CARD_TINT
    foot_pill.line.color.rgb = BORDER_SUBTLE
    tf_fp = foot_pill.text_frame
    tf_fp.margin_top = Inches(0.06)
    p_fp = tf_fp.paragraphs[0]
    p_fp.text = f"✓ {sfoot}"
    p_fp.font.name = "Segoe UI"
    p_fp.font.size = Pt(8.5)
    p_fp.font.bold = True
    p_fp.font.color.rgb = NAVY
    p_fp.alignment = PP_ALIGN.CENTER

# Bottom Formula & Result Card
f_card = add_card(slide8, Inches(0.8), Inches(5.32), Inches(11.733), Inches(1.55), bg_color=CARD_TINT, border_color=BORDER_MAIN)
t_bf = slide8.shapes.add_textbox(Inches(0.95), Inches(5.42), Inches(11.433), Inches(0.28))
p = t_bf.text_frame.paragraphs[0]
p.text = "CÔNG THỨC TOÁN HỌC CƠ CHẾ HOÀN NỢ (DEBT PAYBACK FORMULATION)"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = NAVY

slide8.shapes.add_picture(f"{FORMULA_DIR}/preempt.png", Inches(3.3), Inches(5.74), width=Inches(6.7))

tx_r = slide8.shapes.add_textbox(Inches(0.95), Inches(6.45), Inches(11.433), Inches(0.35))
p = tx_r.text_frame.paragraphs[0]
p.text = "✓ Kết quả thực nghiệm: Phương tiện khẩn cấp di chuyển qua giao lộ với 0 giây chờ đợi; các hướng trực giao được giải phóng ngay sau đó mà không phát sinh ùn ứ dây chuyền."
p.font.name = "Segoe UI"
p.font.size = Pt(9.2)
p.font.bold = True
p.font.color.rgb = NAVY

add_footer(slide8, 8)

# ==============================================================================
# SLIDE 9: SUMO SIMULATION NETWORKS (BALANCED IMAGES)
# ==============================================================================
slide9 = init_slide()
add_header(slide9, "MÔ PHỎNG VI MÔ", "09. Mô Phỏng Vi Mô SUMO & 3 Mạng Lưới Đã Xây Dựng", "Tích hợp TraCI Socket Protocol 10 Hz và 3 mô hình mạng lưới kiểm thử chuyên biệt")

nets = [
    ("1. Mạng Arterial Grid (3x2)", "docs/images/arterial-grid.png", "6 Nút giao liên hoàn", [
        "• Kiểm thử điều phối đèn đa nút",
        "• Giải quyết xung đột làn rẽ trái",
        "• Đồng bộ Dual-Ring 2 chiều"
    ], "6 Nút Đèn Tín Hiệu"),
    
    ("2. Mạng Highway Corridor", "docs/images/highway-corridor.png", "Cao tốc 3 làn & 2 On-Ramp", [
        "• Kiểm thử thuật toán ALINEA",
        "• Ngăn chặn tắc nghẽn sụp đổ",
        "• Khai thác điểm hòa dòng"
    ], "Tuyến Cao Tốc 3.2 km"),
    
    ("3. Mạng Kết Hợp (Combined)", "docs/images/combined-network.png", "Hệ thống đô thị tích hợp", [
        "• Nội đô kết nối cao tốc liên vùng",
        "• Kiểm thử tải toàn diện End-to-End",
        "• Mô hình di chuyển hỗn hợp"
    ], "Đô Thị & Cao Tốc")
]

for i, (title, img_path, badge_txt, bullets, spec_txt) in enumerate(nets):
    left = Inches(0.8 + i * 4.02)
    card = add_card(slide9, left, Inches(1.82), Inches(3.68), Inches(4.35), bg_color=WHITE, border_color=BORDER_MAIN)
    
    t_box = slide9.shapes.add_textbox(left + Inches(0.15), Inches(1.92), Inches(3.38), Inches(0.3))
    p = t_box.text_frame.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = NAVY

    b_box = slide9.shapes.add_textbox(left + Inches(0.15), Inches(2.2), Inches(3.38), Inches(0.25))
    p = b_box.text_frame.paragraphs[0]
    p.text = badge_txt
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY

    # Image container with centered placement
    if os.path.exists(img_path):
        img_container = add_card(slide9, left + Inches(0.15), Inches(2.48), Inches(3.38), Inches(1.85), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
        slide9.shapes.add_picture(img_path, left + Inches(0.22), Inches(2.52), width=Inches(3.24))

    # Bullets
    tx_b = slide9.shapes.add_textbox(left + Inches(0.15), Inches(4.42), Inches(3.38), Inches(1.2))
    tf_b = tx_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    for b in bullets:
        p = tf_b.add_paragraph()
        p.text = b
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.8)
        p.font.color.rgb = NAVY
        p.space_after = Pt(2.5)

    # Bottom badge
    spec_pill = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left + Inches(0.15), Inches(5.68), Inches(3.38), Inches(0.36))
    spec_pill.fill.solid()
    spec_pill.fill.fore_color.rgb = CARD_TINT
    spec_pill.line.color.rgb = BORDER_SUBTLE
    tf_sp = spec_pill.text_frame
    tf_sp.margin_top = Inches(0.06)
    p_sp = tf_sp.paragraphs[0]
    p_sp.text = f"⚙️ {spec_txt}"
    p_sp.font.name = "Segoe UI"
    p_sp.font.size = Pt(8.5)
    p_sp.font.bold = True
    p_sp.font.color.rgb = NAVY
    p_sp.alignment = PP_ALIGN.CENTER

# Bottom Tech specs
b_card = add_card(slide9, Inches(0.8), Inches(6.28), Inches(11.733), Inches(0.6), bg_color=CARD_TINT, border_color=BORDER_MAIN)
tf = b_card.text_frame
tf.margin_left = Inches(0.2)
tf.margin_top = Inches(0.1)
p = tf.paragraphs[0]
p.text = "⚙️ Thông số SUMO: TraCI Socket tần số 10 Hz (Delta_t = 0.1 s) | Mô hình xe bám đuôi Krauss Car-Following Model | Dual-Ring Permissive Left Turn"
p.font.name = "Segoe UI"
p.font.size = Pt(9.5)
p.font.color.rgb = NAVY

add_footer(slide9, 9)

# ==============================================================================
# SLIDE 10: FULL-STACK PLATFORM & DASHBOARD
# ==============================================================================
slide10 = init_slide()
add_header(slide10, "NỀN TẢNG FULL-STACK", "10. Nền Tảng Full-Stack: Backend & Operator Dashboard", "FastAPI Async WebSocket Engine và Next.js 14 Interactive Operator Dashboard")

# Left Column Image Card (Well-framed)
dash_img_path = "docs/images/dashboard.png"
if os.path.exists(dash_img_path):
    add_card(slide10, Inches(0.8), Inches(1.82), Inches(6.2), Inches(5.02), bg_color=WHITE, border_color=BORDER_MAIN)
    slide10.shapes.add_picture(dash_img_path, Inches(0.9), Inches(1.92), width=Inches(6.0))

    cap = slide10.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(6.2), Inches(0.35))
    tf_c = cap.text_frame
    p = tf_c.paragraphs[0]
    p.text = "Giao diện Dashboard: Bản đồ nhiệt trực tiếp, thông số từng nút giao và telemetry thời gian thực"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

# Right Column Features
feats = [
    ("⚡ FASTAPI BACKEND HIGH-CONCURRENCY", [
        "• Khử TCP Backpressure: Bọc lệnh gửi socket với timeout tau_ws <= 0.15 s tránh làm lag luồng mô phỏng.",
        "• Nén Payload JSON: Giảm 45% kích thước gói tin tick-by-tick (32 KB vs 60 KB)."
    ]),
    
    ("🔬 PHÒNG THÍ NGHIỆM ĐUA CHÍNH SÁCH (LAB)", [
        "• Chạy song song 2 phiên mô phỏng đối đầu (Fixed-Time vs Adaptive) cùng seed ngẫu nhiên 42.",
        "• Quan sát trực tiếp sự phân hóa hàng đợi và thời gian chờ tích lũy."
    ]),
    
    ("🤖 TRỢ LÝ GROQ LLM TRAFFIC COPILOT", [
        "• Tích hợp LLM Groq giải thích nguyên nhân chuyển pha đèn bằng ngôn ngữ tự nhiên.",
        "• Đưa ra khuyến nghị điều phối khi phát hiện điểm nghẽn bất thường."
    ])
]

for i, (title, items) in enumerate(feats):
    top = Inches(1.82 + i * 1.72)
    card = add_card(slide10, Inches(7.273), top, Inches(5.26), Inches(1.58), bg_color=WHITE, border_color=BORDER_MAIN)
    
    t_box = slide10.shapes.add_textbox(Inches(7.423), top + Inches(0.12), Inches(4.96), Inches(0.3))
    p = t_box.text_frame.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = NAVY

    tx = slide10.shapes.add_textbox(Inches(7.423), top + Inches(0.48), Inches(4.96), Inches(1.0))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for it in items:
        p = tf.add_paragraph()
        p.text = it
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = NAVY
        p.space_after = Pt(3)

add_footer(slide10, 10)

# ==============================================================================
# SLIDE 11: BENCHMARK RESULTS (PERFECTLY FRAMED)
# ==============================================================================
slide11 = init_slide()
add_header(slide11, "KẾT QUẢ THỰC NGHIỆM", "11. Kết Quả Đo Kiểm Benchmark (HCM Metrics)", "Đánh giá định lượng trên 5,500 phương tiện qua 3 profile nhu cầu (Race Framework đối đầu)")

# Left Column (5.68 in)
# Table Card
add_card(slide11, Inches(0.8), Inches(1.82), Inches(5.68), Inches(2.55), bg_color=WHITE, border_color=BORDER_MAIN)
table_shape = slide11.shapes.add_table(4, 5, Inches(0.92), Inches(1.92), Inches(5.44), Inches(2.35))
table = table_shape.table
table.columns[0].width = Inches(1.2)
table.columns[1].width = Inches(0.75)
table.columns[2].width = Inches(1.0)
table.columns[3].width = Inches(1.0)
table.columns[4].width = Inches(1.49)

b_headers = ["Kịch bản", "Số xe", "Fixed-Time", "Adaptive", "Cải thiện"]
for col_idx, h in enumerate(b_headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = CARD_TINT
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY

b_rows = [
    ("Balanced", "5,500", "65.4 s", "38.9 s", "-40.5% (clear +14%)"),
    ("Asymmetric", "5,500", "88.2 s", "42.1 s", "-52.3% (clear +22%)"),
    ("Extreme", "5,500", "124.6 s", "57.3 s", "-54.0% (clear +28%)")
]

for row_idx, r in enumerate(b_rows):
    for col_idx, val in enumerate(r):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE if row_idx % 2 == 0 else CARD_TINT_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        p.font.color.rgb = NAVY
        if col_idx in (3, 4):
            p.font.bold = True

# HCM Formulas Card
hcm_card = add_card(slide11, Inches(0.8), Inches(4.5), Inches(5.68), Inches(2.34), bg_color=CARD_TINT, border_color=BORDER_MAIN)
t_h = slide11.shapes.add_textbox(Inches(0.95), Inches(4.6), Inches(5.38), Inches(0.3))
p = t_h.text_frame.paragraphs[0]
p.text = "TIÊU CHUẨN HIGHWAY CAPACITY MANUAL (HCM)"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY

f_h = add_card(slide11, Inches(0.95), Inches(4.95), Inches(5.38), Inches(0.72), bg_color=WHITE, border_color=BORDER_SUBTLE)
slide11.shapes.add_picture(f"{FORMULA_DIR}/hcm.png", Inches(1.1), Inches(5.0), width=Inches(5.08))

tx_h = slide11.shapes.add_textbox(Inches(0.95), Inches(5.74), Inches(5.38), Inches(0.98))
tf = tx_h.text_frame
tf.margin_left = tf.margin_top = 0
for b in [
    "• Control Delay: Thời gian hao phí thực tế so với lưu thông tự do vùng 50m",
    "• Throughput: Số chuyến đi hoàn thành thành công rời mạng lưới trên mỗi phút"
]:
    p = tf.add_paragraph()
    p.text = b
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = NAVY
    p.space_after = Pt(3)

# Right Column Image Card (Symmetric & Centered)
w_img_path = "docs/images/waiting-time.png"
if os.path.exists(w_img_path):
    add_card(slide11, Inches(6.853), Inches(1.82), Inches(5.68), Inches(5.02), bg_color=WHITE, border_color=BORDER_MAIN)
    slide11.shapes.add_picture(w_img_path, Inches(6.95), Inches(2.05), width=Inches(5.486))

    cap = slide11.shapes.add_textbox(Inches(6.853), Inches(6.45), Inches(5.68), Inches(0.35))
    tf_c = cap.text_frame
    p = tf_c.paragraphs[0]
    p.text = "Biểu đồ phân phối thời gian chờ: Adaptive AI giải phóng mạng lưới nhanh hơn tới 54%"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER

add_footer(slide11, 11)

# ==============================================================================
# SLIDE 12: PROGRESS ROADMAP & NEXT STEPS (SYMMETRIC & LEFT-ALIGNED)
# ==============================================================================
slide12 = init_slide()
add_header(slide12, "TỔNG KẾT & LỘ TRÌNH", "12. Ma Trận Tiến Độ Đã Hoàn Thành & Định Hướng", "Nghiệm thu 100% các khối AI cốt lõi và định hướng mở rộng hệ thống trong giai đoạn tiếp theo")

# Left Column: Done Matrix (WHITE with BORDER_MAIN)
c_done = add_card(slide12, Inches(0.8), Inches(1.82), Inches(5.68), Inches(5.02), bg_color=WHITE, border_color=BORDER_MAIN)
t_d = slide12.shapes.add_textbox(Inches(0.95), Inches(1.92), Inches(5.38), Inches(0.35))
p = t_d.text_frame.paragraphs[0]
p.text = "✅ CÁC HẠNG MỤC ĐÃ HOÀN THÀNH 100%"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY

done_items = [
    ("Thị giác YOLOv11m & CARLA 10k", "mAP50 = 94.91%, 7 classes nhận diện"),
    ("ByteTrack & Camera Homography H", "Ước lượng vận tốc thực & dừng chờ"),
    ("Thuật toán Leftover-Queue", "EMA smoothing, giảm 54% wait time"),
    ("ALINEA Freeway Ramp Metering", "Điều tiết cao tốc & chống tràn nhánh"),
    ("Emergency Preemption Wave", "Làn sóng xanh & bù nợ sau ưu tiên"),
    ("Mô phỏng SUMO vi mô", "3 mạng lưới: Arterial, Highway, Mix"),
    ("FastAPI Concurrency WebSocket", "Streaming 10 Hz, nén payload 45%"),
    ("Next.js 14 Dashboard & Lab", "Canvas Map, A/B race, Groq Copilot")
]

for idx, (title, detail) in enumerate(done_items):
    top_it = Inches(2.35 + idx * 0.54)
    it_box = add_card(slide12, Inches(0.95), top_it, Inches(5.38), Inches(0.46), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
    tf_it = it_box.text_frame
    tf_it.margin_left = Inches(0.15)
    tf_it.margin_top = Inches(0.04)
    p = tf_it.paragraphs[0]
    p.text = f"✓ {title}"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.LEFT
    
    p_sub = tf_it.add_paragraph()
    p_sub.text = detail
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(8.2)
    p_sub.font.color.rgb = NAVY
    p_sub.alignment = PP_ALIGN.LEFT

# Right Column: Next Steps (WHITE with BORDER_MAIN)
c_next = add_card(slide12, Inches(6.853), Inches(1.82), Inches(5.68), Inches(5.02), bg_color=WHITE, border_color=BORDER_MAIN)
t_n = slide12.shapes.add_textbox(Inches(7.0), Inches(1.92), Inches(5.38), Inches(0.35))
p = t_n.text_frame.paragraphs[0]
p.text = "🚀 KẾ HOẠCH GIAI ĐOẠN TIẾP THEO (STRATEGIC ROADMAP)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY

next_steps = [
    ("1. Nâng cấp Reinforcement Learning (MARL)", 
     "Tích hợp thuật toán học tăng cường sâu đa tác tử (Multi-Agent PPO) kết hợp cùng Leftover-Queue để tối ưu hóa phối hợp giữa các cụm nút giao phức tạp."),
    
    ("2. Triển khai Phần cứng Biên (Edge Device)", 
     "Biên dịch và tối ưu hóa mô hình YOLOv11m sang TensorRT (FP16 / INT8) để chạy trực tiếp trên các kit phần cứng nhúng NVIDIA Jetson Orin Nano / AGX tại cột đèn giao thông."),
    
    ("3. Thử nghiệm Nguồn Video RTSP Thực địa", 
     "Mở rộng kết nối luồng camera giao thông công cộng qua giao thức RTSP phục vụ đánh giá năng lực chạy thực tế diện rộng (Field Pilot Test).")
]

for idx, (title, desc) in enumerate(next_steps):
    top_s = Inches(2.4 + idx * 1.4)
    s_box = add_card(slide12, Inches(7.0), top_s, Inches(5.38), Inches(1.26), bg_color=CARD_TINT, border_color=BORDER_SUBTLE)
    tf_s = s_box.text_frame
    tf_s.margin_left = Inches(0.18)
    tf_s.margin_top = Inches(0.1)
    p = tf_s.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.8)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.LEFT
    p.space_after = Pt(4)

    p_d = tf_s.add_paragraph()
    p_d.text = desc
    p_d.font.name = "Segoe UI"
    p_d.font.size = Pt(9)
    p_d.font.color.rgb = NAVY
    p_d.alignment = PP_ALIGN.LEFT

add_footer(slide12, 12)

# ==============================================================================
# SAVE & COPY
# ==============================================================================
output_pptx = "d:/ai-traffic-management-system/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully to: {output_pptx}")

artifact_pptx = "C:/Users/Admin/.gemini/antigravity/brain/0bd16718-e31e-4a30-ae40-69e42323aea0/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(artifact_pptx)
print(f"Copy saved to artifact directory: {artifact_pptx}")
