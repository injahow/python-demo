# idm-agent-tray.py
import os
import sys
import time
import subprocess
import urllib.parse
import webbrowser
import json
import hashlib
import secrets
import hmac
from threading import Thread
from flask import Flask, request, jsonify
# --- 日志配置 ---
import logging
from logging.handlers import TimedRotatingFileHandler
# --- GUI / 托盘依赖 ---
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox, filedialog

# 获取程序所在目录
if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))
# 日志目录
log_dir = os.path.join(app_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "idm_agent.log")
logger = logging.getLogger("IDM-Agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = TimedRotatingFileHandler(
        log_path,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.suffix = "%Y-%m-%d"
    file_formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    # 控制台日志
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('[%(levelname)s] %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

# --- Windows 注册表（开机启动）---
try:
    import winreg as reg
except ImportError:
    reg = None

# --- 配置 ---
CONFIG_FILE = os.path.join(app_dir, "idm_agent_config.json")
TIME_WINDOW_MS = 30 * 1000  # 30秒，单位：毫秒

# --- 配置管理 ---
def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if "idm_path" not in config:
                    config["idm_path"] = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
                return config
        except Exception as e:
            logger.warning(f"配置加载失败: {e}")
    config = {
        "secret_key": secrets.token_urlsafe(32),
        "idm_path": r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"
    }
    save_config(config)
    return config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        logger.error(f"保存配置失败: {e}")

config = load_config()

# --- Flask App ---
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/download', methods=['OPTIONS'])
def handle_options():
    return '', 200

def generate_md5_signature(params, secret):
    items = [(k, v) for k, v in params.items() if k != 'sign' and v is not None]
    items.sort(key=lambda x: x[0])
    raw = '&'.join(f"{k}={v}" for k, v in items) + secret
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

def verify_md5_signature(params, signature):
    try:
        ts = int(params.get('ts', 0))
    except (ValueError, TypeError):
        logger.warning("ts 无效")
        return False
    now_ms = int(time.time() * 1000)
    if abs(now_ms - ts) > TIME_WINDOW_MS:
        logger.warning("签名已过期")
        return False
    current_secret = config["secret_key"]
    expected_sig = generate_md5_signature(params, current_secret)
    return hmac.compare_digest(expected_sig, signature)

@app.route('/download', methods=['GET', 'POST'])
def add_download():
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        params = {
            "url": data.get('url'),
            "filename": data.get('filename'),
            "ts": data.get('ts')
        }
        signature = data.get('sign')
    else:
        params = {
            "url": request.args.get('url'),
            "filename": request.args.get('filename'),
            "ts": request.args.get('ts')
        }
        signature = request.args.get('sign')

    if not all([params['url'], params['ts'], signature]):
        logger.warning("缺少必要参数: url, ts 或 sign")
        return jsonify({"error": "Missing required fields: url, ts, sign"}), 400

    if not verify_md5_signature(params, signature):
        logger.warning("签名验证失败或已过期")
        return jsonify({"error": "Invalid or expired signature"}), 403

    try:
        idm_exe = config["idm_path"]
        if not os.path.isfile(idm_exe):
            logger.error(f"IDM 未找到: {idm_exe}")
            return jsonify({"error": f"IDM 未找到: {idm_exe}"}), 500

        url = urllib.parse.unquote(params['url'])
        logger.info(f"合法请求: {url}")

        cmd = [idm_exe, "/d", url]
        if params['filename']:
            filename = urllib.parse.unquote(params['filename'])
            cmd.extend(["/f", filename])

        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        return jsonify({"code": 0, "message": "Download sent to IDM"}), 200
    except Exception as e:
        logger.error(f"执行下载时发生异常: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return """
    <h2>IDM Agent 正在运行</h2>
    <p>接口地址: <code>http://127.0.0.1:16880/download</code></p>
    <p>参数: <code>url</code>, <code>filename</code> (可选), <code>ts</code> (毫秒时间戳), <code>sign</code></p>
    """

# --- 工具函数 ---
def create_image():
    ICON_SIZE = (32, 32)    # 32x32正方形（偶数尺寸，居中更易对齐）
    BG_COLOR = (255, 255, 255)  # 纯白色背景
    CROSS_COLOR = (0, 0, 0)     # 纯黑色十字线
    LINE_WIDTH = 4              # 线条宽度（像素）
    PADDING = 2                 # 十字线与边框的留白
    image = Image.new("RGB", ICON_SIZE, BG_COLOR)
    draw = ImageDraw.Draw(image)
    center_x = ICON_SIZE[0] / 2 - 0.5
    center_y = ICON_SIZE[1] / 2 - 0.5
    horizontal_start = (PADDING, center_y)
    horizontal_end = (ICON_SIZE[0] - PADDING, center_y)
    vertical_start = (center_x, PADDING)
    vertical_end = (center_x, ICON_SIZE[1] - PADDING)
    draw.line([horizontal_start, horizontal_end], fill=CROSS_COLOR, width=LINE_WIDTH, joint="round")
    draw.line([vertical_start, vertical_end], fill=CROSS_COLOR, width=LINE_WIDTH, joint="round")
    return image

def is_autostart_enabled():
    if not reg:
        return False
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_READ)
        value, _ = reg.QueryValueEx(key, "IDM-Agent")
        reg.CloseKey(key)
        return os.path.abspath(sys.executable) in value
    except FileNotFoundError:
        return False

def set_autostart(enable=True):
    if not reg:
        return
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_WRITE)
    exe_path = os.path.abspath(sys.executable)
    if enable:
        reg.SetValueEx(key, "IDM-Agent", 0, reg.REG_SZ, exe_path)
    else:
        try:
            reg.DeleteValue(key, "IDM-Agent")
        except FileNotFoundError:
            pass
    reg.CloseKey(key)

# --- 显示密钥窗口 ---
def show_secret_key(icon, item):
    root = tk.Tk()
    root.title("🔐 安全密钥 - IDM Agent")
    root.geometry("560x220")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    BG_COLOR = "#f8f9fa"
    WARNING_COLOR = "#e74c3c"
    KEY_BG = "#ffffff"
    KEY_FG = "#000000"
    BUTTON_BG = "#007bff"
    BUTTON_HOVER = "#0056b3"
    BUTTON_FG = "white"

    root.configure(bg=BG_COLOR)

    warning_frame = tk.Frame(root, bg=BG_COLOR)
    warning_frame.pack(pady=(15, 5), padx=20, fill="x")

    tk.Label(warning_frame, text="⚠️", font=("Arial", 16), fg=WARNING_COLOR, bg=BG_COLOR).pack(side=tk.LEFT)
    tk.Label(
        warning_frame,
        text="此密钥用于接口签名，请勿泄露给他人！",
        font=("Microsoft YaHei", 10, "bold"),
        fg=WARNING_COLOR,
        bg=BG_COLOR,
        anchor="w"
    ).pack(side=tk.LEFT, padx=(8, 0))

    key_frame = tk.Frame(root, bg=BG_COLOR)
    key_frame.pack(pady=10, padx=20, fill="x")

    key_text = tk.Text(
        key_frame,
        height=2,
        width=60,
        font=("Consolas", 10),
        bg=KEY_BG,
        fg=KEY_FG,
        relief="solid",
        borderwidth=1,
        wrap="none"
    )
    key_text.insert("1.0", config["secret_key"])
    key_text.config(state="disabled")
    key_text.pack(fill="x", padx=0, pady=0)

    def copy_key():
        root.clipboard_clear()
        root.clipboard_append(config["secret_key"])
        root.update()
        original = copy_btn.cget("text")
        copy_btn.config(text="✓ 已复制", state="disabled")
        root.after(1500, lambda: copy_btn.config(text=original, state="normal"))

    def close_window():
        root.destroy()

    btn_frame = tk.Frame(root, bg=BG_COLOR)
    btn_frame.pack(pady=10)

    copy_btn = tk.Button(
        btn_frame,
        text="📋 复制密钥",
        command=copy_key,
        font=("Microsoft YaHei", 10, "bold"),
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground=BUTTON_HOVER,
        relief="flat",
        padx=20,
        pady=5
    )
    copy_btn.pack(side=tk.LEFT, padx=10)

    close_btn = tk.Button(
        btn_frame,
        text="✕ 关闭",
        command=close_window,
        font=("Microsoft YaHei", 10),
        bg="#6c757d",
        fg="white",
        activebackground="#5a6268",
        relief="flat",
        padx=20,
        pady=5
    )
    close_btn.pack(side=tk.LEFT, padx=10)

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()

# --- 设置 IDM 路径 ---
def set_idm_path(icon, item):
    root = tk.Tk()
    root.title("📁 设置 IDM 路径")
    root.geometry("600x160")
    root.resizable(False, False)
    root.attributes("-topmost", True)
    root.configure(bg="#f8f9fa")

    current_path = config.get("idm_path", "")

    label = tk.Label(
        root,
        text="请输入或选择 IDM 的主程序路径（IDMan.exe）：",
        bg="#f8f9fa",
        font=("Microsoft YaHei", 10)
    )
    label.pack(pady=(15, 5), padx=20, anchor="w")

    path_var = tk.StringVar(value=current_path)
    path_entry = tk.Entry(root, textvariable=path_var, width=70, font=("Consolas", 9))
    path_entry.pack(pady=5, padx=20, fill="x")

    def browse_file():
        filepath = filedialog.askopenfilename(
            title="选择 IDMan.exe",
            filetypes=[("Executable files", "IDMan.exe"), ("All files", "*.*")]
        )
        if filepath:
            path_var.set(filepath)

    def save_path():
        new_path = path_var.get().strip()
        if not new_path:
            messagebox.showwarning("警告", "路径不能为空！", parent=root)
            return
        if not new_path.endswith("IDMan.exe"):
            messagebox.showwarning("警告", "路径应指向 IDMan.exe！", parent=root)
            return
        if not os.path.isfile(new_path):
            messagebox.showerror("错误", "该文件不存在！", parent=root)
            return

        config["idm_path"] = new_path
        save_config(config)
        logger.info(f"IDM 路径已更新为: {new_path}")
        messagebox.showinfo("成功", "IDM 路径已更新！", parent=root)
        root.destroy()

    btn_frame = tk.Frame(root, bg="#f8f9fa")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="浏览...", command=browse_file, width=10).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="保存", command=save_path, width=10, bg="#28a745", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="取消", command=root.destroy, width=10).pack(side=tk.LEFT, padx=5)

    root.mainloop()

# --- 托盘菜单回调函数（关键！）---
def open_web_ui(icon, item):
    webbrowser.open("http://127.0.0.1:16880")

def toggle_autostart(icon, item):
    current = is_autostart_enabled()
    set_autostart(not current)
    status = "已启用" if not current else "已禁用"
    logger.info(f"开机自启状态已{status}")

def regenerate_secret_key(icon, item):
    root = tk.Tk()
    root.withdraw()
    if messagebox.askyesno("确认", "重新生成密钥将使旧客户端失效，是否继续？"):
        new_key = secrets.token_urlsafe(32)
        config["secret_key"] = new_key
        save_config(config)
        logger.info("安全密钥已重新生成")
        messagebox.showinfo("成功", "新密钥已生成并保存！")
    root.destroy()

def quit_app(icon, item):
    logger.info("程序正在退出...")
    icon.stop()
    os._exit(0)

# --- 主程序 ---
def run_flask():
    app.run(host='127.0.0.1', port=16880, debug=False, threaded=True)

def main():
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    image = create_image()
    menu = (
        pystray.MenuItem("打开 Web UI", open_web_ui),
        pystray.MenuItem(
            "开机自动启动",
            toggle_autostart,
            checked=lambda item: is_autostart_enabled()
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("显示当前密钥", show_secret_key),
        pystray.MenuItem("重新生成密钥", regenerate_secret_key),
        pystray.MenuItem("设置 IDM 路径", set_idm_path),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", quit_app)
    )
    icon = pystray.Icon("IDM-Agent", image, "IDM 下载代理", menu)
    icon.run()
    
# pyinstaller --onefile --windowed --name IDM-Agent idm-agent-tray.py
if __name__ == '__main__':
    main()