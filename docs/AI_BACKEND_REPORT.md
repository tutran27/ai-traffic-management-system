# BÁO CÁO KỸ THUẬT CỐT LÕI BACKEND AI (AI BACKEND TECHNICAL REPORT)
**Hệ thống Điều phối Giao thông Đô thị Thông minh (Intelligent Traffic Management System)**

---

## 1. TỔNG QUAN KIẾN TRÚC BACKEND AI

Hệ thống Backend AI được thiết kế theo mô hình điều khiển phân tầng (hierarchical & distributed control), kết hợp giữa **Thị giác máy tính (Computer Vision - Perception)** và **Điều khiển tối ưu thích nghi (Adaptive Control & Feedback Policies)**.

```
+-----------------------------------------------------------------------------------+
|                            PERCEPTION LAYER (CV PIPELINE)                         |
|  - YOLOv11m Multi-Class Object Detection (7 classes, incl. Emergency)             |
|  - ByteTrack Multi-Object Tracking (Kalman Filter + 2-Stage Data Association)     |
|  - Camera Auto-Calibration & Ground-Plane Homography Matrix H                     |
|  - Metric Speed Estimation & Multi-Lane Stationary Queue Extraction               |
+-----------------------------------------------------------------------------------+
                                          |
                                          v (Queues, Speeds, EV Detection)
+-----------------------------------------------------------------------------------+
|                             DECISION & POLICY LAYER                               |
|  [Arterial Network]                  [Freeway Ramps]           [Emergency Module]  |
|  - Leftover-Queue Adaptive Policy    - ALINEA Integral Law     - Signal Preemption |
|  - EMA Queue Smoothing               - Queue Spillback Override- Starvation Debt   |
|  - Constrained Redistribution        - Dual-Loop Metering        Compensation      |
+-----------------------------------------------------------------------------------+
                                          |
                                          v (SignalCommands: duration_s, phase_index)
+-----------------------------------------------------------------------------------+
|                        EXECUTION & TRAFFIC SIMULATION LAYER                       |
|  - SUMO Microscopic Engine via TraCI Socket Protocol                              |
|  - HCM (Highway Capacity Manual) Control Delay & Network Throughput Trackers      |
|  - Async Non-blocking WebSocket Broadcast with Backpressure Guards               |
+-----------------------------------------------------------------------------------+
```

---

## 2. THỊ GIÁC MÁY TÍNH & PHÂN TÍCH TỆP TRỌNG SỐ HUẤN LUYỆN (YOLOv11m & CV PIPELINE)

### 2.1. Phân tích chi tiết tệp trọng số `best.pt` (Checkpoint Deep Inspection)

Tệp trọng số [`packages/cv-pipeline/models/best.pt`](file:///d:/ai-traffic-management-system/packages/cv-pipeline/models/best.pt) có dung lượng **$40.5\text{ MB}$**, là điểm kiểm tra tốt nhất (best checkpoint) thu được từ tiến trình huấn luyện mô hình thị giác máy tính YOLOv11m trên môi trường GPU CUDA.

#### A. Kiến trúc mạng nơ-ron (Model Architecture)
- **Kiến trúc cốt lõi:** YOLOv11m (`scale: m` - Medium), phát triển trên nền tảng Ultralytics v8.4.45.
- **Tổng số lượng tham số:** **$20,058,405$ tham số** ($\approx 20.06\text{M}$ parameters), $0$ tham số đóng băng tại inference.
- **Đặc trưng Backbone:** Tích hợp khối tích chập chuẩn hóa $\text{Conv}(3\times 3, s=2)$, các mô-đun dư cải tiến $\text{C3k2}$, khối trích xuất ngữ cảnh không gian kim tự tháp $\text{SPPF}$ (Spatial Pyramid Pooling - Fast) và cơ chế chú ý tự động đa tỷ lệ $\text{C2PSA}$ (Cross Stage Partial with Pointwise Spatial Attention).
- **Đặc trưng Neck & Head:** Cấu trúc PANet (Path Aggregation Network) kết hợp các tầng Upsample, Concat và Decoupled Detection Head độc lập giữa phân loại (classification) và hồi quy vị trí hộp bao (bounding box regression).

#### B. Không gian nhãn phân loại (7 Traffic Classes)
Mô hình phân loại chính xác $K = 7$ lớp đối tượng phương tiện giao thông đường bộ:
$$\mathcal{C} = \{0: \text{'car'}, \; 1: \text{'ambulance'}, \; 2: \text{'bus'}, \; 3: \text{'truck'}, \; 4: \text{'police\_car'}, \; 5: \text{'fire\_truck'}, \; 6: \text{'bike'}\}$$

Trong đó, 3 lớp phương tiện ưu tiên gồm `ambulance`, `police_car`, và `fire_truck` đóng vai trò đầu vào kích hoạt trực tiếp cho thuật toán chiếm dụng pha xanh khẩn cấp (**Signal Preemption Module**).

#### C. Thông số siêu tham số huấn luyện (Extracted Hyperparameters)
Trích xuất từ từ điển `train_args` lưu trong checkpoint:

| Siêu tham số (Hyperparameter) | Giá trị thiết lập | Diễn giải kỹ thuật |
| :--- | :--- | :--- |
| **Epochs** | $100$ | Số lượng chu kỳ huấn luyện toàn bộ tập dữ liệu |
| **Batch Size** | $64$ | Kích thước batch huấn luyện song song |
| **Image Size (`imgsz`)** | $640 \times 640$ | Độ phân giải đầu vào chuẩn hóa |
| **Optimizer** | `auto` (SGD / AdamW) | Tự động thích ứng tối ưu gradient |
| **Base Learning Rate ($\eta_0$)** | $0.01$ | Tốc độ học ban đầu |
| **Final Learning Rate ($\eta_f$)** | $0.01 \times \eta_0 = 10^{-4}$ | Tỷ lệ giảm tốc độ học cuối kỳ (`lrf = 0.01`) |
| **Momentum** | $0.937$ | Quán tính gradient trong tối ưu hóa |
| **Weight Decay** | $0.0005$ | Hệ số phạt điều hòa $L_2$ chống quá khớp |
| **Warmup Epochs** | $3.0$ | Số epoch khởi động mềm tốc độ học |
| **Warmup Momentum** | $0.8$ | Quán tính gradient giai đoạn khởi động |
| **Mixed Precision (`amp`)** | `True` (FP16) | Tăng tốc độ tính toán phần cứng và tiết kiệm VRAM |
| **Box Loss Gain ($\lambda_{\text{box}}$)** | $7.5$ | Trọng số phạt sai số vị trí hộp bao |
| **Class Loss Gain ($\lambda_{\text{cls}}$)** | $0.5$ | Trọng số phạt phân loại sai nhãn |
| **DFL Loss Gain ($\lambda_{\text{dfl}}$)** | $1.5$ | Trọng số hàm mất mát phân phối tiêu cự |
| **Mosaic Augmentation** | $1.0$ (tắt ở 10 epoch cuối) | Ghép 4 ảnh tăng cường bối cảnh đa quy mô |
| **Random Erasing** | $0.4$ | Xóa ngẫu nhiên vùng ảnh mô phỏng che khuất |
| **Color Jitter (HSV)** | $h=0.015, s=0.7, v=0.4$ | Biến thiên sắc độ, độ bão hòa, độ sáng |
| **Horizontal Flip** | $0.5$ | Lật gương ngang ngẫu nhiên $50\%$ |

#### D. Hiệu năng thực nghiệm tại điểm hội tụ (Validation Benchmark Results)
Kết quả kiểm định độc lập trên tập kiểm thử (Validation set) ghi nhận trong `train_metrics`:

$$\text{Precision } (P) = \mathbf{96.98\%} \quad (0.96978)$$
$$\text{Recall } (R) = \mathbf{89.67\%} \quad (0.89668)$$
$$\text{mAP}_{50} = \mathbf{94.91\%} \quad (0.94908)$$
$$\text{mAP}_{50-95} = \mathbf{86.49\%} \quad (0.86491)$$
$$\text{Fitness Score} = \mathbf{0.86491}$$

Các giá trị hàm mất mát kiểm định (Validation Losses) khi kết thúc epoch 100:
- $\mathcal{L}_{\text{box}} = 0.3908$
- $\mathcal{L}_{\text{cls}} = 0.2644$
- $\mathcal{L}_{\text{dfl}} = 0.8353$

---

### 2.2. Nguồn gốc & Cấu trúc tập dữ liệu huấn luyện (Training Dataset Specifications)

Tệp trọng số est.pt được huấn luyện trên **Bộ dữ liệu tổng hợp quang học độ chân thực cao (Synthetic Photorealistic Traffic Dataset)** được thiết kế và sinh tự động từ trình mô phỏng **CARLA Simulator (phiên bản 0.9.16)** kết hợp giải thuật cân bằng lớp chủ động.

#### A. Nguồn gốc dữ liệu & Quyết định chiến lược (Data Strategy Pivot)
- **Giai đoạn thử nghiệm ban đầu (Real-world Scraping):** Ban đầu, nhóm nghiên cứu thu thập dữ liệu ảnh từ các camera giao thông thực tế công cộng và gán nhãn thủ công qua nền tảng Roboflow. Mặc dù mô hình đạt $\text{mAP}_{50} = 0.931$ trên tập test cục bộ, nhưng khi đưa vào vận hành thử nghiệm trên camera đô thị thực tế, mô hình bộc lộ nhiều sai số nghiêm trọng do:
  1. *Lệch miền phân phối (Domain Mismatch):* Góc đặt camera, tiêu cự và méo quang học ở mỗi nút giao khác xa dữ liệu cào được.
  2. *Mất cân bằng lớp trầm trọng (Class Imbalance):* Tần suất xuất hiện ngoài thực tế của xe ưu tiên (xe cứu thương, xe cảnh sát, xe cứu hỏa) và xe buýt quá thấp so với ô tô con. Kết quả kiểm thử ban đầu cho thấy độ nhạy (Recall) của lớp xe buýt chỉ đạt vỏn vẹn **.9\%$**.
- **Chuyển dịch sang dữ liệu tổng hợp CARLA:** Để kiểm soát tuyệt đối nhãn dữ liệu và phân phối lớp, nhóm đã chuyển toàn bộ quy trình sang sinh dữ liệu tổng hợp quang học chân thực bằng CARLA Simulator. Mã nguồn kịch bản sinh dữ liệu và cấu hình kịch bản được quản lý tập trung tại kho lưu trữ mã nguồn mở:
  \text{Repository: } \href{https://github.com/OJayyusiO/dataset_capstone}{\texttt{github.com/OJayyusiO/dataset\_capstone}}

#### B. Quy mô và cấu trúc phân chia dữ liệu
- **Tập dữ liệu huấn luyện & thẩm định:** Bao gồm **,064$ ảnh chụp chuẩn hóa** độ phân giải cao ( \times 1080$), được gắn nhãn bounding box chuẩn định dạng YOLO với đầy đủ 7 lớp phương tiện.
- **Tập kiểm thử độc lập (Held-out Test Set):** Gồm **,979$ khung hình video** liên tục từ các kịch bản chạy mới hoàn toàn không nằm trong tập huấn luyện (chứa ,014$ lượt bounding box xuất hiện) để đánh giá cả năng lực nhận diện lẫn theo dõi đa đối tượng ByteTrack.
- **Không gian 7 nhãn phương tiện:**
  \mathcal{C} = \{\text{car}, \; \text{ambulance}, \; \text{bus}, \; \text{truck}, \; \text{police\_car}, \; \text{fire\_truck}, \; \text{bike}\}

#### C. Kỹ thuật trích xuất nhãn tự động đồng bộ (Automated 3D-to-2D Labeling)
Quy trình sinh dữ liệu loại bỏ hoàn toàn sai số do gán nhãn thủ công bằng giải thuật chiếu hình học tự động:
1. **Chế độ đồng bộ thời gian (Synchronous Tick-by-Tick Mode):** Khóa cứng bước thời gian mô phỏng trong CARLA ($\Delta t = 0.05\text{ s}$). Cảm biến máy ảnh ảo chỉ chụp sau khi toàn bộ trạng thái vật lý của phương tiện đã cập nhật hoàn tất, triệt tiêu độ trễ giữa khung hình và tọa độ.
2. **Chiếu hộp bao 3D sang 2D (3D Bounding Box Projection):** Sử dụng ma trận biến đổi không gian thực của CARLA WorldTransform để chiếu 8 đỉnh của hộp thể tích 3D bao quanh xe lên mặt phẳng ảnh pixel 2D của camera thông qua ma trận tham số nội $.
3. **Ngưỡng lọc che khuất (Occlusion Filtering):**
   Thiết lập ngưỡng hiển thị tối thiểu:
   \text{Visibility Ratio} \ge 0.15 \quad (15\%)
   Các phương tiện bị che khuất hơn \%$ diện tích bởi xe khác hoặc công trình ven đường sẽ tự động loại bỏ để tránh gây nhiễu cho mô hình học; ngược lại, các phương tiện lộ diện $\ge 15\%$ vẫn được giữ lại để huấn luyện mô hình khả năng nhận diện xe xếp hàng sát nhau trong giờ cao điểm.

#### D. Cân bằng phân phối lớp (Class Balancing via Spawn Ratios)
Để giải quyết bài toán lớp hiếm, hệ thống can thiệp trực tiếp vào bộ tạo sinh phương tiện (Traffic Manager Spawner):
- Tỷ lệ sinh của xe cảnh sát (police_car), xe buýt (us), và xe máy/xe đạp (ike) được tăng cường nhân tạo lên gấp ** - 3$ lần** tần suất tự nhiên.
- **Hiệu quả thực nghiệm:** Sau khi cân bằng, Recall của xe buýt tăng từ **.9\%$** lên **.0\%$**, độ nhạy của xe cứu thương và xe cảnh sát đều đạt trên \%$, đảm bảo hệ thống không bỏ sót bất kỳ xe ưu tiên nào khi tiếp cận giao lộ.

#### E. Đa dạng hóa môi trường & Bối cảnh quang học (Environmental Diversity)
Tập dữ liệu được chụp trên các bản đồ đô thị đa dạng của CARLA (Town03 ngã tư phức tạp, Town10HD thành phố hiện đại) và biến thiên qua **13 kịch bản thời tiết/ánh sáng** khác nhau:
- *Ban ngày:* ClearNoon, CloudyNoon, HardRainNoon.
- *Hoàng hôn & Chiều tà:* ClearSunset, WetSunset, SoftRainSunset, CloudySunset.
- *Ban đêm & Thời tiết xấu:* Midnight, WetMidnight, HardRainSunset.
Sự đa dạng này giúp mô hình thích nghi tốt với các điều kiện ánh sáng gắt, mặt đường ướt phản chiếu, và bóng tối ban đêm.

#### F. Môi trường phần cứng huấn luyện
Tiến trình huấn luyện 100 epoch được thực hiện trên cụm máy chủ đám mây GPU chuyên dụng:
- **Phần cứng:**  \times \text{NVIDIA L40S } (48\text{ GB VRAM})$.
- **Đường dẫn tệp cấu hình trên máy chủ:** /root/dataset_output/data.yaml (ghi nhận trong checkpoint metadata).
- **Thời gian hoàn tất:** Xấp xỉ .2$ giờ tính toán liên tục với FP16 Mixed Precision và bộ đệm RAM Cache.


---

### 2.3. Cơ chế toán học của hàm mất mát (Mathematical Loss Formulation)

Tổng hàm mất mát tối ưu hóa đa nhiệm trong quá trình huấn luyện:
$$\mathcal{L}_{\text{total}} = \lambda_{\text{box}} \mathcal{L}_{\text{box}} + \lambda_{\text{cls}} \mathcal{L}_{\text{cls}} + \lambda_{\text{dfl}} \mathcal{L}_{\text{dfl}} = 7.5 \cdot \mathcal{L}_{\text{box}} + 0.5 \cdot \mathcal{L}_{\text{cls}} + 1.5 \cdot \mathcal{L}_{\text{dfl}}$$

#### 1. Hồi quy vị trí Bounding Box ($\mathcal{L}_{\text{box}}$ - Complete IoU Loss)
Hệ thống sử dụng **CIoU Loss**, kết hợp sai số diện tích giao, khoảng cách tâm Euclidean và độ tương đồng tỷ lệ khung hình:
$$\mathcal{L}_{\text{box}} = 1 - \text{CIoU} = 1 - \left( \text{IoU} - \frac{\rho^2(\mathbf{b}, \mathbf{b}^{gt})}{c^2} - \alpha v \right)$$

trong đó:
- $\text{IoU} = \frac{|\mathbf{b} \cap \mathbf{b}^{gt}|}{|\mathbf{b} \cup \mathbf{b}^{gt}|}$
- $\rho(\mathbf{b}, \mathbf{b}^{gt})$: Khoảng cách Euclidean giữa tâm của hộp dự đoán và hộp nhãn thực tế.
- $c$: Đường chéo của hình chữ nhật nhỏ nhất bao quanh cả hai hộp.
- $v$: Tham số đo lường sự nhất quán về tỷ lệ co dãn hai chiều:
  $$v = \frac{4}{\pi^2} \left( \arctan\frac{w^{gt}}{h^{gt}} - \arctan\frac{w}{h} \right)^2$$
- $\alpha$: Hệ số bù phạt không cân bằng:
  $$\alpha = \frac{v}{(1 - \text{IoU}) + v}$$

#### 2. Phân loại đối tượng ($\mathcal{L}_{\text{cls}}$ - Binary Cross Entropy with Logits)
Áp dụng hàm mất mát nhị phân đa nhãn cho từng lớp độc lập:
$$\mathcal{L}_{\text{cls}} = -\frac{1}{N} \sum_{i=1}^{N} \sum_{k=1}^{K} \left[ y_{i,k} \log \sigma(p_{i,k}) + (1 - y_{i,k}) \log(1 - \sigma(p_{i,k})) \right]$$
với $K = 7$, $y_{i,k} \in \{0, 1\}$ là nhãn thực tế của lớp $k$, $p_{i,k}$ là giá trị logit đầu ra của mạng, và $\sigma(z) = \frac{1}{1 + e^{-z}}$.

#### 3. Phân phối biên hộp bao vi phân ($\mathcal{L}_{\text{dfl}}$ - Distribution Focal Loss)
Để mô hình học phân phối tọa độ liên tục thay vì giá trị điểm cứng (Dirac delta distribution), DFL tối ưu hóa xác suất tại hai cận nguyên gần nhất $y_l$ và $y_r$ ($y_l \le y \le y_r$):
$$\mathcal{L}_{\text{dfl}}(S_l, S_r) = - \left( (y_r - y) \log(S_l) + (y - y_l) \log(S_r) \right)$$
với $S_l = \frac{y_r - y}{y_r - y_l}$ và $S_r = \frac{y - y_l}{y_r - y_l}$ sinh ra từ lớp Softmax trên các bin khoảng cách.

#### 4. Lịch trình điều chỉnh tốc độ học (Warmup & Linear Decay)
- **Giai đoạn khởi động (Warmup - 3 epoch đầu):**
  $$\eta(t) = \eta_0 \cdot \frac{t}{N_{\text{warmup}}}, \quad \forall t \le 3.0$$
- **Giai đoạn suy giảm tuyến tính (Linear Decay - 97 epoch tiếp theo):**
  $$\eta(t) = \eta_0 \cdot \left[ 1 - \frac{t - N_{\text{warmup}}}{T_{\text{total}} - N_{\text{warmup}}} \cdot (1 - \text{lrf}) \right] = 0.01 \cdot \left[ 1 - \frac{t - 3}{97} \cdot 0.99 \right]$$

---

### 2.4. Hướng dẫn quy trình huấn luyện lại mô hình (Step-by-Step Training Guide)

Để tái huấn luyện (re-train) hoặc tinh chỉnh (fine-tune) mô hình với tập dữ liệu mới, quy trình được thực hiện chuẩn hóa như sau:

#### Bước 1: Chuẩn bị tệp cấu hình dữ liệu `data.yaml`
Tạo file cấu hình dữ liệu trỏ tới thư mục chứa ảnh và nhãn theo định dạng chuẩn YOLO:
```yaml
# data.yaml
path: /path/to/dataset_root
train: train/images
val: val/images
test: test/images

# Danh sách 7 lớp phương tiện đồng bộ với hệ thống
names:
  0: car
  1: ambulance
  2: bus
  3: truck
  4: police_car
  5: fire_truck
  6: bike

nc: 7
```

#### Bước 2: Huấn luyện bằng dòng lệnh Ultralytics CLI
Chạy lệnh trực tiếp trên terminal hỗ trợ GPU CUDA:
```bash
yolo task=detect mode=train \
  model=yolo11m.pt \
  data=data.yaml \
  epochs=100 \
  batch=64 \
  imgsz=640 \
  device=0 \
  workers=8 \
  cache=ram \
  amp=True \
  lr0=0.01 \
  lrf=0.01 \
  momentum=0.937 \
  weight_decay=0.0005 \
  box=7.5 \
  cls=0.5 \
  dfl=1.5 \
  mosaic=1.0 \
  close_mosaic=10 \
  name=traffic_yolo11m_run
```

#### Bước 3: Huấn luyện qua Python Script API
Khởi tạo và thực thi thông qua đoạn mã Python:
```python
from ultralytics import YOLO

def train_traffic_model():
    # 1. Tải trọng số gốc YOLOv11m đã pretrained trên COCO
    model = YOLO("yolo11m.pt")

    # 2. Bắt đầu quá trình huấn luyện
    results = model.train(
        data="data.yaml",
        epochs=100,
        batch=64,
        imgsz=640,
        device=0,               # Chỉ định GPU 0 (hoặc device="cpu")
        workers=8,
        cache="ram",            # Lưu cache RAM để đạt tốc độ nạp dữ liệu tối đa
        amp=True,               # Automatic Mixed Precision FP16
        optimizer="auto",
        lr0=0.01,
        lrf=0.01,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        mosaic=1.0,
        close_mosaic=10,        # Tắt mosaic ở 10 epoch cuối để tinh chỉnh biên hộp
        name="traffic_yolo11m_run",
    )

    # 3. Đánh giá chất lượng sau huấn luyện
    metrics = model.val()
    print(f"Validation mAP@50: {metrics.box.map50:.4f}")
    print(f"Validation mAP@50-95: {metrics.box.map:.4f}")

if __name__ == "__main__":
    train_traffic_model()
```

#### Bước 4: Tích hợp tệp trọng số xuất xưởng vào hệ thống
Sau khi hoàn tất $100$ epoch, file trọng số tối ưu nhất được lưu tự động tại `runs/detect/traffic_yolo11m_run/weights/best.pt`. Copy đè file này vào thư mục:
```bash
cp runs/detect/traffic_yolo11m_run/weights/best.pt packages/cv-pipeline/models/best.pt
```

---

### 2.5. Theo dõi phương tiện liên tục (ByteTrack Multi-Object Tracker)
Sử dụng **ByteTrack** để duy trì danh tính phương tiện ($\text{track\_id}$) liên tục qua các khung hình, không bị gián đoạn do che khuất (occlusion).

1. **Bộ lọc Kalman (State Space Model):**
   Trạng thái chuyển động của hộp bao tại khung hình $t$:
   $$\mathbf{x}_t = [x_c, y_c, a, h, \dot{x}_c, \dot{y}_c, \dot{a}, \dot{h}]^T$$
   trong đó $(x_c, y_c)$ là tâm bbox, $a = \frac{w}{h}$ là tỷ lệ khung hình, $h$ là chiều cao, và các biến đạo hàm thể hiện vận tốc tương ứng.
   
   Phương trình dự báo trạng thái:
   $$\hat{\mathbf{x}}_{t|t-1} = \mathbf{F} \mathbf{x}_{t-1|t-1}$$
   $$\mathbf{P}_{t|t-1} = \mathbf{F} \mathbf{P}_{t-1|t-1} \mathbf{F}^T + \mathbf{Q}$$

2. **Cơ chế ghép nối 2 tầng (Two-Stage Data Association):**
   - **Tầng 1:** Ghép nối các detection có độ tin cậy cao ($c \ge \tau_{\text{high}} = 0.5$) với các track đang hoạt động bằng thuật toán Hungarian trên ma trận khoảng cách $1 - \text{IoU}(\mathbf{b}_{\text{pred}}, \mathbf{b}_{\text{det}})$.
   - **Tầng 2:** Các track chưa được ghép ở tầng 1 tiếp tục được đối sánh với các detection độ tin cậy thấp ($\tau_{\text{low}} \le c < \tau_{\text{high}}$) nhằm phục hồi đối tượng bị che khuất hoặc mờ nhòe do chuyển động.

---

### 2.6. Hiệu chuẩn hình học máy ảnh & Ma trận Homography (Perspective-to-World)
Để tính toán vận tốc thực tế (m/s) và vị trí thế giới thực của phương tiện từ tọa độ pixel 2D $(u, v)$, hệ thống tự động suy dẫn ma trận chuyển đổi đồng dạng Homography mặt đất $H \in \mathbb{R}^{3 \times 3}$.

1. **Ma trận tham số nội (Intrinsic Matrix $K$):**
   Từ độ phân giải $(W, H)$ và góc mở ngang $\text{FOV}$:
   $$f = \frac{W}{2 \tan\left(\frac{\text{FOV} \cdot \pi}{360}\right)}$$
   $$K = \begin{bmatrix} f & 0 & \frac{W}{2} \\ 0 & f & \frac{H}{2} \\ 0 & 0 & 1 \end{bmatrix}$$

2. **Ma trận quay hướng (Extrinsic Rotation Matrix $R$):**
   Từ các góc Euler gồm độ nghiêng (pitch $\theta$), hướng nhìn (yaw $\psi$), góc nghiêng ngang (roll $\phi$):
   $$R = R_z(\psi) R_y(\theta) R_x(\phi)$$
   $$R_z(\psi) = \begin{bmatrix} \cos\psi & -\sin\psi & 0 \\ \sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix}, \quad R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & -\sin\theta \\ 0 & 1 & 0 \\ \sin\theta & 0 & \cos\theta \end{bmatrix}, \quad R_x(\phi) = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\phi & -\sin\phi \\ 0 & \sin\phi & \cos\phi \end{bmatrix}$$

3. **Chiếu tia xuống mặt phẳng đất ($Z_w = 0$):**
   Với điểm pixel quy chiếu tại tiếp điểm bánh xe của bbox:
   $$u_{\text{ref}} = x_1 + 0.5(x_2 - x_1), \quad v_{\text{ref}} = y_1 + 0.85(y_2 - y_1)$$
   Vectơ tia trong hệ tọa độ camera:
   $$\mathbf{r}_c = K^{-1} \begin{bmatrix} u_{\text{ref}} \\ v_{\text{ref}} \\ 1 \end{bmatrix}$$
   Chuyển đổi sang hệ trục thế giới thực $\mathbf{r}_w = R \cdot \mathbf{r}_{\text{ue4}}$. Hệ số co giãn tia chạm mặt phẳng $Z = 0$:
   $$\lambda = -\frac{Z_{\text{cam}}}{r_{w, z}}$$
   Tọa độ thế giới thực $(X_w, Y_w)$:
   $$X_w = X_{\text{cam}} + \lambda r_{w, x}, \quad Y_w = Y_{\text{cam}} + \lambda r_{w, y}$$

4. **Ma trận Homography $H$:**
   Được xấp xỉ bằng phép biến đổi 4 điểm chuẩn hóa góc nhìn thấp của camera giao thông:
   $$\begin{bmatrix} X_w \\ Y_w \\ 1 \end{bmatrix} \sim H \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \begin{bmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & h_{33} \end{bmatrix} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$$
   $$(X_w, Y_w) = \left( \frac{h_{11}u + h_{12}v + h_{13}}{h_{31}u + h_{32}v + h_{33}}, \; \frac{h_{21}u + h_{22}v + h_{23}}{h_{31}u + h_{32}v + h_{33}} \right)$$

---

### 2.7. Ước lượng vận tốc & Nhận diện hàng đợi dừng (Speed & Queue Analytics)
1. **Vận tốc tức thời và làm mịn:**
   Độ dịch chuyển Euclidean trong không gian thực giữa khung hình $t$ và $t - \Delta k$:
   $$v_{\text{raw}}(t) = \frac{\sqrt{(X_w(t) - X_w(t - \Delta k))^2 + (Y_w(t) - Y_w(t - \Delta k))^2}}{\Delta k \cdot \Delta t}$$
   Làm mịn theo cửa sổ trượt $M = 5$ khung hình:
   $$\bar{v}(t) = \frac{1}{M} \sum_{m=0}^{M-1} v_{\text{raw}}(t - m)$$

2. **Tiêu chuẩn xác định xe dừng chờ trong hàng đợi (Queued Vehicle):**
   Một phương tiện được gắn nhãn đang chờ đèn đỏ khi vận tốc thỏa mãn:
   $$\bar{v}(t) < v_{\text{thresh}} = 2.0\text{ m/s } (7.2\text{ km/h}) \quad \text{liên tục trong } \tau_{\text{wait}} \ge 2.0\text{ s}$$
   Chiều dài hàng đợi $Q_d$ của hướng tiếp cận $d$ là tổng số xe thỏa mãn điều kiện nằm trong vùng tiếp cận (ROI polygon) của làn đó.

---

## 3. THUẬT TOÁN ĐIỀU KHIỂN TÍN HIỆU THÍCH NGHI (ADAPTIVE TRAFFIC CONTROL)

### 3.1. Thuật toán phân phối thời lượng xanh theo hàng đợi tồn dư (Leftover-Queue Actuated Policy)

Mục tiêu của thuật toán là điều tiết thời lượng pha đèn xanh $g_i$ của từng nhóm pha dựa trên số lượng xe chưa kịp giải tỏa khi pha đèn xanh kết thúc (thời điểm chớm vàng).

#### Bước 1: Làm mịn hàng đợi tồn dư (EMA Smoothing)
Khi kết thúc pha xanh của nhóm $i$, ghi nhận hàng đợi tồn dư $Q_i(k)$. Tại thời điểm kết thúc một chu kỳ đèn $k$, giá trị hàng đợi được lọc qua bộ lọc thông thấp làm mịn hàm mũ:
$$S_i(k) = \alpha \cdot Q_i(k) + (1 - \alpha) \cdot S_i(k-1)$$
trong đó $\alpha \in [0, 1]$ là hệ số làm mịn ($\alpha = 0.7$).

#### Bước 2: Phân loại trạng thái nhóm pha
Tập hợp các nhóm pha được chia làm hai tập rời rạc:
$$\mathcal{U} = \{i \mid S_i(k) > 0\} \quad (\text{Undersupplied - Nhóm thiếu thời gian xanh, còn xe tồn})$$
$$\mathcal{S} = \{i \mid S_i(k) \le 0\} \quad (\text{Satisfied - Nhóm thông thoáng, đã giải phóng hết xe})$$

#### Bước 3: Thuật toán tái phân phối ngân sách thời gian xanh
1. **Trường hợp toàn bộ mạng lưới thông thoáng ($\sum S_i \le 0$):**
   Hệ thống cho thời lượng xanh trôi dần về giá trị cấu hình cơ sở $g_{i,\text{base}}$:
   $$g_i(k+1) = g_i(k) + \operatorname{clamp}\left(g_{i,\text{base}} - g_i(k), -1.0\text{ s}, +1.0\text{ s}\right)$$

2. **Trường hợp có nhóm pha bị quá tải ($\mathcal{U} \neq \emptyset$ và $\mathcal{S} \neq \emptyset$):**
   - Tổng ngân sách thời gian tối đa có thể trích từ các nhóm thông thoáng $\mathcal{S}$:
     $$R_{\text{donatable}} = \sum_{j \in \mathcal{S}} \max\left(0, g_j(k) - g_{\min}\right)$$
     $$R = \min\left(R_{\max}, R_{\text{donatable}}\right)$$
     trong đó $R_{\max} = 12.0\text{ s}$, $g_{\min} = 10.0\text{ s}$.

   - Khấu trừ thời gian từ các nhóm thông thoáng:
     $$\Delta g_j = -\min\left(\frac{R}{|\mathcal{S}|}, g_j(k) - g_{\min}\right), \quad \forall j \in \mathcal{S}$$
     $$g_j(k+1) = \operatorname{round}\left(g_j(k) + \Delta g_j, 1\right)$$

   - Phân bổ ngân sách $R$ cho các nhóm thiếu hụt tỷ lệ thuận với tỷ trọng hàng đợi tồn dư:
     $$w_i = \frac{S_i(k)}{\sum_{m \in \mathcal{U}} S_m(k)}, \quad \forall i \in \mathcal{U}$$
     $$g_i(k+1) = \operatorname{round}\left(\min\left(g_{\max}, g_i(k) + R \cdot w_i\right), 1\right)$$
     với $g_{\max} = 50.0\text{ s}$.

3. **Trường hợp tất cả các hướng đều tắc ($\mathcal{S} = \emptyset$):**
   Tái cân bằng theo tỷ trọng nhu cầu thực tế:
   $$B = \sum_{i} g_i(k), \quad g_i(k+1) = \operatorname{clamp}\left(g_i(k) + \operatorname{clamp}\left(B \cdot \frac{S_i}{\sum S_m} - g_i(k), -\frac{R_{\max}}{N}, \frac{R_{\max}}{N}\right), g_{\min}, g_{\max}\right)$$

---

### 3.2. Thuật toán điều tiết dòng nhập làn cao tốc ALINEA (Local Ramp Metering)
Hệ thống sử dụng luật điều khiển hồi tiếp vòng kín tích phân **ALINEA (Papageorgiou et al., 1991)** để giữ mật độ giao thông trên tuyến chính cao tốc gần điểm năng lực tới hạn (capacity knee), ngăn chặn hiện tượng tắc nghẽn sụp đổ (traffic breakdown).

```
                      Highway Mainline (Downstream Sensors)
          =========================[ o_measured ]=======================>
                                       ^
                                       | Merge Point
                                   [TLS Meter] (Rate: r(k))
                                       |
                                  On-Ramp Queue
```

#### Luật điều khiển tích phân (Integral Control Law):
$$r(k) = \operatorname{clamp}\left(r(k-1) + K_R \cdot \left(o^* - \hat{o}(k)\right), r_{\min}, r_{\max}\right)$$

trong đó:
- $r(k)$: Tốc độ điều tiết cấp xe nhập làn tại chu kỳ $k$ $(\text{veh/h})$.
- $r(k-1)$: Tốc độ điều tiết ở chu kỳ trước đó.
- $K_R$: Hệ số khuếch đại tích phân ($K_R = 70.0\text{ veh/h/\%}$).
- $o^*$: Mật độ chiếm dụng mục tiêu lý tưởng ($o^* = 20\%$).
- $\hat{o}(k)$: Mật độ chiếm dụng đo lường trung bình trên các làn xuôi dòng (downstream occupancy):
  $$\hat{o}(k) = \frac{100}{|\mathcal{L}_{\text{down}}|} \sum_{l \in \mathcal{L}_{\text{down}}} \text{occupancy}_l(k)$$
- $[r_{\min}, r_{\max}]$: Giới hạn lưu lượng điều tiết ($r_{\min} = 200\text{ veh/h}$, $r_{\max} = 1200\text{ veh/h}$).

#### Quy đổi sang chu kỳ đèn và thời lượng đỏ:
$$T_{\text{cycle}}(k) = \frac{3600}{r(k)} \quad (\text{giây/xe})$$
$$t_{\text{red}}(k) = \max\left(0, T_{\text{cycle}}(k) - t_{\text{green}} - t_{\text{yellow}}\right)$$
với $t_{\text{green}} = 2.0\text{ s}$, $t_{\text{yellow}} = 1.0\text{ s}$.

#### Cơ chế chống tràn nhánh nối (Ramp Queue Spillback Override):
Để ngăn dòng xe xếp hàng trên nhánh nối tràn ngược lại làm tê liệt đường gom đô thị:
$$\text{Nếu } Q_{\text{ramp}}(k) \ge Q_{\max} \; (30\text{ xe}) \implies r(k) = r_{\max} \quad (\text{Xả nhánh ưu tiên})$$

---

### 3.3. Thuật toán ưu tiên xe khẩn cấp & Bù trừ nghẽn (Emergency Vehicle Preemption & Compensation)

Khi xuất hiện phương tiện ưu tiên (xe cứu thương, cảnh sát, cứu hỏa):

1. **Kích hoạt quyền ưu tiên tuyệt đối (Preemption Trigger):**
   Xác định cạnh tiếp cận $e$ và nút giao đích $J$. Ngay lập tức ghi đè pha đèn hiện tại sang pha xanh phục vụ hướng di chuyển của xe khẩn cấp:
   $$\phi_J \leftarrow \phi_{\text{EV}}(e)$$

2. **Tích lũy nợ thời gian xanh (Starvation Debt Accumulation):**
   Trong suốt khoảng thời gian $\Delta t_{\text{preempt}}$ mà hướng ưu tiên chiếm dụng nút giao, các hướng trực giao bị cắt quyền ưu tiên ($\mathcal{D}_{\text{starved}}$) được ghi nhận công nợ thời gian:
   $$D_d(J) \leftarrow D_d(J) + \Delta t_{\text{preempt}}, \quad \forall d \in \mathcal{D}_{\text{starved}}$$

3. **Luật bù trừ công nợ sau ưu tiên (Post-Preemption Debt Payback):**
   Ngay sau khi phương tiện khẩn cấp vượt qua nút giao, hệ thống chuyển sang chế độ bù trừ cho hướng chịu thiệt hại lớn nhất:
   $$d^* = \arg\max_{d} D_d(J)$$
   $$t_{\text{comp}} = \min\left(D_{d^*}(J), 15.0\text{ s}\right)$$
   Pha đèn $d^*$ được cấp thêm thời lượng $t_{\text{comp}}$, sau đó giảm trừ nợ tương ứng:
   $$D_{d^*}(J) \leftarrow D_{d^*}(J) - t_{\text{comp}}$$

---

## 4. CÁC CHỈ SỐ ĐÁNH GIÁ HIỆU NĂNG GIAO THÔNG (TRAFFIC BENCHMARK METRICS)

Hệ thống đo lường hiệu quả điều tiết giao thông theo chuẩn của **Highway Capacity Manual (HCM)**.

### 4.1. Độ trễ điều khiển (HCM Control Delay)
Đo lường thời gian hao phí thực tế của phương tiện khi đi qua nút giao đèn tín hiệu so với điều kiện lưu thông tự do lý tưởng:
$$d_{\text{control}} = t_{\text{dwell}} - t_{\text{free\_flow}}$$

Trong đó:
- Vùng giám sát có chiều dài $L_{\text{zone}} = 50\text{ m}$ trước vạch dừng.
- Thời gian lưu thông tự do chuẩn: $t_{\text{free\_flow}} = \frac{L_{\text{zone}}}{v_{\max}}$.
- Thời gian lưu trú thực tế $t_{\text{dwell}} = t_{\text{exit}} - t_{\text{entry}}$.
- Độ trễ điều khiển tức thời của xe $i$:
  $$d_i = \max\left(0, t_{\text{dwell}, i} - t_{\text{free\_flow}, i}\right)$$

Đo lường trung bình toàn mạng:
$$\bar{D}_{\text{control}} = \frac{1}{N_{\text{samples}}} \sum_{i=1}^{N_{\text{samples}}} d_i \quad (\text{s/veh})$$

---

### 4.2. Lưu lượng thông hành mạng lưới (Network Throughput)
Đo lường tổng số chuyến đi hoàn thành thành công trên một đơn vị thời gian:
$$\text{Throughput} = \frac{N_{\text{completed\_trips}} \times 60}{T_{\text{sim}}} \quad (\text{veh/min})$$

---

### 4.3. Thời gian hành trình trung bình (Average Trip Time)
Thời gian từ khi xe xuất phát tại điểm đầu cho đến khi rời khỏi mạng lưới tại điểm đích:
$$\bar{T}_{\text{trip}} = \frac{1}{N_{\text{completed}}} \sum_{i=1}^{N_{\text{completed}}} (t_{\text{arrival}, i} - t_{\text{departure}, i}) \quad (\text{s})$$

---

## 5. TỐI ƯU HÓA HỆ THỐNG THỜI GIAN THỰC (REAL-TIME ARCHITECTURE & CONCURRENCY)

Để mô phỏng vận hành liên tục ở tần số cao (10 Hz) với hơn 500 phương tiện đồng thời mà không bị nghẽn (deadlock/freeze):

1. **Khử tắc nghẽn TCP Backpressure:**
   - Bộ quản lý kết nối `ConnectionManager` phân phối dữ liệu song song qua `asyncio.gather`.
   - Bọc lệnh gửi socket với ngưỡng thời gian nghiêm ngặt:
     $$\tau_{\text{ws\_send}} = 0.15\text{ s}$$
   - Nếu client bị lag (ví dụ: trình duyệt chạy tác vụ nặng), kết nối sẽ tự động hủy kích hoạt thay vì làm treo luồng mô phỏng chính.

2. **Nén lượng tải gói tin WebSocket (Payload Compaction):**
   - Làm tròn tọa độ $(X, Y)$, vận tốc $v$, thời gian chờ $\tau_w$ xuống 1 chữ số thập phân ($\Delta = 0.1\text{ m}$).
   - Giảm $45\%$ kích thước gói tin JSON mỗi tick ($\approx 32\text{ KB}$ thay vì $60\text{ KB}$).

3. **Cơ chế Dual-Ring Symmetric Signal Phase:**
   - Đảm bảo 2 hướng đối diện (N-S hoặc E-W) luôn đồng bộ tuyệt đối về màu sắc và thời gian đếm ngược.
   - Các làn rẽ trái đối đầu được cấu hình quyền nhường đường $g$ (permissive yield), ngăn ngừa xung đột phương tiện theo mô hình car-following Krauss trong SUMO.

---

*Tài liệu kỹ thuật được chuẩn hóa phục vụ công tác phát triển, kiểm thử và biên soạn công bố khoa học.*
