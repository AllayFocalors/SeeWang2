
def generate_report():
    import cv2
    from PIL import ImageFont, ImageDraw, Image
    import numpy as np
    from collections import Counter

    with open('res.txt','r',encoding='utf-8') as file:
        content = file.read()

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

    # print("\n出现次数最少的是：")
    min_count = most_common[-1][1]
    for name, count in most_common:
        if count == min_count:
            # print(f"{name}: {count}次")
            min_name = name

    bk_img = cv2.imread("Assets/img/report.png")
    #设置需要显示的字体
    fontpath = "MiSans VF.ttf"
    font = ImageFont.truetype(fontpath, 50)
    img_pil = Image.fromarray(bk_img)
    draw = ImageDraw.Draw(img_pil)
    #绘制文字信息
    draw.text((800, 85),  f"{(' '.join((content.split('\n')[0].split('-->--')[0].split(' ')[0:3])))}~\n{' '.join((content.split('\n')[-2].split('-->--')[0].split(' ')[0:3]))}", font = font, fill = (0, 0, 0))
    draw.text((100, 600),  max_name, font = ImageFont.truetype(fontpath, 150), fill = (0, 0, 0))
    draw.text((100, 1200),  min_name, font = ImageFont.truetype(fontpath, 150), fill = (0, 0, 0))
    bk_img = np.array(img_pil)


    cv2.imshow("add_text",bk_img)
    cv2.waitKey()
    cv2.imwrite("add_text.jpg",bk_img)
