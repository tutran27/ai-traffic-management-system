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
# DESIGN SYSTEM: Editorial Academic & Deep-Tech (Single-Technique per Slide)
# ==============================================================================
# 27 Slides: Each core technique / mathematical formula owns its dedicated slide.
# Pure white background, authoritative Deep Navy (#0B192C) ink, elegant hairline
# rules, high visual density with geometric shapes/diagrams, minimal text.
# ==============================================================================

BG_WHITE = RGBColor(255, 255, 255)
INK_NAVY = RGBColor(11, 25, 44)         # #0B192C - Primary ink
INK_SLATE = RGBColor(71, 85, 105)       # #475569 - Secondary text, subtitles, captions
INK_LIGHT_NAVY = RGBColor(30, 58, 138)  # #1E3A8A - Kicker, step badges, accents
HAIRLINE = RGBColor(226, 232, 240)      # #E2E8F0 - Architectural hairline dividers
BORDER_BOX = RGBColor(203, 213, 225)    # #CBD5E1 - Precise borders
TINT_SURFACE = RGBColor(248, 250, 252)  # #F8FAFC - Formula pedestal & card fills
TINT_BAR = RGBColor(241, 245, 249)      # #F1F5F9 - Table headers / badge fills

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

FORMULA_DIR = "temp_formulas_expanded"
os.makedirs(FORMULA_DIR, exist_ok=True)

def render_formula(name, latex_code, fontsize=18, dpi=300):
    fig = plt.figure(figsize=(10, 1.4))
    plt.text(0.5, 0.5, latex_code, fontsize=fontsize, ha='center', va='center', color='#0B192C')
    plt.axis('off')
    path = os.path.join(FORMULA_DIR, f"{name}.png")
    plt.savefig(path, bbox_inches='tight', transparent=True, dpi=dpi)
    plt.close()
    return path

print("Rendering high-res formulas for dedicated slides...")
F = {}
F['ciou'] = render_formula("ciou", r'$\mathcal{L}_{\mathrm{box}} = 1 - \left(\mathrm{IoU} - \frac{\rho^2(\mathbf{b}, \mathbf{b}^{gt})}{c^2} - \alpha v\right)$', fontsize=18)
F['ciou_sub'] = render_formula("ciou_sub", r'$v = \frac{4}{\pi^2}\left(\arctan\frac{w^{gt}}{h^{gt}} - \arctan\frac{w}{h}\right)^2, \quad \alpha = \frac{v}{(1-\mathrm{IoU})+v}$', fontsize=16)
F['bce'] = render_formula("bce", r'$\mathcal{L}_{\mathrm{cls}} = -\frac{1}{N}\sum_{i=1}^N \sum_{k=1}^K [y_{i,k}\log \sigma(p_{i,k}) + (1-y_{i,k})\log(1-\sigma(p_{i,k}))]$', fontsize=17)
F['dfl'] = render_formula("dfl", r'$\mathcal{L}_{\mathrm{dfl}}(S_l, S_r) = -[(y_r - y)\log(S_l) + (y - y_l)\log(S_r)]$', fontsize=18)
F['loss_total'] = render_formula("loss_total", r'$\mathcal{L}_{\mathrm{total}} = 7.5 \cdot \mathcal{L}_{\mathrm{box}} + 0.5 \cdot \mathcal{L}_{\mathrm{cls}} + 1.5 \cdot \mathcal{L}_{\mathrm{dfl}}$', fontsize=20)
F['lr'] = render_formula("lr", r'$\mathrm{Warmup:}\; \eta(t) = \eta_0 \frac{t}{3.0} \quad | \quad \mathrm{Linear:}\; \eta(t) = 0.01 \cdot \left[1 - \frac{t-3}{97} \cdot 0.99\right]$', fontsize=16)
F['kalman_state'] = render_formula("kalman_state", r'$\mathbf{x}_t = [X_c, Y_c, a, h, \dot{X}_c, \dot{Y}_c, \dot{a}, \dot{h}]^T, \quad \mathbf{P}_{t|t-1} = \mathbf{F}\mathbf{P}_{t-1|t-1}\mathbf{F}^T + \mathbf{Q}$', fontsize=16)
F['kalman_update'] = render_formula("kalman_update", r'$\mathbf{K}_t = \mathbf{P}_{t|t-1}\mathbf{H}^T(\mathbf{H}\mathbf{P}_{t|t-1}\mathbf{H}^T + \mathbf{R})^{-1}, \quad \mathbf{x}_{t|t} = \mathbf{x}_{t|t-1} + \mathbf{K}_t(\mathbf{z}_t - \mathbf{H}\mathbf{x}_{t|t-1})$', fontsize=15)
F['homography'] = render_formula("homography", r'$[X_w, Y_w, 1]^T \sim \mathbf{H} [u, v, 1]^T \Rightarrow X_w = \frac{h_{11}u + h_{12}v + h_{13}}{h_{31}u + h_{32}v + h_{33}}, \quad Y_w = \frac{h_{21}u + h_{22}v + h_{23}}{h_{31}u + h_{32}v + h_{33}}$', fontsize=15)
F['speed'] = render_formula("speed", r'$\bar{v}(t) = \frac{1}{M}\sum_{m=0}^{M-1} \frac{\Delta d(t-m)}{\Delta t \cdot \Delta k}, \quad (\bar{v} < 2.0\mathrm{\;m/s}, \; \tau \geq 2.0\mathrm{\;s})$', fontsize=16)
F['ema'] = render_formula("ema", r'$S_i(k) = \alpha \cdot Q_i(k) + (1-\alpha) \cdot S_i(k-1), \quad (\alpha = 0.7)$', fontsize=18)
F['grouping'] = render_formula("grouping", r'$\mathcal{U} = \{i \mid S_i(k) > 0\}, \quad \mathcal{S} = \{j \mid S_j(k) \leq 0\}$', fontsize=18)
F['budget'] = render_formula("budget", r'$R = \min\left(R_{\max}, \sum_{j \in \mathcal{S}} \max(0, g_j - g_{\min})\right), \quad (R_{\max} = 12.0\mathrm{\;s})$', fontsize=16)
F['redist'] = render_formula("redist", r'$g_i(k+1) = \min\left(g_{\max}, \; g_i(k) + R \cdot \frac{S_i}{\sum_{m \in \mathcal{U}} S_m}\right), \quad g_i \in [10.0\mathrm{\;s}, 50.0\mathrm{\;s}]$', fontsize=16)
F['alinea'] = render_formula("alinea", r'$r(k) = \operatorname{clamp}\left(r(k-1) + K_R \cdot (o^* - \hat{o}(k)), \; r_{\min}, \; r_{\max}\right)$', fontsize=17)
F['ramp_cycle'] = render_formula("ramp_cycle", r'$T_{\mathrm{cycle}}(k) = \frac{3600}{r(k)}, \quad t_{\mathrm{red}}(k) = \max\left(0, T_{\mathrm{cycle}}(k) - 3.0\mathrm{s}\right)$', fontsize=16)
F['spillback'] = render_formula("spillback", r'$Q_{\mathrm{ramp}}(k) \geq 30\mathrm{\;vehicles} \Rightarrow r(k) = r_{\max} = 1200\mathrm{\;veh/h}$', fontsize=17)
F['preempt_trigger'] = render_formula("preempt_trigger", r'$\mathrm{EV\;Detected:}\quad \phi(t) \leftarrow \phi_{\mathrm{EV}}(e), \quad t_{\mathrm{delay}} = 0\mathrm{\;s}$', fontsize=17)
F['debt'] = render_formula("debt", r'$D_d(J) \leftarrow D_d(J) + \Delta t_{\mathrm{preempt}}, \quad t_{\mathrm{comp}} = \min(D_{d^*}, \; 15.0\mathrm{\;s})$', fontsize=17)
F['hcm'] = render_formula("hcm", r'$d_i = \max(0, \; t_{\mathrm{dwell}} - t_{\mathrm{free\_flow}}), \quad \mathrm{Throughput} = \frac{N_{\mathrm{completed}} \times 60}{T_{\mathrm{sim}}}$', fontsize=16)
print("All formulas rendered successfully!")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]
TOTAL_SLIDES = 27

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
    p.text = "AI Traffic Management & Monitoring System — Báo cáo kỹ thuật chuyên sâu"
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

def create_formula_slide(slide_num, kicker, title, subtitle, formula_key, eq_label, cards_data, sub_formula_key=None):
    """Template for formula-centric slides: large math stage + 3 structured geometric cards."""
    s = prs.slides.add_slide(blank_layout)
    set_bg(s)
    add_header(s, kicker, title, subtitle)
    
    # 1. Math Stage (Hero pedestal)
    stage_h = Inches(1.8) if sub_formula_key else Inches(1.4)
    stage = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), stage_h)
    stage.fill.solid()
    stage.fill.fore_color.rgb = TINT_SURFACE
    stage.line.color.rgb = BORDER_BOX
    stage.line.width = Pt(0.75)
    
    # Formula Picture
    if sub_formula_key:
        s.shapes.add_picture(F[formula_key], Inches(1.2), Inches(1.75), width=Inches(9.0))
        s.shapes.add_picture(F[sub_formula_key], Inches(1.2), Inches(2.35), width=Inches(9.0))
        cards_top = Inches(3.65)
        cards_h = Inches(3.2)
    else:
        s.shapes.add_picture(F[formula_key], Inches(1.2), Inches(1.78), width=Inches(9.5))
        cards_top = Inches(3.25)
        cards_h = Inches(3.6)
        
    # Equation label on top right of pedestal
    eq_b = s.shapes.add_textbox(Inches(10.8), Inches(1.75), Inches(1.5), Inches(0.3))
    tf = eq_b.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = eq_label
    p.font.name = FONT_CODE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_LIGHT_NAVY
    p.alignment = PP_ALIGN.RIGHT
    
    # 2. 3 Structured Geometric Decomposition Cards
    card_w = Inches(3.75)
    for i, (card_title, items) in enumerate(cards_data):
        c_left = Inches(0.8 + i * (3.75 + 0.24))
        
        # Outer Card
        card = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, cards_top, card_w, cards_h)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_WHITE
        card.line.color.rgb = BORDER_BOX
        card.line.width = Pt(0.75)
        
        # Header strip inside card
        strip = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, cards_top, card_w, Inches(0.42))
        strip.fill.solid()
        strip.fill.fore_color.rgb = TINT_BAR
        strip.line.fill.background()
        
        tb_h = s.shapes.add_textbox(c_left + Inches(0.12), cards_top + Inches(0.08), card_w - Inches(0.24), Inches(0.3))
        tf_h = tb_h.text_frame
        tf_h.margin_left = tf_h.margin_right = tf_h.margin_top = tf_h.margin_bottom = 0
        p = tf_h.paragraphs[0]
        p.text = card_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = INK_NAVY
        
        # Body text inside card
        tb_b = s.shapes.add_textbox(c_left + Inches(0.15), cards_top + Inches(0.52), card_w - Inches(0.3), cards_h - Inches(0.6))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        
        for idx, (lead, body) in enumerate(items):
            p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
            p.text = f"• {lead}: {body}"
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.color.rgb = INK_NAVY
            if idx > 0:
                p.space_before = Pt(6)
                
    add_footer(s, slide_num)
    return s

# ==============================================================================
# SLIDE 1: COVER & EXECUTIVE METRICS
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_bg(s1)
# Left: Title & Metrics
k1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(6.5), Inches(0.3))
tf = k1.text_frame
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "TECHNICAL PROGRESS REPORT  •  Q4 2026"
p.font.name = FONT_HEADING
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

t1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.2), Inches(6.5), Inches(1.3))
tf = t1.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "HỆ THỐNG ĐIỀU PHỐI & GIÁM SÁT GIAO THÔNG THÔNG MINH"
p.font.name = FONT_HEADING
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = INK_NAVY

s1_sub = s1.shapes.add_textbox(Inches(0.8), Inches(2.6), Inches(6.5), Inches(0.6))
tf = s1_sub.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
p = tf.paragraphs[0]
p.text = "Nền tảng Tối ưu hóa Luồng Giao thông Đô thị Thời gian Thực kết hợp Thị giác YOLOv11m, Điều khiển Thích nghi Leftover-Queue, Cao tốc ALINEA & SUMO Engine."
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.color.rgb = INK_SLATE

# Hairline rule on left
line1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.35), Inches(6.2), Inches(0.015))
line1.fill.solid()
line1.fill.fore_color.rgb = HAIRLINE
line1.line.fill.background()

metrics = [
    ("-54.0%", "Thời gian dừng chờ xe", "Giảm trễ trung bình toàn mạng lưới (HCM)"),
    ("94.91%", "mAP@50 Đô thị", "YOLOv11m nhận diện 7 lớp phương tiện"),
    ("27.7 FPS", "Tốc độ Inference Biên", "Xử lý đa luồng camera trực tiếp"),
    ("100% Real-Time", "TraCI Telemetry 10 Hz", "Đồng bộ WebSocket & Next.js 14 Dashboard")
]

for idx, (num, label, desc) in enumerate(metrics):
    row, col = idx // 2, idx % 2
    mb = s1.shapes.add_textbox(Inches(0.8 + col * 3.25), Inches(3.6 + row * 1.5), Inches(3.2), Inches(1.3))
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

# Right: Hero Image
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
# SLIDE 2: KIẾN TRÚC PHÂN TẦNG ĐỘC LẬP (Decoupled Pipeline)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_bg(s2)
add_header(s2, "01 // TỔNG THỂ HỆ THỐNG", "Kiến Trúc Phân Tầng Độc Lập Đã Triển Khai", "Thiết kế Decoupled 4 phân tầng: Cảm biến, Điều khiển, Mô phỏng và Vận hành liên lạc qua Interface chuẩn.")

pipe_box = s2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(0.35))
tf_p = pipe_box.text_frame
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
    if i > 0:
        div = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left - Inches(0.1), Inches(2.1), Inches(0.015), Inches(4.3))
        div.fill.solid()
        div.fill.fore_color.rgb = HAIRLINE
        div.line.fill.background()

    c_box = s2.shapes.add_textbox(c_left, Inches(2.1), col_w, Inches(4.3))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
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

note_box = s2.shapes.add_textbox(Inches(0.8), Inches(6.52), Inches(11.733), Inches(0.35))
tf_n = note_box.text_frame
p = tf_n.paragraphs[0]
p.text = "NGUYÊN TẮC THIẾT KẾ DECOUPLED: Tách rời hoàn toàn cảm biến và điều khiển; sẵn sàng chuyển giao nguồn camera RTSP thực địa mà không phải chỉnh sửa giải thuật cốt lõi."
p.font.name = FONT_BODY
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = INK_SLATE

add_footer(s2, 2)

# ==============================================================================
# SLIDE 3: BỘ DỮ LIỆU TỔNG HỢP CARLA 10K
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_bg(s3)
add_header(s3, "02 // THỊ GIÁC MÁY TÍNH", "Bộ Dữ Liệu Tổng Hợp CARLA 10k & Cân Bằng Lớp", "Khắc phục triệt để Domain Shift và mất cân bằng lớp dữ liệu cào web bằng Simulator 3D.")

# 3 Geometric Info Blocks
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
    ("KỸ THUẬT CÂN BẰNG LỚP (SPAWNER REBALANCING)", [
        ("Vấn đề dữ liệu cào", "Xe buýt, xe cứu thương, xe cảnh sát chỉ chiếm < 2% tần suất tự nhiên."),
        ("Giải pháp Spawner", "Cấu hình bộ sinh xe nhân tạo tăng tỷ lệ xe hiếm lên gấp 2x - 3x."),
        ("Kết quả thực nghiệm", "Recall nhận diện xe buýt tăng vọt từ 5.9% lên mức 92.0%.")
    ])
]

card_w = Inches(3.75)
for i, (ctitle, items) in enumerate(ds_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), card_w, Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), card_w, Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s3.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), card_w - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s3.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), card_w - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.8)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)

add_footer(s3, 3)

# ==============================================================================
# SLIDE 4: MÔ HÌNH YOLOV11M & BENCHMARK THỊ GIÁC
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_bg(s4)
add_header(s4, "02 // THỊ GIÁC MÁY TÍNH", "Mô Hình YOLOv11m: Kiến Trúc & Kết Quả Đo Kiểm", "Đạt mAP@50 = 94.91% trên 7 lớp phương tiện giao thông với tốc độ 27.7 FPS thời gian thực.")

# Left (44%): Publication Table & Specs
t_box = s4.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.15), Inches(0.35))
p = t_box.text_frame.paragraphs[0]
p.text = "KẾT QUẢ ĐO KIỂM MÔ HÌNH (CV BENCHMARK METRICS)"
p.font.name = FONT_HEADING
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = INK_NAVY

table_shape = s4.shapes.add_table(5, 3, Inches(0.8), Inches(2.05), Inches(5.15), Inches(2.4))
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

cp_box = s4.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(5.15), Inches(1.9))
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
    pic = s4.shapes.add_picture(det_img_path, Inches(6.35), Inches(1.6), width=Inches(6.183), height=Inches(4.8))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s4.shapes.add_textbox(Inches(6.35), Inches(6.48), Inches(6.183), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Kiểm thử nhận diện đồng thời 7 lớp xe trong điều kiện trời mưa và ánh sáng thực tế phức tạp"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s4, 4)

# ==============================================================================
# SLIDE 5: HÀM MẤT MÁT HỒI QUY TỌA ĐỘ HỘP BAO (CIoU LOSS)
# ==============================================================================
create_formula_slide(
    slide_num=5,
    kicker="03 // CƠ SỞ TOÁN HỌC",
    title="Hàm Mất Mát Hồi Quy Tọa Độ Hộp Bao (CIoU Loss)",
    subtitle="Complete Intersection over Union: Tối ưu diện tích giao thoa, khoảng cách tâm Euclidean và tỷ lệ khung hình.",
    formula_key="ciou",
    eq_label="[Eq. 01]",
    sub_formula_key="ciou_sub",
    cards_data=[
        ("TỐI ƯU HÓA DIỆN TÍCH IoU", [
            ("Khái niệm IoU", "Đo lường tỷ lệ diện tích giao thoa giữa Bounding Box dự đoán và nhãn thực tế."),
            ("Mục tiêu cực tiểu hóa", "Thành phần 1 - IoU kéo hộp bao dự đoán tiệm cận tối đa với hộp bao đối tượng."),
            ("Đặc tính hình học", "Bất biến với tỷ lệ co giãn kích thước phương tiện gần hay xa camera.")
        ]),
        ("PHẠT KHOẢNG CÁCH TÂM EUCLIDEAN", [
            ("Khoảng cách tâm rho", "Đo khoảng cách Euclid giữa tọa độ tâm dự đoán b và tâm ground-truth b_gt."),
            ("Đường chéo c", "Chuẩn hóa khoảng cách tâm theo đường chéo c của hộp bao nhỏ nhất chứa cả hai."),
            ("Ý nghĩa hội tụ", "Định hướng vector di chuyển của Bounding Box về đúng tâm hình học xe cực nhanh.")
        ]),
        ("BÙ TRỪ TỶ LỆ KHUNG HÌNH (v & alpha)", [
            ("Đo sai lệch góc v", "So sánh độ lệch góc arctan giữa tỷ lệ w/h của dự đoán và nhãn thực."),
            ("Hệ số cân bằng alpha", "Tự động tăng trọng số hình dáng khi IoU lớn hơn ngưỡng tin cậy."),
            ("Chống biến dạng", "Ngăn chặn việc dự đoán đúng diện tích nhưng sai tỷ lệ chiều dài/rộng.")
        ])
    ]
)

# ==============================================================================
# SLIDE 6: HÀM MẤT MÁT PHÂN LOẠI ĐA NHÃN (BCE WITH LOGITS)
# ==============================================================================
create_formula_slide(
    slide_num=6,
    kicker="03 // CƠ SỞ TOÁN HỌC",
    title="Hàm Mất Mát Phân Loại Đa Nhãn (BCE with Logits)",
    subtitle="Binary Cross Entropy with Logits: Phân loại độc lập cho K = 7 lớp xe, triệt tiêu hiện tượng áp chế xác suất.",
    formula_key="bce",
    eq_label="[Eq. 02]",
    cards_data=[
        ("PHÂN LOẠI ĐỘC LẬP K = 7 LỚP", [
            ("Danh mục 7 lớp", "Car, Bus, Truck, Motorcycle, Bicycle, Ambulance, Police."),
            ("Xử lý độc lập", "Mỗi lớp phương tiện được gán một bộ phân loại nhị phân riêng biệt."),
            ("Hàm kích hoạt Sigmoid", "Áp dụng hàm sigma(p) độc lập cho từng kênh logits thay vì Softmax toàn thể.")
        ]),
        ("TRIỆT TIÊU ÁP CHẾ XÁC SUẤT", [
            ("Hạn chế của Softmax", "Bắt buộc tổng xác suất bằng 1, khiến lớp chiếm ưu thế lấn át các lớp xe khác."),
            ("Cải tiến của BCE", "Cho phép hai phương tiện chồng lấn trong cùng một vùng ảnh vẫn được nhận diện chính xác."),
            ("Độ ổn định cao", "Đặc biệt hiệu quả khi các xe bám đuôi sát nhau hoặc xe máy đi cạnh xe buýt.")
        ]),
        ("TRỌNG SỐ TỔNG HỢP LAMBDA_CLS", [
            ("Cân bằng đa nhiệm", "Gán trọng số phạt phân loại lambda_cls = 0.5 trong hàm mất mát tổng hợp."),
            ("Mục tiêu thiết kế", "Ưu tiên độ chính xác tọa độ (hồi quy vị trí) trước khi phân loại chi tiết."),
            ("Độ hội tụ thực tế", "Giúp mô hình hội tụ ổn định sau 100 epochs mà không bị phân kỳ độ dốc.")
        ])
    ]
)

# ==============================================================================
# SLIDE 7: HÀM MẤT MÁT PHÂN PHỐI BIÊN TIÊU CỰ (DFL LOSS)
# ==============================================================================
create_formula_slide(
    slide_num=7,
    kicker="03 // CƠ SỞ TOÁN HỌC",
    title="Hàm Mất Mát Phân Phối Biên Tiêu Cự (Distribution Focal Loss)",
    subtitle="Distribution Focal Loss: Học phân phối xác suất liên tục của biên hộp bao thay cho điểm cứng Dirac delta.",
    formula_key="dfl",
    eq_label="[Eq. 03]",
    cards_data=[
        ("PHÂN PHỐI XÁC SUẤT MỀM CỦA BIÊN", [
            ("Hạn chế của Dirac delta", "Coi biên hộp bao là một tọa độ số nguyên cứng nhắc, bỏ qua độ mờ nhòe thực tế."),
            ("Học phân phối liên tục", "Mô hình học phân phối xác suất quanh hai điểm nguyên lân cận y_l và y_r."),
            ("Biểu diễn bất định", "Phản ánh trung thực độ không chắc chắn tại vị trí tiếp giáp giữa xe và mặt đường.")
        ]),
        ("BÙ TRỪ CHE KHUẤT VÀ MỜ NHÒE", [
            ("Hiện tượng che khuất", "Trong giao thông đô thị, xe thường xuyên bị cột đèn, cây xanh hoặc xe khác che mất cạnh."),
            ("Tăng độ nhạy biên", "DFL tập trung lực kéo gradient vào các điểm lân cận giá trị thực y."),
            ("Độ sắc nét hộp bao", "Giúp Bounding Box bao khít lấy thân xe ngay cả trong điều kiện mưa gió mờ kính.")
        ]),
        ("TRỌNG SỐ THIẾT KẾ LAMBDA_DFL", [
            ("Hệ số khuếch đại", "Thiết lập lambda_dfl = 1.5 trong hàm tối ưu hóa huấn luyện."),
            ("Tính chất hội tụ", "Hội tụ mượt mà theo phân phối tiêu cự Focal Loss, triệt tiêu nhiễu mẫu dễ."),
            ("Đóng góp mAP", "Giúp chỉ số mAP@50-95 đạt tới 86.49%, cực kỳ chuẩn xác cho đo đạc khoảng cách.")
        ])
    ]
)

# ==============================================================================
# SLIDE 8: TỔNG HÀM MẤT MÁT ĐA NHIỆM & LỊCH TRÌNH HỌC
# ==============================================================================
create_formula_slide(
    slide_num=8,
    kicker="03 // CƠ SỞ TOÁN HỌC",
    title="Tổng Hàm Mất Mát Đa Nhiệm & Lịch Trình Tốc Độ Học",
    subtitle="Cân bằng trọng số đa nhiệm và lịch trình suy giảm tốc độ học (Linear Learning Rate Decay).",
    formula_key="loss_total",
    eq_label="[Eq. 04]",
    sub_formula_key="lr",
    cards_data=[
        ("CÂN BẰNG ĐA NHIỆM (MULTI-TASK WEIGHTS)", [
            ("Trọng số vị trí (7.5)", "Ưu tiên cao nhất cho tọa độ hộp bao CIoU nhằm phục vụ đo đạc vận tốc."),
            ("Trọng số phân loại (0.5)", "Đảm bảo phân biệt đúng 7 lớp phương tiện mà không gây nhiễu gradient."),
            ("Trọng số biên (1.5)", "Tăng cường độ sắc nét cạnh hộp bao qua phân phối DFL liên tục.")
        ]),
        ("LỊCH TRÌNH WARMUP (EPOCHS 0 - 3)", [
            ("Giai đoạn khởi động", "Tăng tuyến tính tốc độ học từ 0 lên eta_0 trong 3 epochs đầu tiên."),
            ("Ổn định trọng số", "Tránh hiện tượng bùng nổ gradient khi các lớp tích chập bắt đầu học đặc trưng."),
            ("Cân bằng bộ nhớ", "Khởi tạo ổn định cho bộ nhớ tối ưu hóa AdamW.")
        ]),
        ("SUY GIẢM TUYẾN TÍNH (LINEAR DECAY)", [
            ("Giai đoạn suy giảm", "Từ epoch 3 đến epoch 100, tốc độ học giảm dần về 1% giá trị ban đầu."),
            ("Hội tụ tối ưu", "Giúp mô hình dò tìm nghiệm tối ưu cục bộ tinh vi trong không gian tham số 20.06M."),
            ("Chống Overfitting", "Kết hợp Weight Decay 0.0005 triệt tiêu hiện tượng học vẹt dữ liệu.")
        ])
    ]
)

# ==============================================================================
# SLIDE 9: THEO DÕI ĐA ĐỐI TƯỢNG: BYTETRACK & KALMAN 8D
# ==============================================================================
create_formula_slide(
    slide_num=9,
    kicker="04 // THEO DÕI & ĐO ĐẠC",
    title="Theo Dõi Đa Đối Tượng: ByteTrack & Bộ Lọc Kalman 8D",
    subtitle="Mô hình chuyển động tuyến tính liên tục với vector trạng thái 8 chiều và thuật toán kết hợp Hungarian 2 tầng.",
    formula_key="kalman_state",
    eq_label="[Eq. 05]",
    sub_formula_key="kalman_update",
    cards_data=[
        ("VECTOR TRẠNG THÁI 8 CHIỀU x_t", [
            ("Tọa độ không gian", "X_c, Y_c (tọa độ tâm hộp bao), a (tỷ lệ khung hình w/h), h (chiều cao hộp bao)."),
            ("Vận tốc động học", "X_dot, Y_dot, a_dot, h_dot (vận tốc biến thiên tương ứng theo thời gian thực)."),
            ("Dự báo vị trí P_t|t-1", "Dự báo bước tiếp theo bằng ma trận chuyển trạng thái F và ma trận nhiễu Q.")
        ]),
        ("CẬP NHẬT KALMAN GAIN K_t", [
            ("Độ lợi Kalman K_t", "Cân bằng trọng số giữa dự báo động học và kết quả phát hiện thực tế từ camera."),
            ("Ma trận hiệp phương sai R", "Đo lường độ bất định và nhiễu ngẫu nhiên của cảm biến hình ảnh."),
            ("Cập nhật trạng thái", "Làm mịn quỹ đạo di chuyển của phương tiện, loại bỏ rung giật khung hình.")
        ]),
        ("GHÉP NỐI HUNGARIAN 2 TẦNG (BYTETRACK)", [
            ("Tầng 1 (High-score)", "Ghép nối các phát hiện có độ tin cậy cao (score >= 0.5) với các vệt theo dõi."),
            ("Tầng 2 (Low-score)", "Tận dụng các phát hiện bị mờ nhòe (score < 0.5) để duy trì ID xe bị che khuất."),
            ("Hiệu quả thực nghiệm", "Triệt tiêu hiện tượng nhảy ID (ID Switches) khi xe đi qua gầm cầu hoặc bóng râm.")
        ])
    ]
)

# ==============================================================================
# SLIDE 10: MA TRẬN HOMOGRAPHY MẶT ĐẤT (GROUND-PLANE H)
# ==============================================================================
create_formula_slide(
    slide_num=10,
    kicker="04 // THEO DÕI & ĐO ĐẠC",
    title="Hình Học Phẳng: Ma Trận Homography Mặt Đất H",
    subtitle="Chuyển đổi phối cảnh từ không gian điểm ảnh 2D (u, v) sang hệ tọa độ phẳng thế giới thực (X_w, Y_w) theo mét.",
    formula_key="homography",
    eq_label="[Eq. 06]",
    cards_data=[
        ("BẢN CHẤT HÌNH HỌC PHỐI CẢNH", [
            ("Hiện tượng biến dạng", "Trong ảnh camera giao thông, xe ở gần nhìn to, xe ở xa nhìn nhỏ và méo hình học."),
            ("Phép chiếu phẳng Homography", "Ánh xạ 1-1 giữa mặt phẳng cảm biến máy ảnh và mặt phẳng mặt đường thực tế."),
            ("Giả định cao độ Z_w = 0", "Điểm tiếp đất của bánh xe luôn nằm trên bề mặt phẳng của lòng đường.")
        ]),
        ("MA TRẬN CHUYỂN ĐỔI H 3x3", [
            ("8 bậc tự do", "Ma trận H gồm 9 phần tử với 8 bậc tự do, được hiệu chuẩn qua 4 điểm mốc thực địa."),
            ("Tọa độ thuần nhất", "Tính toán tọa độ thực X_w, Y_w qua phép chia chuẩn hóa tỷ lệ (h31*u + h32*v + h33)."),
            ("Đơn vị chuẩn hóa mét", "Kết quả đầu ra có đơn vị mét chuẩn xác, độc lập hoàn toàn với góc nghiêng camera.")
        ]),
        ("ỨNG DỤNG ĐO ĐẠC GIAO THÔNG", [
            ("Tính toán cự ly thực", "Đo khoảng cách vật lý chính xác giữa các phương tiện (headway)."),
            ("Phát hiện xung đột", "Nhận diện nguy cơ va chạm giao cắt tại ngã tư dựa trên khoảng cách mét thực."),
            ("Vận tốc tuyệt đối", "Cơ sở toán học duy nhất để tính toán vận tốc xe tính bằng km/h từ video camera.")
        ])
    ]
)

# ==============================================================================
# SLIDE 11: ƯỚC LƯỢNG VẬN TỐC THỰC & TIÊU CHUẨN XE CHỜ ĐÈN ĐỎ
# ==============================================================================
s11 = prs.slides.add_slide(blank_layout)
set_bg(s11)
add_header(s11, "04 // THEO DÕI & ĐO ĐẠC", "Ước Lượng Vận Tốc Thực & Tiêu Chuẩn Xe Chờ Đèn Đỏ", "Bộ lọc trượt M = 5 frames và tiêu chuẩn kép (Vận tốc < 2.0 m/s trong thời gian tau >= 2.0s) phát hiện hàng đợi.")

# Top Pedestal
stage11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.4))
stage11.fill.solid()
stage11.fill.fore_color.rgb = TINT_SURFACE
stage11.line.color.rgb = BORDER_BOX
stage11.line.width = Pt(0.75)

s11.shapes.add_picture(F['speed'], Inches(1.5), Inches(1.78), width=Inches(9.0))

eq_b = s11.shapes.add_textbox(Inches(10.8), Inches(1.75), Inches(1.5), Inches(0.3))
p = eq_b.text_frame.paragraphs[0]
p.text = "[Eq. 07]"
p.font.name = FONT_CODE
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY
p.alignment = PP_ALIGN.RIGHT

# Left (46%): 2 Cards
c_w11 = Inches(5.4)
cards11 = [
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

y_pos11 = Inches(3.25)
for title, items in cards11:
    card = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos11, c_w11, Inches(1.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos11, c_w11, Inches(0.38))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s11.shapes.add_textbox(Inches(0.95), y_pos11 + Inches(0.06), c_w11 - Inches(0.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s11.shapes.add_textbox(Inches(0.95), y_pos11 + Inches(0.45), c_w11 - Inches(0.3), Inches(1.2))
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
            
    y_pos11 += Inches(1.85)

# Right (54%): Visual Figure
col_img_path = "docs/images/collision-detection.png"
if os.path.exists(col_img_path):
    pic = s11.shapes.add_picture(col_img_path, Inches(6.5), Inches(3.25), width=Inches(6.033), height=Inches(3.4))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s11.shapes.add_textbox(Inches(6.5), Inches(6.7), Inches(6.033), Inches(0.3))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Nhận diện xe dừng chờ đèn đỏ và phát hiện nguy cơ va chạm giao cắt tức thời"
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s11, 11)

# ==============================================================================
# SLIDE 12: THUẬT TOÁN THÍCH NGHI: BỘ LỌC LÀM MỊN EMA HÀNG ĐỢI
# ==============================================================================
create_formula_slide(
    slide_num=12,
    kicker="05 // ĐIỀU KHIỂN THÍCH NGHI",
    title="Thuật Toán Thích Nghi: Bộ Lọc Làm Mịn EMA Hàng Đợi",
    subtitle="Exponential Moving Average: Khử dao động ngẫu nhiên giữa các chu kỳ đèn và nắm bắt trung thực xu thế dòng xe.",
    formula_key="ema",
    eq_label="[Eq. 08]",
    cards_data=[
        ("GHI NHẬN TẠI THỜI ĐIỂM CHỚM VÀNG", [
            ("Thời điểm đo đạc then chốt", "Số lượng xe dừng chờ Q_i(k) được chốt chính xác tại khoảnh khắc đèn chuyển từ Xanh sang Vàng."),
            ("Ý nghĩa vật lý", "Đại diện cho lượng nhu cầu giao thông chưa được giải tỏa hết trong pha xanh vừa kết thúc."),
            ("Không cần dự báo xa", "Loại bỏ hoàn toàn sự phụ thuộc vào các mô hình dự báo lưu lượng dài hạn thiếu chính xác.")
        ]),
        ("BỘ LỌC THÔNG THẤP EMA (ALPHA = 0.7)", [
            ("Trọng số hiện tại (70%)", "Phản ứng nhạy bén với sự gia tăng đột biến của dòng phương tiện trong chu kỳ vừa qua."),
            ("Trọng số lịch sử (30%)", "Kế thừa trạng thái hàng đợi tích lũy từ chu kỳ k-1 nhằm duy trì tính ổn định."),
            ("Khử nhiễu ngẫu nhiên", "Ngăn chặn thuật toán phản ứng quá mức với một chiếc xe đi chậm hoặc sự cố tạm thời.")
        ]),
        ("CƠ SỞ TÁI PHÂN BỔ BỀN VỮNG", [
            ("Biến trạng thái S_i(k)", "Đóng vai trò là đại lượng đầu vào duy nhất cho thuật toán phân bổ ngân sách pha tiếp theo."),
            ("Tính liên tục thời gian", "Đảm bảo sự chuyển tiếp mượt mà giữa các chu kỳ đèn, không gây sốc nhịp giao thông."),
            ("Độ hội tụ cao", "Giúp hệ số dao động chu kỳ giảm hơn 65% so với việc dùng trực tiếp giá trị đo tức thời Q_i.")
        ])
    ]
)

# ==============================================================================
# SLIDE 13: PHÂN LOẠI TRẠNG THÁI PHA & NGÂN SÁCH TÁI PHÂN BỔ
# ==============================================================================
create_formula_slide(
    slide_num=13,
    kicker="05 // ĐIỀU KHIỂN THÍCH NGHI",
    title="Phân Nhóm Trạng Thái Pha & Trích Xuất Ngân Sách R",
    subtitle="Phân tách rạch ròi giữa nhóm pha thiếu giờ và nhóm pha dư thừa để thành lập ngân sách chia sẻ thời gian xanh.",
    formula_key="grouping",
    eq_label="[Eq. 09]",
    sub_formula_key="budget",
    cards_data=[
        ("NHÓM PHA THIẾU THỜI GIAN (U)", [
            ("Tập hợp Undersupplied U", "Bao gồm các pha có hàng đợi tồn dư S_i(k) > 0 sau khi đèn đã chuyển vàng."),
            ("Bản chất giao thông", "Lưu lượng xe thực tế vượt quá khả năng thông hành của thời lượng xanh hiện tại."),
            ("Quyền ưu tiên nhận viện trợ", "Là đối tượng duy nhất được cấp bù thêm thời gian xanh trong chu kỳ kế tiếp.")
        ]),
        ("NHÓM PHA THỎA MÃN (S)", [
            ("Tập hợp Satisfied S", "Bao gồm các pha có hàng đợi tồn dư S_j(k) <= 0 (đã giải phóng hết xe thông thoáng)."),
            ("Thời gian lãng phí", "Đèn xanh vẫn bật trong khi mặt đường không còn xe lưu thông (Green wastage)."),
            ("Đóng góp ngân sách", "Trích xuất phần thời gian xanh dư thừa (g_j - g_min) để san sẻ cho các nhánh kẹt.")
        ]),
        ("NGÂN SÁCH TRÍCH XUẤT TỐI ĐA R_max", [
            ("Công thức trích xuất R", "Lấy tổng thời gian có thể trích từ nhóm S nhưng chặn trên bởi ngưỡng an toàn."),
            ("Ngưỡng giới hạn R_max = 12.0s", "Không cho phép rút quá 12 giây trong một chu kỳ để bảo vệ dòng xe nhánh phụ."),
            ("Bảo toàn tổng chu kỳ", "Ngân sách R đảm bảo tổng chu kỳ đèn toàn giao lộ không bao giờ bị kéo dài đột ngột.")
        ])
    ]
)

# ==============================================================================
# SLIDE 14: TÁI PHÂN BỔ THỜI GIAN XANH CÓ RÀNG BUỘC
# ==============================================================================
create_formula_slide(
    slide_num=14,
    kicker="05 // ĐIỀU KHIỂN THÍCH NGHI",
    title="Tái Phân Bổ Thời Gian Xanh & Ràng Buộc An Toàn",
    subtitle="Bù thời gian xanh theo tỷ trọng nhu cầu thực tế và tuân thủ nghiêm ngặt khung ràng buộc an toàn tuyệt đối.",
    formula_key="redist",
    eq_label="[Eq. 10]",
    cards_data=[
        ("TÁI PHÂN BỔ THEO TỶ TRỌNG w_i", [
            ("Trọng số phân phối w_i", "Được tính bằng tỷ lệ tồn dư của nhánh i trên tổng lượng tồn dư của nhóm U: S_i / sum(S_m)."),
            ("Nguyên tắc công bằng", "Nhánh nào kẹt xe nặng hơn và có lượng xe tồn đọng lớn hơn sẽ được nhận nhiều thời gian hơn."),
            ("Triệt tiêu hàng đợi tồn", "Giải tỏa triệt để nút thắt cổ chai ngay trong chu kỳ k+1.")
        ]),
        ("RÀNG BUỘC THỜI LƯỢNG [g_min, g_max]", [
            ("Thời lượng tối thiểu g_min = 10.0s", "Đảm bảo tuyệt đối thời gian cho người đi bộ qua đường an toàn theo quy chuẩn."),
            ("Thời lượng tối đa g_max = 50.0s", "Ngăn chặn tình trạng một nhánh giao thông độc quyền đèn xanh gây nghẽn các nhánh khác."),
            ("Bảo toàn chu kỳ", "Tổng thời lượng xanh phân bổ lại luôn bằng đúng tổng thời lượng xanh thu hồi từ nhóm S.")
        ]),
        ("HIỆU QUẢ GIẢM THỜI GIAN CHỜ", [
            ("Giảm 54% thời gian chờ", "Kết quả thực nghiệm trên SUMO chứng minh thời gian chờ xe giảm từ 124.6s xuống còn 57.3s."),
            ("Tăng thông lượng mạng", "Số lượng xe hoàn thành hành trình qua mạng lưới tăng thêm từ 14% đến 28%."),
            ("Khả năng tự thích ứng", "Tự động điều chỉnh linh hoạt khi lưu lượng giao thông thay đổi giữa giờ cao điểm và thấp điểm.")
        ])
    ]
)

# ==============================================================================
# SLIDE 15: ĐIỀU TIẾT CAO TỐC: LUẬT HỒI TIẾP ALINEA
# ==============================================================================
create_formula_slide(
    slide_num=15,
    kicker="06 // ĐIỀU TIẾT CAO TỐC",
    title="Điều Tiết Cao Tốc: Luật Hồi Tiếp Tích Phân ALINEA",
    subtitle="Luật điều khiển phản hồi tích phân vòng kín Papageorgiou et al. giữ mật độ hạ lưu dưới điểm sụp đổ lưu lượng.",
    formula_key="alinea",
    eq_label="[Eq. 11]",
    sub_formula_key="ramp_cycle",
    cards_data=[
        ("NGUYÊN LÝ ĐIỀU KHIỂN HỒI TIẾP", [
            ("Mật độ mục tiêu o* = 20%", "Điểm mật độ chiếm dụng lý tưởng giữ cho tuyến chính cao tốc đạt thông lượng tối đa."),
            ("Cảm biến hạ lưu ô(k)", "Đo mật độ thực tế tại điểm hòa dòng và hồi tiếp về bộ điều khiển sau mỗi 10 giây."),
            ("Cơ chế tích phân (I-Controller)", "Tự động bù trừ sai lệch mật độ mà không để lại sai số xác lập (zero steady-state error).")
        ]),
        ("THAM SỐ THIẾT KẾ & GIỚI HẠN", [
            ("Hệ số khuếch đại K_R = 70.0", "Hệ số phản hồi chuẩn quốc tế đảm bảo hệ thống phản ứng nhanh nhưng không bị dao động kích động."),
            ("Lưu lượng tối thiểu r_min = 200 veh/h", "Tránh việc đóng hoàn toàn nhánh nhập làn gây ức chế tâm lý cho tài xế."),
            ("Lưu lượng tối đa r_max = 1200 veh/h", "Năng lực xả tối đa của một làn xe nhập khi tuyến chính hoàn toàn thông thoáng.")
        ]),
        ("QUY ĐỔI SANG CHU KỲ ĐÈN METERING", [
            ("Thời lượng chu kỳ T_cycle", "Được tính trực tiếp bằng 3600 / r(k) để cấp đúng số lượng xe mong muốn."),
            ("Cố định thời lượng xanh 2.0s", "Chỉ cho phép duy nhất 1 xe nhập làn trong mỗi chu kỳ (One vehicle per green rule)."),
            ("Thời lượng vàng 1.0s & đỏ điều biến", "Thời gian đỏ t_red co giãn tự động để kiểm soát khoảng cách giữa các xe nhập làn.")
        ])
    ]
)

# ==============================================================================
# SLIDE 16: ĐIỀU TIẾT CAO TỐC: CƠ CHẾ GHI ĐÈ CHỐNG TRÀN
# ==============================================================================
s16 = prs.slides.add_slide(blank_layout)
set_bg(s16)
add_header(s16, "06 // ĐIỀU TIẾT CAO TỐC", "Điều Tiết Cao Tốc: Cơ Chế Ghi Đè Chống Tràn Nhánh Nối", "On-Ramp Spillback Override: Mở xả khẩn cấp khi hàng đợi nhánh nối vượt quá 30 xe để bảo vệ đô thị.")

# Top Math Pedestal
stage16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.3))
stage16.fill.solid()
stage16.fill.fore_color.rgb = TINT_SURFACE
stage16.line.color.rgb = BORDER_BOX
stage16.line.width = Pt(0.75)

s16.shapes.add_picture(F['spillback'], Inches(1.5), Inches(1.78), width=Inches(9.0))

eq_b = s16.shapes.add_textbox(Inches(10.8), Inches(1.75), Inches(1.5), Inches(0.3))
p = eq_b.text_frame.paragraphs[0]
p.text = "[Rule. 01]"
p.font.name = FONT_CODE
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY
p.alignment = PP_ALIGN.RIGHT

# Left (50%): 2 Clean Cards
card_w16 = Inches(5.6)
cards16 = [
    ("NGUY CƠ NGHẼN TRÀN NGƯỢC (SPILLBACK RISK)", [
        ("Hiện tượng nghẽn lan tỏa", "Khi đèn Metering giữ đỏ quá lâu, xe xếp hàng dài trên nhánh nối sẽ tràn ra đường nội đô lân cận."),
        ("Tê liệt mạng lưới đô thị", "Làm tắc nghẽn các nút giao đèn tín hiệu phụ cận, gây ra sụp đổ giao thông liên hoàn."),
        ("Cần cơ chế can thiệp khẩn cấp", "Phải ưu tiên giải tỏa nhánh nối khi chiều dài hàng đợi chạm ngưỡng nguy hiểm.")
    ]),
    ("CƠ CHẾ GHI ĐÈ KHẨN CẤP (OVERRIDE ACTIVATION)", [
        ("Ngưỡng kích hoạt Q_ramp >= 30 xe", "Cảm biến trên nhánh nối phát hiện số xe dừng chờ vượt quá 30 phương tiện."),
        ("Ghi đè lưu lượng r_max = 1200 veh/h", "Tạm thời vô hiệu hóa luật ALINEA, mở đèn xanh tối đa để xả nhanh dòng xe."),
        ("Tự động phục hồi", "Khi hàng đợi giảm xuống dưới mức an toàn, hệ thống tự động trả quyền điều khiển về cho ALINEA.")
    ])
]

y_pos16 = Inches(3.15)
for title, items in cards16:
    card = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos16, card_w16, Inches(1.75))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos16, card_w16, Inches(0.38))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s16.shapes.add_textbox(Inches(0.95), y_pos16 + Inches(0.06), card_w16 - Inches(0.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s16.shapes.add_textbox(Inches(0.95), y_pos16 + Inches(0.45), card_w16 - Inches(0.3), Inches(1.2))
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
    y_pos16 += Inches(1.9)

# Right (50%): Geometric Highway Schematic Diagram
diag_box = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(3.15), Inches(5.733), Inches(3.65))
diag_box.fill.solid()
diag_box.fill.fore_color.rgb = TINT_SURFACE
diag_box.line.color.rgb = BORDER_BOX
diag_box.line.width = Pt(0.75)

tb_diag = s16.shapes.add_textbox(Inches(7.1), Inches(3.4), Inches(5.2), Inches(3.2))
tf = tb_diag.text_frame
p = tf.paragraphs[0]
p.text = "SƠ ĐỒ HÒA DÒNG TUYẾN CHÍNH & ON-RAMP METERING"
p.font.name = FONT_HEADING
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = INK_LIGHT_NAVY

p2 = tf.add_paragraph()
p2.text = (
    "\n[ TUYẾN CHÍNH ] ──► [ Cảm biến ô(k) ] ──► Thông suốt\n"
    "                         ▲ Điểm hòa dòng\n"
    "[ NHÁNH NỐI ] ────► [ Đèn Meter r(k) ]\n"
    "  ▲\n"
    "  └── Q_ramp >= 30 xe ──► [ GHI ĐÈ XẢ TRẠM r_max ]"
)
p2.font.name = FONT_CODE
p2.font.size = Pt(8.5)
p2.font.color.rgb = INK_NAVY
p2.space_before = Pt(10)

p3 = tf.add_paragraph()
p3.text = "\nGiải thích cơ chế vận hành:\n• Khi mật độ ô(k) cao nhưng hàng đợi nhánh nối nhỏ: ALINEA xiết van đèn đỏ.\n• Khi hàng đợi nhánh nối chạm ngưỡng 30 xe: Ghi đè xả trạm ngay lập tức để giải cứu đường nội đô lân cận."
p3.font.name = FONT_BODY
p3.font.size = Pt(9.5)
p3.font.italic = True
p3.font.color.rgb = INK_SLATE
p3.space_before = Pt(10)

add_footer(s16, 16)

# ==============================================================================
# SLIDE 17: ƯU TIÊN KHẨN CẤP: LÀN SÓNG XANH TỨC THỜI (EMERGENCY PREEMPTION)
# ==============================================================================
create_formula_slide(
    slide_num=17,
    kicker="07 // ƯU TIÊN KHẨN CẤP",
    title="Ưu Tiên Khẩn Cấp: Làn Sóng Xanh Tức Thời (0s Delay)",
    subtitle="Emergency Vehicle Preemption: Nhận diện xe ưu tiên và cưỡng bức chuyển pha xanh dọn đường tức thời.",
    formula_key="preempt_trigger",
    eq_label="[Rule. 02]",
    cards_data=[
        ("NHẬN DIỆN PHƯƠNG TIỆN KHẨN CẤP", [
            ("Lớp xe ưu tiên", "Xe cứu thương (Ambulance), xe cứu hỏa (Fire Truck), xe cảnh sát (Police)."),
            ("Nguồn phát hiện kép", "Được nhận diện tự động từ camera AI YOLOv11m hoặc nhận tín hiệu định vị GPS/TraCI."),
            ("Xác định lộ trình di chuyển", "Hệ thống tự động tra cứu hướng di chuyển và nút giao mục tiêu J nằm trên đường đi.")
        ]),
        ("CƯỠNG BỨC CHUYỂN PHA DỌN ĐƯỜNG", [
            ("Cắt pha tức thời phi_EV", "Ngay lập tức kích hoạt chu trình chuyển pha an toàn về hướng xe khẩn cấp đang tiến tới."),
            ("Dọn sạch xung đột", "Bật đèn xanh sớm để giải phóng toàn bộ các xe đang dừng chờ chắn trước mặt xe ưu tiên."),
            ("Độ trễ bằng 0 giây", "Xe khẩn cấp băng qua nút giao với tốc độ tối đa mà không phải giảm tốc hoặc dừng chờ.")
        ]),
        ("BẢO VỆ AN TOÀN CHUYỂN PHA", [
            ("Thời gian vàng tối thiểu", "Vẫn duy trì khoảng đệm vàng 3.0s cho các luồng xe trực giao kịp dừng lại an toàn."),
            ("Chống xung đột nguy hiểm", "Khóa cứng các hướng rẽ cắt ngang hành lang di chuyển của xe khẩn cấp."),
            ("Giám sát hành trình liên tục", "Giữ pha xanh dọn đường cho đến khi xe ưu tiên vừa thoát khỏi tâm nút giao.")
        ])
    ]
)

# ==============================================================================
# SLIDE 18: ƯU TIÊN KHẨN CẤP: BÙ TRỪ CÔNG NỢ THỜI GIAN XANH
# ==============================================================================
create_formula_slide(
    slide_num=18,
    kicker="07 // ƯU TIÊN KHẨN CẤP",
    title="Ưu Tiên Khẩn Cấp: Bù Trừ Công Nợ Thời Gian Xanh Công Bằng",
    subtitle="Starvation Debt Compensation: Tích lũy thiệt hại thời gian của các hướng bị cắt và hoàn trả công bằng sau sự cố.",
    formula_key="debt",
    eq_label="[Eq. 12]",
    cards_data=[
        ("SỔ NỢ THỜI GIAN GIAO LỘ D_d(J)", [
            ("Thiệt hại các hướng trực giao", "Các luồng xe bị cưỡng bức dừng đèn đỏ đột ngột trong suốt thời gian ưu tiên Delta_t_preempt."),
            ("Tích lũy công nợ toán học", "Hệ thống ghi nhận chính xác từng giây bị tước quyền ưu tiên vào biến nợ D_d(J)."),
            ("Tính minh bạch điều hành", "Đảm bảo mọi hướng giao thông bị ảnh hưởng đều được hệ thống ghi nhận công bằng.")
        ]),
        ("XÁC ĐỊNH HƯỚNG BỊ NỢ LỚN NHẤT d*", [
            ("Thuật toán tìm d*", "Quét toàn bộ các nhánh giao cắt để tìm hướng có chỉ số công nợ tích lũy cao nhất d*."),
            ("Đánh giá áp lực hàng đợi", "Kết hợp giữa công nợ thời gian và số lượng xe đang bị dồn ứ thực tế tại nhánh d*."),
            ("Thứ tự ưu tiên trả nợ", "Nhánh d* được quyền ưu tiên nhận thời gian bù đầu tiên ngay sau khi xe khẩn cấp rời đi.")
        ]),
        ("CẤP THỜI LƯỢNG BÙ t_comp (MAX 15.0S)", [
            ("Thời lượng đền bù", "Được tính bằng min(D_d*, 15.0s) để tránh việc bù quá mức gây sốc ngược chu kỳ."),
            ("Giải tỏa ùn ứ tức thì", "Nhanh chóng xả sạch hàng đợi tồn đọng phát sinh trong thời gian phục vụ xe ưu tiên."),
            ("Khôi phục cân bằng 1-2 chu kỳ", "Toàn bộ mạng lưới nút giao trở lại trạng thái lưu thông bình thường chỉ sau 1 đến 2 chu kỳ đèn.")
        ])
    ]
)

# ==============================================================================
# SLIDE 19: MÔ PHỎNG VI MÔ: MẠNG ARTERIAL GRID (3x2)
# ==============================================================================
s19 = prs.slides.add_slide(blank_layout)
set_bg(s19)
add_header(s19, "08 // MÔ PHỎNG VI MÔ SUMO", "Mô Phỏng Vi Mô: Mạng Lưới Đô Thị Arterial Grid 3x2", "Kiểm thử điều phối đèn đa nút giao liên hoàn và giải quyết xung đột rẽ trái được bảo hộ (Dual-Ring).")

# Left (48%): Architecture Details
card_w19 = Inches(5.4)
cards19 = [
    ("CẤU TRÚC HÌNH HỌC MẠNG LƯỚI", [
        ("Quy mô 6 nút giao liên hoàn", "Gồm 3 trục dọc và 2 trục ngang kết nối chặt chẽ theo cấu trúc mạng lưới bàn cờ."),
        ("Khoảng cách liên nút 300m", "Cự ly đô thị điển hình, dễ phát sinh hiện tượng sóng dừng và nghẽn lan truyền."),
        ("Làn xe và phân luồng", "Mỗi nhánh gồm 2 làn đi thẳng và 1 làn rẽ trái chuyên biệt (Dedicated Left-Turn Bay).")
    ]),
    ("CƠ CHẾ ĐIỀU PHỐI VÀ KIỂM THỬ", [
        ("Dual-Ring Permissive Left Turn", "Mô phỏng chân thực chu kỳ 8 pha tín hiệu đèn chuẩn NEMA quốc tế."),
        ("Kiểm thử giải thuật Leftover-Queue", "Chứng minh khả năng san sẻ thời gian xanh giữa các nút lân cận theo thời gian thực."),
        ("Khử xung đột nghẽn nghẽn dây chuyền", "Giữ vững thông lượng trục chính ngay cả khi lưu lượng giờ cao điểm tăng 200%.")
    ])
]

y_pos19 = Inches(1.8)
for title, items in cards19:
    card = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos19, card_w19, Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos19, card_w19, Inches(0.4))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s19.shapes.add_textbox(Inches(0.95), y_pos19 + Inches(0.06), card_w19 - Inches(0.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s19.shapes.add_textbox(Inches(0.95), y_pos19 + Inches(0.48), card_w19 - Inches(0.3), Inches(1.6))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(4)
    y_pos19 += Inches(2.4)

# Right (52%): Network Map
art_img_path = "docs/images/arterial-grid.png"
if os.path.exists(art_img_path):
    pic = s19.shapes.add_picture(art_img_path, Inches(6.5), Inches(1.8), width=Inches(6.033), height=Inches(4.6))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s19.shapes.add_textbox(Inches(6.5), Inches(6.5), Inches(6.033), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Sơ đồ mạng lưới: 6 nút đèn tín hiệu phối hợp đa nút giao (Arterial Grid 3x2)"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s19, 19)

# ==============================================================================
# SLIDE 20: MÔ PHỎNG VI MÔ: MẠNG HIGHWAY CORRIDOR
# ==============================================================================
s20 = prs.slides.add_slide(blank_layout)
set_bg(s20)
add_header(s20, "08 // MÔ PHỎNG VI MÔ SUMO", "Mô Phỏng Vi Mô: Mạng Tuyến Cao Tốc Highway Corridor", "Hành lang cao tốc 3 làn dài 3.2 km tích hợp 2 trạm kiểm soát nhập làn ALINEA Ramp Metering.")

# Left (48%): Architecture Details
cards20 = [
    ("ĐẶC ĐIỂM HÌNH HỌC TUYẾN CAO TỐC", [
        ("Chiều dài hành lang 3.2 km", "Tuyến cao tốc thẳng tốc độ thiết kế 100 km/h với 3 làn xe tiêu chuẩn mỗi chiều."),
        ("2 Nhánh nối On-Ramp", "Hai nhánh nhập làn cách nhau 1.2 km, mô phỏng các điểm nghẽn hòa dòng điển hình."),
        ("Làn tăng tốc (Acceleration Lane)", "Chiều dài làn tăng tốc 250m cho phép xe đạt vận tốc an toàn trước khi hòa dòng.")
    ]),
    ("HIỆU QUẢ KIỂM SOÁT HÒA DÒNG ALINEA", [
        ("Chống sụp đổ thông lượng", "Loại bỏ hoàn toàn hiện tượng Capacity Drop tại điểm nghẽn cổ chai."),
        ("Vận tốc hành lang ổn định", "Giữ vận tốc trung bình trên tuyến chính luôn duy trì trên mức 75 km/h."),
        ("Kiểm định cơ chế Spillback", "Chứng minh khả năng tự xả trạm khi lượng xe chờ trên nhánh nối vượt ngưỡng 30 xe.")
    ])
]

y_pos20 = Inches(1.8)
for title, items in cards20:
    card = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos20, card_w19, Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos20, card_w19, Inches(0.4))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s20.shapes.add_textbox(Inches(0.95), y_pos20 + Inches(0.06), card_w19 - Inches(0.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s20.shapes.add_textbox(Inches(0.95), y_pos20 + Inches(0.48), card_w19 - Inches(0.3), Inches(1.6))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(4)
    y_pos20 += Inches(2.4)

# Right (52%): Corridor Map
hw_img_path = "docs/images/highway-corridor.png"
if os.path.exists(hw_img_path):
    pic = s20.shapes.add_picture(hw_img_path, Inches(6.5), Inches(2.0), width=Inches(6.033), height=Inches(4.2))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s20.shapes.add_textbox(Inches(6.5), Inches(6.4), Inches(6.033), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Sơ đồ hành lang cao tốc: 3 làn xe chính và 2 vị trí đèn Metering kiểm soát nhập làn"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s20, 20)

# ==============================================================================
# SLIDE 21: MÔ PHỎNG VI MÔ: MẠNG KẾT HỢP ĐÔ THỊ - CAO TỐC
# ==============================================================================
s21 = prs.slides.add_slide(blank_layout)
set_bg(s21)
add_header(s21, "08 // MÔ PHỎNG VI MÔ SUMO", "Mô Phỏng Vi Mô: Mạng Kết Hợp Đô Thị & Cao Tốc", "Mô hình tích hợp liên vùng kết nối liền mạch từ mạng lưới đường phố đô thị ra trục cao tốc liên vùng.")

cards21 = [
    ("TÍCH HỢP ĐÔ THỊ - CAO TỐC LIÊN VÙNG", [
        ("Mạng lưới phức tạp toàn diện", "Kết hợp trực tiếp mạng Arterial Grid 3x2 với hành lang cao tốc qua các tuyến đường gom."),
        ("Dòng xe hỗn hợp đa cấp độ", "Mô phỏng cả xe cá nhân di chuyển nội đô và xe tải nặng lưu thông đường trường."),
        ("Kiểm thử tải diện rộng (Stress Test)", "Đo lường độ ổn định của hệ thống dưới áp lực 5,500 phương tiện xuất hiện đồng thời.")
    ]),
    ("ĐIỀU PHỐI ĐỒNG BỘ ĐA TẦNG (HIERARCHICAL)", [
        ("Đồng bộ cấp cao", "Thuật toán Leftover-Queue trong phố kết hợp ăn khớp với thuật toán ALINEA ngoài cao tốc."),
        ("Ngăn tắc nghẽn xuyên vùng", "Không để dòng xe nhập cao tốc làm nghẽn nội đô và ngược lại."),
        ("Cơ sở dữ liệu thực nghiệm chuẩn", "Cung cấp môi trường kiểm thử End-to-End sát thực tế nhất cho bộ điều hành AI.")
    ])
]

y_pos21 = Inches(1.8)
for title, items in cards21:
    card = s21.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos21, card_w19, Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s21.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos21, card_w19, Inches(0.4))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s21.shapes.add_textbox(Inches(0.95), y_pos21 + Inches(0.06), card_w19 - Inches(0.3), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s21.shapes.add_textbox(Inches(0.95), y_pos21 + Inches(0.48), card_w19 - Inches(0.3), Inches(1.6))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(4)
    y_pos21 += Inches(2.4)

comb_img_path = "docs/images/combined-network.png"
if os.path.exists(comb_img_path):
    pic = s21.shapes.add_picture(comb_img_path, Inches(6.5), Inches(2.0), width=Inches(6.033), height=Inches(4.2))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s21.shapes.add_textbox(Inches(6.5), Inches(6.4), Inches(6.033), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Sơ đồ mạng tích hợp: Kết nối toàn diện từ mạng lưới đường phố đô thị ra trục cao tốc"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s21, 21)

# ==============================================================================
# SLIDE 22: NỀN TẢNG BACKEND: FASTAPI WEBSOCKET & KHỬ NGHẼN TCP
# ==============================================================================
s22 = prs.slides.add_slide(blank_layout)
set_bg(s22)
add_header(s22, "09 // NỀN TẢNG FULL-STACK", "Nền Tảng Backend: FastAPI WebSocket Engine", "Khử triệt để TCP Backpressure và tối ưu hóa nén JSON payload phục vụ truyền phát dữ liệu 10 Hz.")

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

card_w22 = Inches(3.75)
for i, (ctitle, items) in enumerate(be_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s22.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), card_w22, Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s22.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), card_w22, Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s22.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), card_w22 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s22.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), card_w22 - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)

add_footer(s22, 22)

# ==============================================================================
# SLIDE 23: GIAO DIỆN VẬN HÀNH: NEXT.JS 14 DASHBOARD & SIMULATION LAB
# ==============================================================================
s23 = prs.slides.add_slide(blank_layout)
set_bg(s23)
add_header(s23, "09 // NỀN TẢNG FULL-STACK", "Giao Diện Vận Hành: Next.js 14 Dashboard & Simulation Lab", "Bản đồ nhiệt động học thời gian thực và phòng thí nghiệm đua chính sách đối đầu (Fixed vs Adaptive).")

# Left (58%): Dashboard Screenshot
dash_img_path = "docs/images/dashboard.png"
if os.path.exists(dash_img_path):
    pic = s23.shapes.add_picture(dash_img_path, Inches(0.8), Inches(1.6), width=Inches(6.6), height=Inches(4.7))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s23.shapes.add_textbox(Inches(0.8), Inches(6.4), Inches(6.6), Inches(0.4))
    p = cap.text_frame.paragraphs[0]
    p.text = "Hình: Giao diện Dashboard điều hành: Bản đồ nhiệt trực tiếp, thông số từng nút giao và telemetry vi mô"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

# Right (42%): Key Capabilities
cards23 = [
    ("BẢN ĐỒ NHIỆT ĐỘNG HỌC CANVAS", [
        "Render mượt mà hàng nghìn xe và pha tín hiệu đèn ở tốc độ 60 FPS.",
        "Màu sắc trực quan thể hiện mức độ ùn ứ theo thời gian thực (Xanh - Vàng - Đỏ)."
    ]),
    ("PHÒNG THÍ NGHIỆM ĐUA CHÍNH SÁCH (LAB)", [
        "Chạy song song 2 phiên mô phỏng đối đầu (Fixed-Time vs Adaptive) cùng seed ngẫu nhiên 42.",
        "Quan sát trực tiếp sự phân hóa hàng đợi và thời gian dừng chờ tích lũy ngay trên màn hình."
    ]),
    ("ĐIỀU HÀNH VÀ CAN THIỆP THỦ CÔNG", [
        ("Nút bấm khẩn cấp", "Kích hoạt làn sóng xanh EV cưỡng bức bằng một cú nhấp chuột."),
        ("Tùy biến tham số", "Điều chỉnh linh hoạt các ngưỡng g_min, g_max và hệ số ALINEA trực tiếp.")
    ])
]

y_pos23 = Inches(1.6)
for title, bts in cards23:
    tb = s23.shapes.add_textbox(Inches(7.7), y_pos23, Inches(4.833), Inches(0.35))
    p = tb.text_frame.paragraphs[0]
    p.text = title
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    db = s23.shapes.add_textbox(Inches(7.7), y_pos23 + Inches(0.35), Inches(4.833), Inches(1.1))
    tf = db.text_frame
    tf.word_wrap = True
    for idx, b in enumerate(bts):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        if isinstance(b, tuple):
            p.text = f"• {b[0]}: {b[1]}"
        else:
            p.text = f"• {b}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_SLATE
        if idx > 0:
            p.space_before = Pt(4)
    y_pos23 += Inches(1.65)

add_footer(s23, 23)

# ==============================================================================
# SLIDE 24: TRÍ TUỆ NHÂN TẠO: TRỢ LÝ GROQ LLM TRAFFIC COPILOT
# ==============================================================================
s24 = prs.slides.add_slide(blank_layout)
set_bg(s24)
add_header(s24, "09 // NỀN TẢNG FULL-STACK", "Trí Tuệ Nhân Tạo: Trợ Lý Groq LLM Traffic Copilot", "Tích hợp mô hình ngôn ngữ lớn Groq Llama 3 giải trình nguyên nhân chuyển pha và đưa ra khuyến nghị điều phối.")

copilot_cards = [
    ("GIẢI TRÌNH QUYẾT ĐỊNH CHUYỂN PHA", [
        ("Hạn chế của AI hộp đen", "Các giải thuật AI thường khó hiểu đối với cảnh sát giao thông và kỹ sư vận hành trung tâm."),
        ("Giải trình ngôn ngữ tự nhiên", "Groq LLM tự động tổng hợp telemetry và giải thích: 'Pha 2 được cấp thêm 8s vì lượng xe chờ tại nhánh Bắc chạm ngưỡng 25 xe.'"),
        ("Tăng độ tin cậy", "Giúp con người hiểu rõ cơ sở toán học và quyết định của hệ thống.")
    ]),
    ("CẢNH BÁO VÀ KHUYẾN NGHỊ ĐIỀU HÀNH", [
        ("Phát hiện tắc nghẽn bất thường", "Tự động phát hiện các điểm nghẽn cục bộ có nguy cơ gây tắc lan tỏa."),
        ("Đề xuất kịch bản ứng phó", "Đưa ra khuyến nghị: 'Nên kích hoạt xả trạm On-Ramp 1 để bảo vệ ngã tư B0 trong 5 phút tới.'"),
        ("Tốc độ xử lý siêu tốc", "Sử dụng chip LPU chuyên dụng của Groq cho thời gian phản hồi chỉ dưới 0.5 giây.")
    ]),
    ("TƯƠNG TÁC HỎI ĐÁP ĐIỀU HÀNH (CHAT INTERACTION)", [
        ("Tra cứu thông số thông minh", "Người vận hành có thể hỏi: 'Nút giao nào đang có thời gian chờ cao nhất?'"),
        ("Báo cáo ca trực tự động", "Tự động trích xuất bảng tổng kết lưu lượng và sự cố sau mỗi ca điều hành."),
        ("Cầu nối Con người - AI", "Biến hệ thống điều phối giao thông phức tạp thành một cộng sự thông minh dễ tương tác.")
    ])
]

card_w24 = Inches(3.75)
for i, (ctitle, items) in enumerate(copilot_cards):
    c_left = Inches(0.8 + i * (3.75 + 0.24))
    card = s24.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), card_w24, Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    strip = s24.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, Inches(1.8), card_w24, Inches(0.45))
    strip.fill.solid()
    strip.fill.fore_color.rgb = TINT_BAR
    strip.line.fill.background()
    
    tb = s24.shapes.add_textbox(c_left + Inches(0.12), Inches(1.9), card_w24 - Inches(0.24), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = ctitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    tb_b = s24.shapes.add_textbox(c_left + Inches(0.15), Inches(2.4), card_w24 - Inches(0.3), Inches(3.9))
    tf = tb_b.text_frame
    tf.word_wrap = True
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.text = f"• {lead}: {body}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = INK_NAVY
        if idx > 0:
            p.space_before = Pt(8)

add_footer(s24, 24)

# ==============================================================================
# SLIDE 25: TIÊU CHUẨN ĐO KIỂM HIGHWAY CAPACITY MANUAL (HCM)
# ==============================================================================
create_formula_slide(
    slide_num=25,
    kicker="10 // ĐO KIỂM THỰC NGHIỆM",
    title="Tiêu Chuẩn Đo Kiểm Highway Capacity Manual (HCM)",
    subtitle="Quy chuẩn đánh giá năng lực thông hành quốc tế dựa trên Control Delay và Throughput mạng lưới.",
    formula_key="hcm",
    eq_label="[Eq. 13]",
    cards_data=[
        ("THỜI GIAN TRỄ ĐIỀU KHIỂN (CONTROL DELAY d_i)", [
            ("Thời gian hao phí thực tế", "Đo chênh lệch giữa thời gian lưu lại ngã tư t_dwell và thời gian lưu thông tự do t_free_flow."),
            ("Khu vực đo đạc 50 mét", "Ghi nhận toàn bộ thời gian phương tiện giảm tốc, dừng chờ và tăng tốc trở lại khi qua nút."),
            ("Thước đo chất lượng dịch vụ (LOS)", "Phân hạng chất lượng nút giao từ A (trễ < 10s) đến F (trễ > 80s, sụp đổ giao thông).")
        ]),
        ("THÔNG LƯỢNG MẠNG LƯỚI (THROUGHPUT)", [
            ("Số chuyến đi hoàn thành", "Đo lường số lượng phương tiện N_completed thoát khỏi mạng lưới thành công trên mỗi phút."),
            ("Đại diện cho năng lực thoát xe", "Phản ánh trực tiếp khả năng giải tỏa ách tắc của toàn bộ hệ thống."),
            ("Chuẩn hóa thời gian mô phỏng", "Chia cho thời gian chạy thực nghiệm T_sim đảm bảo số liệu so sánh khách quan tuyệt đối.")
        ]),
        ("KHUNG THỰC NGHIỆM ĐUA CHÍNH SÁCH (RACE FRAMEWORK)", [
            ("Cùng hạt giống ngẫu nhiên (Seed 42)", "Cả 2 mô hình chạy đối đầu cùng xuất hiện lượng xe và thời điểm xe đến giống hệt nhau 100%."),
            ("3 Kịch bản nhu cầu khắt khe", "Cân bằng (Balanced), Lệch tải (Asymmetric), và Quá tải cực hạn (Extreme)."),
            ("Quy mô 5,500 phương tiện", "Đảm bảo độ tin cậy thống kê cao theo tiêu chuẩn các bài báo khoa học hàng đầu.")
        ])
    ]
)

# ==============================================================================
# SLIDE 26: KẾT QUẢ THỰC NGHIỆM ĐỐI ĐẦU: ADAPTIVE AI VS BASELINE
# ==============================================================================
s26 = prs.slides.add_slide(blank_layout)
set_bg(s26)
add_header(s26, "10 // ĐO KIỂM THỰC NGHIỆM", "Kết Quả Thực Nghiệm Đối Đầu: Adaptive AI vs Fixed-Time", "Đánh giá định lượng trên 5,500 phương tiện: Adaptive AI giảm tới 54% thời gian chờ và tăng 28% thông lượng.")

# Left (48%): 3 Hero Metric Cards
metrics_s26 = [
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

y_pos26 = Inches(1.8)
for pct, sc_title, details in metrics_s26:
    card = s26.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y_pos26, Inches(5.4), Inches(1.4))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_WHITE
    card.line.color.rgb = BORDER_BOX
    card.line.width = Pt(0.75)
    
    # Big Number on left of card
    nb = s26.shapes.add_textbox(Inches(1.0), y_pos26 + Inches(0.2), Inches(1.8), Inches(0.9))
    p = nb.text_frame.paragraphs[0]
    p.text = pct
    p.font.name = FONT_HEADING
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    # Text on right of card
    tb = s26.shapes.add_textbox(Inches(2.8), y_pos26 + Inches(0.18), Inches(3.2), Inches(1.1))
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
        
    y_pos26 += Inches(1.6)

# Right (52%): Benchmark Chart
wait_img_path = "docs/images/waiting-time.png"
if os.path.exists(wait_img_path):
    pic = s26.shapes.add_picture(wait_img_path, Inches(6.5), Inches(1.8), width=Inches(6.033), height=Inches(4.6))
    pic.line.color.rgb = BORDER_BOX
    pic.line.width = Pt(1.0)
    cap = s26.shapes.add_textbox(Inches(6.5), Inches(6.5), Inches(6.033), Inches(0.35))
    p = cap.text_frame.paragraphs[0]
    p.text = "Biểu đồ phân phối thời gian chờ: Thuật toán Adaptive AI giải phóng mạng lưới nhanh hơn tới 54%"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = INK_SLATE

add_footer(s26, 26)

# ==============================================================================
# SLIDE 27: MA TRẬN TIẾN ĐỘ 100% & ĐỊNH HƯỚNG 3 HORIZON
# ==============================================================================
s27 = prs.slides.add_slide(blank_layout)
set_bg(s27)
add_header(s27, "11 // TỔNG KẾT & LỘ TRÌNH", "Ma Trận Nghiệm Thu 100% Khối Lõi & Lộ Trình Chiến Lược", "Nghiệm thu toàn bộ 8 khối công nghệ cốt lõi và định hình lộ trình mở rộng hệ thống trong giai đoạn tiếp theo.")

# Left (50%): Completed Core Modules
tb27_l = s27.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.6), Inches(0.35))
p = tb27_l.text_frame.paragraphs[0]
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

db27_l = s27.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(5.6), Inches(4.7))
tf = db27_l.text_frame
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

# Vertical hairline divider
div27 = s27.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.6), Inches(0.015), Inches(5.1))
div27.fill.solid()
div27.fill.fore_color.rgb = HAIRLINE
div27.line.fill.background()

# Right (50%): Strategic Roadmap Horizons
tb27_r = s27.shapes.add_textbox(Inches(6.9), Inches(1.6), Inches(5.633), Inches(0.35))
p = tb27_r.text_frame.paragraphs[0]
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

y_pos27 = Inches(2.1)
for htitle, hdesc in horizons:
    tb = s27.shapes.add_textbox(Inches(6.9), y_pos27, Inches(5.633), Inches(0.3))
    p = tb.text_frame.paragraphs[0]
    p.text = htitle
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = INK_NAVY
    
    db = s27.shapes.add_textbox(Inches(6.9), y_pos27 + Inches(0.32), Inches(5.633), Inches(1.0))
    tf_d = db.text_frame
    tf_d.word_wrap = True
    p = tf_d.paragraphs[0]
    p.text = hdesc
    p.font.name = FONT_BODY
    p.font.size = Pt(9.8)
    p.font.color.rgb = INK_SLATE
    
    y_pos27 += Inches(1.55)

add_footer(s27, 27)

# ==============================================================================
# SAVE PRESENTATION
# ==============================================================================
output_pptx = "d:/ai-traffic-management-system/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
prs.save(output_pptx)
print(f"Presentation saved successfully with 27 dedicated slides to: {output_pptx}")

artifact_path = "C:/Users/Admin/.gemini/antigravity/brain/0bd16718-e31e-4a30-ae40-69e42323aea0/Bao_Cao_Tien_Do_AI_Traffic_Management.pptx"
shutil.copy2(output_pptx, artifact_path)
print(f"Copy saved to artifact directory: {artifact_path}")
