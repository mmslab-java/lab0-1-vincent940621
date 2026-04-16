import os
import requests
import google.generativeai as genai

# 強制使用正確的模型路徑
MODEL_NAME = 'gemini-1.5-flash-latest' 

try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(MODEL_NAME)
    print(f"--- 診斷訊息：目前正在使用的模型是 {MODEL_NAME} ---")
except Exception as e:
    print(f"初始化失敗: {e}")

def solve_leetcode():
    url = "https://leetcode.com/graphql"
    query = {"query": "query questionOfToday { activeDailyCodingChallengeQuestion { question { title content } } }"}
    
    try:
        response = requests.post(url, json=query).json()
        q = response['data']['activeDailyCodingChallengeQuestion']['question']
        print(f"正在挑戰題目：{q['title']}")
        
        # 叫 AI 解題
        prompt = f"Solve LeetCode: {q['title']}\n{q['content']}\nOnly output Python code."
        res = model.generate_content(prompt)
        
        # 儲存結果
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(res.text.strip().replace('```python', '').replace('```', ''))
        print("✅ 成功生成 solution.py！")
            
    except Exception as e:
        print(f"❌ 執行過程中報錯: {e}")
        raise e

if __name__ == "__main__":
    solve_leetcode()
