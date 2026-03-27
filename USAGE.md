# 使用说明 / User Guide

[English](#english) | [中文](#中文)

---

## 中文

### 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **启动程序**
   ```bash
   python main.py
   ```

3. **选择语言**
   - 在界面右上角选择语言（zh_CN 或 en_US）
   - 重启程序使语言生效

4. **分析ELF文件**
   - 点击"浏览"选择ELF文件
   - 可选：选择芯片型号或手动输入ROM/RAM容量
   - 点击"开始分析"
   - 等待分析完成，查看生成的Excel报告

### 语言配置

程序会在首次运行时创建 `config.json` 文件，保存语言设置：

```json
{
  "language": "zh_CN"
}
```

可选值：
- `zh_CN`: 简体中文
- `en_US`: English

### Excel报告说明

生成的Excel报告包含4个工作表：

1. **内存使用摘要** / **Memory Summary**
   - ROM、RAM、Stack、Heap的总体使用情况
   - 包含空隙统计

2. **详细段信息** / **Detailed Sections**
   - 所有内存段的详细信息
   - 显示地址空隙

3. **ROM详细信息** / **ROM Details**
   - ROM相关段的详细分解

4. **RAM详细信息** / **RAM Details**
   - RAM相关段的详细分解

---

## English

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch Program**
   ```bash
   python main.py
   ```

3. **Select Language**
   - Choose language in the top-right corner (zh_CN or en_US)
   - Restart the program for the language change to take effect

4. **Analyze ELF File**
   - Click "Browse" to select an ELF file
   - Optional: Select chip model or manually enter ROM/RAM capacity
   - Click "Start Analysis"
   - Wait for analysis to complete and view the generated Excel report

### Language Configuration

The program creates a `config.json` file on first run to save language settings:

```json
{
  "language": "en_US"
}
```

Available values:
- `zh_CN`: Simplified Chinese
- `en_US`: English

### Excel Report Description

The generated Excel report contains 4 worksheets:

1. **内存使用摘要** / **Memory Summary**
   - Overall usage of ROM, RAM, Stack, Heap
   - Includes gap statistics

2. **详细段信息** / **Detailed Sections**
   - Detailed information for all memory sections
   - Shows address gaps

3. **ROM详细信息** / **ROM Details**
   - Detailed breakdown of ROM-related sections

4. **RAM详细信息** / **RAM Details**
   - Detailed breakdown of RAM-related sections

---

## 技术支持 / Technical Support

如有问题，请提交 Issue：
For issues, please submit an Issue:

https://github.com/your-repo/MemoryMapTool/issues
