#!/bin/bash
# Java 学习日报 - 每日推送 5 道 Java 面试题
# 每天早上 9:30 和晚上 23:00 推送

set -e

DATE=$(date '+%Y-%m-%d')
TIME=$(date '+%H:%M')
LOG_FILE="/root/.openclaw/workspace/logs/java-daily-report.log"
TARGET_USER="ou_a7d902ae2ba72919f55a1e8180357c55"

# 确保日志目录存在
mkdir -p /root/.openclaw/workspace/logs

echo "[$DATE $TIME] 开始生成 Java 学习日报..." >> "$LOG_FILE"

# Java 面试题库（分类 + 题目 + 答案要点）
declare -a QUESTIONS=(
    "Java 基础|HashMap 和 Hashtable 的区别？|HashMap 是非线程安全的，允许 null 键和 null 值；Hashtable 是线程安全的，不允许 null。HashMap 性能更好，Hashtable 是遗留类。|https://www.xiaolincoding.com/interview/java.html"
    "Java 基础|== 和 equals() 的区别？|== 比较基本类型值或引用地址；equals() 比较对象内容。String 重写了 equals() 来比较字符串内容。|https://www.xiaolincoding.com/interview/java.html"
    "Java 基础|final、finally、finalize 的区别？|final 修饰符表示不可变；finally 是异常处理的代码块；finalize() 是 Object 的方法，GC 前调用。|https://www.xiaolincoding.com/interview/java.html"
    "Java 集合|ArrayList 和 LinkedList 的区别？|ArrayList 基于数组，随机访问快 O(1)，插入删除慢；LinkedList 基于双向链表，插入删除快 O(1)，随机访问慢 O(n)。|https://www.xiaolincoding.com/interview/collections.html"
    "Java 集合|HashMap 的底层实现原理？|JDK1.8 之前：数组 + 链表；JDK1.8 之后：数组 + 链表 + 红黑树。链表长度>8 转红黑树，<6 转回链表。|https://www.xiaolincoding.com/interview/collections.html"
    "Java 并发|volatile 关键字的作用？|保证可见性（一个线程修改立即可见）和有序性（禁止指令重排），不保证原子性。|https://www.xiaolincoding.com/interview/juc.html"
    "Java 并发|synchronized 和 ReentrantLock 的区别？|synchronized 是关键字，自动加解锁；ReentrantLock 是类，需要手动 lock()/unlock()。ReentrantLock 功能更丰富（可中断、公平锁、多条件）。|https://www.xiaolincoding.com/interview/juc.html"
    "Java 并发|线程池的核心参数有哪些？|corePoolSize、maximumPoolSize、keepAliveTime、unit、workQueue、threadFactory、handler（拒绝策略）。|https://www.xiaolincoding.com/interview/juc.html"
    "JVM|JVM 内存区域划分？|堆（Heap）、栈（Stack）、方法区（Method Area）、程序计数器、本地方法栈。JDK1.8 后方法区改为元空间。|https://www.xiaolincoding.com/interview/jvm.html"
    "JVM|垃圾回收算法有哪些？|标记 - 清除、标记 - 复制、标记 - 整理、分代收集。新生代用复制算法，老年代用标记 - 整理。|https://www.xiaolincoding.com/interview/jvm.html"
    "Spring|Spring Bean 的生命周期？|实例化→属性赋值→初始化（Aware 接口→BeanPostProcessor 前置→init-method→BeanPostProcessor 后置）→使用→销毁。|https://www.xiaolincoding.com/interview/spring.html"
    "Spring|@Autowired 和@Resource 的区别？|@Autowired 按类型注入（Spring 提供）；@Resource 按名称注入（JSR-250 标准）。@Resource 更精确。|https://www.xiaolincoding.com/interview/spring.html"
    "MySQL|事务的 ACID 特性？|原子性（Atomicity）、一致性（Consistency）、隔离性（Isolation）、持久性（Durability）。|https://www.xiaolincoding.com/interview/mysql.html"
    "MySQL|索引的底层数据结构？|B+ 树。叶子节点存储数据，非叶子节点只存索引，支持范围查询，查询效率稳定。|https://www.xiaolincoding.com/interview/mysql.html"
    "Redis|Redis 有哪些数据类型？|String、List、Set、Hash、ZSet（有序集合）。还有 Bitmap、HyperLogLog、Geo 等高级类型。|https://www.xiaolincoding.com/interview/redis.html"
    "Redis|缓存穿透、击穿、雪崩的区别？|穿透：查不存在的数据；击穿：热点 key 过期；雪崩：大量 key 同时过期。解决方案：布隆过滤器、互斥锁、随机过期时间。|https://www.xiaolincoding.com/interview/redis.html"
    "网络|TCP 三次握手和四次挥手？|三次握手：SYN→SYN+ACK→ACK；四次挥手：FIN→ACK→FIN→ACK。三次握手建立连接，四次挥手断开连接。|https://www.xiaolincoding.com/interview/network.html"
    "网络|HTTP 和 HTTPS 的区别？|HTTPS = HTTP + SSL/TLS。HTTPS 加密传输，端口 443，需要证书，更安全。|https://www.xiaolincoding.com/interview/network.html"
    "操作系统|进程和线程的区别？|进程是资源分配单位，线程是 CPU 调度单位。线程共享进程内存，进程间独立。线程切换开销小。|https://www.xiaolincoding.com/interview/os.html"
    "系统设计|如何设计一个短链接系统？|核心：发号器（自增/分布式 ID）、存储（MySQL/Redis）、缓存（热点数据）、重定向（301/302）。|https://www.xiaolincoding.com/interview/systemdesign.html"
)

# 随机选择 5 道题目（确保不重复）
SELECTED=()
USED_INDICES=()
while [ ${#SELECTED[@]} -lt 5 ]; do
    INDEX=$((RANDOM % ${#QUESTIONS[@]}))
    # 检查是否已选过
    ALREADY_USED=0
    for used in "${USED_INDICES[@]}"; do
        if [ "$used" -eq "$INDEX" ]; then
            ALREADY_USED=1
            break
        fi
    done
    if [ $ALREADY_USED -eq 0 ]; then
        USED_INDICES+=($INDEX)
        SELECTED+=("${QUESTIONS[$INDEX]}")
    fi
done

# 构建消息内容
MESSAGE="📚 *Java 学习日报* - $DATE

今日精选 5 道面试题：

"

COUNT=1
for q in "${SELECTED[@]}"; do
    IFS='|' read -r CATEGORY QUESTION ANSWER LINK <<< "$q"
    MESSAGE+="${COUNT}. *【${CATEGORY}】${QUESTION}*
   💡 ${ANSWER}
   🔗 <${LINK}|查看详细解析>

"
    COUNT=$((COUNT + 1))
done

MESSAGE+="
---
💪 坚持每天学习，大厂 offer 等着你！
来源：小林 coding 面试题汇总"

# 发送消息到飞书
cd /root/.openclaw/workspace
openclaw message send --channel feishu --target "$TARGET_USER" --message "$MESSAGE" 2>&1 | tee -a "$LOG_FILE"

echo "[$DATE $TIME] Java 学习日报发送完成" >> "$LOG_FILE"
