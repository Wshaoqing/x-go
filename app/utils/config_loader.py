import yaml
import os

def load_config():
    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构造 config.yaml 的路径
    config_path = os.path.join(current_dir, '..', 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config