#!/bin/bash

# 创建并激活虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装系统依赖
brew install ta-lib

# 安装 Python 依赖
LDFLAGS="-L/opt/homebrew/lib" CPPFLAGS="-I/opt/homebrew/include" pip3 install TA-Lib
pip3 install flask pandas numpy matplotlib seaborn akshare

# 创建必要的目录
mkdir -p src/templates output

echo "环境配置完成！"