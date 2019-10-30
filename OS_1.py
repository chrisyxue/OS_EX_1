import numpy as np
import pandas as pd
import random

#加载Test Shell文件
def load_txt(path):
    data = pd.read_table(path,header=None)
    return data

"""
小工具函数，比较两个具有相同Key的字典元素a和b
若 a-b 后所有value都大于0，则表示a能吃下b,返回True
否则返回False 
"""
def compare_dict(a,b):
    temp = a.copy()
    for i in temp.keys():
        temp[i] = temp[i] - b[i]
    # 检查是否所有value都大于0
    for value in temp.values():
        if value<0:
            return False
    return True


class PCB():
    # PCB的构造函数 
    def __init__(self,name,priority,status,ID,Parent=None,Brother=None,num_source = {"R1":0,"R2":0,"R3":0,"R4":0},block_req = {"R1":0,"R2":0,"R3":0,"R4":0}):
        self.name = name
        self.priority = priority # 进程的优先级,0,1,2
        self.status = status # 进程的状态，分为ready,block and running
        self.ID = ID #进程的ID号
        self.Parent = Parent #父进程
        self.Brother = Brother #子进程
        self.num_source = num_source #一个字典，表示该进程所占有的资源量
        self.block_req = block_req #一个字典，表示该进程阻塞是，所需要的资源量

    # 修改进程的状态
    def Change_Status(self,sta):
        self.status = sta


# 调度进程（ready队列）
def Scheduler(ready_list):
    # 若有两个以上的进程 
    if len(ready_list)>=2:
        begin = len(ready_list)-1 # 最后一个元素的位置
        while ready_list[begin].priority > ready_list[begin-1].priority&begin>0: # 找到第一个优先级和它一样的 
            tmp = ready_list[begin]
            ready_list[begin] = ready_list[begin-1]
            ready_list[begin-1] = tmp
        return ready_list 
    # 若只有一个或者没有进程
    else:
        # print("There is only one or none process")
        return ready_list

# 调度进程（block队列）
def Scheduler_block(block_list):
    # 若有一个以上的进程 
    if len(block_list)>=2:
        begin = len(block_list)-1 # 最后一个元素的位置
        while block_list[begin].priority > block_list[begin-1].priority&begin>0: # 找到第一个优先级和它一样的 
            tmp = block_list[begin]
            block_list[begin] = block_list[begin-1]
            block_list[begin-1] = tmp
        return block_list
    # 若只有一个或者没有进程
    else:
        # print("There is only one or none process")
        return block_list



# 终断时间
def Time_Out(ready_list):
    if len(ready_list) >= 2:
        pro = ready_list[0] #查看当前需要运行的进程
        pro.status = "ready" #修改状态
        ready_list.remove(ready_list[0]) #删除头元素
        ready_list[0].status = "run" #修改状态
        #print(ready_list[0].name) #打印需要阻塞的进程的名字
        ready_list.append(pro) # 调到尾巴上去
        
        # 按照优先级排序
        ready_list = Scheduler(ready_list)
        ready_list[0].status = "running" # 修改状态 
    else:
        pass # 只有一个进程time_out还是它自己在跑
    return ready_list
    # return ready_list


# 创建进程
def CrePro(ready_list,name,priority,status,ID):
    # ready_list = ready_list.copy()
    # 若不是初始化 
    if len(ready_list) > 0:
        Parent = ready_list[0] # 正在运行的进程作为父进程 
        a = {"R1":0,"R2":0,"R3":0,"R4":0}
        b = {"R1":0,"R2":0,"R3":0,"R4":0}
        pro = PCB(name,priority,status,ID,Parent=Parent,num_source=a,block_req=b) # 创建PCB
        ready_list.append(pro) # 加入队列
        # 按照优先级排序，Scheduler
        if len(ready_list) >= 2:
            ready_list = Scheduler(ready_list)
        ready_list[0].status = "running" # 修改状态 
        ready_list = ready_list.copy()
        print(ready_list[0].name) # 输出当前所运行的进程 
        return ready_list
    
    # 若是初始化
    else:
        pro = PCB(name,priority,status,ID)
        ready_list.append(pro)
        ready_list[0].status = "running" # 修改状态
        print("init",ready_list[0].name)
        return ready_list



# 资源索要 req代表一个要求的量，为一个字典，只有一个元素. name为索要进程的名字
def request_source(ready_list,Resources,block_list,req):
    name = list(req.keys())[0] # 索要资源的名字
    num_req = list(req.values())[0] # 索要该资源的数量
    num_have = Resources[name] # 该资源的还拥有的量
    ready_list = ready_list.copy()
    # 如果ready列表里还有进程 
    if len(ready_list) > 0:
        run_process = ready_list[0]
        #print(run_process.name)
        # 当资源能够满足的时候 
        if num_req <= num_have:
            # 分配资源
            ready_list[0].num_source[name] = ready_list[0].num_source[name] + num_req # 该进程内部加上占有的资源
            #print(ready_list[1].num_source)
            Resources[name] = num_have - num_req # 资源列表减去占有的资源
            # ready_list[0] = run_process # 赋予
            #print(ready_list[0].name) # 打印正在运行的进程 
            return ready_list,Resources,block_list

        # 当资源不满足的时候
        else:
            # 阻塞进程 
            run_process.block_req[name] = num_req # 该进程内部加上阻塞需要的资源
            run_process.status = "block" # 修改状态
            ready_list.remove(ready_list[0]) # 从ready队列中移除
            ready_list[0].status = "running" # 让后一个进程跑起来
            block_list.append(run_process) # 加入block队列
            block_list = Scheduler_block(block_list) # 调度block队列
            #print(ready_list[0].name) # 打印正在运行的进程 
            return ready_list,Resources,block_list

    else: 
        print("No Process is running")
        return ready_list,Resources,block_list

# 扫描一遍block队列，看有没有能加入ready队列中的
def Scan_block(ready_list,block_list,Resources):
    block_list_copy = block_list.copy()
    for pro in block_list_copy:
        # 如果Resource能吃得下
        if compare_dict(Resources,pro.block_req) == True:
            block_list.remove(pro) # 从block队列中删除
            pro.status = "ready" # 修改状态
            # 占有资源
            for i in pro.block_req.keys():
                Resources[i] = Resources[i] - pro.block_req[i]
                pro.num_source[i] = pro.num_source[i] + pro.block_req[i]
                pro.block_req[i] = 0 

            ready_list.append(pro) # 加入到ready队列
            ready_list = Scheduler(ready_list) # 维护ready队列
    return ready_list,block_list,Resources

# 释放进程，name为资源的名字,num为需要释放的资源量
def rel_resource(ready_list,block_list,Resources,name,num):
    # 遍历ready_list
    for pro in ready_list:
        # 释放资源
        num_release = pro.num_source[name]

        # 两种情况
        if num >= num_release:
            pro.num_source[name] = 0
            Resources[name] += num_release
            num = num - num_release
        else:
            pro.num_source[name] = pro.num_source[name] - num
            Resources[name] += num
            num = 0
    # 扫描Block，看是否有进程可以变成ready
    ready_list,block_list,Resources = Scan_block(ready_list,block_list,Resources)
    return ready_list,block_list,Resources


# 删除一个进程, del_name为一个字符串
def del_pro(ready_list,Resources,block_list,del_name):
    
    # 如果该进程在ready队列中
    for i in range(len(ready_list)):
        if ready_list[i].name == del_name: # 找到该进程在ready队列中的位置
            del_pro = ready_list[i]

            # 释放该进程所占有的资源 
            release_source = del_pro.num_source
            for j in release_source.keys():
                Resources[j] += release_source[j]

            ready_list.remove(ready_list[i]) # 把该进程从ready队列中移出来
            ready_list,block_list,Resources = Scan_block(ready_list,block_list,Resources) # 扫描一遍block队列
            ready_list[0].status = "running"
            return ready_list,Resources,block_list

    # 如果该进程在block队列中
    for i in range(len(block_list)):
        if block_list[i].name == del_name:
            del_pro = block_list[i]
            release_source = del_pro.num_source
            for j in release_source.keys():
                Resources[j] += release_source[j]
            block_list.remove(block_list[i])
            ready_list,block_list,Resources = Scan_block(ready_list,block_list,Resources) # 扫描一遍block队列
            return ready_list,Resources,block_list

#初始化系统资源队列
def init_resources(Resources):
    Resources["R1"] = 1
    Resources["R2"] = 2
    Resources["R3"] = 3
    Resources["R4"] = 4
    return Resources

# 打印ready队列和block队列的所有进程信息 
def list_all_processes(ready_list,block_list):
    print("===========Processes(Ready)============")
    for pro in ready_list:
        print(pro.name,pro.status,pro.priority,pro.block_req,pro.num_source)
    print("===========Processes(Block)============")
    for pro in block_list:
        print(pro.name,pro.status,pro.priority,pro.block_req,pro.num_source)
    print("\n")

# 打印资源列表
def list_all_resources(Resoueces):
    print("++++++++++++Resoueces+++++++++++++")
    print(Resoueces) 
    print("\n")

# 打印某个给定进程的信息
def print_process(ready_list,block_list,name):
    for pro in ready_list:
        if pro.name == name:
            print(name)
            print("ID",pro.ID)
            print("Priority",pro.priority)
            print("Status",pro.status)
            print("Parent",pro.Parent.name)
            return 0
    for pro in block_list:
        if pro.name == name:
            print(name)
            print("ID",pro.ID)
            print("Priority",pro.priority)
            print("Status",pro.status)
            print("Parent",pro.Parent.name)
            return 0


# 主函数
def main():
    ready_list,block_list = [],[] #定义ready和block的两个队列，用列表来表示
    Resources = {} #定义一个系统资源队列，用字典
    Resources = init_resources(Resources) #初始化资源队列
    print(Resources)
    data = load_txt("C:\\Users\\del\\Desktop\\input.txt") # 读取指令
    """执行指令"""
    for i in data.index:
        command = data.loc[i,0]
        # print(command.split(" "))
        command = command.split(" ")

        # cr命令
        if command[0] == "cr":
            ready_list = CrePro(ready_list,name=command[1],priority=int(command[2]),ID=random.randint(1,500),status="ready")
            #print(Resources)
            list_all_processes(ready_list,block_list)
        # to 命令
        elif command[0] == "to":
            ready_list = Time_Out(ready_list)
            print(ready_list[0].name)
            #print(Resources)
            list_all_processes(ready_list,block_list)

        # req 命令 
        elif command[0] == "req":
            req = {}
            req[command[1]] = int(command[2])
            #print(Resources)
            ready_list,Resources,block_list = request_source(ready_list,Resources,block_list,req)
            print(ready_list[0].name)
            list_all_processes(ready_list,block_list)
        
        # rel命令
        elif command[0] == "rel":
            name = command[1]
            num = int(command[2])
            ready_list,block_list,Resources = rel_resource(ready_list,block_list,Resources,name,num)

        # de 命令
        elif command[0] == "de":
            ready_list,Resources,block_list = del_pro(ready_list,Resources,block_list,command[1])
            #print(ready_list[0].name)
            #print(block_list)
            #print(Resources)
            print(ready_list[0].name)
            list_all_processes(ready_list,block_list)
            #print(block_list)
        
        # list_pro 命令
        elif command[0] == "list_pro":
            list_all_processes(ready_list,block_list)
        
        # list_res 命令
        elif command[0] == "list_res":
            list_all_resources(Resoueces)

        # show 命令
        elif command[0] == "show":
            signal = print_process(ready_list,block_list,name)



if __name__ == "__main__":
    main()

