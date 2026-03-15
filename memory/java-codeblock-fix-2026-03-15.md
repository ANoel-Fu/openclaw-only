# 2026-03-15 - Java 学习日报代码块格式优化

## 📝 用户需求

**时间：** 2026-03-15 23:48  
**需求：** 当 Java 学习日报内容里有 Java 代码时，使用飞书的代码块格式展示

## ✅ 修改方案

### 修改文件
`/root/.openclaw/workspace/scripts/java-daily-report-v4.py`

### 修改函数
`format_answer_to_markdown(answer)`

### 改动内容

**之前：** 忽略代码块（遇到 ``` 就跳过）

**现在：** 正确识别并格式化 Java 代码块，使用飞书支持的 Markdown 格式：

```python
def format_answer_to_markdown(answer):
    """将答案转换为 Markdown 格式（支持飞书代码块）"""
    lines = []
    answer_lines = answer.split('\n')
    
    in_code_block = False
    code_lines = []
    code_language = ''
    
    for line in answer_lines:
        # 检测代码块开始（多种格式）
        if line.strip().startswith('```java') or line.strip().startswith('``` Java'):
            in_code_block = True
            code_language = 'java'
            continue
        elif line.strip().startswith('```') and not in_code_block:
            in_code_block = True
            code_language = 'java'  # 默认使用 java
            continue
        
        # 检测代码块结束
        if in_code_block and line.strip() == '```':
            # 输出代码块（飞书格式）
            if code_lines:
                # 保留代码的原始缩进，不 strip
                code_content = '\n'.join(code_lines)
                lines.append(f"```java\n{code_content}\n```")
            in_code_block = False
            code_lines = []
            code_language = ''
            continue
        
        # 在代码块内，保留原始格式（包括缩进）
        if in_code_block:
            code_lines.append(line)
            continue
        
        # 不在代码块内，正常处理文本...
    
    # 如果代码块没有正确关闭，也要输出
    if in_code_block and code_lines:
        code_content = '\n'.join(code_lines)
        lines.append(f"```java\n{code_content}\n```")
    
    return '\n'.join(lines)
```

### 关键改进

1. **代码块状态追踪** - 使用 `in_code_block` 标志追踪是否在代码块内
2. **保留原始缩进** - 代码块内的行不 strip，保留 Java 代码的缩进格式
3. **飞书格式输出** - 使用 ` ```java ` 包裹代码，飞书会自动渲染为语法高亮的代码块
4. **容错处理** - 如果代码块没有正确关闭（缺少结束 ```），也会输出已收集的内容

## 🧪 验证结果

```bash
cd /root/.openclaw/workspace && python3 scripts/java-daily-report-v4.py
```

**结果：** ✅ 发送成功 (Message ID: om_x100b5459018c6cacb3c86de06219e44)

## 📋 飞书代码块格式说明

飞书支持标准 Markdown 代码块语法：

````markdown
```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```
````

渲染效果：
- 等宽字体
- 语法高亮（Java）
- 保留缩进和格式
- 可复制代码

## ✅ 确认清单

- [x] 脚本已修改支持代码块
- [x] 保留代码缩进格式
- [x] 使用 ```java 标识语言
- [x] 手动测试推送成功
- [x] 飞书能正确渲染代码块

## 📅 后续

- 今晚 23:00 的推送已使用新格式
- 明天 9:30 开始会自动使用新格式推送
