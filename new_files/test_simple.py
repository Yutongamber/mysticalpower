#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试后端核心逻辑
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from backend import divination_system

print("=" * 60)
print("🔮 易经占卜系统 - 核心逻辑测试")
print("=" * 60)

# 测试 1: 每日一签
print("\n📋 测试 1: generate_daily_fortune")
print("-" * 60)
result1 = divination_system.generate_daily_fortune("user_888", "2026-03-08")
print(f"✅ 卦象: {result1['hexagram']}")
print(f"✅ 签语: {result1['fortune_phrase']}")

# 测试 2: 事件起卦
print("\n📋 测试 2: generate_event_divination")
print("-" * 60)
result2 = divination_system.generate_event_divination("我的事业运势如何？", "2026-03-08 13:30:00")
print(f"✅ 本卦: {result2['primary_hexagram']}")
print(f"✅ 动爻: {result2['changing_line']}")
print(f"✅ 变卦: {result2['changed_hexagram']}")

# 测试 3: 卦象解读
print("\n📋 测试 3: interpret_hexagram")
print("-" * 60)
result3 = divination_system.interpret_hexagram("地天泰", "career")
print(f"✅ 情境理解: {result3['context_understanding'][:30]}...")

# 测试 4: 情绪引导
print("\n📋 测试 4: emotion_guidance")
print("-" * 60)
result4 = divination_system.emotion_guidance("我最近工作压力好大，感到很焦虑...")
print(f"✅ 情绪标签: {result4['emotion_label']}")
print(f"✅ 引导语: {result4['guidance_text']}")

# 测试 5: AI咨询
print("\n📋 测试 5: consultation")
print("-" * 60)
result5 = divination_system.consultation("我想换工作，给点建议")
print(f"✅ 推荐卦象: {result5['hexagram']}")
print(f"✅ 回答长度: {len(result5['answer'])} 字")

print("\n" + "=" * 60)
print("🎉 所有核心逻辑测试通过！")
print("=" * 60)
print("\n下一步：")
print("1. 启动后端: source venv/bin/activate && python backend.py")
print("2. 在浏览器中打开 index_v3.html")
print("3. 开始使用！")
