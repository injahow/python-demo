from flask import Flask, request, jsonify
import subprocess
import os
import urllib.parse

app = Flask(__name__)

# IDM 的安装路径 (请根据你的实际安装路径修改)
IDM_PATH = r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe"

# 检查 IDM 是否存在
if not os.path.exists(IDM_PATH):
    print(f"警告: 未在默认路径找到 IDM: {IDM_PATH}")
    print("请修改 IDM_PATH 变量为你的 IDM 安装路径。")

@app.after_request
def after_request(response):
    # 允许所有来源（生产环境可限制为特定域名）
    response.headers.add('Access-Control-Allow-Origin', '*')
    # 允许的请求方法
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    # 允许的请求头
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

@app.route('/download', methods=['OPTIONS'])
def handle_options():
    return '', 200

@app.route('/download', methods=['GET', 'POST'])
def add_download():
    try:
        # 1. 获取 URL 参数
        # 支持 GET 和 POST 请求
        if request.method == 'POST':
            url = request.json.get('url') if request.is_json else request.form.get('url')
            filename = request.json.get('filename') if request.is_json else request.form.get('filename')
        else: # GET
            url = request.args.get('url')
            filename = request.args.get('filename')
        if not url:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        # URL 解码 (处理中文或特殊字符)
        url = urllib.parse.unquote(url)
        print(f"收到下载请求: {url}")
        cmd = [
            IDM_PATH,
            "/d", url
        ]
        
        if filename:
            filename = urllib.parse.unquote(filename)
            cmd.append("/f")
            cmd.append(filename)
        # 启动 IDM 进程
        subprocess.Popen(cmd)

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
    <p>示例: <a href="/download?url=https://example.com/test.zip">点击这里测试发送指令</a></p>
    """

if __name__ == '__main__':
    print("🚀 IDM 下载代理服务启动中...")
    print(f"监听地址: http://127.0.0.1:16880")
    print("按 Ctrl+C 停止服务")
    # threaded=True 允许同时处理多个请求
    app.run(host='127.0.0.1', port=16880, debug=False, threaded=True)
