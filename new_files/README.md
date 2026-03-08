# 🔮 易经占卜系统 - MysticalPower

基于易经的占卜系统，支持每日一签、事件起卦、AI咨询和情绪陪伴。

## 📋 当前状态

**Phase 1 已完成：**
- ✅ 后端服务（FastAPI）
- ✅ 前端页面（调用后端API）
- ✅ 规则引擎（现有逻辑）

**Phase 2 进行中：**
- 🔄 LLM集成（待实现）

## 🚀 快速开始

### 方法一：使用启动脚本（推荐）

```bash
./start.sh
```

### 方法二：手动启动

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动后端服务
python backend.py
```

启动后端后，在浏览器中打开 `index_v3.html` 即可使用。

## 📁 文件说明

- `backend.py` - FastAPI 后端服务
- `index_v3.html` - 前端页面（调用后端API）
- `requirements.txt` - Python 依赖
- `.env.example` - 环境配置示例
- `start.sh` - 启动脚本

## 🔌 API 接口

### 健康检查
```
GET /health
```

### 每日一签
```
POST /api/daily-fortune
{
  "user_id": "user_xxx",
  "date_str": "2026-03-08"
}
```

### 事件起卦
```
POST /api/divination
{
  "question_text": "我的事业运势如何？",
  "method": "coins"
}
```

### AI咨询
```
POST /api/consultation
{
  "question": "我想换工作，给点建议"
}
```

### 情绪陪伴
```
POST /api/emotion-guidance
{
  "text_input": "我最近工作压力好大"
}
```

## 🎯 技术架构

```
前端 (HTML/JS) → 后端 (FastAPI) → 规则引擎
                                    ↓ (Phase 2)
                                  LLM API
```

## 📝 Phase 2 计划

- [ ] 集成 LLM API（OpenAI/Claude/豆包）
- [ ] 设计 LLM 提示词模板
- [ ] 实现降级策略（LLM 不可用时回退到规则引擎）
- [ ] 增强卦象解读
- [ ] 优化 AI 咨询功能

## 🛠️ 开发说明

### 添加新的 API 接口

在 `backend.py` 中添加：

```python
@app.post("/api/your-endpoint")
async def your_endpoint(request: YourRequestModel):
    # 你的逻辑
    return {"success": True, "data": result}
```

### 前端调用 API

在 `index_v3.html` 中使用：

```javascript
const result = await apiCall('/api/your-endpoint', {
  key: value
});
```

## 📄 许可证

MIT License
