
import json
from pathlib import Path

def process_data():
    # 文件路径配置
    input_file = 'data.json'
    output_file = 'historical_data.json'
    
    # 读取新数据
    try:
        with open(input_file, 'r') as f:
            new_data = json.load(f)
    except FileNotFoundError:
        print(f"错误：输入文件 {input_file} 不存在")
        return

    # 初始化历史数据
    historical_data = {'records': []}
    if Path(output_file).exists():
        with open(output_file, 'r') as f:
            historical_data = json.load(f)

    # 检查时间戳是否有变化
    if historical_data['records'] and \
       new_data['timestamp'] == historical_data['records'][-1]['timestamp']:
        print("数据未更新，跳过存储")
        return

    # 添加新记录并限制数量
    historical_data['records'].append({
        'timestamp': new_data['timestamp'],
        'marketData': new_data['marketData']
    })
    historical_data['records'] = historical_data['records'][-4:]  # 保留最近4条

    # 保存结果
    with open(output_file, 'w') as f:
        json.dump(historical_data, f, indent=2)
    print(f"成功保存新数据，当前记录数：{len(historical_data['records'])}")

if __name__ == '__main__':
    process_data()
