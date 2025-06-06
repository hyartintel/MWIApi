
import json
from pathlib import Path
from collections import defaultdict

def calculate_avg(values):
    """计算有效值的平均值（忽略-1）"""
    filtered = [v for v in values if v != -1]
    return -1 if not filtered else round(sum(filtered)/len(filtered), 2)

def process_data():
    # 文件路径配置
    input_file = 'data_test.json'
    output_file = 'historical_data_test.json'
    
    # 读取新数据
    try:
        with open(input_file, 'r') as f:
            new_data = json.load(f)
    except FileNotFoundError:
        print(f"错误：输入文件 {input_file} 不存在")
        return

    # 初始化历史数据
    historical_data = {'records': [], 'median': {}}
    if Path(output_file).exists():
        with open(output_file, 'r') as f:
            historical_data = json.load(f)

    # 检查时间戳是否有变化
    if historical_data['records'] and \
       new_data['timestamp'] == historical_data['records'][-1]['timestamp']:
        print("数据未更新，跳过存储")
        return

    # 添加新记录
    historical_data['records'].append({
        'timestamp': new_data['timestamp'],
        'marketData': new_data['marketData']
    })
    historical_data['records'] = historical_data['records'][-4:]  # 保留最近4条

    # 计算各项指标的平均值
    avg_data = defaultdict(lambda: defaultdict(lambda: {'a': [], 'b': []}))
    
    for record in historical_data['records']:
        for item_path, item_data in record['marketData'].items():
            for sub_key, values in item_data.items():
                if 'a' in values:
                    avg_data[item_path][sub_key]['a'].append(values['a'])
                if 'b' in values:
                    avg_data[item_path][sub_key]['b'].append(values['b'])

    # 构建median数据结构
    historical_data['median'] = {}
    for item_path, sub_items in avg_data.items():
        historical_data['median'][item_path] = {}
        for sub_key, values in sub_items.items():
            historical_data['median'][item_path][sub_key] = {
                'a': calculate_avg(values['a']),
                'b': calculate_avg(values['b'])
            }

    # 保存结果
    with open(output_file, 'w') as f:
        json.dump(historical_data, f, indent=2)
    print(f"成功保存新数据，当前记录数：{len(historical_data['records'])}")

if __name__ == '__main__':
    process_data()
