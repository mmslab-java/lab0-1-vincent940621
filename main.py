import os
import requests
import google.generativeai as genai

# 1. 設定 AI (嘗試使用最穩定的模型名稱)
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    # 這裡改用 'gemini-pro'，這是目前最不容易報 404 的名稱
    model = genai.GenerativeModel('gemini-pro')
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
        
        # 2. 叫 AI 解題
        prompt = f"請幫我用 Python 解這道 LeetCode 題目：{title}\n題目內容：{content}\n請只輸出程式碼，不要有任何解釋文字。"
        response = model.generate_content(prompt)
        answer = response.text.strip().replace('```python', '').replace('```', '')

        print(f"今日題目：{title}，AI 成功生成解法！")
        
        # 3. 存檔
        with open("solution.py", "w", encoding="utf-8") as f:
            f.write(answer)
            
    except Exception as e:
        print(f"執行過程中發生錯誤: {e}")
        raise e # 讓 GitHub Actions 知道失敗了

if __name__ == "__main__":
    solve_leetcode()
