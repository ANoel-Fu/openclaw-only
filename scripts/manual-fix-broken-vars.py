#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动修复变量名丢失的题目
基于 Java 常识推断正确的变量名
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

# 需要修复的题目和对应的修复规则
FIXES = {
    239: {
        # 依赖注入的题目，之前已经手动修复过
        'replacements': [
            ('private final UserRepository;', 'private final UserRepository userRepository;'),
            ('public UserService(UserRepository){', 'public UserService(UserRepository userRepository) {'),
            ('this. =;', 'this.userRepository = userRepository;'),
            ('private PaymentGateway;', 'private PaymentGateway paymentGateway;'),
            ('public void setGateway(PaymentGateway){', 'public void setGateway(PaymentGateway paymentGateway) {'),
            ('this. =;', 'this.paymentGateway = paymentGateway;'),
        ]
    },
    8: {
        # 值传递和引用传递
        'replacements': [
            ('int = 10;', 'int num = 10;'),
            ('changeValue();', 'changeValue(num);'),
            ('int){', 'int num) {'),
            ('= 20;', 'num = 20;'),
            ('Person = new Person(', 'Person person = new Person('),
            ('Person){', 'Person person) {'),
            ('. = "Bob";', 'person.name = "Bob";'),
        ]
    },
    68: {
        # 责任链模式
        'replacements': [
            ('protected Handler;', 'protected Handler nextHandler;'),
            ('public void setNext(Handler){', 'public void setNext(Handler nextHandler) {'),
            ('this. =;', 'this.nextHandler = nextHandler;'),
            ('public abstract boolean handle(Request);', 'public abstract boolean handle(Request request);'),
        ]
    },
    165: {
        # AQS 公平锁
        'replacements': [
            ('private final Sync;', 'private final Sync sync;'),
            ('= new Sync();', 'sync = new Sync();'),
            ('static final class Sync extends AQS{', 'static final class Sync extends AbstractQueuedSynchronizer {'),
        ]
    },
    193: {
        # 双重检查锁单例
        'replacements': [
            ('private static volatile Singleton;', 'private static volatile Singleton instance;'),
            ('if(== null){', 'if(instance == null) {'),
            ('= new Singleton();', 'instance = new Singleton();'),
            ('return;', 'return instance;'),
        ]
    },
}

def apply_fixes(answer, replacements):
    """应用替换规则"""
    result = answer
    for old, new in replacements:
        result = result.replace(old, new)
    return result

def main():
    print("开始手动修复变量名...")
    
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    fixed_count = 0
    for q in data['questions']:
        if q['id'] in FIXES:
            original = q['answer']
            replacements = FIXES[q['id']]['replacements']
            q['answer'] = apply_fixes(q['answer'], replacements)
            
            if original != q['answer']:
                fixed_count += 1
                print(f"✅ 修复 ID {q['id']}: {q['question'][:30]}...")
    
    print(f"\n共修复 {fixed_count} 道题")
    
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 保存成功！")

if __name__ == "__main__":
    main()
