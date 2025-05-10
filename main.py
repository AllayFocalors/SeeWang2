VERSION  = '2.4.8'
s = f'========SEEWANG {VERSION}========'
print(fr'''                                                                                                                  
  CCCCCCCCCCCCWWWWW       WWWWW    AAAAAA     NNNNN      NNNNN  GGGGGGGGGGGGG             2222222
 CCCCCCCCCCCCCWWWWW WWWWW WWWWW    AAAAAA     NNNNNN     NNNNN GGGGGGGGGGGGGGG         2222222222222
CCCCC         WWWWW WWWWW WWWWW   AAAAAAAA    NNNNNNN    NNNNNGGGGG        GGG       222222   2222222
CCCCC         WWWWW WWWWW WWWWW   AAAAAAAA    NNNNNNNN   NNNNNGGGGG        GGG      22222      222222
CCCCC         WWWWW WWWWW WWWWW  AAAAA AAAA   NNNNNNNNN  NNNNNGGGGG                            22222
CCCCC         WWWWW WWWWW WWWWW  AAAAA AAAA   NNNNNNNNNN NNNNNGGGGG     GGGGG                 22222
CCCCC         WWWWW WWWWW WWWWW AAAAAA  AAAA  NNNNN NNNNNNNNNNGGGGG     GGGGGG               22222         
CCCCC         WWWWW WWWWW WWWWW AAAAAA  AAAA  NNNNN  NNNNNNNNNGGGGG       GGGG             22222      
CCCCC         WWWWW WWWWW WWWWWAAAAAA    AAAA NNNNN   NNNNNNNNGGGGG       GGGG           2222      22
CCCCC         WWWWWWWWWWWWWWWWWAAAAAA    AAAA NNNNN    NNNNNNNGGGGGGGGGGGGGGGG         2222       222
 CCCCCCCCCCCCCCWWWWWWW WWWWWWWAAAAAA      AAAANNNNN     NNNNNN GGGGGGGGGGGGGG        2222       22222  
  CCCCCCCCCCCCCCWWWWW   WWWWW AAAAAA      AAAANNNNN      NNNNN  GGGGGGGGGGGG        222        222222 
{s:^96}
  > AllayCloud 2025
  > By AllayCLoud-Studio: AllayFocalors
''')



import tkinter as tk
import json
from PIL import Image, ImageTk
import WeightChoice as wc
import os
import time
from tkinter import messagebox
from tkinter import ttk
from ffpyplayer.player import MediaPlayer
import ReportGenerator as RG

flag=1 #是否首次启动，如果是的话就不弹窗提示已经刷新
main_font_size = 140
next_obj = []
win = tk.Tk()
win.iconbitmap('Assets/img/icon.ico')
obj_list = []#obj_list就是所有学生的名单，一人一个不重复
chosen_obj = []#已经抽过的学生
os.environ['FFMPEG_HWACCEL'] = 'auto'
chain_info = None #chain_info是存储chain信息的列表，防止和chain_config.txt混淆
style = ttk.Style()
style.configure('ButtonStyle1.TButton',font=('MiSans VF regular',15),background='white')
style.configure('ButtonStyle2.TButton',font=('MiSans VF regular',25),width=15)

animations = {}

CONFIG_FILE_PATH = os.path.abspath('config.txt')
_icon_cache = {}

def get_config():
    return wc.get_config()

def load_icon(icon_path):
    if icon_path in _icon_cache:
        return _icon_cache[icon_path]
    else:
        icon_img = Image.open(icon_path).resize((27, 27), Image.LANCZOS)
        icon_photo = ImageTk.PhotoImage(icon_img)
        _icon_cache[icon_path] = icon_photo
        return icon_photo

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
                    self.stop_animation()
                elif frame is not None:
                    image, pts = frame
                    self.update_canvas(image)
                if not self.is_paused and val is not None:
                    win.after(int(val * 1000), update_frame)
        update_frame()

    def stop_animation(self):
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

def write_res(res):
    with open('res.txt',mode='a',encoding='utf-8') as file:
        file.write(time.asctime()+' -->-- '+res+'\n')
    with open('log.txt',mode='a',encoding='utf-8') as file:
        file.write(time.asctime()+' : SingleChoose : '+res+'\n')

def write_log(info):
    with open('log.txt',mode='a',encoding='utf-8') as file:
        file.write(info+'\n')

def play_animation(filepath):
    animation1lasttime = json.load(open('dev_options.json'))['Animation1lasttime']
    animation2lasttime = json.load(open('dev_options.json'))['Animation2lasttime']
    app = VideoPlayTk(win, filepath)
    if 'V1' in filepath or 'V2' in filepath:
        win.after(animation1lasttime, app.stop_animation)
    elif 'V3' in filepath:
        win.after(animation2lasttime, app.stop_animation)

def show_about():
    abt = tk.Toplevel(win)
    abt.title('希王点名由悦灵云工作室开发')

    def load_images():
        try:
            Img_StudioLogo = ImageTk.PhotoImage(Image.open("Assets/img/StudioLogo.png").resize((512,200),Image.LANCZOS))
            Lab_StudioLogoShow = ttk.Label(abt,image=Img_StudioLogo)
            Img_AppLogo = ImageTk.PhotoImage(Image.open("Assets/img/SeeWangLogo-new.png").resize((512,256),Image.LANCZOS))
            Lab_AppLogoShow = ttk.Label(abt,image=Img_AppLogo)
            Lab_StudioLogoShow.image = Img_StudioLogo
            Lab_AppLogoShow.image = Img_AppLogo
            Lab_StudioLogoShow.pack()
            Lab_AppLogoShow.pack()
        except Exception as e:
            print(e)
    abt.after(1000,load_images)

win.geometry("1500x700+0+5")
win.title(f'希王点名{VERSION}')

animation=0

MainTitle_color = '#5982ff'

def change_animation():
    global animation
    if animation==0:
        animation=1
        But_AnimationOn.config(text='动画样式1')
    elif animation==1:
        animation=2
        But_AnimationOn.config(text='动画样式2')
    elif animation==2:
        animation=0
        But_AnimationOn.config(text='已禁用动画')

def show_weight_set():
    import ConfigGenerator as CG
    # 调用 ConfigGenerator 中的 app 实例的 import_config 方法
    CG.main(file_path=CONFIG_FILE_PATH,obj_quantity=len(obj_list))
    # print(os.path.abspath('config.txt'))

def show_chain_set():
    os.system(f'start notepad ./chain_config.txt')

Lab_chosen_obj = ttk.Label(win,text="已抽学生：",font=("MiSans VF regular",15),wraplength=700)
Lab_Obj = ttk.Label(win,text="找抽",font=("MiSans VF Bold",main_font_size),wraplength=int(win.winfo_width()))

def refresh_weight():
    global config,Lab_chosen_obj,flag
    config = wc.get_config()
    if flag != 1:
        messagebox.showinfo('权重配置成功',f'已加载{len(config)}条权重配置')


refresh_weight()

But_refresh_weight = ttk.Button(win,text="刷新",style='ButtonStyle1.TButton',command=refresh_weight,width=5,image=load_icon('Assets/img/刷新.png'),compound='left')

def reset():
    '''obj_list就是所有学生的名单，一人一个不重复'''
    global obj_list,chosen_obj,config,stu_Quantity,Lab_chosen_obj
    p = []#这个用来在遍历时存储抽过的学生，以防config里面重名bug
    obj_list = []
    chosen_obj = []
    for i in config:
        stu = i.split(',')[0]
        if stu in p:
            continue
        obj_list.append(stu)
        p.append(stu)
    stu_Quantity = len(obj_list)
    Lab_Obj.config(text="找抽",wraplength=int(win.winfo_width()))

def single_choose():
    '''由于choose_one,choose_three,choose_n的逻辑过于臃肿，所以打算都调用这个single_choose函数'''
    global config
    if len(next_obj)==0:#nextobj列表中没人，说明没有触发连锁
        try:
            obj = wc.choose(config=config, chosen_obj=chosen_obj, chain_config=chain_info)
        except Exception as e:
            write_log(info=f'选择对象时发生错误: {e}')
            messagebox.showerror('异常', f'{e}')
            return
        if 'error' in obj:
            messagebox.showerror('错误', obj['error'])
            return
        tar = obj['Tar']
        Next = obj['Next']
        print(f'传回Tar={tar},Next={Next},')
        while Next in chain_info:  # 说明这个obj有next，触发了连锁
            if not Next in chosen_obj:  # 说明这个东西连锁的next也没抽过
                next_obj.insert(0, Next)
                #
                # print(f'Next={Next},next_obj={next_obj}')
            Next = chain_info[Next]  # 获取next的next
            if Next in next_obj:  # 说明是##both模式，所以要再判断一遍，不然死循环
                break
        if (not Next in chosen_obj) and Next is not None:  # 循环完成后再来一遍，因为尾巴上的人是不作为字典的key的，所以要再判断一遍。如果删了这个语句的话，最后尾巴上的人会被忽略。
            next_obj.insert(0, Next)
            # print(f'Next={Next},next_obj={next_obj}')

        Next = obj['Next']
    else:  # next_obj中有人，说明触发了连锁，且下一个人是安排好的
        tar = next_obj.pop()
        Next = None
    write_log(info=f'选择对象: {tar}, 下一个对象: {Next}, 连锁列表: {next_obj}')
    return {'Tar': tar, 'Next': Next}

def find_keys_by_value(d, value):
    keys = [k for k, v in d.items() if v == value]
    return keys

def choose_one():
    global config,animation
    if animation:
        if animation == 1:
            play_animation('Assets/vid/V1.mp4')
        elif animation == 2:
            play_animation('Assets/vid/V3.mp4')
    if len(chosen_obj) < stu_Quantity:
        a = single_choose()
        Tar = a['Tar']
        Next = a['Next']
        print(f'choose_one:Tar={Tar},next={Next},next_obj={next_obj}')
        obj_list.remove(Tar)
        chosen_obj.append(Tar)
        Lab_Obj.config(text=str(Tar),foreground=MainTitle_color)
        Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(' '.join(chosen_obj))}'))   
        write_res(Tar)
    else:
        whether_reset = messagebox.askokcancel('人不够了',f'人不够了，是否重置？')
        if whether_reset:
            reset_all()

def choose_n():
    global stu_Quantity
    if animation:
        if animation == 1:
            play_animation('Assets/vid/V2.mp4')
        elif animation == 2:
            play_animation('Assets/vid/V3.mp4')
    if int(Ent_N.get())>=15:
        messagebox.showwarning('太多了',f'搁着周处除{Ent_N.get()}害呢')
    else:
        if len(chosen_obj) < stu_Quantity-int(Ent_N.get())+1:
            res=''
            for i in range(int(Ent_N.get())):
                a = single_choose()
                Tar = a['Tar']
                Next = a['Next']
                print(f'Tar={Tar},next={Next},next_obj={next_obj}')
                obj_list.remove(Tar)
                chosen_obj.append(Tar)
                res+=str(Tar)+' '
            Lab_Obj.config(text=str(res),foreground=MainTitle_color)
            Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(' '.join(chosen_obj))}'))   
            write_res(res)
        else:
            messagebox.showwarning('人不够了',f'抽不了这么多')

def choose_three():
    global stu_Quantity
    if animation:
        if animation == 1:
            play_animation('Assets/vid/V2.mp4')
        elif animation == 2:
            play_animation('Assets/vid/V3.mp4')
    if len(chosen_obj) < stu_Quantity-2:
        res=''
        for i in range(3):
            a = single_choose()
            Tar = a['Tar']
            Next = a['Next']
            print(f'Tar={Tar},next={Next},next_obj={next_obj}')
            obj_list.remove(Tar)
            chosen_obj.append(Tar)
            res+=str(Tar)+' '
        Lab_Obj.config(text=str(res),foreground=MainTitle_color)
        Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(' '.join(chosen_obj))}'))   
        write_res(res)
    else:
        messagebox.showwarning('人不够了',f'抽不了这么多')
pad=40



def small_mode():
    Small()

class Small:
    def choose_one_small(self):
        global config,animation,Lab_Obj_s,Lab_chosen_obj_s
        if len(chosen_obj) < stu_Quantity:
            tar = wc.choose(config=config,chosen_obj=chosen_obj,chain_config=chain_info)['Tar']
            # print(f'Tar={Tar},obj_list={obj_list}')
            obj_list.remove(tar)
            chosen_obj.append(tar)
            Lab_Obj_s.config(text=str(tar),foreground=MainTitle_color)
            Lab_chosen_obj.config(text=str(f'已抽{len(chosen_obj)}个学生：\n{str(chosen_obj)}'))   

            write_res(tar)
        else:
            whether_reset = messagebox.askokcancel('人不够了',f'人不够了，是否重置？')
            if whether_reset:
                reset()

    def update_Lab_Obj_s_wraplength(self,event):
        Lab_Obj_s.config(wraplength=self.smallwindow.winfo_width(),font=("MiSans VF demibold",int(self.smallwindow.winfo_width()/5)))
        # print(f'winfo-height={win.winfo_height()},h={win.winfo_height()/1017*2}')
    
    def __init__(self):
        global Lab_Obj_s,But_ChooseOne_s,But_choose_three_s,But_choose_n_s,win,smallwindow
        self.smallwindow = tk.Toplevel(win)
        self.smallwindow.bind('<Configure>', self.update_Lab_Obj_s_wraplength)
        self.smallwindow.geometry('400x200')
        self.smallwindow.title('希王小窗')
        self.smallwindow.attributes('-topmost', True) 
        Lab_Obj_s = ttk.Label(self.smallwindow,text="找抽",style='ButtonStyle1.TButton',wraplength=int(self.smallwindow.winfo_width()))
        But_ChooseOne_s = ttk.Button(self.smallwindow,text="单抽",style='ButtonStyle1.TButton',command=self.choose_one_small)
        Lab_Obj_s.pack(expand=True, anchor='center')
        But_ChooseOne_s.pack()

def check_chain_settings():
    global config,chain_info,flag
    chain_info = wc.load_chain_config('chain_config.txt')
    if 'error' in chain_info:
        messagebox.showerror('错误',chain_info['error'])
    else:
        if flag!=1:
            messagebox.showinfo('连锁配置成功',f'已加载{len(chain_info)}条连锁配置')
        flag=0

def generate_report():
    RG.generate_report()
    messagebox.showinfo('通知','周报生成完成')

def show_dev_opt():
    def save_dev_opt():
        global animation,dev_options
        if Ent_Animation1.get().isdigit() and Ent_Animation2.get().isdigit():
            dev_options = {'Animation1lasttime':int(Ent_Animation1.get()),'Animation2lasttime':int(Ent_Animation2.get())}
            with open('dev_options.json','w') as f:
                f.write(json.dumps(dev_options))
                messagebox.showinfo('保存成功',f'已保存{json.dumps(dev_options)}')

    dev_options = tk.Toplevel(win)
    dev_options.geometry('400x200')
    dev_options.title('开发者选项')
    dev_options.attributes('-topmost', True) 
    dev_options.bind('<Configure>', update_Lab_Obj_wraplength)
    ttk.Label(dev_options,text='动画样式1持续时长').pack()
    Ent_Animation1 = ttk.Entry(dev_options,width=13)
    Ent_Animation1.pack()
    ttk.Label(dev_options,text='动画样式2持续时长').pack()
    Ent_Animation2 = ttk.Entry(dev_options,width=13)
    Ent_Animation2.pack()
    ttk.Button(dev_options,text='保存',command=save_dev_opt).pack()



But_ChooseOne = ttk.Button(win,text="单抽",style='ButtonStyle2.TButton',command=choose_one)
But_choose_three = ttk.Button(win,text="三抽",style='ButtonStyle2.TButton',command=choose_three)
But_choose_n = ttk.Button(win,text="N抽",style='ButtonStyle2.TButton',command=choose_n)
Lab_N = ttk.Label(win,text='N = ',style='ButtonStyle1.TButton')
Ent_N = ttk.Entry(win,width=13)
def reset_all():
    reset()
    Lab_chosen_obj.config(text=str(f'☑️重置完成，已抽{len(chosen_obj)}人：{str(chosen_obj)}'),style='ButtonStyle1.TButton')
    print()
check_chain_settings()
reset_all()
But_Reset = ttk.Button(win,text="重置已抽",style='ButtonStyle1.TButton',command=reset_all,image=load_icon('Assets/img/重置.png'),compound='left')
But_EditWeight = ttk.Button(win,text="编辑权重",style='ButtonStyle1.TButton',command=show_weight_set,image=load_icon('Assets/img/权重.png'),compound='left')
But_EditChain = ttk.Button(win,text="编辑连锁",style='ButtonStyle1.TButton',command=show_chain_set,image=load_icon('Assets/img/连锁.png'),compound='left')
But_CheckChain = ttk.Button(win,text="刷新",style='ButtonStyle1.TButton',command=check_chain_settings,width=5,image=load_icon('Assets/img/刷新.png'),compound='left')
But_AnimationOn = ttk.Button(win,text="已禁用动画",style='ButtonStyle1.TButton',command=change_animation)
But_About = ttk.Button(win,text=f"SeeWang v{VERSION}",style='ButtonStyle1.TButton',command=show_about)
But_small_mode = ttk.Button(win,text="小窗模式",style='ButtonStyle1.TButton',command=small_mode,image=load_icon('Assets/img/小窗.png'),compound='left')
But_generate_report= ttk.Button(win,text="生成周报",style='ButtonStyle1.TButton',command=generate_report,image=load_icon('Assets/img/周报.png'),compound='left')
But_DevelopOptions = ttk.Button(win,text="高级选项",style='ButtonStyle1.TButton',command=show_dev_opt,image=load_icon('Assets/img/开发.png'),compound='left')

left_side_first_y = 220
Lab_Obj.pack()
But_ChooseOne.pack()
But_choose_three.pack()
But_choose_n.pack()
Lab_N.place(x=100,y=left_side_first_y)
Ent_N.place(x=150,y=left_side_first_y+5)
But_Reset.place(x=100,y=left_side_first_y+pad)   
But_EditWeight.place(x=100,y=left_side_first_y+pad*2)
But_refresh_weight.place(x=300,y=left_side_first_y+pad*2)
But_EditChain.place(x=100,y=left_side_first_y+pad*3)
But_CheckChain.place(x=300,y=left_side_first_y+pad*3)
But_AnimationOn.place(x=100,y=left_side_first_y+pad*4)
Lab_chosen_obj.pack()

Lab_chosen_obj.config(text=str(f'希王点名2\n界面布局更新'))
def update_Lab_Obj_wraplength(event):
    global pad
    Lab_Obj.config(wraplength=win.winfo_width(),font=("MiSans VF",int(win.winfo_width()/14)))
    right_side_first_y = 220
    But_About.place(x=win.winfo_width()-300,y=right_side_first_y)
    But_small_mode.place(x=win.winfo_width()-300,y=right_side_first_y+pad)
    But_generate_report.place(x=win.winfo_width()-300,y=right_side_first_y+pad*2)
    But_DevelopOptions.place(x=win.winfo_width()-300,y=right_side_first_y+pad*3)
win.bind('<Configure>', update_Lab_Obj_wraplength)
update_Lab_Obj_wraplength(None)
win.mainloop()