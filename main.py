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
from i18n import get_i18n


class MemoryMapToolGUI:
    """内存映射工具GUI"""

    def __init__(self, root):
        self.root = root
        self.i18n = get_i18n()
        self.root.title(self.i18n.t('app_title'))
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # 芯片配置
        self.chip_configs = {
            "R7F701372A": {"rom": 4096, "ram": 480},  # ROM: 4MB, RAM: 480KB
            "R7F701374A": {"rom": 2048, "ram": 320},  # ROM: 2MB, RAM: 320KB
            "R7F701382": {"rom": 1024, "ram": 192},   # ROM: 1MB, RAM: 192KB
            "R7F701312": {"rom": 1024, "ram": 128}      # ROM: 1MB, RAM: 128KB
        }

        # 变量
        self.elf_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.chip_model = tk.StringVar(value="")
        self.rom_total = tk.StringVar(value="")
        self.ram_total = tk.StringVar(value="")
        self.language = tk.StringVar(value=self.i18n.get_language())

        self._create_widgets()

    def _create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 语言选择
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=0, column=0, columnspan=3, sticky=tk.E, pady=(0, 10))
        ttk.Label(lang_frame, text=self.i18n.t('language'), font=(self.i18n.get_font_name(), 9)).pack(side=tk.LEFT, padx=5)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.language,
                                  values=list(self.i18n.LANGUAGES.keys()),
                                  state='readonly', width=10)
        lang_combo.pack(side=tk.LEFT)
        lang_combo.bind('<<ComboboxSelected>>', self._on_language_changed)

        # 标题
        self.title_label = ttk.Label(main_frame, text=self.i18n.t('app_title'),
                               font=(self.i18n.get_font_name(), 16, 'bold'))
        self.title_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # ELF文件选择
        self.elf_label = ttk.Label(main_frame, text=self.i18n.t('elf_file'), font=(self.i18n.get_font_name(), 10))
        self.elf_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.elf_path, width=50).grid(
            row=2, column=1, padx=5, pady=5)
        self.browse_elf_button = ttk.Button(main_frame, text=self.i18n.t('browse'), command=self._browse_elf)
        self.browse_elf_button.grid(row=2, column=2, pady=5)

        # 输出文件选择
        self.output_label = ttk.Label(main_frame, text=self.i18n.t('output_excel'), font=(self.i18n.get_font_name(), 10))
        self.output_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_path, width=50).grid(
            row=3, column=1, padx=5, pady=5)
        self.browse_output_button = ttk.Button(main_frame, text=self.i18n.t('browse'), command=self._browse_output)
        self.browse_output_button.grid(row=3, column=2, pady=5)

        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)

        # 可选配置
        self.config_label = ttk.Label(main_frame, text=self.i18n.t('chip_config'),
                 font=(self.i18n.get_font_name(), 10, 'bold'))
        self.config_label.grid(row=5, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # 芯片型号选择
        self.chip_label = ttk.Label(main_frame, text=self.i18n.t('chip_model'), font=(self.i18n.get_font_name(), 10))
        self.chip_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        chip_combo = ttk.Combobox(main_frame, textvariable=self.chip_model,
                                  values=[""] + list(self.chip_configs.keys()),
                                  state='readonly', width=18)
        chip_combo.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        chip_combo.bind('<<ComboboxSelected>>', self._on_chip_selected)

        # ROM总容量
        self.rom_label = ttk.Label(main_frame, text=self.i18n.t('rom_total'), font=(self.i18n.get_font_name(), 10))
        self.rom_label.grid(row=7, column=0, sticky=tk.W, pady=5)
        rom_entry = ttk.Entry(main_frame, textvariable=self.rom_total, width=20)
        rom_entry.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)

        # RAM总容量
        self.ram_label = ttk.Label(main_frame, text=self.i18n.t('ram_total'), font=(self.i18n.get_font_name(), 10))
        self.ram_label.grid(row=8, column=0, sticky=tk.W, pady=5)
        ram_entry = ttk.Entry(main_frame, textvariable=self.ram_total, width=20)
        ram_entry.grid(row=8, column=1, sticky=tk.W, padx=5, pady=5)

        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.progress.grid(row=10, column=0, columnspan=3, pady=10)

        # 状态标签
        self.status_label = ttk.Label(main_frame, text=self.i18n.t('ready'), font=(self.i18n.get_font_name(), 9))
        self.status_label.grid(row=11, column=0, columnspan=3, pady=5)

        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=12, column=0, columnspan=3, pady=20)

        # 分析按钮
        self.analyze_button = ttk.Button(button_frame, text=self.i18n.t('start_analysis'),
                                         command=self._start_analysis, width=15)
        self.analyze_button.grid(row=0, column=0, padx=10)

        # 退出按钮
        self.exit_button = ttk.Button(button_frame, text=self.i18n.t('exit'), command=self.root.quit, width=15)
        self.exit_button.grid(row=0, column=1, padx=10)

    def _on_language_changed(self, event=None):
        """语言切换事件处理"""
        new_lang = self.language.get()
        self.i18n.set_language(new_lang)
        messagebox.showinfo(
            self.i18n.t('success'),
            "Language changed successfully! Please restart the application.\n语言已更改！请重启应用程序。"
        )

    def _browse_elf(self):
        """浏览ELF文件"""
        filename = filedialog.askopenfilename(
            title=self.i18n.t('select_elf'),
            filetypes=[(self.i18n.t('elf_files'), "*.elf *.out"), (self.i18n.t('all_files'), "*.*")]
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
            title=self.i18n.t('save_excel'),
            defaultextension=".xlsx",
            filetypes=[(self.i18n.t('excel_files'), "*.xlsx"), (self.i18n.t('all_files'), "*.*")]
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
            messagebox.showerror(self.i18n.t('error'), self.i18n.t('error_no_elf'))
            return

        if not self.output_path.get():
            messagebox.showerror(self.i18n.t('error'), self.i18n.t('error_no_output'))
            return

        if not os.path.exists(self.elf_path.get()):
            messagebox.showerror(self.i18n.t('error'), self.i18n.t('error_elf_not_exist'))
            return

        # 在新线程中执行分析
        thread = threading.Thread(target=self._analyze)
        thread.daemon = True
        thread.start()

    def _analyze(self):
        """执行分析（在后台线程中）"""
        try:
            # 更新UI
            self.root.after(0, self._update_status, self.i18n.t('parsing_elf'))
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
            self.root.after(0, self._update_status, self.i18n.t('generating_excel'))
            generator = ExcelReportGenerator(self.output_path.get(), self.i18n)

            # 获取芯片配置信息
            chip_info = {
                'model': self.chip_model.get() if self.chip_model.get() else None,
                'rom_total_kb': float(self.rom_total.get()) if self.rom_total.get().strip() else None,
                'ram_total_kb': float(self.ram_total.get()) if self.ram_total.get().strip() else None
            }

            generator.generate_report(summary, sections, rom_total, ram_total, chip_info)

            # 完成
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.analyze_button.config(state='normal'))
            self.root.after(0, self._update_status, self.i18n.t('analysis_complete'))
            self.root.after(0, lambda: messagebox.showinfo(
                self.i18n.t('success'),
                f"{self.i18n.t('analysis_complete')}\n\n{self.i18n.t('rom_usage')}: {summary['ROM']['used'] / 1024:.2f} KB\n"
                f"{self.i18n.t('ram_usage')}: {summary['RAM']['used'] / 1024:.2f} KB\n\n"
                f"{self.i18n.t('report_saved')}:\n{self.output_path.get()}"
            ))

        except Exception as e:
            error_msg = str(e)
            # 针对权限错误给出更友好的提示
            if "Permission denied" in error_msg or "PermissionError" in str(type(e)):
                error_msg = f"{error_msg}\n\n{self.i18n.t('permission_hint')}"

            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.analyze_button.config(state='normal'))
            self.root.after(0, self._update_status, f"{self.i18n.t('error')}: {str(e)}")
            self.root.after(0, lambda msg=error_msg: messagebox.showerror(self.i18n.t('error'), f"{self.i18n.t('analysis_failed')}:\n{msg}"))

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