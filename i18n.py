"""
国际化支持模块
提供中英文语言切换功能
"""

import json
import os


class I18n:
    """国际化管理类"""

    # 支持的语言
    LANGUAGES = {
        'zh_CN': '简体中文',
        'en_US': 'English'
    }

    # 翻译字典
    TRANSLATIONS = {
        'zh_CN': {
            # GUI界面
            'app_title': 'GHS ELF内存分析工具',
            'elf_file': 'ELF文件:',
            'output_excel': '输出Excel:',
            'browse': '浏览...',
            'chip_config': '芯片配置（选择芯片型号或手动输入容量）',
            'chip_model': '芯片型号:',
            'rom_total': 'ROM总容量(KB):',
            'ram_total': 'RAM总容量(KB):',
            'start_analysis': '开始分析',
            'exit': '退出',
            'ready': '就绪',
            'language': '语言:',

            # 文件对话框
            'select_elf': '选择ELF文件',
            'save_excel': '保存Excel报告',
            'elf_files': 'ELF文件',
            'excel_files': 'Excel文件',
            'all_files': '所有文件',

            # 消息框
            'error': '错误',
            'success': '成功',
            'error_no_elf': '请选择ELF文件',
            'error_no_output': '请指定输出文件路径',
            'error_elf_not_exist': 'ELF文件不存在',
            'parsing_elf': '正在解析ELF文件...',
            'generating_excel': '正在生成Excel报告...',
            'analysis_complete': '分析完成！',
            'analysis_failed': '分析失败',
            'rom_usage': 'ROM使用',
            'ram_usage': 'RAM使用',
            'report_saved': '报告已保存至',
            'permission_hint': '提示：请检查输出文件是否已被其他程序打开（如Excel），\n如果是，请关闭后重试，或选择新的输出路径。',

            # Excel报告
            'memory_usage_report': '内存使用统计报告',
            'memory_type': '内存类型',
            'section_size_bytes': '段大小(字节)',
            'actual_usage_bytes': '实际用量(字节)',
            'remaining_bytes': '剩余容量(字节)',
            'section_size_kb': '段大小(KB)',
            'actual_usage_kb': '实际用量(KB)',
            'remaining_kb': '剩余容量(KB)',
            'section_usage_percent': '段使用率(%)',
            'mcu_usage_percent': 'MCU使用率(%)',
            'rom_flash_code': 'ROM (Flash/Code)',
            'ram_data_bss': 'RAM (Data/BSS)',
            'stack': 'Stack (栈)',
            'heap': 'Heap (堆)',
            'rom_gap': 'ROM 空隙',
            'ram_gap': 'RAM 空隙',
            'not_specified': '未指定',
            'na': 'N/A',

            # Excel工作表名称
            'sheet_memory_summary': '内存使用摘要',
            'sheet_detailed_sections': '详细段信息',
            'sheet_rom_details': 'ROM详细信息',
            'sheet_ram_details': 'RAM详细信息',

            # 详细段信息表头
            'section_name': '段名称',
            'address': '地址',
            'section_size': '段大小(字节)',
            'actual_usage': '实际用量(字节)',
            'remaining': '剩余容量(字节)',
            'section_size_kb_short': '段大小(KB)',
            'type': '类型',
            'gap': '空隙',
            'total': '总计',
            'gap_total': '空隙总计',
        },
        'en_US': {
            # GUI界面
            'app_title': 'GHS ELF Memory Analysis Tool',
            'elf_file': 'ELF File:',
            'output_excel': 'Output Excel:',
            'browse': 'Browse...',
            'chip_config': 'Chip Configuration (Select chip model or enter capacity manually)',
            'chip_model': 'Chip Model:',
            'rom_total': 'ROM Total (KB):',
            'ram_total': 'RAM Total (KB):',
            'start_analysis': 'Start Analysis',
            'exit': 'Exit',
            'ready': 'Ready',
            'language': 'Language:',

            # 文件对话框
            'select_elf': 'Select ELF File',
            'save_excel': 'Save Excel Report',
            'elf_files': 'ELF Files',
            'excel_files': 'Excel Files',
            'all_files': 'All Files',

            # 消息框
            'error': 'Error',
            'success': 'Success',
            'error_no_elf': 'Please select an ELF file',
            'error_no_output': 'Please specify output file path',
            'error_elf_not_exist': 'ELF file does not exist',
            'parsing_elf': 'Parsing ELF file...',
            'generating_excel': 'Generating Excel report...',
            'analysis_complete': 'Analysis complete!',
            'analysis_failed': 'Analysis failed',
            'rom_usage': 'ROM Usage',
            'ram_usage': 'RAM Usage',
            'report_saved': 'Report saved to',
            'permission_hint': 'Hint: Please check if the output file is already opened by another program (e.g., Excel).\nIf so, please close it and retry, or select a new output path.',

            # Excel报告
            'memory_usage_report': 'Memory Usage Report',
            'memory_type': 'Memory Type',
            'section_size_bytes': 'Section Size (Bytes)',
            'actual_usage_bytes': 'Actual Usage (Bytes)',
            'remaining_bytes': 'Remaining (Bytes)',
            'section_size_kb': 'Section Size (KB)',
            'actual_usage_kb': 'Actual Usage (KB)',
            'remaining_kb': 'Remaining (KB)',
            'section_usage_percent': 'Section Usage (%)',
            'mcu_usage_percent': 'MCU Usage (%)',
            'rom_flash_code': 'ROM (Flash/Code)',
            'ram_data_bss': 'RAM (Data/BSS)',
            'stack': 'Stack',
            'heap': 'Heap',
            'rom_gap': 'ROM Gap',
            'ram_gap': 'RAM Gap',
            'not_specified': 'Not Specified',
            'na': 'N/A',

            # Excel工作表名称
            'sheet_memory_summary': 'Memory Summary',
            'sheet_detailed_sections': 'Detailed Sections',
            'sheet_rom_details': 'ROM Details',
            'sheet_ram_details': 'RAM Details',

            # 详细段信息表头
            'section_name': 'Section Name',
            'address': 'Address',
            'section_size': 'Section Size (Bytes)',
            'actual_usage': 'Actual Usage (Bytes)',
            'remaining': 'Remaining (Bytes)',
            'section_size_kb_short': 'Size (KB)',
            'type': 'Type',
            'gap': 'Gap',
            'total': 'Total',
            'gap_total': 'Gap Total',
        }
    }

    def __init__(self):
        """初始化国际化管理器"""
        self.config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        self.current_language = self._load_language()

    def _load_language(self):
        """从配置文件加载语言设置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    lang = config.get('language', 'zh_CN')
                    if lang in self.LANGUAGES:
                        return lang
            except:
                pass
        return 'zh_CN'  # 默认中文

    def _save_language(self):
        """保存语言设置到配置文件"""
        try:
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

            config['language'] = self.current_language

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except:
            pass

    def set_language(self, language):
        """设置当前语言"""
        if language in self.LANGUAGES:
            self.current_language = language
            self._save_language()

    def get_language(self):
        """获取当前语言"""
        return self.current_language

    def get_language_name(self):
        """获取当前语言名称"""
        return self.LANGUAGES.get(self.current_language, 'Unknown')

    def t(self, key):
        """翻译指定的键"""
        translations = self.TRANSLATIONS.get(self.current_language, {})
        return translations.get(key, key)

    def get_font_name(self):
        """获取适合当前语言的字体名称"""
        if self.current_language == 'zh_CN':
            return '微软雅黑'
        else:
            return 'Arial'


# 全局实例
_i18n_instance = None


def get_i18n():
    """获取国际化实例（单例模式）"""
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18n()
    return _i18n_instance
