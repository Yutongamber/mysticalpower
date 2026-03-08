/**
 * Netlify Function: LLM API 代理
 * 解决前端直接调用 LLM API 的 CORS 问题
 */

// 带超时的 fetch
async function fetchWithTimeout(url, options, timeout = 60000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error(`请求超时 (${timeout/1000}秒)`);
        }
        throw error;
    }
}

exports.handler = async (event, context) => {
    // 设置 CORS 头
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // 处理 OPTIONS 预检请求
    if (event.httpMethod === 'OPTIONS') {
        return {
            statusCode: 200,
            headers,
            body: ''
        };
    }

    // 只允许 POST 请求
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        // 解析请求体
        const requestData = JSON.parse(event.body);
        const { apiType, apiEndpoint, apiKey, requestBody } = requestData;

        if (!apiEndpoint || !apiKey || !requestBody) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: '缺少必要参数: apiEndpoint, apiKey, requestBody' })
            };
        }

        console.log('🔍 代理请求:');
        console.log('   API 类型:', apiType);
        console.log('   端点:', apiEndpoint);
        console.log('   模型:', requestBody.model);

        // 转发请求到实际的 LLM API（60秒超时）
        const response = await fetchWithTimeout(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify(requestBody)
        }, 60000);

        // 获取响应
        const responseText = await response.text();

        console.log('📡 响应状态:', response.status);

        // 尝试解析为 JSON
        let responseData;
        try {
            responseData = JSON.parse(responseText);
        } catch (e) {
            // 如果不是 JSON，返回原始文本
            responseData = { raw: responseText };
        }

        // 返回响应
        return {
            statusCode: response.status,
            headers,
            body: JSON.stringify({
                success: response.ok,
                status: response.status,
                data: responseData
            })
        };

    } catch (error) {
        console.error('❌ 代理错误:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({
                success: false,
                error: error.message || '代理请求失败'
            })
        };
    }
};
