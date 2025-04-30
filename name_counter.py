from collections import Counter

def process_file(filename):
    # 存储所有提取的名字
    names = []
    
    # 读取文件并提取名字
    with open(filename, 'r') as file:
        for line in file:
            # 使用分割方法提取名字
            if '-->--' in line:
                name = line.split('-->--')[1].strip()
                names.append(name)
    
    # 使用Counter统计名字出现次数
    name_counts = Counter(names)
    
    # 找出出现次数最多的名字
    most_common = name_counts.most_common()
    
    # 打印结果
    print("\n统计结果：")
    for name, count in name_counts.items():
        print(f"{name}: {count}次")
    
    print("\n出现次数最多的是：")
    max_count = most_common[0][1]
    for name, count in most_common:
        if count == max_count:
            print(f"{name}: {count}次")

if __name__ == "__main__":
    process_file('input.txt')