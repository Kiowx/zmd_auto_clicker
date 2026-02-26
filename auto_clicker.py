import ctypes
import sys
import os

# ================== [新增] 修复无控制台模式下 tqdm 报错问题 ==================
# 如果标准输出/错误流为空（通常在 PyInstaller -w 模式下发生）
# 则将它们重定向到系统的空设备（"黑洞"）
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
# ==============================================================================

# 告诉系统不要对鼠标坐标进行缩放偏移
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
# ... (保留你后面的所有代码)
from paddleocr import PaddleOCR
import logging

# 告诉系统不要对鼠标坐标进行缩放偏移
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

logging.getLogger("ppocr").setLevel(logging.WARNING)

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("终末地快递小助手")
        self.root.geometry("360x600") 
        self.root.attributes("-topmost", True) 

        self.running = False
        self.ocr = PaddleOCR(use_angle_cls=False, lang="ch") 

        # ================== 1. 目标设置区 ==================
        frame1 = tk.LabelFrame(root, text="目标设置", fg="blue")
        frame1.pack(fill="x", padx=10, pady=5)

        f1_r1 = tk.Frame(frame1)
        f1_r1.pack(fill="x", pady=2)
        tk.Label(f1_r1, text="易碎信息:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.fragility_var = tk.StringVar()
        self.fragility_combo = ttk.Combobox(f1_r1, textvariable=self.fragility_var, state="readonly")
        self.fragility_combo['values'] = ("不限", "不易损", "易损", "极易损")
        self.fragility_combo.current(0)
        self.fragility_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        f1_r2 = tk.Frame(frame1)
        f1_r2.pack(fill="x", pady=2)
        tk.Label(f1_r2, text="接收点:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.destination_var = tk.StringVar()
        self.destination_combo = ttk.Combobox(f1_r2, textvariable=self.destination_var, state="readonly")
        self.destination_combo['values'] = ("不限", "源石研究园", "矿脉源区", "供能高地", "武陵城")
        self.destination_combo.current(0)
        self.destination_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        # ================== 2. 时间与频率区 ==================
        frame2 = tk.LabelFrame(root, text="时间与频率", fg="blue")
        frame2.pack(fill="x", padx=10, pady=5)

        f2_r1 = tk.Frame(frame2)
        f2_r1.pack(fill="x", pady=2)
        tk.Label(f2_r1, text="识别间隔:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.freq_var = tk.StringVar()
        self.freq_combo = ttk.Combobox(f2_r1, textvariable=self.freq_var, state="readonly")
        self.freq_combo['values'] = ("0秒", "0.5秒", "1秒", "2秒", "3秒")
        self.freq_combo.current(1) 
        self.freq_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        f2_r2 = tk.Frame(frame2)
        f2_r2.pack(fill="x", pady=2)
        tk.Label(f2_r2, text="刷新等待:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.refresh_var = tk.StringVar()
        self.refresh_combo = ttk.Combobox(f2_r2, textvariable=self.refresh_var, state="readonly")
        self.refresh_combo['values'] = ("3秒", "5秒", "8秒")
        self.refresh_combo.current(0) 
        self.refresh_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        # ================== 3. 终极滑动设置区 ==================
        frame3 = tk.LabelFrame(root, text="滑动行为设置", fg="blue")
        frame3.pack(fill="x", padx=10, pady=5)

        f3_r1 = tk.Frame(frame3)
        f3_r1.pack(fill="x", pady=2)
        tk.Label(f3_r1, text="滑动方式:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.scroll_method_var = tk.StringVar()
        self.scroll_method_combo = ttk.Combobox(f3_r1, textvariable=self.scroll_method_var, state="readonly")
        self.scroll_method_combo['values'] = ("鼠标拖拽 (模拟器推荐)", "滚轮滚动")
        self.scroll_method_combo.current(0) 
        self.scroll_method_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        f3_r4 = tk.Frame(frame3)
        f3_r4.pack(fill="x", pady=2)
        tk.Label(f3_r4, text="滑动模式:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.scroll_mode_var = tk.StringVar()
        self.scroll_mode_combo = ttk.Combobox(f3_r4, textvariable=self.scroll_mode_var, state="readonly")
        self.scroll_mode_combo['values'] = ("智能滑动", "仅向下滑动", "仅向上滑动", "先下后上 (最严谨)")
        self.scroll_mode_combo.current(0) 
        self.scroll_mode_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        f3_r2 = tk.Frame(frame3)
        f3_r2.pack(fill="x", pady=2)
        tk.Label(f3_r2, text="单向次数:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.scroll_times_var = tk.StringVar()
        self.scroll_times_combo = ttk.Combobox(f3_r2, textvariable=self.scroll_times_var, state="readonly")
        self.scroll_times_combo['values'] = ("1次", "2次", "3次", "4次", "5次")
        self.scroll_times_combo.current(2) 
        self.scroll_times_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        f3_r3 = tk.Frame(frame3)
        f3_r3.pack(fill="x", pady=2)
        tk.Label(f3_r3, text="单次距离:", width=12, anchor="e").pack(side=tk.LEFT, padx=5)
        self.scroll_dist_var = tk.StringVar()
        self.scroll_dist_combo = ttk.Combobox(f3_r3, textvariable=self.scroll_dist_var, state="readonly")
        self.scroll_dist_combo['values'] = ("短距 (500)", "中距 (800)", "长距 (1200)")
        self.scroll_dist_combo.current(1) 
        self.scroll_dist_combo.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        # ================== 底部操作区 ==================
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(self.btn_frame, text="▶ 开始运行", bg="#2e7d32", fg="white", font=("", 10, "bold"), width=12, command=self.start_script)
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(self.btn_frame, text="⏹ 停止运行", bg="#c62828", fg="white", font=("", 10, "bold"), width=12, command=self.stop_script, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(root, text="状态: 待命休眠中...", fg="grey")
        self.status_label.pack(pady=5)

    def update_status(self, msg, color="blue"):
        self.root.after(0, lambda: self.status_label.config(text=msg, fg=color))

    def start_script(self):
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.update_status("状态: 监控巡航中...", "green")
        
        self.root.iconify()
        
        params = {
            "fragility": self.fragility_var.get(),
            "destination": self.destination_var.get(),
            "detect_freq": float(self.freq_var.get().replace("秒", "")),
            "refresh_interval": int(self.refresh_var.get().replace("秒", "")),
            "scroll_method": self.scroll_method_var.get(),
            "scroll_mode": self.scroll_mode_var.get(),
            "scroll_times": int(self.scroll_times_var.get().replace("次", "")),
            "scroll_dist": int(self.scroll_dist_var.get().split("(")[1].replace(")", ""))
        }
        
        threading.Thread(target=self.automation_loop, args=(params,), daemon=True).start()

    def stop_script(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.update_status("状态: 强制中断或任务完成", "red")
        
        self.root.deiconify()
        self.root.attributes("-topmost", True)

    def automation_loop(self, p):
        times = p["scroll_times"]
        mode = p["scroll_mode"]
        
        current_smart_dir = "down" 
        
        if "仅向下滑动" in mode:
            scroll_sequence = ["down"] * times + ["refresh"]
        elif "仅向上滑动" in mode:
            scroll_sequence = ["up"] * times + ["refresh"]
        elif "智能滑动" in mode:
            scroll_sequence = ["down"] * times + ["refresh"]
        else:
            scroll_sequence = ["down"] * times + ["up"] * times + ["refresh"]
            
        scroll_index = 0 
        screen_w, screen_h = pyautogui.size() 
        
        while self.running:
            if p["detect_freq"] > 0:
                time.sleep(p["detect_freq"])
                
            self.update_status("正在截图并分析数据源...", "blue") 
            
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save("temp_screen.png")
                result = self.ocr.ocr("temp_screen.png", cls=False)
            except Exception as e:
                print(f"识别发生异常: {e}")
                time.sleep(1)
                continue
            
            if not result or not result[0]:
                time.sleep(1)
                continue

            all_items = []
            refresh_btn_pos = None
            
            for line in result[0]:
                if line is None:
                    continue
                box = line[0] 
                text = line[1][0] 
                
                y_center = (box[0][1] + box[2][1]) / 2
                x_center = (box[0][0] + box[1][0]) / 2
                
                if text in ["开始运行", "停止运行", "目标设置", "时间与频率", "状态:"] or "设置" in text or "滑动" in text:
                    continue
                
                if "刷新" in text:
                    refresh_btn_pos = (x_center, y_center)
                    continue
                    
                all_items.append({'text': text, 'x': x_center, 'y': y_center})

            accept_buttons = []
            for item in all_items:
                txt = item['text']
                if ("接取" in txt or "按取" in txt or "运送" in txt) and "列表" not in txt:
                    if item['x'] > screen_w * 0.5: 
                        accept_buttons.append(item)
            
            match_found = False
            
            for btn in accept_buttons:
                btn_y = btn['y']
                row_texts = [item['text'] for item in all_items if abs(item['y'] - btn_y) < 80]
                
                frag_match = False
                dest_match = False
                
                for txt in row_texts:
                    target_frag = p["fragility"]
                    if target_frag == "不限":
                        frag_match = True
                    elif target_frag == "不易损" and "不易损" in txt:
                        frag_match = True
                    elif target_frag == "极易损" and "极易损" in txt:
                        frag_match = True
                    elif target_frag == "易损":
                        if "易损" in txt and "不易损" not in txt and "极易损" not in txt:
                            frag_match = True

                    clean_txt = txt.replace("(", "").replace(")", "").replace("（", "").replace("）", "")
                    if p["destination"] == "不限" or p["destination"] in clean_txt:
                        dest_match = True
                        
                if frag_match and dest_match:
                    self.update_status(f"🎯 成功锁定目标并点击！验证中...", "green")
                    print(f"===> 确认接取该行: {row_texts}")
                    
                    pyautogui.moveTo(btn['x'], btn['y'], duration=0.2)
                    time.sleep(0.1) 
                    pyautogui.mouseDown()
                    time.sleep(0.05) 
                    pyautogui.mouseUp()
                    
                    # ================== [新增] 接取失败验证逻辑 ==================
                    # 点击后等待 1.5 秒，让游戏的“失败”提示框有时间弹出来
                    time.sleep(1.5) 
                    
                    try:
                        check_screen = pyautogui.screenshot()
                        check_result = self.ocr.ocr(check_screen, cls=False)
                        
                        is_failed = False
                        if check_result and check_result[0]:
                            for check_line in check_result[0]:
                                if check_line is None: continue
                                check_text = check_line[1][0]
                                # 只要捕捉到“失败”这两个字，或者完整的句子，就判定为接取失败
                                if "委托失败" in check_text:
                                    is_failed = True
                                    break
                        
                        if is_failed:
                            self.update_status("⚠️ 检测到接取失败，放弃当前目标！", "orange")
                            print("===> 提示接取失败，继续寻找下一个目标。")
                            # 点击一下屏幕左上角安全区域，以关闭可能残留的提示弹窗
                            pyautogui.click(10, 10)
                            time.sleep(0.5)
                            
                            # 将 match_found 保持为 False，并 break 出当前的接取循环
                            # 这样程序就会当做“当前页没找到”，从而继续执行滚动或刷新逻辑
                            match_found = False
                            break 
                        else:
                            # 如果没有检测到失败，则判定为真正接取成功，结束脚本
                            self.update_status("🎉 接取成功！任务完成。", "green")
                            match_found = True
                            self.root.after(0, self.stop_script) 
                            return 

                    except Exception as e:
                        print(f"验证结果时发生异常: {e}")
                        # 验证环节哪怕报错了，保险起见还是停止运行
                        self.root.after(0, self.stop_script) 
                        return
                    # ==============================================================

            if not match_found and self.running:
                action = scroll_sequence[scroll_index]
                
                if action == "down" or action == "up":
                    self.update_status(f"当前页未找到或接取失败，向{ '下' if action == 'down' else '上' }滑动...", "orange")
                    pyautogui.moveTo(screen_w * 0.7, screen_h * 0.5)
                    time.sleep(0.1)
                    
                    if "拖拽" in p["scroll_method"]:
                        drag_y = -p["scroll_dist"] if action == "down" else p["scroll_dist"]
                        pyautogui.dragRel(0, drag_y, duration=0.5, button='left')
                    else:
                        scroll_val = -p["scroll_dist"] if action == "down" else p["scroll_dist"]
                        pyautogui.scroll(scroll_val) 
                        
                    pyautogui.moveTo(10, 10, duration=0.1) 
                    time.sleep(1.5) 
                    scroll_index += 1
                    
                elif action == "refresh":
                    self.update_status(f"列表已阅毕，点击刷新... 等待 {p['refresh_interval']} 秒", "purple")
                    if refresh_btn_pos:
                        pyautogui.moveTo(refresh_btn_pos[0], refresh_btn_pos[1], duration=0.2)
                        time.sleep(0.1)
                        pyautogui.mouseDown()
                        time.sleep(0.05)
                        pyautogui.mouseUp()
                        pyautogui.moveTo(10, 10, duration=0.1)
                    else:
                        print("未能找到刷新按钮")
                    
                    time.sleep(p['refresh_interval']) 
                    scroll_index = 0 

                    if "智能滑动" in mode:
                        if current_smart_dir == "down":
                            current_smart_dir = "up"
                            scroll_sequence = ["up"] * times + ["refresh"]
                            print(f"\n🔁 智能翻转: 下一步路线切换为 [向上滑动]")
                        else:
                            current_smart_dir = "down"
                            scroll_sequence = ["down"] * times + ["refresh"]
                            print(f"\n🔁 智能翻转: 下一步路线切换为 [向下滑动]")

# ================== 提权检测函数 ==================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ================== 启动入口 ==================
if __name__ == "__main__":
    if is_admin():
        root = tk.Tk()
        app = AutoClickerApp(root)
        root.mainloop()
    else:
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()