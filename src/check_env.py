import sys
import importlib

def check_module(module_name):
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} 已安装")
        return True
    except ImportError:
        print(f"❌ {module_name} 未安装")
        return False

def main():
    modules = ['flask', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'akshare']
    all_installed = all(check_module(m) for m in modules)
    
    if all_installed:
        print("\n所有依赖已正确安装！")
    else:
        print("\n请运行以下命令安装缺失的依赖：")
        print("pip3 install flask pandas numpy matplotlib seaborn akshare")

if __name__ == "__main__":
    main()