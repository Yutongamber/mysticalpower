/**
 * MysticalPower - API Adapter
 * 支持 OpenAI 和火山引擎 ARK 两种格式的 API 适配器
 */

(function() {
    'use strict';

    // 全局配置
    window.LLM_CONFIG = {
        apiType: 'openai', // 'openai' 或 'ark'
        apiEndpoint: 'https://api.openai.com/v1/chat/completions',
        apiKey: '',
        model: 'gpt-4o-mini',
        temperature: 0.7,
        maxTokens: 2000
    };

    /**
     * 选择 API 类型
     */
    window.selectApiType = function(type) {
        window.LLM_CONFIG.apiType = type;
        
        // 更新按钮样式（如果元素存在）
        const btnOpenai = document.getElementById('api-type-openai');
        const btnArk = document.getElementById('api-type-ark');
        
        if (btnOpenai) btnOpenai.classList.remove('selected');
        if (btnArk) btnArk.classList.remove('selected');
        
        const activeBtn = document.getElementById('api-type-' + type);
        if (activeBtn) activeBtn.classList.add('selected');
        
        // 自动设置默认端点和模型
        if (type === 'openai') {
            const endpointInput = document.getElementById('api-endpoint');
            const modelInput = document.getElementById('model-name');
            if (endpointInput) endpointInput.value = 'https://api.openai.com/v1/chat/completions';
            if (modelInput) modelInput.value = 'gpt-4o-mini';
        } else if (type === 'ark') {
            const endpointInput = document.getElementById('api-endpoint');
            const modelInput = document.getElementById('model-name');
            if (endpointInput) endpointInput.value = 'https://ark.cn-beijing.volces.com/api/v3/responses';
            if (modelInput) modelInput.value = 'glm-4-7-251222';
        }
    };

    /**
     * 通用 LLM 调用函数（支持 OpenAI 和 ARK 格式）
     */
    window.callLLM = async function(systemPrompt, userMessage, conversationHistory = []) {
        if (!window.LLM_CONFIG.apiKey.trim()) {
            console.log('未配置 API Key');
            return null;
        }
        
        let requestBody;
        let endpoint = window.LLM_CONFIG.apiEndpoint;
        
        if (window.LLM_CONFIG.apiType === 'openai') {
            // OpenAI 格式
            let messages = [{ role: 'system', content: systemPrompt }];
            
            // 添加历史对话
            conversationHistory.forEach(chat => {
                messages.push({ role: 'user', content: chat.user });
                if (chat.ai) {
                    messages.push({ role: 'assistant', content: typeof chat.ai === 'string' ? chat.ai : JSON.stringify(chat.ai) });
                }
            });
            
            // 添加当前用户消息
            messages.push({ role: 'user', content: userMessage });
            
            requestBody = {
                model: window.LLM_CONFIG.model,
                messages: messages,
                temperature: window.LLM_CONFIG.temperature,
                max_tokens: window.LLM_CONFIG.maxTokens
            };
        } else if (window.LLM_CONFIG.apiType === 'ark') {
            // 火山引擎 ARK 格式
            let input = [];
            
            // 添加历史对话
            conversationHistory.forEach(chat => {
                input.push({
                    role: 'user',
                    content: [{ type: 'input_text', text: chat.user }]
                });
                if (chat.ai) {
                    input.push({
                        role: 'assistant',
                        content: [{ type: 'input_text', text: typeof chat.ai === 'string' ? chat.ai : JSON.stringify(chat.ai) }]
                    });
                }
            });
            
            // 添加系统提示和当前用户消息
            const fullMessage = systemPrompt ? `${systemPrompt}\n\n${userMessage}` : userMessage;
            input.push({
                role: 'user',
                content: [{ type: 'input_text', text: fullMessage }]
            });
            
            requestBody = {
                model: window.LLM_CONFIG.model,
                input: input
            };
        } else {
            throw new Error('未知的 API 类型');
        }
        
        console.log('🔍 API 调用调试信息：');
        console.log('   API 类型:', window.LLM_CONFIG.apiType);
        console.log('   端点:', endpoint);
        console.log('   模型:', window.LLM_CONFIG.model);
        console.log('   请求体:', JSON.stringify(requestBody, null, 2));
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${window.LLM_CONFIG.apiKey}`
                },
                body: JSON.stringify(requestBody)
            });
            
            console.log('📡 响应状态:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API 请求失败:', response.status, errorText);
                return null;
            }
            
            const data = await response.json();
            console.log('📄 完整响应:', data);
            
            // 提取回复内容
            let content;
            if (window.LLM_CONFIG.apiType === 'openai') {
                content = data.choices[0].message.content.trim();
            } else if (window.LLM_CONFIG.apiType === 'ark') {
                // ARK 格式 - 尝试提取内容
                if (data.output && data.output.message && data.output.message.content) {
                    content = data.output.message.content;
                } else if (data.choices && data.choices.length > 0) {
                    content = data.choices[0].message.content.trim();
                } else {
                    console.error('❌ 无法从 ARK 响应中提取内容:', data);
                    return null;
                }
            }
            
            console.log('✅ 提取到的内容:', content);
            return content;
            
        } catch (error) {
            console.error('❌ LLM 调用失败:', error);
            return null;
        }
    };

    /**
     * 从 localStorage 加载配置
     */
    window.loadLLMConfigFromStorage = function() {
        const savedType = localStorage.getItem('llm_api_type');
        const savedEndpoint = localStorage.getItem('llm_api_endpoint');
        const savedKey = localStorage.getItem('llm_api_key');
        const savedModel = localStorage.getItem('llm_model');
        
        if (savedType) {
            window.LLM_CONFIG.apiType = savedType;
        }
        
        if (savedEndpoint) {
            window.LLM_CONFIG.apiEndpoint = savedEndpoint;
        }
        
        if (savedKey) {
            window.LLM_CONFIG.apiKey = savedKey;
        }
        
        if (savedModel) {
            window.LLM_CONFIG.model = savedModel;
        }
    };

    console.log('✅ API Adapter 已加载');
})();
