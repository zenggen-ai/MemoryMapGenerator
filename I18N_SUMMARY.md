# 国际化实现总结 / Internationalization Implementation Summary

## 实现内容 / Implementation

### 1. 新增文件 / New Files

- **i18n.py**: 国际化核心模块，提供语言切换和翻译功能
- **config.json**: 自动生成的配置文件，保存用户的语言偏好
- **README_EN.md**: 英文版项目文档
- **USAGE.md**: 中英文双语使用说明
- **test_i18n.py**: 国际化功能测试脚本

### 2. 修改文件 / Modified Files

- **main.py**:
  - 集成国际化支持
  - 添加语言选择器
  - 所有界面文本使用翻译函数

- **excel_generator.py**:
  - 接收 i18n 实例
  - Excel报告内容支持多语言
  - 工作表名称、表头、标签等全部国际化

- **README.md**:
  - 添加多语言支持说明
  - 更新版本历史

## 支持的语言 / Supported Languages

- **zh_CN**: 简体中文 (默认)
- **en_US**: English

## 功能特性 / Features

### 1. 自动语言检测
- 首次运行默认使用中文
- 语言设置自动保存到 config.json
- 下次启动自动加载上次选择的语言

### 2. 完整的界面翻译
- GUI界面所有文本
- 文件对话框标题和过滤器
- 消息框标题和内容
- 状态提示信息

### 3. Excel报告国际化
- 工作表名称
- 表头和列名
- 内存类型标签
- 统计信息标签

### 4. 字体自适应
- 中文使用"微软雅黑"
- 英文使用"Arial"

## 使用方法 / Usage

### 切换语言 / Change Language

1. 在界面右上角选择语言下拉框
2. 选择 "zh_CN" (中文) 或 "en_US" (英文)
3. 重启应用程序使更改生效

### 编程方式 / Programmatic

```python
from i18n import get_i18n

# 获取国际化实例
i18n = get_i18n()

# 获取当前语言
current_lang = i18n.get_language()  # 'zh_CN' 或 'en_US'

# 切换语言
i18n.set_language('en_US')

# 翻译文本
title = i18n.t('app_title')

# 获取适合当前语言的字体
font_name = i18n.get_font_name()
```

## 扩展新语言 / Adding New Languages

要添加新语言，只需在 `i18n.py` 中：

1. 在 `LANGUAGES` 字典中添加语言代码和名称
2. 在 `TRANSLATIONS` 字典中添加该语言的翻译

示例 / Example:

```python
LANGUAGES = {
    'zh_CN': '简体中文',
    'en_US': 'English',
    'ja_JP': '日本語'  # 新增日语
}

TRANSLATIONS = {
    'zh_CN': { ... },
    'en_US': { ... },
    'ja_JP': {  # 新增日语翻译
        'app_title': 'GHS ELFメモリ解析ツール',
        'start_analysis': '解析開始',
        ...
    }
}
```

## 测试 / Testing

运行测试脚本验证国际化功能：

```bash
python test_i18n.py
```

## 注意事项 / Notes

1. **语言切换需要重启**: 由于 tkinter 的限制，语言切换后需要重启应用程序才能完全生效

2. **配置文件位置**: config.json 保存在项目根目录，与 main.py 同级

3. **编码问题**: 所有文件使用 UTF-8 编码，确保中文正常显示

4. **Excel字体**: Excel报告会根据选择的语言自动使用合适的字体

## 版本历史 / Version History

### v1.1.0 (2026-03-27)
- ✅ 实现完整的中英文双语支持
- ✅ GUI界面国际化
- ✅ Excel报告国际化
- ✅ 语言配置持久化
- ✅ 字体自适应
- ✅ 创建双语文档

### v1.0.0 (2026-03-26)
- 初始版本（仅中文）
