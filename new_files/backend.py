#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
易经占卜系统 - Backend API
基于 FastAPI 的后端服务
"""

import os
import json
import random
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 加载环境变量
load_dotenv()

app = FastAPI(title="易经占卜系统 API", version="2.0")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 请求模型 ==========
class DailyFortuneRequest(BaseModel):
    user_id: str
    date_str: Optional[str] = None


class DivinationRequest(BaseModel):
    question_text: str
    time_str: Optional[str] = None
    method: Optional[str] = "coins"


class InterpretHexagramRequest(BaseModel):
    hexagram_id: str
    question_type: Optional[str] = "general"


class EmotionGuidanceRequest(BaseModel):
    text_input: str


class ConsultationRequest(BaseModel):
    question: str


# ========== 占卜系统类 ==========
class DivinationSystem:
    """
    易经占卜系统
    """
    
    def __init__(self):
        # ========== 六十四卦数据 ==========
        self.hexagrams = [
            "乾为天", "坤为地", "水雷屯", "山水蒙", "水天需", "天水讼", "地水师", "水地比",
            "风天小畜", "天泽履", "地天泰", "天地否", "天火同人", "火天大有", "地山谦", "雷地豫",
            "泽雷随", "山风蛊", "地泽临", "风地观", "火雷噬嗑", "山火贲", "山地剥", "地雷复",
            "天雷无妄", "山天大畜", "山雷颐", "泽风大过", "坎为水", "离为火", "泽山咸", "雷风恒",
            "天山遁", "雷天大壮", "火地晋", "地火明夷", "风火家人", "火泽睽", "水山蹇", "雷水解",
            "山泽损", "风雷益", "泽天夬", "天风姤", "泽地萃", "地风升", "泽水困", "水风井",
            "泽火革", "火风鼎", "震为雷", "艮为山", "风山渐", "雷泽归妹", "雷火丰", "火山旅",
            "巽为风", "兑为泽", "风水涣", "水泽节", "风泽中孚", "雷山小过", "水火既济", "火水未济"
        ]
        
        # ========== 常用卦数据（简化版） ==========
        self.common_hexagrams = ["乾为天", "坤为地", "地天泰", "天地否", "水天需", "山水蒙"]
        
        # ========== 卦象解读数据库 ==========
        self.hexagram_db = {
            "乾为天": {
                "context": "你正处于充满活力和机遇的时期，可以积极展现自己。",
                "symbolism": "乾卦象天，代表刚健进取，如太阳般充满能量。",
                "advice": "保持积极心态，把握机遇，展现能力，保持谦虚。",
                "emotion": "相信自己的能力，你有足够的力量去面对挑战。"
            },
            "坤为地": {
                "context": "你正处于需要稳定和包容的时期，学会承受和接纳。",
                "symbolism": "坤卦象地，代表包容稳定，如大地般宽厚温和。",
                "advice": "保持稳重踏实，学会倾听，多关心他人，打好基础。",
                "emotion": "大地能承载万物，你也能包容一切，保持耐心。"
            },
            "地天泰": {
                "context": "你正处于运势极佳的时期，天地交融万事顺遂。",
                "symbolism": "上坤下乾地在天上，象征天地交泰吉祥如意。",
                "advice": "把握机遇，顺势而为，保持谦虚，感恩身边的人。",
                "emotion": "恭喜你！这是运势极佳的一卦，好好把握。"
            },
            "天地否": {
                "context": "你正处于运势受阻的时期，诸事不顺需要韬光养晦。",
                "symbolism": "上乾下坤天在地上，象征天地不交闭塞不通。",
                "advice": "韬光养晦，保存实力，不要冒险，充实自己等待转机。",
                "emotion": "人生有起有落，这只是暂时的，相信否极泰来。"
            },
            "水天需": {
                "context": "你正处于等待时机的阶段，需要一些耐心和准备。",
                "symbolism": "上坎下乾水在天上，象征等待降雨时机成熟。",
                "advice": "耐心等待，做好准备，不要急躁，保持乐观心态。",
                "emotion": "好饭不怕晚，好的时机值得等待，你已经准备好了。"
            },
            "山水蒙": {
                "context": "你正处于学习探索的阶段，保持好奇心和求知欲。",
                "symbolism": "上艮下坎山在水上，象征蒙昧待启需要学习引导。",
                "advice": "保持谦虚，主动请教，不要不懂装懂，循序渐进。",
                "emotion": "学习是渐进的过程，不懂是正常的，保持好奇心。"
            }
        }
        
        # ========== 变卦映射 ==========
        self.changed_hexagram_map = {
            "乾为天": "天风姤",
            "坤为地": "地雷复",
            "地天泰": "地泽临",
            "天地否": "天山遁",
            "水天需": "水风井",
            "山水蒙": "山地剥"
        }
        
        # ========== 每日一签数据 ==========
        self.daily_symbolism = {
            "乾为天": "刚健进取，自强不息",
            "坤为地": "厚德载物，柔顺包容",
            "地天泰": "天地交泰，吉祥如意",
            "天地否": "天地不交，闭塞不通",
            "水天需": "等待时机，待机而动",
            "山水蒙": "启蒙发智，虚心求学"
        }
        
        self.daily_advice = {
            "乾为天": "积极进取，把握机遇",
            "坤为地": "稳重踏实，厚积薄发",
            "地天泰": "把握机遇，顺势而为",
            "天地否": "韬光养晦，等待转机",
            "水天需": "耐心等待，时机成熟",
            "山水蒙": "学习积累，虚心求教"
        }
        
        self.emotion_tips = [
            "保持平和的心态", "相信自己的能力",
            "一切都会好起来的", "耐心等待转机",
            "保持积极乐观", "珍惜当下时光"
        ]
        
        self.fortune_phrases = [
            "今日运势上佳，把握机遇", "保持耐心，好事自然来",
            "今天适合学习和积累", "人际关系顺利，心情愉快",
            "稳步前进，不要急躁", "相信自己，你能做到",
            "新的开始，新的希望", "保持谦虚，路会更宽"
        ]
        
        # ========== 情绪引导数据 ==========
        self.emotion_labels = ["焦虑", "迷茫", "失落", "冲动", "愤怒", "孤独"]
        
        self.emotion_guidances = {
            "焦虑": "我能感受到你现在的焦虑，没关系，让我们一起来面对。",
            "迷茫": "感到迷茫是很正常的，给自己一点时间，答案会慢慢浮现。",
            "失落": "我知道你现在有些失落，这都会过去的，你不是一个人。",
            "冲动": "深呼吸，让我们先冷静下来，再想想怎么做更好。",
            "愤怒": "我理解你的愤怒，试着让自己平静一点，好吗？",
            "孤独": "感到孤独的时候，记得还有我在这里陪着你。"
        }
        
        self.recommended_hexagrams = {
            "焦虑": ["水天需", "地山谦", "风地观", "艮为山"],
            "迷茫": ["山水蒙", "巽为风", "风水涣", "地风升"],
            "失落": ["地天泰", "火天大有", "雷地豫", "泽火革"],
            "冲动": ["艮为山", "坤为地", "水地比", "地水师"],
            "愤怒": ["坎为水", "离为火", "水火既济", "火水未济"],
            "孤独": ["泽山咸", "雷风恒", "风泽中孚", "泽雷随"]
        }
    
    def generate_daily_fortune(self, user_id, date_str=None):
        """
        生成每日一签
        """
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")
        
        user_num = abs(hash(str(user_id))) % 100000
        seed = int(date_str.replace("-", "")) * 100000 + user_num
        random.seed(seed)
        
        hexagram = random.choice(self.common_hexagrams)
        symbolism = self.daily_symbolism.get(hexagram, "卦象蕴含深刻智慧")
        action_advice = self.daily_advice.get(hexagram, "保持谨慎多观察思考")
        
        random.seed(seed + 1)
        emotion_tip = random.choice(self.emotion_tips)
        random.seed(seed + 2)
        fortune_phrase = random.choice(self.fortune_phrases)
        
        def truncate(text, max_len=20):
            text = text.strip()
            return text[:max_len] if len(text) > max_len else text
        
        return {
            "date": date_str,
            "hexagram": hexagram,
            "symbolism": truncate(symbolism, 20),
            "action_advice": truncate(action_advice, 20),
            "emotion_tip": truncate(emotion_tip, 20),
            "fortune_phrase": fortune_phrase
        }
    
    def generate_event_divination(self, question_text, time_str=None, method="coins"):
        """
        生成事件起盘
        """
        if not time_str:
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        seed = abs(hash(question_text + time_str + method))
        random.seed(seed)
        
        primary_hexagram = random.choice(self.common_hexagrams)
        changing_line_num = random.randint(1, 6)
        changing_line = f"第{changing_line_num}爻"
        changed_hexagram = self.changed_hexagram_map.get(primary_hexagram, primary_hexagram)
        
        interpretation = self.hexagram_db.get(primary_hexagram, {
            "context": "此卦象提示我们保持开放的心态去探索。",
            "symbolism": f"{primary_hexagram}卦蕴含着值得体会的智慧。",
            "advice": "建议保持谨慎，多观察思考再行动。",
            "emotion": "保持平和的心态，相信自己的判断。"
        })
        
        return {
            "primary_hexagram": primary_hexagram,
            "changing_line": changing_line,
            "changed_hexagram": changed_hexagram,
            "interpretation": {
                "context": interpretation["context"],
                "symbolism": interpretation["symbolism"],
                "advice": interpretation["advice"],
                "emotion": interpretation["emotion"]
            }
        }
    
    def interpret_hexagram(self, hexagram_id, question_type="general"):
        """
        解读卦象
        """
        if isinstance(hexagram_id, int) and 1 <= hexagram_id <= 64:
            hexagram_name = self.hexagrams[hexagram_id - 1]
        else:
            hexagram_name = str(hexagram_id)
        
        data = self.hexagram_db.get(hexagram_name, {
            "context": "此卦象提示我们保持开放的心态去探索。",
            "symbolism": f"{hexagram_name}卦蕴含着值得体会的智慧。",
            "advice": "建议保持谨慎，多观察思考再行动。",
            "emotion": "保持平和的心态，相信自己的判断。"
        })
        
        type_prefix = {
            "career": "在事业方面，",
            "relationship": "在感情方面，",
            "decision": "在做决策时，",
            "emotion": "关于情绪方面，",
            "general": ""
        }
        
        prefix = type_prefix.get(question_type, "")
        
        def truncate(text, max_len=60):
            text = text.strip()
            if len(text) <= max_len:
                return text
            for i in range(min(max_len, len(text)-1), 20, -1):
                if text[i] in "。！？；,.!?; ":
                    return text[:i+1].strip()
            return text[:max_len].strip()
        
        return {
            "context_understanding": truncate(prefix + data["context"], 60),
            "hexagram_symbolism": truncate(data["symbolism"], 60),
            "practical_advice": truncate(data["advice"], 60),
            "emotional_support": truncate(data["emotion"], 60)
        }
    
    def emotion_guidance(self, text_input):
        """
        情绪引导
        """
        seed = abs(hash(text_input))
        random.seed(seed)
        
        emotion_label = random.choice(self.emotion_labels)
        emotion_confidence = round(random.uniform(0.7, 0.95), 2)
        guidance_text = self.emotion_guidances.get(emotion_label, "保持平和的心态，一切都会好起来的。")
        recommended_hexagrams = self.recommended_hexagrams.get(emotion_label, ["水天需", "地山谦"])
        
        tone_styles = {
            "焦虑": "温和安抚，循序渐进",
            "迷茫": "耐心引导，循序渐进",
            "失落": "温暖鼓励，给予支持",
            "冲动": "冷静提醒，理性分析",
            "愤怒": "温和安抚，化解戾气",
            "孤独": "温暖陪伴，给予慰藉"
        }
        
        tone_style = tone_styles.get(emotion_label, "温和友好，循循善诱")
        
        return {
            "emotion_label": emotion_label,
            "emotion_confidence": emotion_confidence,
            "recommended_hexagrams": recommended_hexagrams,
            "tone_style": tone_style,
            "guidance_text": guidance_text,
            "template_used": f"{emotion_label}模板"
        }
    
    def consultation(self, question):
        """
        AI咨询（目前用规则实现，后续接入LLM）
        """
        seed = abs(hash(question))
        random.seed(seed)
        
        i = random.randint(0, len(self.common_hexagrams) - 1)
        hexagram = self.common_hexagrams[i]
        data = self.hexagram_db.get(hexagram, {})
        
        answer = f"根据易经「{hexagram}」卦的启示：\n\n{data.get('context', '')}\n\n{data.get('symbolism', '')}\n\n💡 建议：{data.get('advice', '')}\n\n{data.get('emotion', '')}"
        
        return {
            "hexagram": hexagram,
            "answer": answer
        }


# ========== 初始化系统 ==========
divination_system = DivinationSystem()


# ========== API 路由 ==========
@app.get("/")
async def root():
    return {
        "message": "🔮 易经占卜系统 API",
        "version": "2.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/daily-fortune")
async def daily_fortune(request: DailyFortuneRequest):
    try:
        result = divination_system.generate_daily_fortune(
            user_id=request.user_id,
            date_str=request.date_str
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/divination")
async def divination(request: DivinationRequest):
    try:
        result = divination_system.generate_event_divination(
            question_text=request.question_text,
            time_str=request.time_str,
            method=request.method
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/interpret-hexagram")
async def interpret_hexagram(request: InterpretHexagramRequest):
    try:
        result = divination_system.interpret_hexagram(
            hexagram_id=request.hexagram_id,
            question_type=request.question_type
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/emotion-guidance")
async def emotion_guidance(request: EmotionGuidanceRequest):
    try:
        result = divination_system.emotion_guidance(
            text_input=request.text_input
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/consultation")
async def consultation(request: ConsultationRequest):
    try:
        result = divination_system.consultation(
            question=request.question
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== 启动服务 ==========
if __name__ == "__main__":
    import uvicorn
    print("🔮 易经占卜系统 - Backend API")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
