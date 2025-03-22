from flask import Flask, render_template, jsonify, request
from stock_screener import TailTradeScreener
from config import ScreenerConfig
import json
import socket

app = Flask(__name__)
config = ScreenerConfig()
screener = TailTradeScreener(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stocks')
def get_stocks():
    try:
        params = {
            'min_score': float(request.args.get('min_score', 0.4)),
            'min_price': float(request.args.get('min_price', 5.0)),
            'max_price': float(request.args.get('max_price', 100.0)),
            'min_volume': float(request.args.get('min_volume', 100)),
            'max_turnover': float(request.args.get('max_turnover', 10))
        }
        
        result = screener.screen_stocks(**params)
        
        if result is None:
            return jsonify({'error': '获取数据失败'}), 500
            
        return jsonify(result.to_dict('records'))
        
    except ValueError as e:
        return jsonify({'error': '参数格式错误'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_config', methods=['POST'])
def update_config():
    data = request.json
    config.min_score = float(data.get('min_score', config.min_score))
    config.min_price = float(data.get('min_price', config.min_price))
    config.max_price = float(data.get('max_price', config.max_price))
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    ports = [8080, 8081, 8082, 3000, 3001]  # 避开系统常用端口
    
    for port in ports:
        try:
            print(f"\n尝试启动服务，端口: {port}")
            print(f"请访问: http://127.0.0.1:{port}")
            app.run(debug=True, port=port, host='0.0.0.0')
            break  # 如果成功启动就退出循环
        except OSError as e:
            print(f"端口 {port} 被占用，尝试下一个端口...")
            continue
        except Exception as e:
            print(f"启动失败: {str(e)}")
            break