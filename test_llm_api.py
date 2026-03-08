#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM API 测试脚本 - 使用 OpenAI SDK
支持火山引擎 ARK 等 OpenAI 兼容格式的 API
"""

import os
import sys
from openai import OpenAI


def test_llm_api(api_endpoint, api_key, model="gpt-4o-mini", temperature=0.7, max_tokens=500):
    """
    测试 LLM API（使用 OpenAI SDK）
    
    参数:
        api_endpoint: API 端点（例如：https://ark.cn-beijing.volces.com/api/v3）
        api_key: API Key
        model: 模型名称
        temperature: 温度参数
        max_tokens: 最大 token 数
    
    返回:
        (success: bool, result: dict)
    """
    print("=" * 70)
    print("🔮 LLM API 测试 (OpenAI SDK)")
    print("=" * 70)
    print()
    
    # 配置信息
    print("📋 配置信息：")
    print(f"   API 端点: {api_endpoint}")
    print(f"   模型: {model}")
    print(f"   API Key: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else api_key}")
    print()
    
    try:
        # 初始化客户端
        print("🔧 初始化 OpenAI 客户端...")
        client = OpenAI(
            base_url=api_endpoint,
            api_key=api_key
        )
        print("✅ 客户端初始化成功")
        print()
        
        # 测试消息
        test_messages = [
            {"role": "system", "content": "你是一个 helpful 的助手。"},
            {"role": "user", "content": "请用一句话介绍易经。"}
        ]
        
        print("🧪 发送请求...")
        print(f"   提示词: {test_messages[1]['content']}")
        print()
        
        # 发送请求
        response = client.chat.completions.create(
            model=model,
            messages=test_messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        print("✅ API 调用成功！")
        print()
        print("📄 完整响应对象：")
        print(response)
        print()
        
        # 提取内容
        if response.choices and len(response.choices) > 0:
            content = response.choices[0].message.content
            print("💬 AI 回复：")
            print(f"   {content}")
            print()
            
            # 打印用量信息
            if response.usage:
                print("📊 使用量统计：")
                print(f"   Prompt tokens: {response.usage.prompt_tokens}")
                print(f"   Completion tokens: {response.usage.completion_tokens}")
                print(f"   Total tokens: {response.usage.total_tokens}")
                print()
        
        return True, response
    
    except Exception as e:
        print(f"❌ 发生错误：{type(e).__name__}: {e}")
        print()
        
        # 尝试获取更详细的错误信息
        if hasattr(e, 'response') and e.response is not None:
            print("📄 错误响应：")
            try:
                print(e.response.json())
            except:
                print(e.response.text)
            print()
        
        import traceback
        traceback.print_exc()
        print()
        
        return False, {"error": str(e)}


def main():
    print()
    print("=" * 70)
    print("🔮 LLM API 测试工具 (OpenAI SDK)")
    print("=" * 70)
    print()
    
    # 默认配置 - 火山引擎 ARK
    DEFAULT_API_ENDPOINT = "https://ark.cn-beijing.volces.com/api/v3"
    DEFAULT_MODEL = "glm-4-7-251222"
    
    # 尝试从环境变量获取
    env_api_key = os.getenv('ARK_API_KEY')
    
    # 从命令行参数获取，或者交互式输入
    api_endpoint = None
    api_key = None
    model = None
    
    if len(sys.argv) >= 3:
        api_endpoint = sys.argv[1]
        api_key = sys.argv[2]
        model = sys.argv[3] if len(sys.argv) > 3 else None
    elif env_api_key:
        print("📦 从环境变量 ARK_API_KEY 读取到 API Key")
        print()
        api_endpoint = DEFAULT_API_ENDPOINT
        api_key = env_api_key
        model = DEFAULT_MODEL
    
    if not api_endpoint or not api_key:
        print("请输入你的 API 配置：")
        print()
        
        if not api_endpoint:
            api_endpoint = input(f"API 端点 [{DEFAULT_API_ENDPOINT}]: ").strip()
            if not api_endpoint:
                api_endpoint = DEFAULT_API_ENDPOINT
        
        if not api_key:
            api_key = input("API Key: ").strip()
            if not api_key:
                print("❌ API Key 不能为空！")
                return
        
        if not model:
            model = input(f"模型名称 [{DEFAULT_MODEL}]: ").strip()
            if not model:
                model = DEFAULT_MODEL
        
        print()
    
    # 运行测试
    success, result = test_llm_api(
        api_endpoint=api_endpoint,
        api_key=api_key,
        model=model
    )
    
    print("=" * 70)
    if success:
        print("🎉 测试通过！API 工作正常！")
        print("   你可以在网页中使用相同的配置了。")
        print()
        print("💡 提示：在网页设置中填入：")
        print(f"   API 端点: {api_endpoint}")
        print(f"   API Key: {api_key[:10]}...")
        print(f"   模型: {model}")
    else:
        print("❌ 测试失败！")
        print("   请检查配置是否正确。")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
