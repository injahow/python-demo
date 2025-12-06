# idm-agent-tray.py
import os
import sys
import subprocess
import urllib.parse
import webbrowser
from threading import Thread
from flask import Flask, request, jsonify

# --- 系统托盘相关 ---
import pystray
from PIL import Image, ImageDraw
import winreg as reg

# --- Flask App（原逻辑）---
app = Flask(__name__)
IDM_PATH = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"

if not os.path.exists(IDM_PATH):
    print(f"警告: 未在默认路径找到 IDM: {IDM_PATH}")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

@app.route('/download', methods=['OPTIONS'])
def handle_options():
    return '', 200

@app.route('/download', methods=['GET', 'POST'])
def add_download():
    try:
        if request.method == 'POST':
            url = request.json.get('url') if request.is_json else request.form.get('url')
            filename = request.json.get('filename') if request.is_json else request.form.get('filename')
        else:
            url = request.args.get('url')
            filename = request.args.get('filename')

        if not url:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        url = urllib.parse.unquote(url)
        print(f"收到下载请求: {url}")

        cmd = [IDM_PATH, "/d", url]
        if filename:
            filename = urllib.parse.unquote(filename)
            cmd.extend(["/f", filename])

        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW)
        return jsonify({"code": 0, "message": "指令已发送给 IDM"}), 200
    except Exception as e:
        error_msg = str(e)
        print(f"错误: {error_msg}")
        return jsonify({"error": f"IDM 启动失败: {error_msg}"}), 500

@app.route('/')
def index():
    return """
    <h1>IDM 下载代理服务</h1>
    <p>服务正在运行。请通过发送 POST 或 GET 请求到 <code>/download?url=你的链接</code> 来使用。</p>
    """

# --- 工具函数 ---
def create_image():
    # 创建一个简单的托盘图标（白色背景 + 黑色圆圈）
    width, height = 64, 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    dc = ImageDraw.Draw(image)
    dc.ellipse((16, 16, 48, 48), fill=(0, 0, 0))
    return image

def is_autostart_enabled():
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_READ)
        value, _ = reg.QueryValueEx(key, "IDM-Agent")
        reg.CloseKey(key)
        return os.path.abspath(sys.executable) in value
    except FileNotFoundError:
        return False

def set_autostart(enable=True):
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_WRITE)
    if enable:
        reg.SetValueEx(key, "IDM-Agent", 0, reg.REG_SZ, os.path.abspath(sys.executable))
    else:
        try:
            reg.DeleteValue(key, "IDM-Agent")
        except FileNotFoundError:
            pass
    reg.CloseKey(key)

def open_web_ui(icon, item):
    webbrowser.open("http://127.0.0.1:16880")

def toggle_autostart(icon, item):
    current = is_autostart_enabled()
    set_autostart(not current)

def quit_app(icon, item):
    icon.stop()
    os._exit(0)

# --- 主程序 ---
def run_flask():
    app.run(host='127.0.0.1', port=16880, debug=False, threaded=True)

def main():
    # 启动 Flask 在后台线程
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 创建托盘图标
    image = create_image()
    menu = (
        pystray.MenuItem("打开 Web UI", open_web_ui),
        pystray.MenuItem(
            "开机自动启动",
            toggle_autostart,
            checked=lambda item: is_autostart_enabled()
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("退出", quit_app)
    )
    icon = pystray.Icon("IDM-Agent", image, "IDM 下载代理", menu)
    icon.run()

if __name__ == '__main__':
    main()