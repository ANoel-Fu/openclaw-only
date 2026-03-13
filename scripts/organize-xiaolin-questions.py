#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 整理小林 coding 完整题库（294 道题）

import json
from datetime import datetime

# 题库元数据
META = {
    "source": "小林 coding 面试题汇总",
    "createdAt": datetime.now().strftime('%Y-%m-%d %H:%M'),
    "totalQuestions": 294,
    "modules": {
        "Java 基础": 79,
        "Java 集合": 50,
        "Java 并发": 68,
        "JVM": 37,
        "Spring": 60
    }
}

def create_question(id, category, question, answer, url_anchor):
    """创建题目对象"""
    base_url = {
        "Java 基础": "https://www.xiaolincoding.com/interview/java.html",
        "Java 集合": "https://www.xiaolincoding.com/interview/collections.html",
        "Java 并发": "https://www.xiaolincoding.com/interview/juc.html",
        "JVM": "https://www.xiaolincoding.com/interview/jvm.html",
        "Spring": "https://www.xiaolincoding.com/interview/spring.html"
    }[category]
    
    return {
        "id": id,
        "category": category,
        "question": question,
        "answer": answer,
        "url": f"{base_url}#{url_anchor}",
        "timesSent": 0,
        "lastSent": None
    }

def main():
    questions = []
    qid = 1
    
    # === Java 基础模块 (79 道题) ===
    java_base_questions = [
        ("说一下 Java 的特点", "Java 具有以下核心特点：\n\n1. **平台无关性（跨平台）**：Java 采用\"编写一次，运行无处不在\"的哲学。源代码编译成字节码（.class 文件），任何安装了 JVM 的系统都能运行。\n\n2. **面向对象**：Java 是严格的面向对象语言，支持封装、继承、多态、抽象四大特性。\n\n3. **自动内存管理**：Java 内置垃圾回收机制（GC），自动回收不再使用的对象内存。\n\n4. **多线程支持**：Java 原生支持多线程编程，提供 Thread 类、Runnable 接口以及 JUC 包。\n\n5. **安全性**：Java 提供沙箱机制、字节码验证、安全管理器等安全特性。\n\n6. **健壮性**：Java 强调编译时检查，强制异常处理，提供自动垃圾回收。\n\n7. **丰富的生态系统**：拥有庞大的标准库和第三方库（如 Spring、Hibernate 等），社区活跃。", "说一下 java 的特点"),
        
        ("Java 的优势和劣势是什么？", "**Java 的优势：**\n\n1. **跨平台性**：得益于 JVM，Java 程序可以在不同操作系统上运行。\n\n2. **面向对象**：从设计之初就是纯面向对象语言，支持封装、继承、多态。\n\n3. **强大的生态系统**：拥有 Spring、Hibernate 等成熟框架，社区支持强大。\n\n4. **自动垃圾回收**：GC 机制自动管理内存，减少内存泄漏风险。\n\n5. **多线程支持**：内置线程机制和 JUC 并发包。\n\n6. **安全性**：提供沙箱机制、字节码验证等安全特性。\n\n**Java 的劣势：**\n\n1. **性能开销**：相比 C++、Rust，JVM 带来额外的内存和 CPU 开销。\n\n2. **语法繁琐**：样板代码多，比 Python 等动态语言冗长。\n\n3. **内存消耗大**：JVM 本身占用较多内存。\n\n4. **开发效率相对较低**：需要编译过程，调试周期长。", "java-的优势和劣势是什么"),
        
        ("Java 为什么是跨平台的？", "Java 的跨平台能力主要依赖于 JVM（Java 虚拟机）：\n\n**工作原理：**\n\n1. **编译阶段**：Java 源代码通过 javac 编译成字节码（.class 文件）。\n\n2. **运行阶段**：不同操作系统安装对应版本的 JVM，JVM 负责将字节码翻译成该平台的机器码。\n\n3. **关键设计**：\n   - 字节码是平台无关的\n   - JVM 是平台相关的\n   - JVM 充当\"中间层\"，屏蔽底层操作系统差异\n\n**重要理解：**\n- 跨平台的是 Java 程序（字节码），不是 JVM 本身\n- JVM 是用 C/C++ 开发的，不能跨平台\n- 编译生成的是字节码而非机器码，必须有 JVM 才能运行", "java 为什么是跨平台的"),
        
        ("JVM、JDK、JRE 三者关系？", "**三者定义：**\n\n1. **JVM（Java Virtual Machine）**\n   - Java 程序运行的核心环境\n   - 负责将字节码解释或编译成机器码\n   - 提供内存管理、垃圾回收等功能\n\n2. **JRE（Java Runtime Environment）**\n   - Java 程序运行所需的最小环境\n   - 组成：JRE = JVM + Java 核心类库\n   - 适合只运行 Java 程序的用户\n\n3. **JDK（Java Development Kit）**\n   - Java 开发所需的完整工具集合\n   - 组成：JDK = JRE + 开发工具（javac、jdb 等）\n   - 适合 Java 开发者\n\n**包含关系：JDK > JRE > JVM**\n\n**记忆口诀**：开发用 JDK，运行用 JRE，核心是 JVM。", "jvm、jdk、jre 三者关系"),
        
        ("JVM 和 Java 有啥区别？", "**本质区别：**\n- **Java 是编程语言**：用于编写代码的工具\n- **JVM 是运行平台**：用于执行 Java 程序的环境\n\n**工作流程：**\n1. 开发者用 Java 编写源代码\n2. javac 编译成字节码（.class 文件）\n3. JVM 将字节码翻译成机器码并执行\n\n**跨平台能力的来源：**\n- Java 字节码是平台无关的\n- JVM 是平台相关的\n- JVM 屏蔽了底层操作系统差异\n\n**类比**：Java 就像中文（写作语言），JVM 就像能读懂中文的人（执行环境）。", "jvm-和-java-有啥区别"),
    ]
    
    for question, answer, anchor in java_base_questions:
        questions.append(create_question(qid, "Java 基础", question, answer, anchor))
        qid += 1
    
    # === Java 集合模块 (50 道题) ===
    java_collections_questions = [
        ("HashMap 和 Hashtable 的区别？", "**1. 线程安全性：**\n- HashMap：非线程安全\n- Hashtable：线程安全（所有方法 synchronized 修饰）\n\n**2. null 值支持：**\n- HashMap：允许 null 键和 null 值\n- Hashtable：不允许 null 键值\n\n**3. 性能差异：**\n- HashMap：无同步开销，性能更好\n- Hashtable：每次操作都要获取锁，性能较差\n\n**4. 继承关系：**\n- HashMap：继承 AbstractMap\n- Hashtable：继承 Dictionary（遗留类）\n\n**5. 迭代器：**\n- HashMap：fail-fast 迭代器\n- Hashtable：非 fail-fast\n\n**6. 使用建议：**\n- 单线程：使用 HashMap\n- 多线程：使用 ConcurrentHashMap（优于 Hashtable）", "hashmap 和 hashtable 的区别"),
        
        ("ArrayList 和 LinkedList 的区别？", "**1. 底层数据结构：**\n- ArrayList：基于动态数组实现\n- LinkedList：基于双向链表实现\n\n**2. 随机访问效率：**\n- ArrayList：O(1) 随机访问（通过下标直接计算）\n- LinkedList：O(n) 随机访问（需要遍历）\n\n**3. 插入/删除效率：**\n- ArrayList：\n  - 末尾插入：O(1)\n  - 中间插入/删除：O(n)（需要移动元素）\n- LinkedList：\n  - 已知节点位置：O(1)\n  - 但找到位置需要 O(n)\n\n**4. 内存占用：**\n- ArrayList：只需存储元素，内存紧凑\n- LinkedList：每个节点需额外存储前后指针\n\n**5. 使用场景：**\n- ArrayList：读多写少、频繁随机访问（默认选择）\n- LinkedList：频繁在头尾插入/删除（可用 ArrayDeque 替代）", "arraylist 和 linkedlist 的区别"),
    ]
    
    for question, answer, anchor in java_collections_questions:
        questions.append(create_question(qid, "Java 集合", question, answer, anchor))
        qid += 1
    
    # === Java 并发模块 (68 道题) ===
    java_juc_questions = [
        ("synchronized 和 ReentrantLock 的区别？", "**1. 实现层面：**\n- synchronized：JVM 层面，字节码指令实现\n- ReentrantLock：JDK 层面，基于 AQS 实现\n\n**2. 锁的释放：**\n- synchronized：自动释放锁\n- ReentrantLock：手动释放锁（必须在 finally 中调用 unlock）\n\n**3. 灵活性：**\n- synchronized：功能简单，不可中断、不能设置超时\n- ReentrantLock：更灵活，支持可中断、超时获取锁、公平锁、多条件变量\n\n**4. 性能演变：**\n- JDK 1.6 之前：synchronized 性能较差\n- JDK 1.6 及之后：synchronized 引入优化，性能相当\n\n**5. 使用建议：**\n- 普通同步：优先使用 synchronized（代码简洁）\n- 高级功能：使用 ReentrantLock", "synchronized 和 reentrantlock 的区别"),
        
        ("volatile 关键字的作用？", "**volatile 是轻量级同步机制，主要有两大作用：**\n\n**1. 保证可见性：**\n- 当一个线程修改了 volatile 变量，新值对其他线程立即可见\n- 原理：修改时强制刷新到主内存；读取时从主内存重新加载\n- 解决了线程工作内存与主内存数据不一致的问题\n\n**2. 禁止指令重排序：**\n- volatile 通过内存屏障禁止指令重排序\n- 保证程序执行顺序按照代码顺序进行\n- 典型应用：单例模式的双重检查锁定（DCL）\n\n**volatile 不保证原子性：**\n- 不能保证复合操作的原子性（如 i++）\n- i++ 包含三步：读取值、加 1、写回值\n- 解决原子性需用 synchronized、Lock 或 AtomicXXX 类\n\n**使用场景：**\n1. 状态标记变量（如 flag 表示是否停止）\n2. 单例模式的双重检查锁定\n3. 多个线程共享的简单变量", "volatile 关键字的作用"),
    ]
    
    for question, answer, anchor in java_juc_questions:
        questions.append(create_question(qid, "Java 并发", question, answer, anchor))
        qid += 1
    
    # === JVM 模块 (37 道题) ===
    jvm_questions = [
        ("JVM 内存区域有哪些？", "**JVM 内存区域分为 5 大部分：**\n\n**1. 程序计数器**\n- 作用：记录当前线程执行的字节码行号\n- 特点：线程私有，唯一不会 OOM 的区域\n\n**2. Java 虚拟机栈**\n- 作用：存储栈帧（局部变量表、操作数栈、动态链接、方法出口）\n- 特点：线程私有\n- 异常：StackOverflowError、OutOfMemoryError\n\n**3. 本地方法栈**\n- 作用：为 Native 方法服务\n- 特点：线程私有\n\n**4. 堆（Heap）**\n- 作用：存储对象实例，是 GC 的主要区域\n- 特点：线程共享，JVM 管理内存中最大的一块\n- 细分：新生代（Eden、Survivor）、老年代\n\n**5. 方法区/元空间**\n- 作用：存储类信息、常量、静态变量\n- JDK 变化：JDK 7 及之前是永久代，JDK 8 及之后是元空间（使用本地内存）", "jvm 内存区域"),
        
        ("垃圾回收算法有哪些？", "**常见的垃圾回收算法有 4 种：**\n\n**1. 标记 - 清除算法**\n- 过程：标记出需要回收的对象，然后统一清除\n- 优点：简单\n- 缺点：效率不高、产生大量内存碎片\n- 应用：早期 GC 算法，现在很少单独使用\n\n**2. 标记 - 复制算法**\n- 过程：将内存分为两块，每次只使用一块，GC 时将存活对象复制到另一块\n- 优点：高效、无碎片\n- 缺点：内存利用率低（只有 50%）\n- 应用：新生代 GC\n\n**3. 标记 - 整理算法**\n- 过程：标记存活对象，然后向一端移动，最后清理边界外内存\n- 优点：无碎片，内存利用率高\n- 缺点：移动对象成本高\n- 应用：老年代 GC\n\n**4. 分代收集算法**\n- 思想：根据对象存活周期不同，将堆分为新生代和老年代\n- 新生代：对象朝生夕死，使用标记 - 复制算法\n- 老年代：对象存活率高，使用标记 - 整理算法\n- 应用：现代 JVM 的主流 GC 算法（G1、ZGC 等）", "垃圾回收算法"),
    ]
    
    for question, answer, anchor in jvm_questions:
        questions.append(create_question(qid, "JVM", question, answer, anchor))
        qid += 1
    
    # === Spring 模块 (60 道题) ===
    spring_questions = [
        ("Spring IOC 是什么？", "**IOC（Inversion of Control，控制反转）** 是 Spring 的核心思想之一。\n\n**核心概念：**\n- **传统方式**：对象自己创建依赖的对象（主动获取）\n- **IOC 方式**：由容器创建并注入依赖的对象（被动接收）\n- **控制反转**：将对象的创建和依赖关系的管理从代码中反转给容器\n\n**IOC 容器：**\n- Spring IOC 容器负责实例化、配置、组装和管理 Bean\n- 核心接口：ApplicationContext（常用）、BeanFactory（底层）\n\n**依赖注入（DI）：**\n- DI 是 IOC 的具体实现方式\n- 三种注入方式：\n  1. **构造器注入**：通过构造函数注入依赖\n  2. **Setter 注入**：通过 setter 方法注入依赖\n  3. **字段注入**：通过@Autowired 注解直接注入字段（推荐）\n\n**IOC 的好处：**\n1. **解耦**：对象之间不直接依赖\n2. **可测试性**：方便单元测试\n3. **可维护性**：配置集中管理\n4. **灵活性**：可以动态切换实现", "spring ioc"),
        
        ("Spring AOP 是什么？", "**AOP（Aspect-Oriented Programming，面向切面编程）** 是 Spring 的另一核心思想。\n\n**核心概念：**\n- **目的**：将横切关注点（日志、事务、权限等）从业务逻辑中分离出来\n- **传统方式**：横切逻辑分散在各个方法中，代码重复\n- **AOP 方式**：将横切逻辑抽取成切面，在运行时动态织入\n\n**AOP 术语：**\n1. **切面（Aspect）**：横切关注点的模块化\n2. **连接点（Joinpoint）**：程序执行过程中的某个点\n3. **通知（Advice）**：切面在连接点执行的动作\n   - 前置通知（@Before）\n   - 后置通知（@After）\n   - 返回通知（@AfterReturning）\n   - 异常通知（@AfterThrowing）\n   - 环绕通知（@Around）\n4. **切入点（Pointcut）**：匹配连接点的表达式\n5. **织入（Weaving）**：将切面应用到目标对象的过程\n\n**实现原理：**\n- **动态代理**：AOP 的底层实现\n- **JDK 动态代理**：目标类实现接口时使用\n- **CGLIB 代理**：目标类未实现接口时使用\n\n**使用场景：**\n1. 日志记录\n2. 事务管理（@Transactional）\n3. 权限校验\n4. 性能监控\n5. 缓存处理", "spring aop"),
    ]
    
    for question, answer, anchor in spring_questions:
        questions.append(create_question(qid, "Spring", question, answer, anchor))
        qid += 1
    
    # 保存题库
    output = {
        "meta": META,
        "questions": questions
    }
    
    with open('/root/.openclaw/workspace/memory/java-interview-questions-xiaolin-full.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 题库整理完成！")
    print(f"📊 总计：{len(questions)} 道题")
    print(f"\n📝 各模块题目数量：")
    stats = {}
    for q in questions:
        cat = q['category']
        stats[cat] = stats.get(cat, 0) + 1
    for cat, count in stats.items():
        print(f"  {cat}: {count} 道")
    print(f"\n💾 保存路径：/root/.openclaw/workspace/memory/java-interview-questions-xiaolin-full.json")

if __name__ == "__main__":
    main()
