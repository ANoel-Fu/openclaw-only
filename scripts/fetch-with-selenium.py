#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用 Selenium + Chrome 抓取小林 coding 题库
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time

URLS = {
    "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
    "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
    "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
    "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
    "Spring": "https://www.xiaolincoding.com/interview/spring.html",
}

def setup_driver():
    """配置 Chrome 驱动"""
    options = Options()
    options.add_argument('--headless')  # 无头模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    service = Service('/usr/bin/google-chrome')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def fetch_questions(driver, url, category):
    """抓取单个页面的题目"""
    print(f"  正在抓取：{category}")
    
    driver.get(url)
    
    # 等待页面加载
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # 等待更多内容加载
    time.sleep(5)
    
    questions = []
    
    # 查找所有问题（h3 标签）
    headers = driver.find_elements(By.TAG_NAME, 'h3')
    
    for header in headers:
        try:
            question_text = header.text.strip()
            
            # 跳过不包含问号的
            if '?' not in question_text or len(question_text) < 5:
                continue
            
            # 获取答案（查找后面的兄弟元素）
            answer_parts = []
            next_elem = header.find_element(By.XPATH, "following-sibling::*[1]")
            
            count = 0
            while next_elem and count < 20:
                tag_name = next_elem.tag_name
                if tag_name in ['h1', 'h2', 'h3', 'h4']:
                    break
                
                text = next_elem.text.strip()
                if text and len(text) > 20:
                    answer_parts.append(text)
                
                try:
                    next_elem = next_elem.find_element(By.XPATH, "following-sibling::*[1]")
                except:
                    break
                
                count += 1
            
            answer = '\n\n'.join(answer_parts)
            
            if answer and len(answer) > 100:
                questions.append({
                    "category": category,
                    "question": question_text,
                    "answer": answer[:5000],
                    "url": url
                })
        except Exception as e:
            continue
    
    print(f"    抓取到 {len(questions)} 道题目")
    return questions

def main():
    print("=" * 60)
    print("小林 coding 题库抓取器 - Selenium 版")
    print("=" * 60)
    
    driver = setup_driver()
    all_questions = []
    
    try:
        for category, url in URLS.items():
            questions = fetch_questions(driver, url, category)
            all_questions.extend(questions)
    finally:
        driver.quit()
    
    print("\n" + "=" * 60)
    print(f"总共抓取到 {len(all_questions)} 道题目")
    print("=" * 60)
    
    # 保存
    output = {
        "questions": all_questions,
        "lastUpdated": "2026-03-12",
        "modules": list(URLS.keys()),
        "totalQuestions": len(all_questions),
        "source": "小林 coding 面试题汇总",
        "status": "completed"
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-selenium.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 已保存到：/root/.openclaw/workspace/memory/java-interview-questions-selenium.json")

if __name__ == "__main__":
    main()
