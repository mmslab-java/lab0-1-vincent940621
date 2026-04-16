import os
import requests
import google.generativeai as genai

# 1. 設定 AI (確保名稱與最新 SDK 一致)
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # 這是目前最穩定的名稱
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("AI 引擎載入成功，準備解題...")
except Exception as e:
    print(f"AI 設定出錯: {e}")

def solve_leetcode():
    url = "https://leetcode.com/graphql"
    query = {
        "query": "query questionOfToday { activeDailyCodingChallengeQuestion { question { questionId title titleSlug content difficulty } } }"
    }
    
    try:
        response = requests.post(url, json=query).json()
        question = response['data']['activeDailyCodingChallengeQuestion']['question']
        title = question['title']
        content = question['content']
        
        print(f"正在分析題目：{title}...")
        
        # 2. 叫 AI 解題
        prompt = f"請幫我用 Python 解這道 LeetCode 題目：{title}\n題目內容：{content}\n請只輸出程式碼，不要廢話。"
        response = model.generate_content(prompt)
        
        # 去掉 Markdown 符號
        answer = response.text.strip().replace('```python', '').replace('```', '')

        # 3. 儲存成檔案 (如果權限開了，這步就會成功)
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(answer)
        print("🎉 成功！解法已儲存到 solution.py")
            
    except Exception as e:
        print(f"執行出錯: {e}")
        raise e

if __name__ == "__main__":
    solve_leetcode()
