from stock_screener import TailTradeScreener
from config import ScreenerConfig
from visualizer import StockVisualizer
import os
from datetime import datetime  # 添加这行，用于export_results函数
from flask import Flask, jsonify, request
import time

def clear_screen():
    os.system('clear')

def modify_parameters(config):
    while True:
        clear_screen()
        print("\n=== 参数设置 ===")
        print(f"1. 最小得分阈值 (当前: {config.min_score})")
        print(f"2. 最低价格 (当前: {config.min_price})")
        print(f"3. 最高价格 (当前: {config.max_price})")
        print(f"4. 最小成交量 (当前: {config.min_volume})")
        print(f"5. 技术指标权重设置")
        print("6. 返回主菜单")
        
        choice = input("\n请选择要修改的参数 (1-6): ")
        
        if choice == '1':
            config.min_score = float(input("请输入新的最小得分阈值 (0-1): "))
        elif choice == '2':
            config.min_price = float(input("请输入新的最低价格: "))
        elif choice == '3':
            config.max_price = float(input("请输入新的最高价格: "))
        elif choice == '4':
            config.min_volume = int(input("请输入新的最小成交量: "))
        elif choice == '5':
            modify_weights(config)
        elif choice == '6':
            break

def modify_weights(config):
    clear_screen()
    print("\n=== 权重设置 ===")
    for key, value in config.weights.items():
        new_value = float(input(f"请输入{key}的新权重 (当前: {value}): "))
        config.weights[key] = new_value
    
    # 归一化权重
    total = sum(config.weights.values())
    for key in config.weights:
        config.weights[key] /= total

def export_results(result):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"选股结果_{timestamp}.csv"
    result.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"\n结果已导出到: {filename}")

def show_visualization_menu(visualizer, result):
    while True:
        clear_screen()
        print("\n=== 可视化菜单 ===")
        print("1. 显示强度分布图")
        print("2. 显示Top10强势股")
        print("3. 查看单只股票技术指标")
        print("4. 保存所有图表")
        print("5. 返回主菜单")
        
        choice = input("\n请选择操作 (1-5): ")
        
        if choice == '1':
            visualizer.plot_strength_distribution(result)
        elif choice == '2':
            visualizer.plot_top_stocks(result)
        elif choice == '3':
            stock_name = input("\n请输入股票名称: ")
            visualizer.plot_indicators(result, stock_name)
        elif choice == '4':
            output_dir = '/Users/andyjames/treecode/WeiPanXuanGuV1.0/output'
            os.makedirs(output_dir, exist_ok=True)
            visualizer.save_plots(result, output_dir)
            print(f"\n图表已保存到: {output_dir}")
            input("\n按回车键继续...")
        elif choice == '5':
            break

def main():
    config = ScreenerConfig()
    screener = TailTradeScreener(config)
    visualizer = StockVisualizer()
    
    while True:
        clear_screen()
        print("\n=== 尾盘选股系统 ===")
        print("1. 执行选股")
        print("2. 修改参数")
        print("3. 导出结果")
        print("4. 查看图表")
        print("5. 退出")
        
        choice = input("\n请选择操作 (1-5): ")
        
        if choice == '1':
            clear_screen()
            print("\n正在获取数据并分析...")
            result = screener.screen_stocks()
            
            if result is not None and not result.empty:
                print("\n=== 选股结果 ===")
                print(result.to_string(index=False))
            else:
                print("\n未找到符合条件的股票")
                
            input("\n按回车键继续...")
            
        elif choice == '2':
            modify_parameters(config)
            
        elif choice == '3':
            if 'result' in locals() and result is not None:
                export_results(result)
            else:
                print("\n没有可导出的结果！")
            input("\n按回车键继续...")
            
        elif choice == '4':
            if 'result' in locals() and result is not None:
                show_visualization_menu(visualizer, result)
            else:
                print("\n没有可视化的数据！请先执行选股。")
                input("\n按回车键继续...")
                
        elif choice == '5':
            print("\n感谢使用！")
            break

@app.route('/api/stocks')
def get_stocks():
    try:
        # 获取数据
        result = screener.screen_stocks()
        
        if result is not None and not result.empty:
            # 确保涨跌幅为数值类型
            result['涨跌幅'] = result['涨跌幅'].astype(float)
            
            # 转换为字典列表，确保数据格式正确
            stocks_data = result.to_dict('records')
            
            return jsonify({
                'status': 'success',
                'data': stocks_data,
                'timestamp': time.time()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': '未找到符合条件的股票',
                'timestamp': time.time()
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }), 500

if __name__ == "__main__":
    main()