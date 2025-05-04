import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math

def calculate_dimensions(obj_n):
    """计算最接近正方形的 n x m 布局，满足 n * m >= obj_n"""
    if obj_n <= 0:
        return (0, 0)
    m = math.ceil(math.sqrt(obj_n))
    while True:
        n = math.ceil(obj_n / m)
        if n * m >= obj_n:
            return (n, m)
        m += 1

class Application(tk.Tk):

    def test(self,t):
        print('test',t)

    def __init__(self,obj_quantity=46):
        super().__init__()
        self.title("配置生成器")
        self.geometry("800x600")
        self.current_obj_n = 0  # 保存当前输入的人数
        self.create_widgets(obj_quantity=obj_quantity)

    def create_widgets(self,obj_quantity=46):
        # 输入区域
        input_frame = ttk.Frame(self)
        input_frame.pack(pady=10, fill=tk.X)

        self.obj_n_entry = ttk.Entry(input_frame, width=10)
        self.obj_n_entry.pack(side=tk.LEFT, padx=5)
        self.obj_n_entry.insert(0, str(obj_quantity))  # 默认示例值

        self.relayout_btn = ttk.Button(input_frame, text="重新布局", command=self.relayout)
        self.relayout_btn.pack(side=tk.LEFT, padx=5)

        self.generate_btn = ttk.Button(input_frame, text="生成配置文件", command=self.generate_config)
        self.generate_btn.pack(side=tk.LEFT, padx=5)

        self.import_btn = ttk.Button(input_frame, text="导入配置", command=self.import_config)
        self.import_btn.pack(side=tk.LEFT, padx=5)

        # 表格区域
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 响应窗口大小调整
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def relayout(self):
        try:
            obj_n = int(self.obj_n_entry.get())
            if obj_n <= 0:
                raise ValueError
        except:
            messagebox.showerror("错误", "请输入有效的正整数人数。")
            return

        self.current_obj_n = obj_n
        n, m = calculate_dimensions(obj_n)
        self.n = n
        self.m = m

        # 清空旧表格
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.cells = []  # 存储单元格的Entry控件

        # 创建新表格
        for row in range(n):
            row_cells = []
            for col in range(m):
                cell_frame = ttk.Frame(self.table_frame)
                cell_frame.grid(row=row, column=col, padx=4, pady=4)

                name_entry = ttk.Entry(cell_frame, width=8)
                name_entry.pack(pady=1)

                weight_entry = ttk.Entry(cell_frame, width=8)
                weight_entry.pack(pady=1)

                group_entry = ttk.Entry(cell_frame, width=8)
                group_entry.pack(pady=1)

                row_cells.append((name_entry, weight_entry, group_entry))
            self.cells.append(row_cells)

    def generate_config(self):
        if not hasattr(self, 'current_obj_n') or self.current_obj_n <= 0:
            messagebox.showerror("错误", "请先输入人数并重新布局。")
            return

        config_data = []
        count = 0
        # 按行优先顺序取前 current_obj_n 个单元格
        for row_cells in self.cells:
            for cell in row_cells:
                if count >= self.current_obj_n:
                    break
                name = cell[0].get().strip()
                weight = cell[1].get().strip()
                group = cell[2].get().strip()
                config_data.append(f"{name},{weight},{group}")
                count += 1
            if count >= self.current_obj_n:
                break

        # 文件保存
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="保存配置文件"
        )
        if file_path:
            try:
                with open(file_path, 'w',encoding='utf-8') as f:
                    f.write('\n'.join(config_data))
                messagebox.showinfo("成功", "配置文件已保存。")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败：{e}")

    def import_config(self,file_path=''):
        if file_path=='':
            file_path = filedialog.askopenfilename(
                filetypes=[("Text files", "*.txt")],
                title="选择配置文件"
            )
            if not file_path:
                return

        try:
            with open(file_path, 'r',encoding = 'utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败：{e}")
            return

        # 处理每一行
        data = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 3:
                messagebox.showerror("错误", f"第{i+1}行格式错误，必须包含三个字段。")
                return
            data.append(parts)

        # 检查数据量是否匹配
        if not hasattr(self, 'current_obj_n') or self.current_obj_n <= 0:
            messagebox.showerror("错误", "请先输入人数并重新布局。")
            return

        if len(data) != self.current_obj_n:
            messagebox.showerror("错误", f"文件行数（{len(data)}）与当前设置人数（{self.current_obj_n}）不一致。")
            return

        # 检查表格是否存在
        if not hasattr(self, 'cells') or not self.cells:
            messagebox.showerror("错误", "表格未初始化，请先重新布局。")
            return

        # 填充表格
        for idx, (name, weight, group) in enumerate(data):
            row = idx // self.m
            col = idx % self.m
            # 清空并插入新内容
            self.cells[row][col][0].delete(0, tk.END)
            self.cells[row][col][0].insert(0, name)
            self.cells[row][col][1].delete(0, tk.END)
            self.cells[row][col][1].insert(0, weight)
            self.cells[row][col][2].delete(0, tk.END)
            self.cells[row][col][2].insert(0, group)


def main(file_path='',obj_quantity=46):
    global app
    app = Application(obj_quantity=obj_quantity)
    app.relayout()
    app.import_config(file_path)
    app.mainloop()


if __name__ == "__main__":
    main()

if __name__ == 'ConfigGenerator':
    ...