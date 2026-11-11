import os
import matplotlib.pyplot as plt
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 1. Colors
NAVY_PRIMARY = RGBColor(11, 25, 44)     # #0B192C - Deep Navy
NAVY_SECONDARY = RGBColor(30, 62, 98)   # #1E3E62 - Slate Navy
BLUE_ACCENT = RGBColor(37, 99, 235)     # #2563EB - Electric Blue
BLUE_BG = RGBColor(240, 247, 255)       # #F0F7FF - Soft Tint
SLATE_TEXT = RGBColor(51, 65, 85)       # #334155 - Dark Slate
MUTED_TEXT = RGBColor(100, 116, 139)    # #64748B - Gray Muted
BORDER_COLOR = RGBColor(203, 213, 225)  # #CBD5E1 - Border
WHITE = RGBColor(255, 255, 255)
GREEN_ACCENT = RGBColor(5, 150, 105)    # #059669 - Emerald
GREEN_BG = RGBColor(240, 253, 244)      # Soft green tint
AMBER_ACCENT = RGBColor(217, 119, 6)    # Amber
AMBER_BG = RGBColor(255, 251, 235)

FORMULA_DIR = "temp_formulas"
os.makedirs(FORMULA_DIR, exist_ok=True)

# 2. Render LaTeX Formulas to Transparent PNGs
formulas = {
    'loss_total': r'$\mathcal{L}_{\mathrm{total}} = 7.5 \cdot \mathcal{L}_{\mathrm{box}} + 0.5 \cdot \mathcal{L}_{\mathrm{cls}} + 1.5 \cdot \mathcal{L}_{\mathrm{dfl}}$',
    'ciou': r'$\mathcal{L}_{\mathrm{box}} = 1 - \left( \mathrm{IoU} - \frac{\rho^2(\mathbf{b}, \mathbf{b}^{gt})}{c^2} - \alpha v \right)$',
    'ciou_v': r'$v = \frac{4}{\pi^2} \left( \arctan\frac{w^{gt}}{h^{gt}} - \arctan\frac{w}{h} \right)^2, \quad \alpha = \frac{v}{(1 - \mathrm{IoU}) + v}$',
    'cls': r'$\mathcal{L}_{\mathrm{cls}} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} \left[ y_{i,k} \log \sigma(p_{i,k}) + (1 - y_{i,k}) \log(1 - \sigma(p_{i,k})) \right]$',
    'dfl': r'$\mathcal{L}_{\mathrm{dfl}}(S_l, S_r) = - \left( (y_r - y) \log(S_l) + (y - y_l) \log(S_r) \right)$',
    'lr': r'$\mathrm{Warmup: } \eta(t) = \eta_0 \frac{t}{3.0} \quad | \quad \mathrm{Linear: } \eta(t) = 0.01 \left[ 1 - \frac{t - 3}{97} \cdot 0.99 \right]$',
    'kalman': r'$\mathbf{x}_t = [x_c, y_c, a, h, \dot{x}_c, \dot{y}_c, \dot{a}, \dot{h}]^T, \quad \mathbf{P}_{t|t-1} = \mathbf{F} \mathbf{P}_{t-1|t-1} \mathbf{F}^T + \mathbf{Q}$',
    'homography': r'$[X_w, Y_w, 1]^T \sim \mathbf{H} [u, v, 1]^T \Rightarrow X_w = \frac{h_{11}u + h_{12}v + h_{13}}{h_{31}u + h_{32}v + h_{33}}, \; Y_w = \frac{h_{21}u + h_{22}v + h_{23}}{h_{31}u + h_{32}v + h_{33}}$',
    'speed': r'$\bar{v}(t) = \frac{1}{M} \sum_{m=0}^{M-1} \frac{\Delta d(t-m)}{\Delta t \cdot \Delta k} \quad (\bar{v} < 2.0\mathrm{ m/s}, \; \tau \geq 2.0\mathrm{ s})$',
    'ema': r'$S_i(k) = 0.7 \cdot Q_i(k) + 0.3 \cdot S_i(k-1)$',
    'redistribution': r'$R = \min\left(12.0\mathrm{ s}, \sum_{j \in \mathcal{S}} \max(0, g_j - g_{\min})\right), \quad g_i(k+1) = \min\left(g_{\max}, g_i(k) + R \cdot \frac{S_i}{\sum S_m}\right)$',
    'alinea': r'$r(k) = \mathrm{clamp}\left( r(k-1) + K_R \cdot (o^* - \hat{o}(k)), \; r_{\min}, \; r_{\max} \right)$',
    'ramp_cycle': r'$T_{\mathrm{cycle}}(k) = \frac{3600}{r(k)}, \quad t_{\mathrm{red}}(k) = \max\left( 0, T_{\mathrm{cycle}}(k) - t_{\mathrm{green}} - t_{\mathrm{yellow}} \right)$',
    'preempt': r'$D_d(J) \leftarrow D_d(J) + \Delta t_{\mathrm{preempt}}, \quad t_{\mathrm{comp}} = \min(D_{d^*}, 15.0\mathrm{ s})$',
    'hcm': r'$d_i = \max(0, t_{\mathrm{dwell}} - t_{\mathrm{free\_flow}}), \quad \mathrm{Throughput} = \frac{N_{\mathrm{completed}} \times 60}{T_{\mathrm{sim}}}$'
}

print("Rendering formula images...")
for name, latex in formulas.items():
    fig = plt.figure(figsize=(9, 1.2))
    plt.axis('off')
    plt.text(0.5, 0.5, latex, fontsize=16, ha='center', va='center', color='#0B192C')
    plt.savefig(f'{FORMULA_DIR}/{name}.png', bbox_inches='tight', transparent=True, dpi=300)
    plt.close()

# 3. Initialize Presentation (16:9 widescreen)
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

def set_slide_background(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_header(slide, tag_text, title_text, subtitle_text=""):
    # Tag Pill
    tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.4), Inches(3.2), Inches(0.32))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = BLUE_BG
    tag_box.line.color.rgb = RGBColor(191, 219, 254)
    tag_box.line.width = Pt(1)
    tf = tag_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = tag_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = NAVY_SECONDARY
    p.alignment = PP_ALIGN.CENTER

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.78), Inches(11.7), Inches(0.55))
    tf = title_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Segoe UI"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    # Subtitle
    if subtitle_text:
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.35))
        tf = sub_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = subtitle_text
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.color.rgb = MUTED_TEXT

def add_footer(slide, current_slide, total_slides=12):
    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.01))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(226, 232, 240)
    line.line.fill.background()

    # Left text
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(8.0), Inches(0.3))
    tf = tx_box.text_frame
    p = tf.paragraphs[0]
    p.text = "AI Traffic Management & Monitoring System — Báo cáo tiến độ kỹ thuật"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED_TEXT

    # Right slide number
    tx_box2 = slide.shapes.add_textbox(Inches(10.5), Inches(7.08), Inches(2.0), Inches(0.3))
    tf2 = tx_box2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = f"Slide {current_slide} / {total_slides}"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_SECONDARY
    p2.alignment = PP_ALIGN.RIGHT

def add_card(slide, left, top, width, height, bg_color=WHITE, border_color=BORDER_COLOR):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1)
    return shape

# ==========================================
# SLIDE 1: COVER & OVERVIEW
# ==========================================
slide1 = prs.slides.add_slide(blank_layout)
set_slide_background(slide1, WHITE)

# Top badge
badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(0.6), Inches(3.7), Inches(0.35))
badge.fill.solid()
badge.fill.fore_color.rgb = BLUE_BG
badge.line.color.rgb = RGBColor(191, 219, 254)
p = badge.text_frame.paragraphs[0]
p.text = "BÁO CÁO TIẾN ĐỘ KỸ THUẬT (PROGRESS REPORT)"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
p.alignment = PP_ALIGN.CENTER

# Main Title
title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.05), Inches(11.333), Inches(0.8))
p = title_box.text_frame.paragraphs[0]
p.text = "HỆ THỐNG ĐIỀU PHỐI & GIÁM SÁT GIAO THÔNG THÔNG MINH"
p.font.name = "Segoe UI"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY
p.alignment = PP_ALIGN.CENTER

sub_box = slide1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(0.45))
p = sub_box.text_frame.paragraphs[0]
p.text = "AI-Based Traffic Management & Monitoring System (YOLOv11m • Leftover-Queue • ALINEA • Next.js 14)"
p.font.name = "Segoe UI"
p.font.size = Pt(12)
p.font.color.rgb = MUTED_TEXT
p.alignment = PP_ALIGN.CENTER

# Hero Image
hero_img_path = "docs/images/hero-banner.png"
if os.path.exists(hero_img_path):
    add_card(slide1, Inches(1.8), Inches(2.35), Inches(9.733), Inches(3.2), bg_color=RGBColor(15, 23, 42))
    slide1.shapes.add_picture(hero_img_path, Inches(1.85), Inches(2.4), width=Inches(9.633))

# 4 Metric Cards
metrics = [
    ("-40.5% ~ -54%", "Giảm thời gian chờ xe", NAVY_SECONDARY, BLUE_BG, RGBColor(191, 219, 254)),
    ("94.91%", "YOLOv11m mAP50 (7 Lớp)", NAVY_PRIMARY, WHITE, BORDER_COLOR),
    ("27.7 FPS", "Tốc độ Edge Inference", NAVY_SECONDARY, BLUE_BG, RGBColor(191, 219, 254)),
    ("100% Real-Time", "WebSocket Streaming (10 Hz)", GREEN_ACCENT, GREEN_BG, RGBColor(187, 247, 208))
]

for i, (val, label, color, bg, border) in enumerate(metrics):
    left = Inches(0.8 + i * 3.0)
    card = add_card(slide1, left, Inches(5.8), Inches(2.75), Inches(1.05), bg_color=bg, border_color=border)
    tf = card.text_frame
    p1 = tf.paragraphs[0]
    p1.text = val
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = color
    p1.alignment = PP_ALIGN.CENTER
    p2 = tf.add_paragraph()
    p2.text = label
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(10)
    p2.font.color.rgb = SLATE_TEXT
    p2.alignment = PP_ALIGN.CENTER

add_footer(slide1, 1)

# ==========================================
# SLIDE 2: ARCHITECTURE
# ==========================================
slide2 = prs.slides.add_slide(blank_layout)
set_slide_background(slide2, WHITE)
add_header(slide2, "TỔNG THỂ HỆ THỐNG", "02. Kiến Trúc Phân Tầng Độc Lập Đã Triển Khai", "Hierarchical & Distributed AI Architecture: Cảm biến → Ra quyết định → Mô phỏng → Nền tảng điều hành")

layers = [
    ("TẦNG 1: PERCEPTION", "packages/cv-pipeline", [
        "YOLOv11m Detect 7 lớp xe",
        "ByteTrack Multi-Object Tracker",
        "Camera Homography Matrix H",
        "Đo vận tốc thực & Hàng đợi dừng"
    ], "Output: Q_i, v_avg, EV alerts", BLUE_BG, RGBColor(191, 219, 254), NAVY_SECONDARY),
    
    ("TẦNG 2: DECISION & POLICY", "packages/adaptive-policy", [
        "Leftover-Queue Redistribution",
        "ALINEA Freeway Ramp Metering",
        "Emergency Preemption Green Wave",
        "Starvation Debt Compensation"
    ], "Output: SignalCommands (phase, dur)", RGBColor(238, 242, 255), RGBColor(199, 210, 254), RGBColor(67, 56, 202)),
    
    ("TẦNG 3: SIMULATION", "packages/sumo-engine", [
        "SUMO TraCI Engine (10 Hz)",
        "3 Mạng lưới (Arterial, Highway, Mix)",
        "Krauss Car-Following Model",
        "HCM Control Delay & Throughput"
    ], "Output: Telemetry TickData", AMBER_BG, RGBColor(253, 230, 138), AMBER_ACCENT),
    
    ("TẦNG 4: FULL-STACK PLATFORM", "backend & frontend", [
        "FastAPI Async WebSocket Stream",
        "Next.js 14 Interactive Canvas Map",
        "Simulation Lab (A/B Policy Race)",
        "Groq LLM Traffic Copilot"
    ], "UX: Giám sát & Điều hành tức thì", GREEN_BG, RGBColor(187, 247, 208), GREEN_ACCENT)
]

for i, (title, pkg, items, out_text, bg, border, title_color) in enumerate(layers):
    left = Inches(0.8 + i * 3.0)
    card = add_card(slide2, left, Inches(1.85), Inches(2.75), Inches(4.3), bg_color=WHITE, border_color=border)
    tf = card.text_frame
    
    # Layer badge
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = title_color
    
    p_pkg = tf.add_paragraph()
    p_pkg.text = pkg
    p_pkg.font.name = "Consolas"
    p_pkg.font.size = Pt(9)
    p_pkg.font.color.rgb = MUTED_TEXT
    
    p_pkg.space_after = Pt(14)
    
    for item in items:
        pi = tf.add_paragraph()
        pi.text = f"• {item}"
        pi.font.name = "Segoe UI"
        pi.font.size = Pt(10)
        pi.font.color.rgb = SLATE_TEXT
        pi.space_after = Pt(6)
        
    p_out = tf.add_paragraph()
    p_out.text = f"\n✓ {out_text}"
    p_out.font.name = "Segoe UI"
    p_out.font.size = Pt(9.5)
    p_out.font.bold = True
    p_out.font.color.rgb = title_color

# Bottom Highlight
bot_card = add_card(slide2, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.6), bg_color=RGBColor(248, 250, 252))
tf = bot_card.text_frame
p = tf.paragraphs[0]
p.text = "💡 Điểm nhấn kiến trúc: Thiết kế phân tách ghép lỏng (Decoupled Architecture) — Có thể chuyển từ mô phỏng SUMO sang tiếp nhận luồng Camera RTSP thực địa mà không cần sửa đổi thuật toán tầng Policy."
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.color.rgb = SLATE_TEXT

add_footer(slide2, 2)

# ==========================================
# SLIDE 3: YOLOv11m & CARLA DATASET
# ==========================================
slide3 = prs.slides.add_slide(blank_layout)
set_slide_background(slide3, WHITE)
add_header(slide3, "THỊ GIÁC MÁY TÍNH", "03. Phân Hệ Thị Giác Máy Tính & Dữ Liệu CARLA", "Huấn luyện YOLOv11m trên 10,064 ảnh độ chân thực cao từ CARLA Simulator kết hợp cân bằng lớp")

# Left Column (5.8 in)
c1 = add_card(slide3, Inches(0.8), Inches(1.85), Inches(5.6), Inches(1.5), bg_color=BLUE_BG, border_color=RGBColor(191, 219, 254))
tf = c1.text_frame
p = tf.paragraphs[0]
p.text = "DỮ LIỆU TỔNG HỢP CARLA 0.9.16 (SYNTHETIC PHOTOREALISTIC)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY

p2 = tf.add_paragraph()
p2.text = "• Khắc phục triệt để lệch miền (Domain Shift) và mất cân bằng lớp của dữ liệu cào web.\n• 10,064 ảnh độ phân giải 1920x1080 qua 13 điều kiện thời tiết (Nắng, Mưa, Hoàng hôn, Đêm).\n• Tăng cường sinh Spawner: Tỷ lệ xe buýt, xe ưu tiên được nhân tạo gấp 2x - 3x."
p2.font.name = "Segoe UI"
p2.font.size = Pt(9.5)
p2.font.color.rgb = SLATE_TEXT

# Table
t_card = add_card(slide3, Inches(0.8), Inches(3.5), Inches(5.6), Inches(2.2), bg_color=WHITE)
table_shape = slide3.shapes.add_table(5, 3, Inches(0.9), Inches(3.6), Inches(5.4), Inches(1.9))
table = table_shape.table
table.columns[0].width = Inches(2.0)
table.columns[1].width = Inches(1.4)
table.columns[2].width = Inches(2.0)

headers = ["Chỉ số kiểm định", "Kết quả", "Ý nghĩa kỹ thuật"]
for col_idx, h in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

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
        cell.fill.fore_color.rgb = WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        if col_idx == 1:
            p.font.bold = True
            p.font.color.rgb = GREEN_ACCENT if "%" in text else NAVY_PRIMARY
        else:
            p.font.color.rgb = SLATE_TEXT

# Checkpoint note
chk = add_card(slide3, Inches(0.8), Inches(5.85), Inches(5.6), Inches(1.0), bg_color=RGBColor(248, 250, 252))
tf = chk.text_frame
p = tf.paragraphs[0]
p.text = "Checkpoint: packages/cv-pipeline/models/best.pt"
p.font.name = "Consolas"
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
p2 = tf.add_paragraph()
p2.text = "Dung lượng 40.5 MB | 20.06M tham số | 100 Epochs trên GPU NVIDIA L40S (48GB VRAM)"
p2.font.name = "Segoe UI"
p2.font.size = Pt(9)
p2.font.color.rgb = MUTED_TEXT

# Right Column Image
r_img_path = "docs/images/realworld-detections.png"
if os.path.exists(r_img_path):
    add_card(slide3, Inches(6.7), Inches(1.85), Inches(5.8), Inches(4.5), bg_color=RGBColor(15, 23, 42))
    slide3.shapes.add_picture(r_img_path, Inches(6.75), Inches(1.9), width=Inches(5.7))

cap = slide3.shapes.add_textbox(Inches(6.7), Inches(6.4), Inches(5.8), Inches(0.4))
p = cap.text_frame.paragraphs[0]
p.text = "Ảnh kiểm thử: Nhận diện đồng thời 7 lớp xe trong điều kiện giao thông phức tạp"
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.italic = True
p.font.color.rgb = MUTED_TEXT
p.alignment = PP_ALIGN.CENTER

add_footer(slide3, 3)

# ==========================================
# SLIDE 4: MATHEMATICAL LOSS FUNCTIONS
# ==========================================
slide4 = prs.slides.add_slide(blank_layout)
set_slide_background(slide4, WHITE)
add_header(slide4, "CƠ SỞ TOÁN HỌC", "04. Công Thức Toán Học - Hàm Mất Mát Thị Giác", "Tối ưu hóa đa nhiệm kết hợp CIoU Bounding Box Loss, BCE Classification và Distribution Focal Loss (DFL)")

# Total loss banner
banner = add_card(slide4, Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.1), bg_color=BLUE_BG, border_color=RGBColor(191, 219, 254))
slide4.shapes.add_picture(f"{FORMULA_DIR}/loss_total.png", Inches(3.2), Inches(2.05), width=Inches(6.9))

# 3 Loss Cards
losses = [
    ("1. HỒI QUY VỊ TRÍ (CIoU LOSS)", "ciou", [
        "Tối ưu hóa diện tích giao IoU",
        "Phạt khoảng cách tâm Euclidean rho",
        "Bù trừ tỷ lệ co dãn hai chiều v và alpha"
    ], "ciou_v"),
    ("2. PHÂN LOẠI (BCE WITH LOGITS)", "cls", [
        "Phân loại độc lập cho K = 7 lớp",
        "Tránh áp chế xác suất giữa các lớp xe",
        "Trọng số phạt lỗi phân loại: lambda = 0.5"
    ], None),
    ("3. PHÂN PHỐI BIÊN TIÊU CỰ (DFL)", "dfl", [
        "Học phân phối xác suất liên tục biên",
        "Thay thế điểm cứng Dirac delta",
        "Tăng độ nhạy khi xe bị mờ / che khuất"
    ], None)
]

for i, (title, f_name, bullets, f_sub) in enumerate(losses):
    left = Inches(0.8 + i * 4.0)
    card = add_card(slide4, left, Inches(3.1), Inches(3.733), Inches(2.7), bg_color=WHITE)
    tf = card.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_SECONDARY
    
    # Add formula image
    slide4.shapes.add_picture(f"{FORMULA_DIR}/{f_name}.png", left + Inches(0.2), Inches(3.6), width=Inches(3.333))
    
    if f_sub:
        slide4.shapes.add_picture(f"{FORMULA_DIR}/{f_sub}.png", left + Inches(0.2), Inches(4.2), width=Inches(3.333))
        
    top_bullets = Inches(4.75) if f_sub else Inches(4.4)
    b_box = slide4.shapes.add_textbox(left + Inches(0.2), top_bullets, Inches(3.333), Inches(1.0))
    tf_b = b_box.text_frame
    for b in bullets:
        pb = tf_b.add_paragraph()
        pb.text = f"• {b}"
        pb.font.name = "Segoe UI"
        pb.font.size = Pt(9)
        pb.font.color.rgb = SLATE_TEXT

# Learning rate scheduler bar
lr_card = add_card(slide4, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.85), bg_color=RGBColor(248, 250, 252))
slide4.shapes.add_picture(f"{FORMULA_DIR}/lr.png", Inches(2.2), Inches(6.15), width=Inches(8.9))

add_footer(slide4, 4)

# ==========================================
# SLIDE 5: BYTETRACK & HOMOGRAPHY
# ==========================================
slide5 = prs.slides.add_slide(blank_layout)
set_slide_background(slide5, WHITE)
add_header(slide5, "THEO DÕI & ĐO ĐẠC", "05. Theo Dõi Đa Đối Tượng & Chiếu Tọa Độ Thực", "ByteTrack duy trì ID phương tiện liên tục và ma trận Homography chuyển đổi pixel sang tọa độ thực tế")

# Left Column
c1 = add_card(slide5, Inches(0.8), Inches(1.85), Inches(5.8), Inches(1.4), bg_color=WHITE)
tf = c1.text_frame
p = tf.paragraphs[0]
p.text = "1. THEO DÕI LIÊN TỤC VỚI BYTETRACK & KALMAN FILTER"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
slide5.shapes.add_picture(f"{FORMULA_DIR}/kalman.png", Inches(1.0), Inches(2.35), width=Inches(5.4))

c2 = add_card(slide5, Inches(0.8), Inches(3.4), Inches(5.8), Inches(1.6), bg_color=WHITE)
tf = c2.text_frame
p = tf.paragraphs[0]
p.text = "2. MA TRẬN HOMOGRAPHY MẶT ĐẤT (GROUND-PLANE H)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
slide5.shapes.add_picture(f"{FORMULA_DIR}/homography.png", Inches(1.0), Inches(3.95), width=Inches(5.4))

c3 = add_card(slide5, Inches(0.8), Inches(5.15), Inches(5.8), Inches(1.65), bg_color=GREEN_BG, border_color=RGBColor(187, 247, 208))
tf = c3.text_frame
p = tf.paragraphs[0]
p.text = "3. ƯỚC LƯỢNG VẬN TỐC THỰC & TIÊU CHUẨN XE CHỜ ĐÈN ĐỎ"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GREEN_ACCENT
slide5.shapes.add_picture(f"{FORMULA_DIR}/speed.png", Inches(1.0), Inches(5.65), width=Inches(5.4))

# Right Column Image
col_img_path = "docs/images/collision-detection.png"
if os.path.exists(col_img_path):
    add_card(slide5, Inches(6.9), Inches(1.85), Inches(5.633), Inches(4.5), bg_color=RGBColor(15, 23, 42))
    slide5.shapes.add_picture(col_img_path, Inches(6.95), Inches(1.9), width=Inches(5.533))

cap = slide5.shapes.add_textbox(Inches(6.9), Inches(6.4), Inches(5.633), Inches(0.4))
p = cap.text_frame.paragraphs[0]
p.text = "Trực quan: Khung theo dõi ID phương tiện, quỹ đạo di chuyển và cảnh báo xung đột"
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.italic = True
p.font.color.rgb = MUTED_TEXT
p.alignment = PP_ALIGN.CENTER

add_footer(slide5, 5)

# ==========================================
# SLIDE 6: LEFTOVER-QUEUE REDISTRIBUTION
# ==========================================
slide6 = prs.slides.add_slide(blank_layout)
set_slide_background(slide6, WHITE)
add_header(slide6, "ĐIỀU KHIỂN THÍCH NGHI", "06. Thuật Toán Tái Phân Bổ Hàng Đợi Tồn Dư", "Leftover-Queue Actuated Signal Control: Tái cân bằng pha đèn dựa trên số xe chưa giải phóng khi chớm vàng")

# 3 Steps
steps = [
    ("BƯỚC 1: LÀM MỊN HÀNG ĐỢI TỒN", "Lọc qua bộ lọc EMA với alpha = 0.7 để khử nhiễu ngẫu nhiên:", "ema", [
        "Ghi nhận hàng đợi Q_i(k) tại thời điểm vàng",
        "Bộ lọc thông thấp phản ánh xu hướng thực",
        "Tránh sốc điều khiển khi có xe bất ngờ rẽ"
    ]),
    ("BƯỚC 2: PHÂN LOẠI TRẠNG THÁI", "Chia các nhóm pha thành hai tập rời rạc:", None, [
        "Nhóm U (Undersupplied): S_i > 0 (Còn xe tồn)",
        "Nhóm S (Satisfied): S_j <= 0 (Đã thông thoáng)",
        "Trích ngân sách hiến tặng từ nhóm S"
    ]),
    ("BƯỚC 3: TÁI PHÂN PHỐI CÓ RÀNG BUỘC", "San sẻ ngân sách thời gian xanh chu kỳ kế tiếp:", "redistribution", [
        "Khấu trừ thời gian từ các hướng thông thoáng",
        "Cấp thêm thời gian theo tỷ trọng thiếu hụt w_i",
        "Tuân thủ nghiêm ngặt biên an toàn giao lộ"
    ])
]

for i, (stitle, sdesc, sfname, sbullets) in enumerate(steps):
    left = Inches(0.8 + i * 4.0)
    card = add_card(slide6, left, Inches(1.85), Inches(3.733), Inches(4.0), bg_color=WHITE)
    tf = card.text_frame
    p = tf.paragraphs[0]
    p.text = stitle
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_SECONDARY
    
    pd = tf.add_paragraph()
    pd.text = sdesc
    pd.font.name = "Segoe UI"
    pd.font.size = Pt(9.5)
    pd.font.color.rgb = SLATE_TEXT
    pd.space_after = Pt(10)
    
    if sfname:
        slide6.shapes.add_picture(f"{FORMULA_DIR}/{sfname}.png", left + Inches(0.2), Inches(2.7), width=Inches(3.333))
        
    top_b = Inches(3.6) if sfname else Inches(2.6)
    b_box = slide6.shapes.add_textbox(left + Inches(0.2), top_b, Inches(3.333), Inches(1.8))
    tf_b = b_box.text_frame
    for b in sbullets:
        pb = tf_b.add_paragraph()
        pb.text = f"• {b}"
        pb.font.name = "Segoe UI"
        pb.font.size = Pt(9)
        pb.font.color.rgb = SLATE_TEXT
        pb.space_after = Pt(4)

# Safety Box
safe_card = add_card(slide6, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.85), bg_color=RGBColor(248, 250, 252))
tf = safe_card.text_frame
p = tf.paragraphs[0]
p.text = "🛡️ RÀNG BUỘC AN TOÀN TUYỆT ĐỐI (HARD SAFETY CONSTRAINTS)"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY
p2 = tf.add_paragraph()
p2.text = "Thời lượng xanh tối thiểu g_min = 10.0 s (đảm bảo cho người đi bộ qua đường) | Thời lượng xanh tối đa g_max = 50.0 s | Biên độ thay đổi mỗi chu kỳ R_max = 12.0 s"
p2.font.name = "Segoe UI"
p2.font.size = Pt(9.5)
p2.font.color.rgb = SLATE_TEXT

add_footer(slide6, 6)

# ==========================================
# SLIDE 7: ALINEA RAMP METERING
# ==========================================
slide7 = prs.slides.add_slide(blank_layout)
set_slide_background(slide7, WHITE)
add_header(slide7, "ĐIỀU TIẾT CAO TỐC", "07. Điều Tiết Nhập Làn Cao Tốc ALINEA & Chống Tràn", "Luật điều khiển tích phân vòng kín Papageorgiou et al. giữ mật độ tuyến chính dưới điểm sụp đổ lưu lượng")

# Left Column (5.8 in)
c1 = add_card(slide7, Inches(0.8), Inches(1.85), Inches(5.8), Inches(2.2), bg_color=WHITE)
tf = c1.text_frame
p = tf.paragraphs[0]
p.text = "1. LUẬT ĐIỀU KHIỂN HỒI TIẾP TÍCH PHÂN ALINEA"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
slide7.shapes.add_picture(f"{FORMULA_DIR}/alinea.png", Inches(1.0), Inches(2.35), width=Inches(5.4))

p_exp = slide7.shapes.add_textbox(Inches(1.0), Inches(3.1), Inches(5.4), Inches(0.8))
tf_e = p_exp.text_frame
p = tf_e.paragraphs[0]
p.text = "• K_R = 70.0 veh/h/%: Hệ số khuếch đại tích phân\n• o* = 20%: Mật độ chiếm dụng mục tiêu lý tưởng tại hạ lưu\n• [r_min, r_max] = [200, 1200] veh/h: Biên giới hạn lưu lượng cấp xe"
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.color.rgb = SLATE_TEXT

c2 = add_card(slide7, Inches(0.8), Inches(4.2), Inches(5.8), Inches(2.0), bg_color=WHITE)
tf = c2.text_frame
p = tf.paragraphs[0]
p.text = "2. QUY ĐỔI SANG THỜI LƯỢNG ĐÈN METERING"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
slide7.shapes.add_picture(f"{FORMULA_DIR}/ramp_cycle.png", Inches(1.0), Inches(4.7), width=Inches(5.4))

p_exp2 = slide7.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(5.4), Inches(0.6))
tf_e2 = p_exp2.text_frame
p = tf_e2.paragraphs[0]
p.text = "Thời lượng xanh cố định t_green = 2.0 s (cho 1 xe qua), thời gian vàng t_yellow = 1.0 s; thời lượng đỏ t_red điều biến tự động theo chu kỳ T_cycle."
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.color.rgb = MUTED_TEXT

# Right Column
c3 = add_card(slide7, Inches(6.9), Inches(1.85), Inches(5.633), Inches(2.2), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
tf = c3.text_frame
p = tf.paragraphs[0]
p.text = "⚠️ CƠ CHẾ GHI ĐÈ CHỐNG TRÀN NHÁNH NỐI (SPILLBACK OVERRIDE)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = RGBColor(185, 28, 28)

p2 = tf.add_paragraph()
p2.text = "Khi hàng đợi trên nhánh nối chạm ngưỡng tới hạn Q_ramp >= 30 xe:\n\n⇒ Ngay lập tức ghi đè tốc độ r(k) = r_max (1200 veh/h)\n\nMục tiêu: Ngăn chặn dòng xe dồn ứ tràn ngược lại làm tê liệt mạng lưới đường gom đô thị bên dưới."
p2.font.name = "Segoe UI"
p2.font.size = Pt(9.5)
p2.font.color.rgb = SLATE_TEXT

c4 = add_card(slide7, Inches(6.9), Inches(4.2), Inches(5.633), Inches(2.0), bg_color=RGBColor(248, 250, 252))
tf = c4.text_frame
p = tf.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & ON-RAMP"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_PRIMARY

p2 = tf.add_paragraph()
p2.text = "Mainline Freeway ══════[ Điểm hòa dòng ]══════[ Cảm biến ô(k) ]══▶\n                                     ▲\nOn-Ramp Queue ───────[ Đèn Meter r(k) ]"
p2.font.name = "Consolas"
p2.font.size = Pt(9)
p2.font.color.rgb = NAVY_SECONDARY

add_footer(slide7, 7)

# ==========================================
# SLIDE 8: EMERGENCY PREEMPTION
# ==========================================
slide8 = prs.slides.add_slide(blank_layout)
set_slide_background(slide8, WHITE)
add_header(slide8, "ƯU TIÊN KHẨN CẤP", "08. Cơ Chế Ưu Tiên Xe Khẩn Cấp & Bù Nợ Xanh", "Phát hiện xe cứu thương, cứu hỏa, cảnh sát → Kích hoạt làn sóng xanh → Hoàn trả công nợ thời gian")

# 3 Stages
stages = [
    ("GIAI ĐOẠN 1: KÍCH HOẠT ƯU TIÊN", "Nhận diện phương tiện ưu tiên:", BLUE_BG, RGBColor(191, 219, 254), NAVY_SECONDARY, [
        "Camera / SUMO phát hiện Ambulance/Police",
        "Xác định hướng tiếp cận e và giao lộ J",
        "Ghi đè pha đèn hiện tại sang pha xanh cho xe khẩn cấp: phi_J <- phi_EV(e)"
    ]),
    ("GIAI ĐOẠN 2: TÍCH LŨY CÔNG NỢ", "Ghi nhận thiệt hại các hướng khác:", AMBER_BG, RGBColor(253, 230, 138), AMBER_ACCENT, [
        "Các hướng trực giao bị cắt quyền lưu thông",
        "Tích lũy công nợ thời gian trong suốt delta_t",
        "Ghi nhận vào sổ nợ giao lộ: D_d(J) <- D_d(J) + delta_t_preempt"
    ]),
    ("GIAI ĐOẠN 3: BÙ NỢ CÔNG BẰNG", "Hoàn trả thời gian xanh sau ưu tiên:", GREEN_BG, RGBColor(187, 247, 208), GREEN_ACCENT, [
        "Xe khẩn cấp vừa rời khỏi giao lộ",
        "Tìm hướng chịu thiệt hại lớn nhất d*",
        "Cấp thêm thời gian xanh bù: t_comp = min(D_d*, 15.0 s)"
    ])
]

for i, (title, desc, bg, border, color, bullets) in enumerate(stages):
    left = Inches(0.8 + i * 4.0)
    card = add_card(slide8, left, Inches(1.85), Inches(3.733), Inches(3.2), bg_color=bg, border_color=border)
    tf = card.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = color
    
    pd = tf.add_paragraph()
    pd.text = desc
    pd.font.name = "Segoe UI"
    pd.font.size = Pt(9.5)
    pd.font.color.rgb = SLATE_TEXT
    pd.space_after = Pt(8)
    
    for b in bullets:
        pb = tf.add_paragraph()
        pb.text = f"• {b}"
        pb.font.name = "Segoe UI"
        pb.font.size = Pt(9)
        pb.font.color.rgb = SLATE_TEXT
        pb.space_after = Pt(4)

# Formula & Result
f_card = add_card(slide8, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.6), bg_color=WHITE)
tf = f_card.text_frame
p = tf.paragraphs[0]
p.text = "CÔNG THỨC TOÁN HỌC CƠ CHẾ HOÀN NỢ (DEBT PAYBACK FORMULATION)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY

slide8.shapes.add_picture(f"{FORMULA_DIR}/preempt.png", Inches(3.2), Inches(5.6), width=Inches(6.8))

p_res = tf.add_paragraph()
p_res.text = "✓ Kết quả thực nghiệm: Phương tiện khẩn cấp di chuyển qua giao lộ với 0 giây chờ đợi; các hướng trực giao được giải phóng ngay sau đó mà không phát sinh ùn ứ dây chuyền."
p_res.font.name = "Segoe UI"
p_res.font.size = Pt(9.5)
p_res.font.bold = True
p_res.font.color.rgb = GREEN_ACCENT

add_footer(slide8, 8)

# ==========================================
# SLIDE 9: SUMO SIMULATION NETWORKS
# ==========================================
slide9 = prs.slides.add_slide(blank_layout)
set_slide_background(slide9, WHITE)
add_header(slide9, "MÔ PHỎNG VI MÔ", "09. Mô Phỏng Vi Mô SUMO & 3 Mạng Lưới Đã Xây Dựng", "Tích hợp TraCI Socket Protocol 10 Hz và 3 mô hình mạng lưới kiểm thử chuyên biệt")

nets = [
    ("1. Mạng Arterial Grid (3x2)", "docs/images/arterial-grid.png", "6 Nút giao liên hoàn", [
        "Kiểm thử điều phối đèn đa nút",
        "Giải quyết xung đột làn rẽ trái",
        "Đồng bộ Dual-Ring 2 chiều"
    ]),
    ("2. Mạng Highway Corridor", "docs/images/highway-corridor.png", "Cao tốc 3 làn & 2 On-Ramp", [
        "Kiểm thử thuật toán ALINEA",
        "Ngăn chặn tắc nghẽn sụp đổ",
        "Khai thác điểm hòa dòng"
    ]),
    ("3. Mạng Kết Hợp (Combined)", "docs/images/combined-network.png", "Hệ thống đô thị tích hợp", [
        "Nội đô kết nối cao tốc liên vùng",
        "Kiểm thử tải toàn diện End-to-End",
        "Mô hình di chuyển hỗn hợp"
    ])
]

for i, (title, img_path, badge_txt, bullets) in enumerate(nets):
    left = Inches(0.8 + i * 4.0)
    card = add_card(slide9, left, Inches(1.85), Inches(3.733), Inches(4.3), bg_color=WHITE)
    tf = card.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    pb = tf.add_paragraph()
    pb.text = badge_txt
    pb.font.name = "Segoe UI"
    pb.font.size = Pt(9)
    pb.font.color.rgb = NAVY_SECONDARY
    pb.space_after = Pt(6)
    
    if os.path.exists(img_path):
        add_card(slide9, left + Inches(0.2), Inches(2.6), Inches(3.333), Inches(1.9), bg_color=RGBColor(15, 23, 42))
        slide9.shapes.add_picture(img_path, left + Inches(0.22), Inches(2.62), width=Inches(3.29))
        
    b_box = slide9.shapes.add_textbox(left + Inches(0.2), Inches(4.6), Inches(3.333), Inches(1.4))
    tf_b = b_box.text_frame
    for b in bullets:
        pi = tf_b.add_paragraph()
        pi.text = f"• {b}"
        pi.font.name = "Segoe UI"
        pi.font.size = Pt(9)
        pi.font.color.rgb = SLATE_TEXT

# Bottom Tech specs
b_card = add_card(slide9, Inches(0.8), Inches(6.3), Inches(11.733), Inches(0.6), bg_color=RGBColor(248, 250, 252))
tf = b_card.text_frame
p = tf.paragraphs[0]
p.text = "⚙️ Thông số SUMO: TraCI Socket tần số 10 Hz (Delta_t = 0.1 s) | Mô hình xe bám đuôi Krauss Car-Following Model | Dual-Ring Permissive Left Turn"
p.font.name = "Segoe UI"
p.font.size = Pt(9.5)
p.font.color.rgb = SLATE_TEXT

add_footer(slide9, 9)

# ==========================================
# SLIDE 10: FULL-STACK PLATFORM & DASHBOARD
# ==========================================
slide10 = prs.slides.add_slide(blank_layout)
set_slide_background(slide10, WHITE)
add_header(slide10, "NỀN TẢNG FULL-STACK", "10. Nền Tảng Full-Stack: Backend & Operator Dashboard", "FastAPI Async WebSocket Engine và Next.js 14 Interactive Operator Dashboard")

# Left Column Image
dash_img_path = "docs/images/dashboard.png"
if os.path.exists(dash_img_path):
    add_card(slide10, Inches(0.8), Inches(1.85), Inches(6.4), Inches(4.5), bg_color=RGBColor(15, 23, 42))
    slide10.shapes.add_picture(dash_img_path, Inches(0.85), Inches(1.9), width=Inches(6.3))

cap = slide10.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(6.4), Inches(0.4))
p = cap.text_frame.paragraphs[0]
p.text = "Giao diện Dashboard: Bản đồ nhiệt trực tiếp, thông số từng nút giao và biểu đồ thời gian thực"
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.italic = True
p.font.color.rgb = MUTED_TEXT
p.alignment = PP_ALIGN.CENTER

# Right Column Features
feats = [
    ("⚡ FASTAPI BACKEND HIGH-CONCURRENCY", [
        "Khử TCP Backpressure: Bọc lệnh gửi socket với timeout tau_ws <= 0.15 s tránh lag luồng mô phỏng.",
        "Nén lượng tải gói tin JSON: Giảm 45% kích thước (32 KB vs 60 KB) mỗi tick."
    ], BLUE_BG, RGBColor(191, 219, 254), NAVY_SECONDARY),
    
    ("🔬 PHÒNG THÍ NGHIỆM ĐUA CHÍNH SÁCH (LAB)", [
        "Chạy song song 2 phiên mô phỏng đối đầu (Fixed-Time vs Adaptive) cùng seed ngẫu nhiên 42.",
        "Quan sát trực tiếp sự phân hóa hàng đợi và thời gian chờ tích lũy."
    ], RGBColor(238, 242, 255), RGBColor(199, 210, 254), RGBColor(67, 56, 202)),
    
    ("🤖 TRỢ LÝ GROQ LLM TRAFFIC COPILOT", [
        "Tích hợp LLM Groq giải thích nguyên nhân chuyển pha đèn bằng ngôn ngữ tự nhiên.",
        "Đưa ra khuyến nghị điều phối khi phát hiện điểm nghẽn bất thường."
    ], GREEN_BG, RGBColor(187, 247, 208), GREEN_ACCENT)
]

for i, (title, items, bg, border, color) in enumerate(feats):
    top = Inches(1.85 + i * 1.5)
    card = add_card(slide10, Inches(7.4), top, Inches(5.133), Inches(1.35), bg_color=WHITE, border_color=border)
    tf = card.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = color
    
    for it in items:
        pi = tf.add_paragraph()
        pi.text = f"• {it}"
        pi.font.name = "Segoe UI"
        pi.font.size = Pt(8.5)
        pi.font.color.rgb = SLATE_TEXT

add_footer(slide10, 10)

# ==========================================
# SLIDE 11: BENCHMARK RESULTS
# ==========================================
slide11 = prs.slides.add_slide(blank_layout)
set_slide_background(slide11, WHITE)
add_header(slide11, "KẾT QUẢ THỰC NGHIỆM", "11. Kết Quả Đo Kiểm Benchmark (HCM Metrics)", "Đánh giá định lượng trên 5,500 phương tiện qua 3 profile nhu cầu (Race Framework đối đầu)")

# Left Column (6.2 in)
# Table
add_card(slide11, Inches(0.8), Inches(1.85), Inches(6.0), Inches(2.5), bg_color=WHITE)
table_shape = slide11.shapes.add_table(4, 5, Inches(0.9), Inches(1.95), Inches(5.8), Inches(2.2))
table = table_shape.table
table.columns[0].width = Inches(1.3)
table.columns[1].width = Inches(0.8)
table.columns[2].width = Inches(1.1)
table.columns[3].width = Inches(1.1)
table.columns[4].width = Inches(1.5)

b_headers = ["Kịch bản", "Số xe", "Fixed-Time", "Adaptive", "Cải thiện"]
for col_idx, h in enumerate(b_headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
    p = cell.text_frame.paragraphs[0]
    p.text = h
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

b_rows = [
    ("Balanced", "5,500", "65.4 s", "38.9 s", "-40.5% (clear +14%)"),
    ("Asymmetric", "5,500", "88.2 s", "42.1 s", "-52.3% (clear +22%)"),
    ("Extreme", "5,500", "124.6 s", "57.3 s", "-54.0% (clear +28%)")
]

for row_idx, r in enumerate(b_rows):
    for col_idx, val in enumerate(r):
        cell = table.cell(row_idx + 1, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = "Segoe UI"
        p.font.size = Pt(9)
        if col_idx == 4:
            p.font.bold = True
            p.font.color.rgb = GREEN_ACCENT
        elif col_idx == 3:
            p.font.bold = True
            p.font.color.rgb = NAVY_SECONDARY
        else:
            p.font.color.rgb = SLATE_TEXT

# HCM Formulas Card
hcm_card = add_card(slide11, Inches(0.8), Inches(4.5), Inches(6.0), Inches(2.0), bg_color=BLUE_BG, border_color=RGBColor(191, 219, 254))
tf = hcm_card.text_frame
p = tf.paragraphs[0]
p.text = "TIÊU CHUẨN HIGHWAY CAPACITY MANUAL (HCM)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY

slide11.shapes.add_picture(f"{FORMULA_DIR}/hcm.png", Inches(1.0), Inches(5.0), width=Inches(5.6))

p_sub = tf.add_paragraph()
p_sub.text = "• Control Delay: Thời gian hao phí thực tế so với lưu thông tự do trong vùng 50m\n• Throughput: Số xe hoàn thành hành trình rời mạng lưới trên mỗi phút"
p_sub.font.name = "Segoe UI"
p_sub.font.size = Pt(9)
p_sub.font.color.rgb = SLATE_TEXT

# Right Column Image
w_img_path = "docs/images/waiting-time.png"
if os.path.exists(w_img_path):
    add_card(slide11, Inches(7.0), Inches(1.85), Inches(5.533), Inches(4.4), bg_color=RGBColor(15, 23, 42))
    slide11.shapes.add_picture(w_img_path, Inches(7.05), Inches(1.9), width=Inches(5.433))

cap = slide11.shapes.add_textbox(Inches(7.0), Inches(6.3), Inches(5.533), Inches(0.4))
p = cap.text_frame.paragraphs[0]
p.text = "Biểu đồ phân phối thời gian chờ: Adaptive AI giải phóng xe nhanh hơn 54%"
p.font.name = "Segoe UI"
p.font.size = Pt(9)
p.font.italic = True
p.font.color.rgb = MUTED_TEXT
p.alignment = PP_ALIGN.CENTER

add_footer(slide11, 11)

# ==========================================
# SLIDE 12: PROGRESS ROADMAP & NEXT STEPS
# ==========================================
slide12 = prs.slides.add_slide(blank_layout)
set_slide_background(slide12, WHITE)
add_header(slide12, "TỔNG KẾT & LỘ TRÌNH", "12. Ma Trận Tiến Độ Đã Hoàn Thành & Định Hướng", "Nghiệm thu 100% các khối AI cốt lõi và định hướng mở rộng hệ thống trong giai đoạn tiếp theo")

# Left Column: Done Matrix
c_done = add_card(slide12, Inches(0.8), Inches(1.85), Inches(5.8), Inches(4.8), bg_color=GREEN_BG, border_color=RGBColor(187, 247, 208))
tf = c_done.text_frame
p = tf.paragraphs[0]
p.text = "✅ CÁC HẠNG MỤC ĐÃ HOÀN THÀNH 100%"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = GREEN_ACCENT
p.space_after = Pt(8)

done_items = [
    ("Thị giác YOLOv11m & CARLA 10k", "mAP50 = 94.91%, 7 classes"),
    ("ByteTrack & Camera Homography H", "Ước lượng vận tốc thực & dừng chờ"),
    ("Thuật toán Leftover-Queue Redistribution", "EMA smoothing, giảm 54% wait time"),
    ("ALINEA Freeway Ramp Metering", "Điều tiết cao tốc & chống tràn nhánh"),
    ("Emergency Preemption Wave", "Làn sóng xanh & bù nợ sao ưu tiên"),
    ("Mô phỏng SUMO vi mô", "3 mạng lưới: Arterial, Highway, Mix"),
    ("FastAPI Concurrency WebSocket", "Streaming 10 Hz, nén payload 45%"),
    ("Next.js 14 Operator Dashboard & Lab", "Canvas Map, A/B race, Groq Copilot")
]

for title, detail in done_items:
    pi = tf.add_paragraph()
    pi.text = f"✓ {title}: "
    pi.font.name = "Segoe UI"
    pi.font.size = Pt(9.5)
    pi.font.bold = True
    pi.font.color.rgb = NAVY_PRIMARY
    
    # detail
    pi.text = f"✓ {title} — {detail}"
    pi.font.bold = False
    pi.space_after = Pt(4)

# Right Column: Next Steps
c_next = add_card(slide12, Inches(6.8), Inches(1.85), Inches(5.733), Inches(4.8), bg_color=BLUE_BG, border_color=RGBColor(191, 219, 254))
tf = c_next.text_frame
p = tf.paragraphs[0]
p.text = "🚀 KẾ HOẠCH GIAI ĐOẠN TIẾP THEO (STRATEGIC ROADMAP)"
p.font.name = "Segoe UI"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = NAVY_SECONDARY
p.space_after = Pt(12)

next_steps = [
    ("1. Nâng cấp Reinforcement Learning (MARL)", 
     "Tích hợp thuật toán học tăng cường sâu đa tác tử (Multi-Agent PPO) kết hợp cùng Leftover-Queue để tối ưu hóa phối hợp giữa các cụm nút giao phức tạp."),
    
    ("2. Triển khai Phần cứng Biên (Edge Device)", 
     "Biên dịch và tối ưu hóa mô hình YOLOv11m sang TensorRT (FP16 / INT8) để chạy trực tiếp trên các kit phần cứng nhúng NVIDIA Jetson Orin Nano / AGX tại cột đèn giao thông."),
    
    ("3. Thử nghiệm Nguồn Video RTSP Thực địa", 
     "Mở rộng kết nối luồng camera giao thông công cộng qua giao thức RTSP phục vụ đánh giá năng lực chạy thực tế diện rộng (Field Pilot Test).")
]

for title, desc in next_steps:
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(10)
    p_t.font.bold = True
    p_t.font.color.rgb = NAVY_PRIMARY
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = "Segoe UI"
    p_d.font.size = Pt(9)
    p_d.font.color.rgb = SLATE_TEXT
    p_d.space_after = Pt(10)

add_footer(slide12, 12)

# 4. Save Presentation
output_pptx = "d:/ai-traffic-management-system/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully to: {output_pptx}")

# Also copy to artifact directory
artifact_pptx = "C:/Users/Admin/.gemini/antigravity/brain/0bd16718-e31e-4a30-ae40-69e42323aea0/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(artifact_pptx)
print(f"Copy saved to artifact directory: {artifact_pptx}")
