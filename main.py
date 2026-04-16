import os
import requests
import google.generativeai as genai

# 1. 設定 AI (使用你的 Gemini Key)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def solve_leetcode():
    # 這裡我們使用 LeetCode 的 GraphQL API 抓取每日一題
    url = "https://leetcode.com/graphql"
    query = {
        "query": "query questionOfToday { activeDailyCodingChallengeQuestion { question { questionId title titleSlug content difficulty } } }"
    }
    
    # 抓取題目
    response = requests.post(url, json=query).json()
    question = response['data']['activeDailyCodingChallengeQuestion']['question']
    title = question['title']
    content = question['content']
    slug = question['titleSlug']

    # 2. 叫 Gemini 解題
    prompt = f"請幫我解這道 LeetCode 題目：{title}\n內容如下：{content}\n請只輸出 Python 程式碼，不要有任何解釋文字。"
    answer = model.generate_content(prompt).text.strip().replace('```python', '').replace('```', '')

    print(f"今日題目：{title}，AI 已生成解法。")
    
    # 3. 提交 (這裡需要處理 Cookie 與 CSRF 邏輯，腳本會模擬瀏覽器行為)
    # 為了簡化，初學者可以先用這個腳本生成解法，再進階實作自動 Submit 邏輯
    # 或者搜尋 "leetcode-api-python" 這個 library 來簡化提交動作
    with open("solution.py", "w") as f:
        f.write(answer)

if __name__ == "__main__":
    solve_leetcode()
