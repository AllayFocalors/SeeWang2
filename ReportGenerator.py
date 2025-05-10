from tkinter import messagebox


def generate_report():
    import cv2
    from PIL import ImageFont, ImageDraw, Image
    import numpy as np
    from collections import Counter

    try:
        with open('res.txt', 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        messagebox.showerror("错误", "未找到 res.txt 文件。")
        return
    except Exception as e:
        messagebox.showerror("错误", f"读取 res.txt 文件失败：{e}")
        return

    # print(' '.join((content.split('\n')[0].split('-->--')[0].split(' ')[0:3])))
    # print(' '.join((content.split('\n')[-1].split('-->--')[0].split(' ')[0:3])))
    names=[]
    lines=content.split('\n')
    for line in lines:
        # 使用分割方法提取名字
        if '-->--' in line:
            name = line.split('-->--')[1].strip()
            for j in name.split(' '):
                names.append(j)
    # print(names)
    name_counts = Counter(names)

    # print("\n统计结果：")
    for name, count in name_counts.items():
        ...
        # print(f"{name}: {count}次")
    # print("\n出现次数最多的是：")
    most_common = name_counts.most_common()
    max_count = most_common[0][1]

    for name, count in most_common:
        if count == max_count:
            # print(f"{name}: {count}次")
            max_name = name
            max_quan = max_count

    # print("\n出现次数最少的是：")
    min_count = most_common[-1][1]
    for name, count in most_common:
        if count == min_count:
            # print(f"{name}: {count}次")
            min_name = name
            min_quan = min_count

    try:
        bk_img = cv2.imread("Assets/img/report.png")
        if bk_img is None:
            raise FileNotFoundError("report.png 未找到")
    except FileNotFoundError as e:
        messagebox.showerror("错误", str(e))
        return
    except Exception as e:
        messagebox.showerror("错误", f"读取 report.png 失败：{e}")
        return

    # 设置需要显示的字体
    fontpath = "MiSans VF.ttf"
    try:
        font = ImageFont.truetype(fontpath, 50)
    except IOError:
        messagebox.showerror("错误", "字体文件 MiSans VF.ttf 未找到。")
        return
    except Exception as e:
        messagebox.showerror("错误", f"加载字体失败：{e}")
        return

    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    # 绘制文字信息
    draw.text((950, 85), f"{(' '.join((content.split('\n')[0].split('-->--')[0].split(' ')[0:3])))}~\n{' '.join((content.split('\n')[-2].split('-->--')[0].split(' ')[0:3]))}", font=font, fill=(0, 0, 0))
    draw.text((960, 400), max_name, font=ImageFont.truetype(fontpath, 120), fill=(0, 0, 0))
    draw.text((450, 530), str(max_quan), font=ImageFont.truetype(fontpath, 120), fill=(0, 0, 0))
    draw.text((960, 1010), min_name, font=ImageFont.truetype(fontpath, 120), fill=(0, 0, 0))
    draw.text((450, 1150), str(min_quan), font=ImageFont.truetype(fontpath, 120), fill=(0, 0, 0))

    bk_img = np.array(img_pil)

    # cv2.imshow("add_text", bk_img)
    cv2.waitKey()
    try:
        cv2.imwrite("add_text.jpg", bk_img)
    except Exception as e:
        messagebox.showerror("错误", f"保存图片失败：{e}")
        return

if __name__ == '__main__':
    generate_report()