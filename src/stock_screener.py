import akshare as ak
import pandas as pd
import numpy as np
import talib
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class TailTradeScreener:
    def __init__(self, config):
        self.config = config
        self.stock_data = None
        
    def get_realtime_data(self):
        """获取实时行情数据"""
        try:
            df = ak.stock_zh_a_spot_em()
            
            # 确保列名和数据一致
            required_columns = ['代码', '名称', '最新价', '涨跌幅', '涨跌额', 
                             '成交量', '成交额', '振幅', '最高', '最低', 
                             '今开', '昨收', '量比', '换手率']
            
            # 只保留需要的列
            df = df[required_columns].copy()
            
            # 确保数据类型正确
            df['最新价'] = df['最新价'].astype(float)
            df['涨跌幅'] = df['涨跌幅'].astype(float)
            df['量比'] = df['量比'].astype(float)
            
            self.stock_data = df
            return True
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return False
    
    def calculate_tail_strength(self):
        """计算尾盘强度指标"""
        if self.stock_data is None:
            return None
                
        df = self.stock_data.copy()
        
        try:
            # 数据预处理，确保数值类型正确
            numeric_columns = ['涨跌幅', '换手率', '量比', '最新价', '今开', '最高', '最低', '成交量']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 移除无效数据
            df = df.dropna(subset=numeric_columns)
            
            # 机构建仓特征
            institutional_mask = (
                (df['涨跌幅'].between(4, 7)) &
                (df['换手率'].between(3, 8)) &
                (df['量比'].between(1.5, 3)) &
                (df['最新价'] > df['今开']) &
                (df['成交量'] > 500000)
            )
            
            # 游资活跃特征
            active_trader_mask = (
                (df['涨跌幅'] > 6) &
                (df['换手率'] > 8) &
                (df['量比'] > 2.5) &
                ((df['最高'] - df['最新价']) / df['最新价'] < 0.002) &  # 改用相对价差判断
                (df['成交量'] > 800000)
            )
            
            # 综合筛选
            mask = institutional_mask | active_trader_mask
            df = df[mask].copy()
            
            if len(df) == 0:
                return None
                
            # 机构型得分计算
            df['机构型得分'] = (
                (df['换手率'].clip(3, 8) - 3) / 5 * 2 +
                (df['量比'].clip(1.5, 3) - 1.5) / 1.5 * 2 +
                df['涨跌幅'].clip(4, 7) / 7
            ).clip(0, 5)
            
            # 游资型得分计算
            df['游资型得分'] = (
                (df['换手率'].clip(8, 15) - 8) / 7 * 2 +
                (df['量比'].clip(2.5, 4) - 2.5) / 1.5 * 2 +
                df['涨跌幅'].clip(6, 8) / 8
            ).clip(0, 5)
            
            # 最终得分
            df['尾盘强度'] = df[['机构型得分', '游资型得分']].max(axis=1).round(2)
            df['操作类型'] = df.apply(lambda row: 
                '机构' if row['机构型得分'] >= row['游资型得分'] else '游资', axis=1)
            
            return df
            
        except Exception as e:
            print(f"计算得分失败: {str(e)}")
            return None
    def screen_stocks(self, min_score=0.4, min_price=5.0, max_price=100.0, 
                 min_volume=100, max_turnover=10):
        """筛选股票"""
        try:
            if not self.get_realtime_data():
                return None
                
            df = self.calculate_tail_strength()
            if df is None:
                return None
            
            # 转换数据类型
            df['换手率'] = pd.to_numeric(df['换手率'], errors='coerce')
            df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
            
            # 应用筛选条件
            mask = (
                (df['尾盘强度'] >= float(min_score)) & 
                (df['最新价'] >= float(min_price)) & 
                (df['最新价'] <= float(max_price)) &
                (df['成交量'] / 10000 >= float(min_volume)) &
                (df['换手率'] <= float(max_turnover))  # 只保留最大换手率条件
            )
            
            result = df.loc[mask].sort_values(by=['尾盘强度'], ascending=[False])
            
            columns = ['代码', '名称', '最新价', '涨跌幅', '成交量', 
                      '换手率', '量比', '振幅', '尾盘强度']
            
            return result[columns]
            
        except Exception as e:
            print(f"筛选股票失败: {str(e)}")
            return None
