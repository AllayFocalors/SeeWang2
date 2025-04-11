print(r'''                                                                                                                  
SSSSSSSSSSSS       WWW         WWW         22222222
SSSSSSSSSSSSSS     WWW         WWW      22222222222222
SSS        SSS     WWW         WWW    2222          2222 
SSS                WWW         WWW    222           2222 
SSS                WWW         WWW                 2222  
SSSSSSSSSSSSSS     WWW    W    WWW                2222
SSSSSSSSSSSSSS     WWW   WWW   WWW               2222
           SSS     WWW   WWW   WWW             2222
           SSS     WWW  WWWWW  WWW            2222
SSS        SSS     WWW   WWW   WWW          2222         2
SSSSSSSSSSSSSS     wWWW  WWW  WWWw       222222        222   
  SSSSSSSSSSSS     wwWWWWWWWWWWWww    22222222222222222222  
----AllayCloud 2025----
  >By AllayFocalors
''')

import tkinter as tk
from PIL import Image, ImageTk
import random as r
import time as t
import WeightChoice as wc
import os
import threading
import time
from tkinter import messagebox
from tkinter import ttk
from ffpyplayer.player import MediaPlayer

main_font_size = 140
next_obj = []
win = tk.Tk()
style = ttk.Style()
style.theme_use('clam')
obj_list = []
chosen_obj = []
os.environ['FFMPEG_HWACCEL'] = 'auto'
chain_info = None
# #chain_info是存储chain信息的列表，防止和chain_config.txt混淆

def GetConfig():
    return wc.GetConfig()

class VideoPlayTk:
    # 初始化函数
    def __init__(self, root,filepath):
        self.root = root
 
        # 创建一个画布用于显示视频帧
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.place(x=0, y=0, width=root.winfo_width(), height=root.winfo_height())
        self.player = MediaPlayer(filepath, ff_opts={'hwaccel': 'auto'})

        # 初始化播放器和播放状态标
        self.is_stopped = False
        self.is_paused = False
        # self.thread = threading.Thread(target=self.play_video_thread)
        self.play_video_thread()
        self.root.update()
        # self.thread.daemon = True
        # self.thread.start()
    
    def play_video_thread(self):
        def update_frame():
            if not self.is_stopped:
                frame, val = self.player.get_frame()
                if val == 'eof':
                    self.StopAnimation()
                elif frame is not None:
                    image, pts = frame
                    self.update_canvas(image)
                if not self.is_paused and val is not None:
                    win.after(int(val * 1000), update_frame)
        update_frame()

    def StopAnimation(self):
        self.is_stopped = True
        self.canvas.place_forget()
        if self.player:
            self.player.close_player()
            self.player = None  # 如果停止播放，则释放播放器资源
        if hasattr(self, 'canvas_image'):
            del self.canvas_image

    def update_canvas(self, image):
        canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        img = Image.frombytes("RGB", image.get_size(), bytes(image.to_bytearray()[0]))
        img = img.resize((canvas_width, canvas_height), Image.NEAREST)  # 使用最近邻插值
        photo = ImageTk.PhotoImage(image=img)###
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.canvas.image = photo

def writeLog(res):
    with open('res.txt',mode='a',encoding='utf-8') as file:
        file.write(time.asctime()+' -->-- '+res+'\n')

def PlayAnimation(filepath):

    app = VideoPlayTk(win, filepath)
    win.after(5700, app.StopAnimation)

def ShowAbout():
    abt = tk.Toplevel(win)
    abt.title('希王点名由悦灵云工作室开发')

    def load_images():
        try:
            Img_StudioLogo = ImageTk.PhotoImage(Image.open("StudioLogo.png").resize((512,200),Image.LANCZOS))
            Lab_StudioLogoShow = tk.Label(abt,image=Img_StudioLogo)
            Img_AppLogo = ImageTk.PhotoImage(Image.open("SeeWangLogo-new.png").resize((512,256),Image.LANCZOS))
            Lab_AppLogoShow = tk.Label(abt,image=Img_AppLogo)
            Lab_StudioLogoShow.image = Img_StudioLogo
            Lab_AppLogoShow.image = Img_AppLogo
            Lab_StudioLogoShow.pack()
            Lab_AppLogoShow.pack()
        except Exception as e:
            print(e)
    abt.after(1000,load_images)

win.geometry("1500x700+0+5")
win.title('希王点名系统')

animation=False

MainTitle_color = '#5982ff'

def changeAnimation():
    global animation
    if animation:
        animation=False
        But_AnimationOn.config(text='🔳已禁用动画')
    else:
        animation=True
        But_AnimationOn.config(text='🔲已启用动画')

def ShowWeightSettings():
    os.system(f'start notepad ./config.txt')

def ShowChainSettings():
    os.system(f'start notepad ./chain_config.txt')

Lab_chosen_obj = tk.Label(win,text="已抽学生：",font=("MiSans VF",15),wraplength=800)
Lab_Number = tk.Label(win,text="找抽",font=("MiSans VF Bold",main_font_size),wraplength=int(win.winfo_width()))

def RefreshWeight():
    global config,Lab_chosen_obj
    config = wc.GetConfig()
    messagebox.showinfo('权重配置成功',f'已加载{len(config)}条权重配置')

RefreshWeight()

But_RefreshWeight = tk.Button(win,text="刷新",font=("MiSans VF regular",15),command=RefreshWeight,border=1)

def reset():
    '''obj_list就是所有学生的名单，一人一个不重复'''
    global obj_list,chosen_obj,config,stu_Quantity,Lab_chosen_obj
    obj_list = []
    chosen_obj = []
    for i in config:
        obj_list.append(i.split(',')[0])
    stu_Quantity = len(obj_list)
    Lab_chosen_obj.config(text=str(f'重置完成'))
    Lab_Number.config(text="找抽",wraplength=int(win.winfo_width()))

def SingleChoose():
    '''由于ChooseOne,ChooseThree,ChooseN的逻辑过于臃肿，所以打算都调用这个singlechoose函数'''
    global config
    if len(next_obj)==0:#nextobj列表中没人，说明没有触发连锁
        obj = wc.Choice(config=config,chosen_obj=chosen_obj,chain_config=chain_info)
        Tar = obj['Tar']
        Next = obj['Next']
        print(f'Tar={Tar},Next={Next},')
        while Next in chain_info:#说明这个obj有next，触发了连锁
            if not Next in chosen_obj:#说明这个东西连锁的next也没抽过
                next_obj.insert(0,Next)
                print(f'Next={Next},next_obj={next_obj}')
            Next=chain_info[Next]#获取next的next
        if (not Next in chosen_obj) and Next != None:#循环完成后再来一遍，因为尾巴上的人是不作为字典的key的，所以要再判断一遍。如果删了这个语句的话，最后尾巴上的人会被忽略。
            next_obj.insert(0,Next)
            print(f'Next={Next},next_obj={next_obj}')

        Next = obj['Next']
    else:#next_obj中有人，说明触发了连锁，且下一个人是安排好的
        Tar = next_obj.pop()
        Next = None
    return Tar,Next
    
                    
    

def find_keys_by_value(d, value):
    keys = [k for k, v in d.items() if v == value]
    return keys

def ChooseOne():
    global config,animation
    if animation:
        PlayAnimation('V1lower.mp4')
    if len(chosen_obj) < stu_Quantity:
        Tar,Next = SingleChoose()
        print(f'Tar={Tar},next={Next},next_obj={next_obj}')
        obj_list.remove(Tar)
        chosen_obj.append(Tar)
        Lab_Number.config(text=str(Tar),fg=MainTitle_color)
        Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(chosen_obj)}'))   
        writeLog(Tar)
    else:
        whether_reset = messagebox.askokcancel('人不够了',f'人不够了，是否重置？')
        if whether_reset:
            resetAll()

def ChooseN():
    global stu_Quantity
    if animation:
        PlayAnimation('V2low.mp4')
    if int(Ent_N.get())>=15:
        messagebox.showwarning('太多了',f'搁着周处除{Ent_N.get()}害呢')
    else:
        if len(chosen_obj) < stu_Quantity-int(Ent_N.get())+1:
            res=''
            for i in range(int(Ent_N.get())):
                Tar,Next = SingleChoose()
                print(f'Tar={Tar},next={Next},next_obj={next_obj}')
                obj_list.remove(Tar)
                chosen_obj.append(Tar)
                res+=str(Tar)+' '
            Lab_Number.config(text=str(res),fg=MainTitle_color)
            Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(chosen_obj)}'))   
            writeLog(res)
        else:
            messagebox.showwarning('人不够了',f'抽不了这么多')

def ChooseThree():
    global stu_Quantity
    if animation:
        PlayAnimation('V2low.mp4')
    if len(chosen_obj) < stu_Quantity-2:
        res=''
        for i in range(3):
            Tar,Next = SingleChoose()
            print(f'Tar={Tar},next={Next},next_obj={next_obj}')
            obj_list.remove(Tar)
            chosen_obj.append(Tar)
            res+=str(Tar)+' '
        Lab_Number.config(text=str(res),fg=MainTitle_color)
        Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(chosen_obj)}'))   
        writeLog(res)
    else:
        messagebox.showwarning('人不够了',f'抽不了这么多')

def update_Lab_Number_wraplength(event):
    Lab_Number.config(wraplength=win.winfo_width(),font=("MiSans VF",int(win.winfo_width()/14)))
    # print(f'winfo-height={win.winfo_height()},h={win.winfo_height()/1017*2}')
    But_ChoiseOne.config(font=("MiSans VF",int(win.winfo_width()/70-5)))
    But_ChooseThree.config(font=("MiSans VF",int(win.winfo_width()/70-5)))
    But_ChooseN.config(font=("MiSans VF",int(win.winfo_width()/70-5)))

def SmallMode():
    Small()

class Small:
    def ChooseOne_small(self):
        global config,animation,Lab_Number_s,Lab_chosen_obj_s
        if len(chosen_obj) < stu_Quantity:
            Tar = wc.Choice(config,chosen_obj,stu_Quantity)
            # print(f'Tar={Tar},obj_list={obj_list}')
            obj_list.remove(Tar)
            chosen_obj.append(Tar)
            Lab_Number_s.config(text=str(Tar),fg=MainTitle_color)
            Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(chosen_obj)}'))   

            writeLog(Tar)
        else:
            whether_reset = messagebox.askokcancel('人不够了',f'人不够了，是否重置？')
            if whether_reset:
                reset()

    def update_Lab_Number_s_wraplength(self,event):
        Lab_Number_s.config(wraplength=self.smallwindow.winfo_width(),font=("MiSans VF demibold",int(self.smallwindow.winfo_width()/5)))
        # print(f'winfo-height={win.winfo_height()},h={win.winfo_height()/1017*2}')
    
    def __init__(self):
        global Lab_Number_s,But_ChoiseOne_s,But_ChooseThree_s,But_ChooseN_s,win,smallwindow
        self.smallwindow = tk.Toplevel(win)
        self.smallwindow.bind('<Configure>', self.update_Lab_Number_s_wraplength)
        self.smallwindow.geometry('400x200')
        self.smallwindow.title('希王小窗')
        self.smallwindow.attributes('-topmost', True) 
        Lab_Number_s = tk.Label(self.smallwindow,text="找抽",font=("MiSans VF demibold",int(self.smallwindow.winfo_width()/20)),wraplength=int(self.smallwindow.winfo_width()))
        But_ChoiseOne_s = tk.Button(self.smallwindow,text="单抽",font=("MiSans VF medium",15),border=1,command=self.ChooseOne_small)
        Lab_Number_s.pack()
        But_ChoiseOne_s.pack()

def CheckChainSettings():
    global config,chain_info
    chain_info = wc.load_chain_config('chain_config.txt')
    if 'error' in chain_info:
        messagebox.showerror('错误',chain_info['error'])
    else:
        messagebox.showinfo('连锁配置成功',f'已加载{len(chain_info)}条连锁配置')

CheckChainSettings()
win.bind('<Configure>', update_Lab_Number_wraplength)

But_ChoiseOne = tk.Button(win,text="单抽",font=("MiSans ",20),height=2,width=30,border=1,command=ChooseOne)
But_ChooseThree = tk.Button(win,text="三抽",font=("MiSans VF",20),height=2,width=30,border=1,command=ChooseThree)
But_ChooseN = tk.Button(win,text="N抽",font=("MiSans VF",20),height=2,width=30,border=1,command=ChooseN)
Lab_N = tk.Label(win,text='N = ',font=("MiSans VF regular",15))
Ent_N = tk.Entry(win,width=5,font=("MiSans VF regular",15))
def resetAll():
    reset()
    Lab_chosen_obj.config(text=str(f'☑️重置完成，已抽{len(chosen_obj)}人：{str(chosen_obj)}'),font=("MiSans VF regular",15))
    print()
resetAll()
But_Reset = tk.Button(win,text="🔁重置已抽",font=("MiSans VF regular",15),command=resetAll,border=1)
But_EditWeight = tk.Button(win,text="🔡编辑权重",font=("MiSans VF regular",15),command=ShowWeightSettings,border=1)
But_EditChain = tk.Button(win,text="➿编辑连锁",font=("MiSans VF regular",15),command=ShowChainSettings,border=1)
But_CheckChain = tk.Button(win,text="❓刷新",font=("MiSans VF regular",15),command=CheckChainSettings,border=1)
But_AnimationOn = tk.Button(win,text="🔳已禁用动画",font=("MiSans VF regular",15),command=changeAnimation,border=1)
But_About = tk.Button(win,text="SeeWang - AllayCloud",font=("MiSans VF light",15),command=ShowAbout,border=1)
But_SmallMode = tk.Button(win,text="🪟小窗模式",font=("MiSans VF regular",15),command=SmallMode,border=1)


left_side_first_y = 220
pad=50
Lab_Number.pack()
But_ChoiseOne.pack()
But_ChooseThree.pack()
But_ChooseN.pack()
Lab_N.place(x=100,y=left_side_first_y)
Ent_N.place(x=150,y=left_side_first_y)
But_Reset.place(x=100,y=left_side_first_y+pad)   
But_EditWeight.place(x=100,y=left_side_first_y+pad*2)
But_RefreshWeight.place(x=240,y=left_side_first_y+pad*2)
But_EditChain.place(x=100,y=left_side_first_y+pad*3)
But_CheckChain.place(x=240,y=left_side_first_y+pad*3)
But_AnimationOn.place(x=100,y=left_side_first_y+pad*4)
But_About.place(x=100,y=left_side_first_y+pad*5)
But_SmallMode.place(x=100,y=left_side_first_y+pad*6)
Lab_chosen_obj.pack()

Lab_chosen_obj.config(text=str(f'希王点名2\n小窗模式更新！'))
update_Lab_Number_wraplength(None)
win.mainloop()