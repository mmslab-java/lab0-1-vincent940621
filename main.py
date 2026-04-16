import os
import requests
import google.generativeai as genai

# 1. 設定 AI
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # 使用 gemini-pro 是最穩定的
    model = genai.GenerativeModel('gemini-pro')
    print("AI 模型載入成功")
except Exception as e:
    print(f"AI 設定失敗: {e}")

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
        
        print(f"正在解題：{title}...")
        
        # 2. 叫 AI 解題
        prompt = f"請幫我用 Python 解這道 LeetCode 題目：{title}\n內容：{content}\n請只輸出程式碼，不要廢話。"
        response = model.generate_content(prompt)
        
        # 處理 AI 回傳的文字，去掉 Markdown 標籤
        answer = response.text.strip().replace('```python', '').replace('```', '')

        # 3. 儲存成檔案
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(answer)
        print("解法已儲存至 solution.py")
            
    except Exception as e:
        print(f"執行出錯: {e}")
        raise e

if __name__ == "__main__":
    solve_leetcode()
