"""
国际化功能测试脚本
"""

from i18n import get_i18n

def test_i18n():
    """测试国际化功能"""
    print("=" * 60)
    print("国际化功能测试 / I18n Functionality Test")
    print("=" * 60)

    i18n = get_i18n()

    # 测试中文
    print("\n1. 测试中文 (Testing Chinese)")
    print("-" * 60)
    i18n.set_language('zh_CN')
    print(f"当前语言 / Current Language: {i18n.get_language_name()}")
    print(f"应用标题 / App Title: {i18n.t('app_title')}")
    print(f"开始分析 / Start Analysis: {i18n.t('start_analysis')}")
    print(f"字体名称 / Font Name: {i18n.get_font_name()}")

    # 测试英文
    print("\n2. 测试英文 (Testing English)")
    print("-" * 60)
    i18n.set_language('en_US')
    print(f"当前语言 / Current Language: {i18n.get_language_name()}")
    print(f"应用标题 / App Title: {i18n.t('app_title')}")
    print(f"开始分析 / Start Analysis: {i18n.t('start_analysis')}")
    print(f"字体名称 / Font Name: {i18n.get_font_name()}")

    # 测试Excel相关翻译
    print("\n3. 测试Excel翻译 (Testing Excel Translations)")
    print("-" * 60)

    # 中文
    i18n.set_language('zh_CN')
    print("中文 (Chinese):")
    print(f"  - 工作表名称: {i18n.t('sheet_memory_summary')}")
    print(f"  - ROM类型: {i18n.t('rom_flash_code')}")
    print(f"  - RAM类型: {i18n.t('ram_data_bss')}")
    print(f"  - 空隙: {i18n.t('gap')}")

    # 英文
    i18n.set_language('en_US')
    print("\n英文 (English):")
    print(f"  - Sheet Name: {i18n.t('sheet_memory_summary')}")
    print(f"  - ROM Type: {i18n.t('rom_flash_code')}")
    print(f"  - RAM Type: {i18n.t('ram_data_bss')}")
    print(f"  - Gap: {i18n.t('gap')}")

    # 测试消息框翻译
    print("\n4. 测试消息框翻译 (Testing Message Box Translations)")
    print("-" * 60)

    # 中文
    i18n.set_language('zh_CN')
    print("中文 (Chinese):")
    print(f"  - 错误: {i18n.t('error')}")
    print(f"  - 成功: {i18n.t('success')}")
    print(f"  - 分析完成: {i18n.t('analysis_complete')}")

    # 英文
    i18n.set_language('en_US')
    print("\n英文 (English):")
    print(f"  - Error: {i18n.t('error')}")
    print(f"  - Success: {i18n.t('success')}")
    print(f"  - Analysis Complete: {i18n.t('analysis_complete')}")

    print("\n" + "=" * 60)
    print("测试完成！/ Test Complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_i18n()
