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
    #ready抽签筒配置
    ready = []
    for i in config:
        if i.split(',')[0] in chosen_obj:
            continue
        else:
            for j in range(int(i.split(',')[1])):
                ready.append(i.split(',')[0])

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