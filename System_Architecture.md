# 🏛️ System Architecture - OpenCV Detector v1.4.0

This document outlines the core logic, architectural design, and frame-processing pipeline of the **OpenCV Detector v1.4.0**. The system is engineered for low-latency computer vision tasks, focusing on structural modularity, runtime adaptability, and stable telemetry reporting.

---

### 1. Self-Healing Dependency Engine
The system initializes with an automated environment verification sub-routine to guarantee cross-platform compatibility:
* **Runtime Verification:** Checks for the presence of exact bindings for `OpenCV` (`cv2`) and `NumPy` at thread execution startup.
* **Auto-Recovery Sequence:** If dependencies are broken or missing, the initialization sequence spawns an isolated subprocess to invoke `pip install`, followed by an instant binary reload (`os.execl`) to resume execution cleanly without user intervention.

### 2. Decoupled Configuration & Dynamic UI Engine
Global parameters and control states are fully decoupled from the underlying processing algorithms, allowing **"tuning without touching"**:
* **Dynamic UI Layout Configurator:** The HUD rendering sequence is controlled by a structured list array (`UI_MENU_LAYOUT`). Developers can manipulate, reorder, or completely swap menu items dynamically on the screen without modifying the execution loops or event listeners.
* **State Mapping Matrix:** Key matrices handle hotkey intercept maps, checking active/inactive states for features like color reading, tracking boxes, or recording pipelines instantly.

### 3. Computer Vision & Frame Processing Pipeline
To eliminate environmental noise, sensor jitter, and illumination shifts, every captured frame undergoes a strictly synchronized, multi-tier pipeline:

1. **Acquisition:** Captures high-speed raw BGR matrix streams from the hardware index defined in `CAM_CONFIG`.
2. **Lighting Stabilization (CLAHE):** Rather than standard histogram equalization, the system converts frames to the **YUV color space** and applies **Contrast Limited Adaptive Histogram Equalization (CLAHE)** to the luminance channel (Y). This prevents over-amplification of background noise and stabilizes tracking under volatile outdoor or field lighting conditions.
3. **Color Space Isolation:** Converts stabilized frames into the **HSV (Hue, Saturation, Value) model** for highly resilient color profiling.
4. **Adaptive Filtering (Noise Reduction):** Dynamically toggles between standard **Gaussian Blur** and an optional **Median Filter Engine** depending on the selected operational profile to isolate contours effectively.
5. **Morphological Refinement:** Executes sequential mathematical morphology operations (`MORPH_OPEN` to eliminate isolated outlier pixels, followed by `MORPH_CLOSE` to bridge small holes inside objects) using custom structural kernels.

### 4. Mathematical Object Recognition & Geometry Analysis
Advanced mathematical morphology rules are utilized for real-time spatial object tracking:
* **Contour Extraction:** Extracts structural outlines from binary masks, safely filtering out background interference using a strict `min_area` pixel threshold.
* **Polygon Approximation:** Implements the **Douglas-Peucker algorithm** ($\epsilon$-coefficient curve approximation) to map out geometric vertices and isolate triangles, rectangles, or complex polygons.
* **Circularity Analysis:** Validates precise spherical properties regardless of perspective distortion or pixel stretching by processing the mathematical roundness equation:
  $$Circularity = 4 \pi \times \frac{\text{Area}}{\text{Perimeter}^2}$$
* **Dynamic Target Tracking:** When active, bounding boxes map coordinates to target boundaries, locking onto objects with high visual contrast.

### 5. Smooth Telemetry Engine & HUD
The Ground Control HUD splits telemetry feeds into an isolated, multi-threaded interface sidebar:
* **Rolling Average Telemetry Buffer:** To prevent erratic telemetry jumps, real-time metrics pass through a rolling average filter engine ($N=15$). Frame performance data is calculated over the last 15 ticks, generating locked, ultra-smooth **FPS** and **Latency** readouts.
* **MAVLink Serial Stream Simulation:** Simulates full downlink connectivity, displaying real-time data overlays for mock link state, Altitude, Pitch, and Roll matrices using live trigonometric wave generation.

---

> [!CAUTION]
> **Resource Management & Shutdown Sequence:** Always terminate execution by pressing the secure key mapped in `CAM_CONFIG` (Default: **"q"**). Forcing a hard terminal kill or destroying the canvas window manually bypasses camera resource de-allocation, which can lock the webcam peripheral interface or cause video encoding cache leaks.
