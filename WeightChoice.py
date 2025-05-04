import random as r

#加入：连锁抽取

default_dev_options = {
    'manual_operate': False,
}

   

def load_chain_config(file_path):
    try:
        chain_config = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if '##' in line:
                    names=line.split(',')[:-1]
                    if '##sin' in line:
                        chain_config[names[0]] = names[1:]
                    elif '##bot' in line:
                        for i in range(len(names)-1):
                            chain_config[names[i]] = names[i+1]
                    else:
                        return {'error':'config error'}
                else:
                    continue
        return chain_config
    except Exception as e:
        return {'error':str(e)}

def get_config():
    global ready
    with open('./config.txt','r',encoding='utf-8') as f:
        config = f.read()
        config = config.split('''\n''')
    # print(config)
    return config

def get_chain():
    global ready
    with open('./chain_config.txt','r',encoding='utf-8') as f:
        config = f.read()
        config = config.split('''\n''')

def choose(config,chosen_obj,chain_config,dev_options=default_dev_options):

    '''
    组权重配置规则
    格式：
    ##,权重,组名
    即当人名为##时，这一条配置规则为小组配置
    此时权重为对应组名的权重
    算法：
    先遍历配置规则获取每个组对应的权重，存储起来
    接着在抽签筒处理个人权重时顺带看看这个人所属的组有没有特别配置过权重
    有的话就再乘以其权重
        '''

    group_weight = {}

    for i in config:
        ii = i.split(',')
        if ii[0] == '##':
            group_weight[ii[2]] = int(ii[1])

    #ready抽签筒配置
    ready = []
    for i in config:
        ii = i.split(',') #ii为i分割后的列表，格式为名字,权重,组名
        if ii[0] != '##':#我们使用##作为组配置标识符
            if ii[0] in chosen_obj:
                continue
            else:
                if ii[2] in group_weight:
                    for j in range(int(ii[1])*group_weight[ii[2]]):
                        ready.append(i.split(',')[0])
                else:
                    for j in range(int(ii[1])):
                        ready.append(i.split(',')[0])
        else:
            continue#如果这一条是组配置，跳过不管，因为这里正在处理的是个人配置
    print(ready)#配置好了检查一下
    #chain连锁配置
    if dev_options['manual_operate'] != False:
        rNum=dev_options['manual_operate']
    else:
        if len(ready)>1:
            rNum = r.randint(0,len(ready)-1)
        else:
            rNum = 0
    '''连锁格式：
    名字1,名字2,名字3, ... ,名字N,##(sin|bot)
    (sin|bot)： sin表示单向连锁，即只有抽到了名字1才会按顺序抽下去
    bot表示双向连锁，即抽到了这些名字中任意一个都会按照顺序抽下去
    '''
    # print(load_chain_config('./chain_config.txt'))
    if ready[rNum] in chain_config:
        next = chain_config[ready[rNum]]
        if isinstance(next,list):
            next=next[0]
    else:
        next = None
    # print('next=',next)
    # print(chain_config)
    return {'Tar':ready[rNum],'Next':next}

if __name__ == '__main__':
    config = get_config()
    chain_config = load_chain_config('./chain_config.txt')
    # print(chain_config)
    # print(Choice(config=config,chosen_obj=[],chain_config=chain_config,dev_options={'manual_operate':1}))