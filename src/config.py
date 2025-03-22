# Tushare API配置
TUSHARE_TOKEN = "你的TOKEN"

# 选股参数配置
SCREENING_PARAMS = {
    'min_score': 0.4,          # 最小尾盘强度得分
    'min_price': 5.0,          # 最低股价
    'max_price': 100.0,        # 最高股价
    'min_volume': 1000000      # 最小成交量
}


class ScreenerConfig:
    def __init__(self):
        self.min_score = 0.4
        self.min_price = 5.0
        self.max_price = 100.0
        self.min_volume = 1000000
        
        # 技术指标权重
        self.weights = {
            'volume_ratio': 0.3,    # 量比权重
            'price_speed': 0.2,     # 涨速权重
            'five_min_change': 0.2, # 5分钟涨跌权重
            'macd': 0.15,          # MACD权重
            'rsi': 0.15            # RSI权重
        }
        
        # 技术指标参数
        self.tech_params = {
            'rsi_period': 14,
            'macd_fast': 12,
            'macd_slow': 26,
            'macd_signal': 9
        }