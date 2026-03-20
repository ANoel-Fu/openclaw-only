#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复题库中代码块的格式
"""

import json
import re

QUESTIONS_FILE = "/root/.openclaw/workspace/memory/java-interview-questions-complete.json"

# 需要修复的题目 ID 和对应的正确代码
FIXES = {
    239: {
        # 修复依赖注入的代码块
        'code_blocks': [
            # 构造器注入
            '''```java
@Service
public class UserService {
    private final UserRepository userRepository;
    
    // 构造器注入（Spring 4.3+ 自动识别单构造器，无需显式@Autowired）
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```''',
            # Setter 注入
            '''```java
public class PaymentService {
    private PaymentGateway paymentGateway;
    
    @Autowired
    public void setGateway(PaymentGateway paymentGateway) {
        this.paymentGateway = paymentGateway;
    }
}
```''',
            # 字段注入
            '''```java
@Service
public class OrderService {
    @Autowired
    private OrderRepository orderRepository;
}
```'''
        ]
    }
}

def fix_question_239(answer):
    """专门修复题目 239 的代码块"""
    lines = answer.split('\n')
    new_lines = []
    code_block_index = 0
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测代码块开始
        if line.strip() == '```':
            # 下一行是代码内容
            if i + 1 < len(lines):
                code_line = lines[i + 1]
                
                # 根据代码内容选择正确的格式
                if 'UserService' in code_line:
                    new_lines.append(FIXES[239]['code_blocks'][0])
                elif 'PaymentService' in code_line:
                    new_lines.append(FIXES[239]['code_blocks'][1])
                elif 'OrderService' in code_line:
                    new_lines.append(FIXES[239]['code_blocks'][2])
                else:
                    # 保持原样
                    new_lines.append(f'```java\n{code_line}\n```')
                
                # 跳过代码块结束标记
                i += 2
                if i < len(lines) and lines[i].strip() == '```':
                    i += 1
                continue
        
        new_lines.append(line)
        i += 1
    
    return '\n'.join(new_lines)

def main():
    print("正在加载题库...")
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    questions = data['questions']
    
    # 修复题目 239
    for q in questions:
        if q['id'] == 239:
            print(f"修复题目 {q['id']}: {q['question']}")
            q['answer'] = fix_question_239(q['answer'])
            break
    
    # 保存
    print("正在保存...")
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ 修复完成！")

if __name__ == "__main__":
    main()
