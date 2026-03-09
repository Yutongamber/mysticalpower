# 🔮 MysticalPower - 易经占卜系统

基于易经的 AI 占卜系统，支持每日一签、事件起卦、AI咨询和情绪陪伴。

## ✨ 功能特性

- 📅 **每日一签** - 抽取今日卦象
- 🎲 **起卦占卜** - 支持铜钱起卦和时间起卦
- 🤖 **AI咨询** - Oracle AI 人生顾问
- 💭 **情绪陪伴** - 基于易经的情绪陪伴
- 📝 **历史记录** - 保存占卜历史
- 🔧 **多 API 支持** - 兼容 OpenAI 和火山引擎 ARK

---

## 🚀 快速开始

### 1. 打开页面

直接在浏览器中打开 `index.html` 即可使用！
或者`python -m http.server 8080`然后打开`http://localhost:8080/`

### 2. 配置 API

进入设置页面，配置你的 LLM API：

#### 选项一：OpenAI 格式
- **API 类型**: 选择 "🟢 OpenAI 格式"
- **API 端点**: `https://api.openai.com/v1/chat/completions`
- **API Key**: 你的 OpenAI API Key
- **模型名称**: `gpt-4o-mini`（或其他模型）

#### 选项二：火山引擎 ARK
- **API 类型**: 选择 "🔴 火山引擎 ARK"
- **API 端点**: `https://ark.cn-beijing.volces.com/api/v3/responses`
- **API Key**: 你的火山引擎 API Key
- **模型名称**: `glm-4-7-251222`（或其他模型）

### 3. 开始使用

配置完成后，就可以使用所有 AI 功能了！

---

## 🔧 配置说明

### API 类型选择

系统支持两种 API 格式：

| API 类型 | 端点格式 | 适用平台 |
|---------|---------|---------|
| **OpenAI 格式** | `/api/v3/chat/completions` | OpenAI、Azure OpenAI、其他兼容平台 |
| **火山引擎 ARK** | `/api/v3/responses` | 火山引擎 ARK |

### 配置保存

配置会自动保存到浏览器的 `localStorage` 中，刷新页面后不会丢失。

---

## 📋 功能说明

### 📅 每日一签
- 每天每人抽到的签文是固定的（基于日期和用户ID）
- 包含卦象、签语和行动建议

### 🎲 起卦占卜
- **铜钱起卦**：模拟铜钱摇卦过程
- **时间起卦**：基于当前时间起卦
- 起卦后可以查看详细解读
- 支持围绕卦象继续提问（Hexagram Conversation）

### 🤖 AI咨询
- 基于易经哲学的人生咨询
- 支持多轮对话
- 对话历史自动保存

### 💭 情绪陪伴
- 选择情绪类型
- AI 推荐合适的卦象
- 给出温暖的安抚建议

---

## 🔍 调试工具

### API 调试页面

如果遇到 API 调用问题，可以使用调试工具：

- `debug.html` - 通用 API 调试工具
- `debug_ark.html` - 火山引擎 ARK 专用调试工具

### 常见问题

#### Q: API 调用失败怎么办？
A: 
1. 检查 API 端点是否正确
2. 确认 API Key 是否有效
3. 检查模型名称是否正确
4. 使用调试页面测试 API 是否正常

#### Q: 火山引擎 ARK 格式有什么不同？
A: 
- 端点: `/api/v3/responses`（不是 `/chat/completions`）
- 请求字段: 用 `input` 而不是 `messages`
- 内容格式: `content: [{type: "input_text", text: "..."}]`

#### Q: 历史记录存在哪里？
A: 存在浏览器的 `localStorage` 中，清缓存会丢失。

---

## 🤔 什么时候需要后端？

### 当前纯前端架构的优势：
- ✅ 无需服务器，开箱即用
- ✅ 部署简单，只需静态文件
- ✅ 隐私性好，数据留在本地

### 需要后端的场景：
- 🔐 **API Key 安全** - 把 Key 存在服务端，前端不接触
- 📱 **多设备同步** - 手机、电脑都能看到历史
- 💾 **数据持久化** - 长期保存，不丢失
- 💰 **成本控制** - 服务端缓存，复用结果
- 👥 **用户系统** - 多用户支持
- ⚙️ **复杂逻辑** - 个性化推荐、数据分析等

---

## 📄 项目结构

```
mysticalpower/
├── index.html          # 主页面
├── index.html.backup   # 备份文件
├── README.md          # 本文档
├── debug.html         # 通用调试工具
├── debug_ark.html     # ARK 专用调试工具
└── test_llm_api.py    # Python API 测试脚本
```

---

## 🎯 技术栈

- **前端**: 原生 HTML/CSS/JavaScript
- **存储**: localStorage
- **AI API**: OpenAI 兼容格式 / 火山引擎 ARK
- **设计**: 东方美学，神秘风格

---

## 📝 更新日志

### v2.0 - 火山引擎 ARK 支持
- 支持 OpenAI 和火山引擎 ARK 两种 API 格式
- 添加 API 类型选择
- 自动格式转换
- 更新设置页面

### v1.0 - 初始版本
- 基础占卜功能
- OpenAI API 集成
- 历史记录功能

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 💡 免责声明

本系统仅供娱乐和参考，不构成任何决策建议。易经智慧重在启发思考，人生决策请理性判断。
