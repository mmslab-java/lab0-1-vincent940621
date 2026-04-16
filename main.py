import os
import requests
import google.generativeai as genai

# 1. 設定 AI 並自動偵測可用模型
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    
    # 列出所有可用的模型，看看你的 API Key 權限
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    print(f"--- 診斷訊息：你的 API Key 可以使用的模型有 {available_models} ---")
    
    # 優先選 flash，沒 flash 就選第一個能用的
    target_model = next((m for m in available_models if 'gemini-1.5-flash' in m), available_models[0])
    model = genai.GenerativeModel(target_model)
    print(f"--- 最終選擇模型：{target_model} ---")
    
except Exception as e:
    print(f"初始化診斷失敗: {e}")
    # 如果連 list_models 都失敗，代表 API Key 可能有問題
    raise e

def solve_leetcode():
    url = "https://leetcode.com/graphql"
    query = {"query": "query questionOfToday { activeDailyCodingChallengeQuestion { question { title content } } }"}
    
    try:
        response = requests.post(url, json=query).json()
        q = response['data']['activeDailyCodingChallengeQuestion']['question']
        print(f"正在分析題目：{q['title']}")
        
        # 2. 叫 AI 解題
        prompt = f"Solve LeetCode: {q['title']}\n{q['content']}\nOnly output Python code."
        res = model.generate_content(prompt)
        
        # 3. 儲存結果
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(res.text.strip().replace('```python', '').replace('```', ''))
        print("✅ 成功！解法已產出到 solution.py")
            
    except Exception as e:
        print(f"執行過程中報錯: {e}")
        raise e

if __name__ == "__main__":
    solve_leetcode()
