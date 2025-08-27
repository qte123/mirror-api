"""
镜子API (Mirror/Echo API)
功能：接收任何HTTP请求，并返回请求的详细信息，用于调试和测试。
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime

# 创建Flask应用实例
app = Flask(__name__)

# 根路径：显示美观的API文档页面
@app.route('/', methods=['GET'])
def api_documentation():
    """
    API详细说明页面 - 返回美观的HTML页面
    """
    # 只需要传递时间戳，其他所有显示内容都在HTML中
    return render_template('index.html', timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# API信息端点（返回JSON格式）
@app.route('/info', methods=['GET'])
def api_info():
    """
    API信息端点 - 返回JSON格式的API信息
    """
    return jsonify({
        'api': '🔍 Mirror API - 请求镜子',
        'version': '1.0.0',
        'description': '一个用于调试和测试的API，可以返回 incoming 请求的详细信息',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            '/mirror': '简洁版镜像端点',
            '/mirror/detail': '详细版镜像端点',
            '/health': '健康检查',
            '/info': 'API信息',
            '/': 'API文档页面'
        },
        'message': '访问根路径 / 查看美观的文档页面'
    }), 200


# 简洁镜像端点：/mirror
@app.route('/mirror', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def mirror_simple():
    """
    简洁镜像端点 - 返回核心的请求信息，格式简洁
    """
    current_time = datetime.now().isoformat()
    mirror_data = {
        'status': 'success',
        'timestamp': current_time,
        'endpoint': '/mirror',
        'description': '简洁版请求信息',
        'request': {
            'method': request.method,
            'url': request.url,
            'path': request.path,
            'query_params': dict(request.args),
        },
        'headers': {
            'content_type': request.headers.get('Content-Type'),
            'user_agent': request.headers.get('User-Agent'),
            'authorization': request.headers.get('Authorization'),
            'accept': request.headers.get('Accept'),
            'host': request.headers.get('Host'),
        },
        'data_summary': {
            'has_json': request.is_json,
            'has_form_data': bool(request.form),
            'has_query_params': bool(request.args),
            'body_length': len(request.get_data(as_text=True))
        },
        'client': {
            'ip_address': request.remote_addr,
        }
    }
    if request.is_json:
        json_data = request.get_json(silent=True)
        if json_data:
            mirror_data['data_summary']['json_sample'] = str(json_data)[:100] + '...' if len(str(json_data)) > 100 else str(json_data)
    mirror_data['headers'] = {k: v for k, v in mirror_data['headers'].items() if v}
    return jsonify(mirror_data), 200


# 详细镜像端点：/mirror/detail
@app.route('/mirror/detail', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD'])
def mirror_detail():
    """
    详细镜像端点 - 返回完整的请求详细信息
    """
    current_time = datetime.now().isoformat()
    mirror_data = {
        'status': 'success',
        'timestamp': current_time,
        'endpoint': '/mirror/detail',
        'description': '详细版请求信息',
        'request': {
            'method': request.method,
            'url': request.url,
            'path': request.path,
            'full_path': request.full_path,
            'base_url': request.base_url,
            'host': request.host,
            'host_url': request.host_url,
        },
        'headers': dict(request.headers),
        'query_params': dict(request.args),
        'form_data': dict(request.form),
        'json_data': request.get_json(silent=True) or {},
        'raw_body': request.get_data(as_text=True),
        'cookies': dict(request.cookies),
        'client': {
            'ip_address': request.remote_addr,
            'user_agent': request.user_agent.string,
            'remote_port': request.environ.get('REMOTE_PORT'),
        },
        'server': {
            'server_name': request.environ.get('SERVER_NAME'),
            'server_port': request.environ.get('SERVER_PORT'),
            'request_scheme': request.scheme,
        },
        'statistics': {
            'headers_count': len(request.headers),
            'query_params_count': len(request.args),
            'form_fields_count': len(request.form),
            'cookies_count': len(request.cookies),
            'body_size_bytes': len(request.get_data()),
            'body_size_chars': len(request.get_data(as_text=True)),
        }
    }
    try:
        if request.is_json:
            mirror_data['json_parsed'] = request.get_json()
    except Exception as e:
        mirror_data['json_error'] = f'Invalid JSON data: {str(e)}'
    return jsonify(mirror_data), 200


# 健康检查端点
@app.route('/health', methods=['GET'])
def health_check():
    """
    健康检查端点
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Mirror API is running normally',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'mirror_simple': '/mirror - 简洁版请求信息',
            'mirror_detail': '/mirror/detail - 详细版请求信息',
            'health': '/health - 健康检查',
            'info': '/info - API信息',
            'root': '/ - API文档页面'
        }
    }), 200


# 错误处理
@app.errorhandler(404)
def not_found(error):
    """
    处理404错误
    """
    return jsonify({
        'status': 'error',
        'error': 'Not found',
        'message': '请求的端点不存在，请检查URL是否正确。',
        'timestamp': datetime.now().isoformat(),
        'available_endpoints': [
            {'path': '/', 'description': 'API文档页面'},
            {'path': '/mirror', 'description': '简洁版镜像端点'},
            {'path': '/mirror/detail', 'description': '详细版镜像端点'},
            {'path': '/health', 'description': '健康检查'},
            {'path': '/info', 'description': 'API信息'}
        ],
        'suggestion': '请访问根路径 / 查看完整的API文档'
    }), 404


# 主程序入口
if __name__ == '__main__':
    """
    启动Flask开发服务器
    """
    print("🌐 Mirror API Server Starting...")
    print("=" * 50)
    print("🔗 Server URLs:")
    print("   📍 http://127.0.0.1:5000")
    print("   📍 http://localhost:5000")
    print("\n📂 Available Endpoints:")
    print("   📄 /              - API文档页面 (美观HTML)")
    print("   🪞 /mirror        - 简洁版请求镜像 (JSON)")
    print("   🔍 /mirror/detail  - 详细版请求镜像 (JSON)")
    print("   ❤️  /health        - 健康检查 (JSON)")
    print("   ℹ️  /info          - API信息 (JSON)")
    print("\n🚀 Quick Start:")
    print("   直接在浏览器中访问: http://localhost:5000/")
    print("   或者使用curl测试: curl \"http://localhost:5000/mirror?test=hello\"")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)

    # 启动服务器
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )