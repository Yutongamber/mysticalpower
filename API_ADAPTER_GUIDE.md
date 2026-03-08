# API Adapter 使用指南

## 📁 文件说明

- `api-adapter.js` - API 适配器文件，支持 OpenAI 和火山引擎 ARK 两种格式
- `API_ADAPTER_GUIDE.md` - 本文档

---

## 🚀 快速开始

### 方法一：使用 API Adapter（推荐）

1. 在 `index.html` 的 `<head>` 标签中添加：
```html
<script src="api-adapter.js"></script>
```

2. 删除或注释掉 index.html 中原来的这些代码：
   - `const LLM_CONFIG = { ... }`
   - `function selectApiType(...) { ... }`
   - `function callLLM(...) { ... }`
   - `function loadLLMConfigFromStorage(...) { ... }`

3. 确保这些函数使用 `window.LLM_CONFIG` 和 `window.callLLM()`

---

## 🔧 核心功能

### `window.LLM_CONFIG`
全局配置对象：
```javascript
window.LLM_CONFIG = {
    apiType: 'openai',      // 'openai' 或 'ark'
    apiEndpoint: '...',      // API 端点
    apiKey: '',             // API Key
    model: 'gpt-4o-mini',  // 模型名称
    temperature: 0.7,       // 温度参数
    maxTokens: 2000         // 最大 token 数
};
```

### `window.selectApiType(type)`
选择 API 类型并自动设置默认端点和模型：
```javascript
window.selectApiType('openai');  // OpenAI 格式
window.selectApiType('ark');      // 火山引擎 ARK 格式
```

### `window.callLLM(systemPrompt, userMessage, conversationHistory)`
通用 LLM 调用函数：
```javascript
const content = await window.callLLM(
    '你是一个 helpful 的助手',
    '你好',
    []  // 可选：对话历史
);
```

### `window.loadLLMConfigFromStorage()`
从 localStorage 加载配置：
```javascript
window.loadLLMConfigFromStorage();
```

---

## 📋 配置说明

### OpenAI 格式
- API 类型: `openai`
- API 端点: `https://api.openai.com/v1/chat/completions`
- 模型示例: `gpt-4o-mini`, `gpt-4`, `gpt-3.5-turbo`

### 火山引擎 ARK
- API 类型: `ark`
- API 端点: `https://ark.cn-beijing.volces.com/api/v3/responses`
- 模型示例: `glm-4-7-251222`

---

## 🔍 调试功能

API Adapter 内置了详细的调试日志：

```javascript
// 会在控制台输出：
// 🔍 API 调用调试信息：
//    API 类型: ark
//    端点: https://ark.cn-beijing.volces.com/api/v3/responses
//    模型: glm-4-7-251222
//    请求体: {...}
// 📡 响应状态: 200
// 📄 完整响应: {...}
// ✅ 提取到的内容: ...
```

打开浏览器的开发者工具（F12），在 Console 标签页查看详细日志。

---

## 💡 使用示例

### 示例 1：简单调用
```javascript
const content = await window.callLLM(
    '你是一个 helpful 的助手',
    '请用一句话介绍易经'
);
console.log(content);
```

### 示例 2：带对话历史
```javascript
const history = [
    { user: '你好', ai: '你好！有什么可以帮你的？' }
];

const content = await window.callLLM(
    '你是一个 helpful 的助手',
    '今天天气怎么样？',
    history
);
```

### 示例 3：解析 JSON 响应
```javascript
const content = await window.callLLM(systemPrompt, userMessage);

if (content) {
    try {
        const jsonMatch = content.match(/\{[\s\S]*\}/);
        if (jsonMatch) {
            const result = JSON.parse(jsonMatch[0]);
            console.log(result);
        }
    } catch (e) {
        console.error('JSON 解析失败:', e);
    }
}
```

---

## ⚠️ 注意事项

1. **API Key 安全**: API Key 保存在浏览器 localStorage 中，注意保护
2. **CORS**: 直接调用第三方 API 可能遇到 CORS 问题，必要时需要后端代理
3. **降级策略**: API 调用失败时，建议使用固定回复作为降级方案
4. **localStorage**: 配置和历史记录都保存在 localStorage 中，清除浏览器数据会丢失

---

## 🆘 常见问题

### Q: 为什么调用失败？
A: 检查：
1. API 端点是否正确
2. API Key 是否有效
3. 模型名称是否正确
4. 打开浏览器控制台查看详细错误信息

### Q: ARK 格式和 OpenAI 格式有什么区别？
A:
- OpenAI: `messages` + `content: "字符串"`
- ARK: `input` + `content: [{type: "input_text", text: "..."}]`

### Q: 如何切换 API 类型？
A: 调用 `window.selectApiType('openai')` 或 `window.selectApiType('ark')`，会自动设置默认端点和模型。

---

## 📞 技术支持

如有问题，请查看浏览器控制台的调试日志，或者提交 Issue。
