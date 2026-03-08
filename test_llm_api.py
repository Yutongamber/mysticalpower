#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM API 测试脚本
用于测试 OpenAI 兼容格式的 API 是否能正常工作
"""

import requests
import json
import sys


def test_llm_api(api_endpoint, api_key, model="gpt-4o-mini", temperature=0.7, max_tokens=500):
    """
    测试 LLM API
    
    参数:
        api_endpoint: API 端点（例如：https://api.openai.com/v1/chat/completions）
        api_key: API Key
        model: 模型名称
        temperature: 温度参数
        max_tokens: 最大 token 数
    
    返回:
        (success: bool, result: dict)
    """
    print("=" * 70)
    print("🔮 LLM API 测试")
    print("=" * 70)
    print()
    
    # 配置信息
    print("📋 配置信息：")
    print(f"   API 端点: {api_endpoint}")
    print(f"   模型: {model}")
    print(f"   API Key: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else api_key}")
    print()
    
    # 测试消息
    test_messages = [
        {"role": "system", "content": "你是一个 helpful 的助手。"},
        {"role": "user", "content": "请用一句话介绍易经。"}
    ]
    
    # 构建请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": model,
        "messages": test_messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    print("🧪 发送请求...")
    print(f"   提示词: {test_messages[1]['content']}")
    print()
    
    try:
        # 发送请求
        response = requests.post(
            api_endpoint,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 响应状态码: {response.status_code}")
        print()
        
        if response.status_code == 200:
            # 成功
            data = response.json()
            print("✅ API 调用成功！")
            print()
            print("📄 完整响应：")
            print(json.dumps(data, ensure_ascii=False, indent=2))
            print()
            
            # 提取内容
            if "choices" in data and len(data["choices"]) > 0:
                content = data["choices"][0]["message"]["content"]
                print("💬 AI 回复：")
                print(f"   {content}")
                print()
            
            return True, data
        else:
            # 失败
            print("❌ API 调用失败！")
            print()
            print("📄 错误响应：")
            try:
                error_data = response.json()
                print(json.dumps(error_data, ensure_ascii=False, indent=2))
            except:
                print(response.text)
            print()
            
            return False, {"status_code": response.status_code, "text": response.text}
    
    except requests.exceptions.Timeout:
        print("❌ 请求超时！")
        print("   请检查网络连接或 API 端点是否正确。")
        print()
        return False, {"error": "timeout"}
    
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误！")
        print("   请检查 API 端点是否正确，网络是否正常。")
        print()
        return False, {"error": "connection_error"}
    
    except Exception as e:
        print(f"❌ 发生错误：{type(e).__name__}: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        return False, {"error": str(e)}


def main():
    print()
    print("=" * 70)
    print("🔮 LLM API 测试工具")
    print("=" * 70)
    print()
    
    # 默认配置（可以修改这里）
    DEFAULT_API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
    DEFAULT_MODEL = "gpt-4o-mini"
    
    # 从命令行参数获取，或者交互式输入
    if len(sys.argv) >= 3:
        api_endpoint = sys.argv[1]
        api_key = sys.argv[2]
        model = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MODEL
    else:
        print("请输入你的 API 配置：")
        print()
        
        api_endpoint = input(f"API 端点 [{DEFAULT_API_ENDPOINT}]: ").strip()
        if not api_endpoint:
            api_endpoint = DEFAULT_API_ENDPOINT
        
        api_key = input("API Key: ").strip()
        if not api_key:
            print("❌ API Key 不能为空！")
            return
        
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
    else:
        print("❌ 测试失败！")
        print("   请检查配置是否正确。")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
