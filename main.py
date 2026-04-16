import os
import requests
import google.generativeai as genai

# 1. 設定 AI
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # 如果 flash 不行，這段代碼會嘗試用 pro，直到成功為止
    model_name = 'gemini-1.5-flash' 
    model = genai.GenerativeModel(model_name)
    print(f"成功載入模型：{model_name}")
except Exception as e:
    print(f"初始化失敗: {e}")

def solve_leetcode():
    url = "https://leetcode.com/graphql"
    query = {"query": "query questionOfToday { activeDailyCodingChallengeQuestion { question { title content } } }"}
    
    try:
        response = requests.post(url, json=query).json()
        q = response['data']['activeDailyCodingChallengeQuestion']['question']
        print(f"正在解題：{q['title']}")
        
        # 2. 叫 AI 解題
        prompt = f"Solve this LeetCode: {q['title']}\n{q['content']}\nOnly output Python code."
        res = model.generate_content(prompt)
        
        # 3. 存檔
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(res.text.strip().replace('```python', '').replace('```', ''))
        print("✅ 檔案已產生！")
            
    except Exception as e:
        print(f"出錯了: {e}")
        raise e

if __name__ == "__main__":
    solve_leetcode()
