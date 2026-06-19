# Scripted by Emir Karadağ [2026-2027]
# GitHub: @Scriptionz [https://github.com/Scriptionz] 
# LinkedIn: @Emir Karadağ [https://www.linkedin.com/in/emir-karadağ-617a013a2/]

# !! Licensed under the MIT License. Please check the license before using the system. !!

# --------------- LIBRARY IMPORTER (AUTO) ----------------- #
import os
import sys
import subprocess
import time
import uuid  

def install_dependencies():
    """Checks for required libraries and installs them if missing."""
    required = {'opencv-python', 'numpy'}
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("SYSTEM: Missing libraries detected. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"FATAL ERROR 003: {e}")
            sys.exit()

install_dependencies()

import cv2
import numpy as np

# --------------- CENTRAL CONFIGURATION MENUS ----------------- #

PRINT_SETTINGS = {
    "show_welcome_banner": True,      
    "show_license_logs": True,        
    "show_startup_msg": True,         
    "show_system_errors": True        
}

SYSTEM_CONFIG = {
    "DEMO_MODE": True,                # TRUE: Bypasses network/license validation and boots into full version.
    "IS_PREMIUM": True,               # Forced to TRUE during demo runtime to unlock all diagnostic systems.
    "CURRENT_VERSION": "v1.4.0",
    "PRODUCT_ID": "uav_premium_demo_4857"
}

# Live Status Runtime Values for System Modules
SETTINGS = {
    "dot_color_reader": True,         
    "draw_crosshair": True,           
    "telemetry_overlay": True,        
    "auto_brightness": True,          
    "shape_detection": False,     
    "target_identifier": False,   
    "use_advanced_blur": False,   
    "show_binary_mask": False,    
    "video_recording": False,     
    "uav_connected": False        
}

# =========================================================================
# 🛠️ DYNAMIC UI MENU LAYOUT CONFIGURATOR (Reorder or Modify Items Here)
# =========================================================================
# To change the rendering sequence on the HUD, simply rearrange the list elements.
# Schema: {"hotkey": "KeyboardKey", "label": "OnScreenLabel", "setting_key": "SETTINGS_Dictionary_Key", "premium": True/False}
UI_MENU_LAYOUT = [
    {"hotkey": "1", "label": "Color Reader",      "setting_key": "dot_color_reader",   "premium": False},
    {"hotkey": "2", "label": "Crosshair",         "setting_key": "draw_crosshair",      "premium": False},
    {"hotkey": "3", "label": "Telemetry HUD",     "setting_key": "telemetry_overlay",   "premium": False},
    {"hotkey": "4", "label": "Auto Brightness",   "setting_key": "auto_brightness",    "premium": False},
    {"hotkey": "5", "label": "Shape Detection",   "setting_key": "shape_detection",    "premium": True},
    {"hotkey": "6", "label": "Target Lock Box",   "setting_key": "target_identifier",  "premium": True},
    {"hotkey": "7", "label": "Fast Blur Engine",  "setting_key": "use_advanced_blur",  "premium": True},
    {"hotkey": "8", "label": "Show Binary Mask",  "setting_key": "show_binary_mask",   "premium": True},
    {"hotkey": "9", "label": "Video Recorder",    "setting_key": "video_recording",    "premium": False},
    {"hotkey": "0", "label": "UAV Serial Link",   "setting_key": "uav_connected",      "premium": False}
]

DETECTION_PARAMS = {
    "min_area": 4500,               
    "blur_size": (9, 9),
    "median_blur_kernel": 5,          
    "epsilon_coeff": 0.04,          
    "line_thickness": 2,            
    "hsv_lower": np.array([0, 70, 50]),
    "hsv_upper": np.array([180, 255, 255]),
    "circularity_threshold": 0.75   
}

CAM_CONFIG = {
    "width": 1280, 
    "height": 720,
    "sidebar_width": 360,             
    "device_index": 0, 
    "exit_key": "q"
}

# --------------- CODETOPIA LICENSING SYSTEM (W.I.P BYPASS) ----------------- #

if PRINT_SETTINGS["show_welcome_banner"]:
    print("-" * 60)
    print(f"   Welcome to CODETOPIA UAV Vision System {SYSTEM_CONFIG['CURRENT_VERSION']}   ")
    print("   [W.I.P DEMO BUILD] - License Network Handshake Bypassed ")
    print("-" * 60)

if SYSTEM_CONFIG["DEMO_MODE"]:
    if PRINT_SETTINGS["show_license_logs"]:
        print("SYSTEM LOG: Running in Local Premium Demo Runtime Mode.")
        print("STATUS    : All premium protocols enabled for testing.\n")
    VERSION_TAG = "BETA-DEMO"
else:
    VERSION_TAG = "Free"

# --------------- LOCALIZATION & LANGUAGE ----------------- #

LANGUAGE_SETTINGS = {
    "startup_msg": f"UAV X DEVELOPMENT - {SYSTEM_CONFIG['CURRENT_VERSION']} Loading Framework...",
    "err_no_cam": "ERROR 001: Camera hardware endpoint not detected.",
    "ui_window_name": f"Codetopia Ground Control Station - {SYSTEM_CONFIG['CURRENT_VERSION']}",
    "mask_window_name": "UAV Binary Mask Stream (Debug)",
    "color_names": {"red": "RED", "orange": "ORANGE", "yellow": "YELLOW", "green": "GREEN", "blue": "BLUE", "purple": "PURPLE"},
    "shape_labels": {"tri": "TRIANGLE", "rect": "RECTANGLE", "pent": "PENTAGON", "hex": "HEXAGON", "poly": "POLYGON", "circle": "CIRCLE"}
}

# --------------- CORE SYSTEM ----------------- #

if PRINT_SETTINGS["show_startup_msg"]: print(LANGUAGE_SETTINGS["startup_msg"])

cap = cv2.VideoCapture(CAM_CONFIG["device_index"])
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_CONFIG["width"])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_CONFIG["height"])

if not cap.isOpened():
    if PRINT_SETTINGS["show_system_errors"]: print(LANGUAGE_SETTINGS["err_no_cam"])
    sys.exit()

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
video_writer = None
prev_time = time.time() 

# Telemetry Smoothing Filter Variables (Rolling Average Buffers)
fps_history = []
latency_history = []
smoothing_window = 15 # Window size determining telemetry stability (Averages the last 15 frames)

while True:
    ret, frame = cap.read()
    if not ret: break

    # --- [STEP 1: LIGHTING STABILIZATION (CLAHE)] --- 
    if SETTINGS["auto_brightness"]:
        img_yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
        frame = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    hsv_frame = None
    if SETTINGS["dot_color_reader"] or SETTINGS["shape_detection"] or SETTINGS["show_binary_mask"]:
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- [STEP 2: COLOR ANALYSIS] ---
    if SETTINGS["dot_color_reader"] and hsv_frame is not None:
        height, width, _ = frame.shape
        cx, cy = width // 2, height // 2
        hue = hsv_frame[cy, cx][0]
        b, g, r = map(int, frame[cy, cx])

        c = LANGUAGE_SETTINGS["color_names"]
        if hue < 5 or hue > 170: color_str = c["red"]
        elif hue < 22: color_str = c["orange"]
        elif hue < 33: color_str = c["yellow"]
        elif hue < 78: color_str = c["green"]
        elif hue < 131: color_str = c["blue"]
        else: color_str = c["purple"]

        cv2.rectangle(frame, (cx - 150, 600), (cx + 150, 680), (255, 255, 255), -1)
        cv2.putText(frame, color_str, (cx - 100, 655), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (b, g, r), 3)
        
        if SETTINGS["draw_crosshair"]:
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.line(frame, (cx - 20, cy), (cx + 20, cy), (0, 255, 0), 2)
            cv2.line(frame, (cx, cy - 20), (cx, cy + 20), (0, 255, 0), 2)

    # --- [STEP 3: SHAPE DETECTION & MASKING] ---
    if (SETTINGS["shape_detection"] or SETTINGS["show_binary_mask"]) and hsv_frame is not None:
        if SETTINGS["use_advanced_blur"]:
            blurred_hsv = cv2.medianBlur(hsv_frame, DETECTION_PARAMS["median_blur_kernel"])
        else:
            blurred_hsv = cv2.GaussianBlur(hsv_frame, DETECTION_PARAMS["blur_size"], 0) 
            
        mask = cv2.inRange(blurred_hsv, DETECTION_PARAMS["hsv_lower"], DETECTION_PARAMS["hsv_upper"])
        kernel = np.ones((7,7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        if SETTINGS["show_binary_mask"]:
            cv2.imshow(LANGUAGE_SETTINGS["mask_window_name"], mask)
        else:
            try: cv2.destroyWindow(LANGUAGE_SETTINGS["mask_window_name"])
            except: pass

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > DETECTION_PARAMS["min_area"]:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, DETECTION_PARAMS["epsilon_coeff"] * peri, True)
                circularity = (4 * np.pi * area) / (peri**2)
                
                label = "UNKNOWN"
                if circularity > DETECTION_PARAMS["circularity_threshold"]:
                    label = LANGUAGE_SETTINGS["shape_labels"]["circle"]
                elif len(approx) == 3: label = LANGUAGE_SETTINGS["shape_labels"]["tri"]
                elif len(approx) == 4: label = LANGUAGE_SETTINGS["shape_labels"]["rect"]
                elif 5 <= len(approx) <= 6: label = LANGUAGE_SETTINGS["shape_labels"]["poly"]
                else: continue

                x, y, w, h = cv2.boundingRect(approx)
                if SETTINGS["target_identifier"]:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(frame, "TARGET LOCKED", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    else:
        try: cv2.destroyWindow(LANGUAGE_SETTINGS["mask_window_name"])
        except: pass

    # --- [VIDEO RECORDING CAM OVERLAY] ---
    if SETTINGS["video_recording"]:
        if video_writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            video_writer = cv2.VideoWriter('uav_mission_log.avi', fourcc, 20.0, (CAM_CONFIG["width"], CAM_CONFIG["height"]))
        video_writer.write(frame)
        cv2.circle(frame, (30, 80), 8, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (45, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    else:
        if video_writer is not None:
            video_writer.release()
            video_writer = None

    # --- [SMOOTH TELEMETRY CALCULATOR] ---
    now = time.time()
    raw_fps = 1 / (now - prev_time) if (now - prev_time) > 0 else 0
    prev_time = now
    raw_latency = (1 / raw_fps) * 1000 if raw_fps > 0 else 0

    # Process Rolling Average Buffer (FPS Filtering Engine)
    fps_history.append(raw_fps)
    latency_history.append(raw_latency)
    if len(fps_history) > smoothing_window:
        fps_history.pop(0)
        latency_history.pop(0)

    smooth_fps = int(sum(fps_history) / len(fps_history))
    smooth_latency = int(sum(latency_history) / len(latency_history))
    
    fps_text = str(smooth_fps)
    latency_text = f"{smooth_latency}ms"
    
    if SETTINGS["telemetry_overlay"]:
        cv2.putText(frame, f"FPS: {fps_text} | LATENCY: {latency_text}", 
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # --- [SIDEBAR HUD GENERATOR] ---
    total_width = CAM_CONFIG["width"] + CAM_CONFIG["sidebar_width"]
    combined_ui = np.zeros((CAM_CONFIG["height"], total_width, 3), dtype=np.uint8)
    combined_ui[0:720, 0:1280] = frame
    combined_ui[0:720, 1280:total_width] = (24, 24, 24)

    sb_x = 1300 
    cv2.putText(combined_ui, "CODETOPIA UAV PANEL", (sb_x, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.putText(combined_ui, f"SYS VER: {SYSTEM_CONFIG['CURRENT_VERSION']} ({VERSION_TAG})", (sb_x, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (170, 170, 170), 1)
    cv2.line(combined_ui, (1290, 85), (1620, 85), (60, 60, 60), 1)

    # --- DYNAMIC MENU RENDERING ENGINE ---
    current_y = 120
    y_spacing = 35  # Row spacing configuration

    for item in UI_MENU_LAYOUT:
        hotkey = item["hotkey"]
        label = item["label"]
        setting_key = item["setting_key"]
        is_premium = item["premium"]
        is_active = SETTINGS[setting_key]

        # Render Left Label (e.g., "1. Color Reader")
        cv2.putText(combined_ui, f"{hotkey}. {label}", (sb_x, current_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
        
        # Render Right Status Box Text
        if is_premium and not SYSTEM_CONFIG["IS_PREMIUM"]:
            cv2.putText(combined_ui, "[ LOCKED ]", (sb_x + 210, current_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        else:
            status_str = "[  ON  ]" if is_active else "[  OFF ]"
            status_color = (0, 255, 0) if is_active else (100, 100, 100)
            cv2.putText(combined_ui, status_str, (sb_x + 210, current_y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, status_color, 2)
        
        current_y += y_spacing

    # --- LIVE TELEMETRY & UAV SERIAL LOGS SECTION ---
    cv2.line(combined_ui, (1290, 490), (1620, 490), (60, 60, 60), 1)
    cv2.putText(combined_ui, "LIVE TELEMETRY LOGS", (sb_x, 520), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    
    if SETTINGS["uav_connected"]:
        sim_alt = 142.5 + np.sin(time.time()) * 2.3
        sim_pitch = np.cos(time.time() * 2) * 1.5
        sim_roll = np.sin(time.time() * 1.5) * 3.1
        
        cv2.putText(combined_ui, f"LINK STATE : CONNECTED (MAVLink)", (sb_x, 555), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 0), 1)
        cv2.putText(combined_ui, f"ALTITUDE   : {sim_alt:.2f} m", (sb_x, 585), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
        cv2.putText(combined_ui, f"PITCH ANG  : {sim_pitch:.1f} deg", (sb_x, 615), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
        cv2.putText(combined_ui, f"ROLL ANG   : {sim_roll:.1f} deg", (sb_x, 645), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
    else:
        cv2.putText(combined_ui, "LINK STATE : NO CONNECTION", (sb_x, 555), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 255), 1)
        cv2.putText(combined_ui, "ALTITUDE   : ---", (sb_x, 585), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 100, 100), 1)
        cv2.putText(combined_ui, "PITCH ANG  : ---", (sb_x, 615), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 100, 100), 1)
        cv2.putText(combined_ui, "ROLL ANG   : ---", (sb_x, 645), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (100, 100, 100), 1)

    cv2.putText(combined_ui, f"SYS FPS: {fps_text} | LAT: {latency_text}", (sb_x, 685), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (150, 150, 150), 1)
    cv2.putText(combined_ui, "Press 'Q' to Secure Exit", (sb_x, 708), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 165, 255), 1)

    cv2.imshow(LANGUAGE_SETTINGS["ui_window_name"], combined_ui)
    
    # --- DYNAMIC KEYBOARD INPUT EXECUTION ENGINE ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord(CAM_CONFIG["exit_key"]): 
        break
    
    # Matches the key dynamically against layout map items to switch mode states cleanly
    for item in UI_MENU_LAYOUT:
        if key == ord(item["hotkey"]):
            if item["premium"] and not SYSTEM_CONFIG["IS_PREMIUM"]:
                break # Do nothing if the premium feature is locked
            
            s_key = item["setting_key"]
            SETTINGS[s_key] = not SETTINGS[s_key]
            break

if video_writer is not None:
    video_writer.release()
cap.release()
cv2.destroyAllWindows()
