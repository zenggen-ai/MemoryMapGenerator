"""
ELF文件解析模块
用于解析GHS编译器生成的ELF文件，提取内存段信息
"""

from elftools.elf.elffile import ELFFile
from typing import Dict, List, Tuple
import os


class MemorySection:
    """内存段信息"""
    def __init__(self, name: str, address: int, size: int, section_type: str):
        self.name = name
        self.address = address
        self.end_address = address + size  # 结束地址
        self.size = size
        self.type = section_type
        self.used_size = 0  # 实际用量（符号占用）
        self.remaining_size = 0  # 剩余容量
        self.symbols = []  # 该段内的符号列表

    def __repr__(self):
        return f"MemorySection({self.name}, 0x{self.address:08X}-0x{self.end_address:08X}, {self.size} bytes, {self.type}, used={self.used_size})"


class ELFAnalyzer:
    """ELF文件分析器"""

    # ROM段类型（代码和只读数据）
    ROM_SECTIONS = {'.text', '.rodata', '.init', '.fini', '.ctors', '.dtors',
                    '.eh_frame', '.gcc_except_table', '.init_array', '.fini_array'}

    # RAM段类型（已初始化数据）
    DATA_SECTIONS = {'.data', '.sdata', '.sdata2'}

    # BSS段类型（未初始化数据）
    BSS_SECTIONS = {'.bss', '.sbss', '.sbss2'}

    # 栈和堆段
    STACK_HEAP_SECTIONS = {'.stack', '.heap'}

    def __init__(self, elf_path: str):
        """
        初始化ELF分析器

        Args:
            elf_path: ELF文件路径
        """
        if not os.path.exists(elf_path):
            raise FileNotFoundError(f"ELF文件不存在: {elf_path}")

        self.elf_path = elf_path
        self.sections: List[MemorySection] = []
        self.elf_file = None
        self._parse_elf()
        self._parse_symbols()

    def _parse_elf(self):
        """解析ELF文件"""
        with open(self.elf_path, 'rb') as f:
            self.elf_file = ELFFile(f)

            # 遍历所有段
            for section in self.elf_file.iter_sections():
                name = section.name
                size = section['sh_size']
                address = section['sh_addr']

                # 跳过空段和无地址段
                if size == 0 or address == 0:
                    continue

                # 判断段类型
                section_type = self._classify_section(name, section)

                if section_type:
                    mem_section = MemorySection(name, address, size, section_type)
                    self.sections.append(mem_section)

    def _classify_section(self, name: str, section) -> str:
        """
        分类内存段

        Args:
            name: 段名称
            section: ELF段对象

        Returns:
            段类型: 'ROM', 'DATA', 'BSS', 'STACK', 'HEAP', 'CUSTOM'
        """
        # 检查段标志
        flags = section['sh_flags']
        is_alloc = flags & 0x2  # SHF_ALLOC
        is_write = flags & 0x1  # SHF_WRITE
        is_exec = flags & 0x4   # SHF_EXECINSTR

        # 必须是可分配的段
        if not is_alloc:
            return None

        # 获取段地址，用于地址范围判断
        address = section['sh_addr']

        # 栈段（优先判断）
        if 'stack' in name.lower():
            return 'STACK'

        # 堆段（优先判断）
        if 'heap' in name.lower():
            return 'HEAP'

        # 根据地址范围判断（基于芯片的内存映射规则）
        # 0xFE 开头的地址：RAM 区域
        if (address & 0xFF000000) == 0xFE000000:
            if section['sh_type'] == 'SHT_NOBITS':
                return 'BSS'
            else:
                return 'DATA'

        # 0x00 开头的地址：ROM 区域
        if (address & 0xFF000000) == 0x00000000:
            return 'ROM'

        # 其他高地址段（>= 0x20000000），通常是 RAM
        if address >= 0x20000000:
            if section['sh_type'] == 'SHT_NOBITS':
                return 'BSS'
            else:
                return 'DATA'

        # 按段名称判断
        if name in self.ROM_SECTIONS:
            return 'ROM'

        if name in self.DATA_SECTIONS:
            return 'DATA'

        if name in self.BSS_SECTIONS:
            return 'BSS'

        # 按标志位判断
        # ROM段：可执行或只读
        if is_exec and not is_write:
            return 'ROM'

        # 其他可写段归类为DATA或BSS
        if is_write:
            # 如果段类型是NOBITS，归类为BSS
            if section['sh_type'] == 'SHT_NOBITS':
                return 'BSS'
            else:
                return 'DATA'

        # 其他只读段归类为ROM
        if not is_write:
            return 'ROM'

        # 自定义段
        return 'CUSTOM'

    def _parse_symbols(self):
        """解析符号表并计算每个段的实际使用量"""
        with open(self.elf_path, 'rb') as f:
            elf = ELFFile(f)

            # 查找符号表
            symtab = elf.get_section_by_name('.symtab')
            if not symtab:
                # 如果没有符号表，所有段的 used_size 保持为 0
                for section in self.sections:
                    section.remaining_size = section.size
                return

            # 为每个段收集符号区间
            section_intervals = {section: [] for section in self.sections}

            # 遍历符号表
            for symbol in symtab.iter_symbols():
                # 过滤有效符号
                if not self._is_valid_symbol(symbol):
                    continue

                sym_addr = symbol['st_value']
                sym_size = symbol['st_size']
                sym_name = symbol.name

                # 查找符号所属的段
                for section in self.sections:
                    # 检查符号起始地址是否在段内
                    if section.address <= sym_addr < section.address + section.size:
                        # 计算符号在该段内的实际范围
                        sym_end = sym_addr + sym_size
                        section_end = section.address + section.size

                        if sym_end > section_end:
                            # 符号超出段边界，只统计段内部分
                            actual_end = section_end
                        else:
                            # 符号完全在段内
                            actual_end = sym_end

                        # 记录符号区间
                        section_intervals[section].append((sym_addr, actual_end))
                        section.symbols.append({
                            'name': sym_name,
                            'address': sym_addr,
                            'size': sym_size,
                            'actual_size': actual_end - sym_addr
                        })
                        break

            # 计算每个段的实际使用量（合并重叠区间）
            for section in self.sections:
                intervals = section_intervals[section]
                if intervals:
                    # 合并重叠区间
                    merged = self._merge_intervals(intervals)
                    # 计算总使用量
                    section.used_size = sum(end - start for start, end in merged)

                section.remaining_size = section.size - section.used_size

    def _merge_intervals(self, intervals):
        """
        合并重叠的地址区间

        Args:
            intervals: 地址区间列表 [(start, end), ...]

        Returns:
            合并后的区间列表
        """
        if not intervals:
            return []

        # 按起始地址排序
        sorted_intervals = sorted(intervals)
        merged = [sorted_intervals[0]]

        for current_start, current_end in sorted_intervals[1:]:
            last_start, last_end = merged[-1]

            if current_start <= last_end:
                # 区间重叠，合并
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                # 区间不重叠，添加新区间
                merged.append((current_start, current_end))

        return merged

    def _is_valid_symbol(self, symbol) -> bool:
        """
        判断符号是否有效

        Args:
            symbol: ELF符号对象

        Returns:
            是否为有效符号
        """
        # 获取符号类型
        sym_type = symbol['st_info']['type']
        sym_shndx = symbol['st_shndx']
        sym_size = symbol['st_size']

        # 排除未定义符号
        if sym_shndx == 'SHN_UNDEF':
            return False

        # 只包含函数和数据对象
        if sym_type not in ('STT_FUNC', 'STT_OBJECT'):
            return False

        # 只包含有大小的符号
        if sym_size == 0:
            return False

        return True

    def get_memory_summary(self) -> Dict[str, Dict[str, int]]:
        """
        获取内存使用摘要

        Returns:
            字典，包含各类型内存的使用情况
        """
        summary = {
            'ROM': {'used': 0, 'sections': []},
            'RAM': {'used': 0, 'sections': []},
            'STACK': {'used': 0, 'sections': []},
            'HEAP': {'used': 0, 'sections': []},
            'CUSTOM': {'used': 0, 'sections': []}
        }

        for section in self.sections:
            if section.type == 'ROM':
                summary['ROM']['used'] += section.size
                summary['ROM']['sections'].append(section)
            elif section.type in ('DATA', 'BSS'):
                summary['RAM']['used'] += section.size
                summary['RAM']['sections'].append(section)
            elif section.type == 'STACK':
                summary['STACK']['used'] += section.size
                summary['STACK']['sections'].append(section)
            elif section.type == 'HEAP':
                summary['HEAP']['used'] += section.size
                summary['HEAP']['sections'].append(section)
            elif section.type == 'CUSTOM':
                summary['CUSTOM']['used'] += section.size
                summary['CUSTOM']['sections'].append(section)

        return summary

    def get_detailed_sections(self) -> List[MemorySection]:
        """
        获取详细的段信息列表

        Returns:
            所有内存段的列表
        """
        return sorted(self.sections, key=lambda x: x.address)
