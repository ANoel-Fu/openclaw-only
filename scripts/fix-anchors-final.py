#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 修复锚点链接 - 最终版本

import json
from urllib.parse import quote

# 正确的锚点映射（根据网页实际内容）
CORRECT_ANCHORS = {
    # JVM 模块
    "类加载过程是什么？": "讲一下类加载过程",
    "垃圾回收算法有哪些？": "垃圾回收算法有哪些",
    "JVM 内存区域有哪些？": "jvm 的内存模型介绍一下",
    "垃圾回收器有哪些？": "常见的垃圾收集器有哪些",
    "常见的垃圾收集器有哪些？": "常见的垃圾收集器有哪些",
    
    # Java 基础模块
    "说一下 Java 的特点": "说一下 java 的特点",
    "Java 为什么是跨平台的？": "java 为什么是跨平台的",
    "JVM、JDK、JRE 三者关系？": "jvm、jdk、jre 三者关系",
    "JVM 和 Java 有啥区别？": "jvm 和 java 有啥区别",
    "为什么 Java 解释和编译都有？": "为什么 java 解释和编译都有",
    "值传递和引用传递的区别？": "值传递和引用传递的区别",
    
    # Java 集合模块
    "HashMap 和 Hashtable 的区别？": "hashmap 和 hashtable 的区别",
    "ArrayList 和 LinkedList 的区别？": "arraylist 和 linkedlist 的区别",
    "HashMap 的底层实现原理？": "hashmap 底层实现",
    "HashMap 底层实现": "hashmap 底层实现",
    
    # Java 并发模块
    "synchronized 和 ReentrantLock 的区别？": "synchronized 和 reentrantlock 的区别",
    "volatile 关键字的作用？": "volatile 关键字的作用",
    "ConcurrentHashMap 的实现原理？": "concurrenthashmap 怎么实现的",
    "线程池的核心参数有哪些？": "线程池的参数有哪些",
    
    # Spring 模块
    "Spring IOC 是什么？": "spring ioc 和 aop 介绍一下",
    "Spring AOP 是什么？": "spring 的 aop 介绍一下",
    "Spring Bean 的生命周期？": "bean 的生命周期说一下",
}

def fix_anchor(question):
    """根据问题文本找到正确的锚点"""
    # 1. 先查映射表
    if question in CORRECT_ANCHORS:
        return CORRECT_ANCHORS[question]
    
    # 2. 去除问号等标点符号
    anchor = question.rstrip('?？')
    
    # 3. 转为小写
    anchor = anchor.lower()
    
    return anchor

def create_url(base_url, question):
    """创建正确的 URL"""
    anchor = fix_anchor(question)
    # 直接 URL 编码，保留空格（浏览器会处理）
    encoded_anchor = quote(anchor, safe='-_.!~*\'()')
    return f"{base_url}#{encoded_anchor}"

def main():
    QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-detailed.json"
    
    # 加载题库
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    # 基础 URL 映射
    base_urls = {
        "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
        "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
        "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
        "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
        "Spring": "https://www.xiaolincoding.com/interview/spring.html"
    }
    
    print("修复链接锚点（最终版本）：")
    fixed_count = 0
    
    for q in questions:
        old_url = q['url']
        category = q['category']
        question = q['question']
        
        # 生成新 URL
        new_url = create_url(base_urls[category], question)
        
        if old_url != new_url:
            old_anchor = old_url.split('#')[-1]
            new_anchor = new_url.split('#')[-1]
            
            # 只打印重要的修改
            if '类加载' in question or '垃圾回收' in question or 'Spring' in question:
                print(f"✓ {q['id']}. {question[:40]}...")
                print(f"  旧：#{old_anchor[:60]}...")
                print(f"  新：#{new_anchor[:60]}...")
            fixed_count += 1
        
        q['url'] = new_url
    
    # 保存修复后的题库
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 共修复 {fixed_count} 道题目的链接锚点")
    
    # 显示修复后的示例
    print("\n📋 修复后的链接示例（点击可测试）：")
    test_questions = [q for q in questions if '类加载' in q['question'] or '垃圾回收' in q['question']][:3]
    for i, q in enumerate(test_questions, 1):
        print(f"  {i}. {q['question']}")
        print(f"     {q['url']}")

if __name__ == "__main__":
    main()
