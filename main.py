"""
GUI主程序
提供图形界面用于选择ELF文件并生成Excel报告
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
from elf_analyzer import ELFAnalyzer
from excel_generator import ExcelReportGenerator


class MemoryMapToolGUI:
    """内存映射工具GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("GHS ELF内存分析工具")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # 芯片配置
        self.chip_configs = {
            "R7F701372A": {"rom": 4096, "ram": 480},  # ROM: 4MB, RAM: 480KB
            "R7F701374A": {"rom": 2048, "ram": 320},  # ROM: 2MB, RAM: 320KB
            "R7F701382": {"rom": 1024, "ram": 256},   # ROM: 1MB, RAM: 256KB
            "R7F701312": {"rom": 1024, "ram": 128}      # ROM: 1MB, RAM: 128KB
        }

        # 变量
        self.elf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.chip_model = tk.StringVar(value="")
        self.rom_total = tk.StringVar(value="")
        self.ram_total = tk.StringVar(value="")

        self._create_widgets()

    def _create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 标题
        title_label = ttk.Label(main_frame, text="GHS ELF内存分析工具",
                               font=('微软雅黑', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # ELF文件选择
        ttk.Label(main_frame, text="ELF文件:", font=('微软雅黑', 10)).grid(
            row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.elf_path, width=50).grid(
            row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="浏览...", command=self._browse_elf).grid(
            row=1, column=2, pady=5)

        # 输出文件选择
        ttk.Label(main_frame, text="输出Excel:", font=('微软雅黑', 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(
            row=2, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="浏览...", command=self._browse_output).grid(
            row=2, column=2, pady=5)

        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)

        # 可选配置
        ttk.Label(main_frame, text="芯片配置（选择芯片型号或手动输入容量）",
                 font=('微软雅黑', 10, 'bold')).grid(
            row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # 芯片型号选择
        ttk.Label(main_frame, text="芯片型号:", font=('微软雅黑', 10)).grid(
            row=5, column=0, sticky=tk.W, pady=5)
        chip_combo = ttk.Combobox(main_frame, textvariable=self.chip_model,
                                  values=[""] + list(self.chip_configs.keys()),
                                  state='readonly', width=18)
        chip_combo.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        chip_combo.bind('<<ComboboxSelected>>', self._on_chip_selected)

        # ROM总容量
        ttk.Label(main_frame, text="ROM总容量(KB):", font=('微软雅黑', 10)).grid(
            row=6, column=0, sticky=tk.W, pady=5)
        rom_entry = ttk.Entry(main_frame, textvariable=self.rom_total, width=20)
        rom_entry.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)

        # RAM总容量
        ttk.Label(main_frame, text="RAM总容量(KB):", font=('微软雅黑', 10)).grid(
            row=7, column=0, sticky=tk.W, pady=5)
        ram_entry = ttk.Entry(main_frame, textvariable=self.ram_total, width=20)
        ram_entry.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)

        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.progress.grid(row=9, column=0, columnspan=3, pady=10)

        # 状态标签
        self.status_label = ttk.Label(main_frame, text="就绪", font=('微软雅黑', 9))
        self.status_label.grid(row=10, column=0, columnspan=3, pady=5)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=11, column=0, columnspan=3, pady=20)

        # 分析按钮
        self.analyze_button = ttk.Button(button_frame, text="开始分析",
                                         command=self._start_analysis, width=15)
        self.analyze_button.grid(row=0, column=0, padx=10)

        # 退出按钮
        ttk.Button(button_frame, text="退出", command=self.root.quit, width=15).grid(
            row=0, column=1, padx=10)

    def _browse_elf(self):
        """浏览ELF文件"""
        filename = filedialog.askopenfilename(
            title="选择ELF文件",
            filetypes=[("ELF文件", "*.elf *.out"), ("所有文件", "*.*")]
        )
        if filename:
            self.elf_path.set(filename)
            # 自动设置输出路径
            if not self.output_path.get():
                base_name = os.path.splitext(filename)[0]
                self.output_path.set(f"{base_name}_memory_report.xlsx")

    def _browse_output(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(
            title="保存Excel报告",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if filename:
            self.output_path.set(filename)

    def _on_chip_selected(self, event=None):
        """芯片型号选择事件处理"""
        chip = self.chip_model.get()
        if chip and chip in self.chip_configs:
            config = self.chip_configs[chip]
            self.rom_total.set(str(config["rom"]))
            self.ram_total.set(str(config["ram"]))
        elif not chip:
            # 清空选择时不自动清空容量值，允许用户手动输入
            pass

    def _start_analysis(self):
        """开始分析"""
        # 验证输入
        if not self.elf_path.get():
            messagebox.showerror("错误", "请选择ELF文件")
            return

        if not self.output_path.get():
            messagebox.showerror("错误", "请指定输出文件路径")
            return

        if not os.path.exists(self.elf_path.get()):
            messagebox.showerror("错误", "ELF文件不存在")
            return

        # 在新线程中执行分析
        thread = threading.Thread(target=self._analyze)
        thread.daemon = True
        thread.start()

    def _analyze(self):
        """执行分析（在后台线程中）"""
        try:
            # 更新UI
            self.root.after(0, self._update_status, "正在解析ELF文件...")
            self.root.after(0, self.progress.start)
            self.root.after(0, lambda: self.analyze_button.config(state='disabled'))

            # 解析ELF文件
            analyzer = ELFAnalyzer(self.elf_path.get())
            summary = analyzer.get_memory_summary()
            sections = analyzer.get_detailed_sections()

            # 获取总容量配置
            rom_total = None
            ram_total = None

            if self.rom_total.get().strip():
                try:
                    rom_total = int(float(self.rom_total.get()) * 1024)
                except ValueError:
                    pass

            if self.ram_total.get().strip():
                try:
                    ram_total = int(float(self.ram_total.get()) * 1024)
                except ValueError:
                    pass

            # 生成Excel报告
            self.root.after(0, self._update_status, "正在生成Excel报告...")
            generator = ExcelReportGenerator(self.output_path.get())
            generator.generate_report(summary, sections, rom_total, ram_total)

            # 完成
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.analyze_button.config(state='normal'))
            self.root.after(0, self._update_status, "分析完成！")
            self.root.after(0, lambda: messagebox.showinfo(
                "成功",
                f"分析完成！\n\nROM使用: {summary['ROM']['used'] / 1024:.2f} KB\n"
                f"RAM使用: {summary['RAM']['used'] / 1024:.2f} KB\n\n"
                f"报告已保存至:\n{self.output_path.get()}"
            ))

        except Exception as e:
            error_msg = str(e)
            # 针对权限错误给出更友好的提示
            if "Permission denied" in error_msg or "PermissionError" in str(type(e)):
                error_msg = f"{error_msg}\n\n提示：请检查输出文件是否已被其他程序打开（如Excel），\n如果是，请关闭后重试，或选择新的输出路径。"

            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.analyze_button.config(state='normal'))
            self.root.after(0, self._update_status, f"错误: {str(e)}")
            self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", f"分析失败:\n{msg}"))

    def _update_status(self, message):
        """更新状态标签"""
        self.status_label.config(text=message)


def main():
    """主函数"""
    root = tk.Tk()
    app = MemoryMapToolGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()