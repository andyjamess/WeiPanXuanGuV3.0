import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

class StockVisualizer:
    def __init__(self):
        plt.style.use('seaborn')
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 解决中文显示问题
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        
    def plot_strength_distribution(self, df):
        """绘制强度分布图"""
        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='尾盘强度', bins=30)
        plt.title('股票尾盘强度分布')
        plt.xlabel('强度得分')
        plt.ylabel('数量')
        plt.show()
        
    def plot_top_stocks(self, df, top_n=10):
        """绘制前N名股票的得分对比"""
        plt.figure(figsize=(12, 6))
        top_stocks = df.head(top_n)
        sns.barplot(data=top_stocks, x='名称', y='尾盘强度')
        plt.title(f'前{top_n}支强势股票')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
    def plot_indicators(self, df, stock_name):
        """绘制单只股票的技术指标"""
        stock_data = df[df['名称'] == stock_name]
        if stock_data.empty:
            return
            
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # 绘制RSI
        ax1.plot(stock_data['RSI'], label='RSI')
        ax1.axhline(y=70, color='r', linestyle='--', alpha=0.3)
        ax1.axhline(y=30, color='g', linestyle='--', alpha=0.3)
        ax1.set_title(f'{stock_name} - RSI指标')
        ax1.legend()
        
        # 绘制MACD
        ax2.plot(stock_data['MACD'], label='MACD')
        ax2.plot(stock_data['MACD_SIGNAL'], label='Signal')
        ax2.bar(range(len(stock_data)), stock_data['MACD_HIST'], label='Histogram')
        ax2.set_title('MACD指标')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()
        
    def save_plots(self, df, output_dir):
        """保存所有图表"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 保存强度分布图
        plt.figure(figsize=(12, 6))
        sns.histplot(data=df, x='尾盘强度', bins=30)
        plt.title('股票尾盘强度分布')
        plt.savefig(f'{output_dir}/strength_distribution_{timestamp}.png')
        plt.close()
        
        # 保存top10图表
        plt.figure(figsize=(12, 6))
        top_stocks = df.head(10)
        sns.barplot(data=top_stocks, x='名称', y='尾盘强度')
        plt.title('前10支强势股票')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/top_stocks_{timestamp}.png')
        plt.close()