#!/usr/bin/env python3
"""
前端求职情报日报 - GitHub Actions 版本
"""
import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

EMAIL_CONFIG = {
    "smtp_server": "smtp.qq.com",
    "smtp_port": 587,
    "sender_email": "1402328968@qq.com",
    "sender_password": os.environ.get('EMAIL_PASSWORD', ''),
    "receiver_email": os.environ.get('RECEIVER_EMAIL', '1402328968@qq.com')
}

JOB_DATA = [
    {"company": "字节跳动", "position": "高级前端开发", "salary": "35-55K·16薪", "location": "上海·浦东", "stack": "React, TypeScript, Node.js"},
    {"company": "蚂蚁集团", "position": "前端技术专家", "salary": "45-70K·16薪", "location": "上海·浦东", "stack": "React, TypeScript, Rust"},
    {"company": "拼多多", "position": "资深前端开发", "salary": "40-60K·18薪", "location": "上海·长宁", "stack": "Vue3, TypeScript, SSR"},
    {"company": "小红书", "position": "前端架构师", "salary": "50-80K·15薪", "location": "上海·黄浦", "stack": "React, RN, Flutter"},
    {"company": "B站", "position": "高级前端开发", "salary": "30-50K·15薪", "location": "上海·杨浦", "stack": "Vue3, Vite, Node.js"},
    {"company": "美团", "position": "前端技术专家", "salary": "40-65K·15薪", "location": "上海·闵行", "stack": "React, TypeScript, 工程化"},
]

TECH_TRENDS = [
    {"name": "TypeScript", "demand": "92%", "trend": "↑ 持续上涨"},
    {"name": "React", "demand": "85%", "trend": "→ 稳定"},
    {"name": "Vue3", "demand": "72%", "trend": "↑ 快速增长"},
    {"name": "Node.js", "demand": "68%", "trend": "→ 稳定"},
    {"name": "微前端", "demand": "45%", "trend": "↑ 新兴需求"},
]

INTERVIEW_QUESTIONS = [
    {"category": "JavaScript", "q": "请解释Event Loop机制", "a": "事件循环是JS异步核心。调用栈执行同步代码，微任务队列（Promise）和宏任务队列（setTimeout）管理异步。栈清空后先执行所有微任务，再取一个宏任务。", "follow": ["微任务宏任务区别？", "Promise vs setTimeout执行顺序？"]},
    {"category": "React", "q": "React 18有哪些重要更新？", "a": "并发渲染、自动批处理、Transition API、Suspense改进、新Hooks（useId、useDeferredValue）。", "follow": ["并发模式如何影响现有代码？", "useTransition使用场景？"]},
    {"category": "Vue", "q": "Vue3相比Vue2有哪些核心改进？", "a": "响应式系统重写（Proxy）、Composition API、更好的TS支持、Tree-shaking优化、性能提升约1.2-2倍。", "follow": ["Proxy vs defineProperty？", "Composition API优势？"]},
    {"category": "工程化", "q": "Webpack构建流程是什么？", "a": "初始化参数→创建Compiler→加载插件→run方法→编译模块（从entry递归解析）→输出资源→写入文件系统。", "follow": ["Loader vs Plugin？", "Vite为什么更快？"]},
    {"category": "性能优化", "q": "前端性能优化主要手段？", "a": "加载优化：压缩、CDN、懒加载、HTTP/2、缓存。渲染优化：虚拟列表、防抖节流、rAF、Web Worker。监控：Performance API、LCP/FID/CLS。", "follow": ["如何定位性能瓶颈？", "首屏优化方案？"]},
    {"category": "系统设计", "q": "如何设计前端监控系统？", "a": "数据采集（错误、性能、行为）→数据上报（sendBeacon）→数据处理（解析、聚合）→可视化→告警。关键指标：错误率、首屏时间、API成功率。", "follow": ["如何保证上报可靠性？", "告警规则设计？"]},
    {"category": "TypeScript", "q": "TypeScript泛型是什么？如何使用？", "a": "泛型是类型参数化，允许创建可复用的组件。用于函数、接口、类。常见场景：API响应类型、工具函数类型推导。", "follow": ["泛型约束？", "条件类型？"]},
]

COMPANY_INSIGHTS = [
    {"name": "字节跳动", "culture": "技术驱动、快速迭代", "style": "重算法、重原理", "tip": "刷LeetCode中等难度"},
    {"name": "蚂蚁集团", "culture": "技术深度、稳定性", "style": "重原理、重架构", "tip": "准备金融场景方案"},
    {"name": "拼多多", "culture": "效率优先、简单直接", "style": "重实战、重性能", "tip": "准备性能优化案例"},
    {"name": "小红书", "culture": "社区氛围、产品导向", "style": "重产品理解", "tip": "展示跨端经验"},
    {"name": "B站", "culture": "技术氛围好", "style": "重基础、重兴趣", "tip": "开源项目加分"},
    {"name": "美团", "culture": "务实、业务导向", "style": "重工程化", "tip": "准备架构方案"},
    {"name": "腾讯", "culture": "产品导向、生态完善", "style": "重基础、重综合", "tip": "准备全栈能力展示"},
]

def get_daily_data():
    weekday = datetime.now().weekday()
    return {
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday],
        "jobs": JOB_DATA[:5],
        "tech_trends": TECH_TRENDS,
        "question": INTERVIEW_QUESTIONS[weekday % len(INTERVIEW_QUESTIONS)],
        "company": COMPANY_INSIGHTS[weekday % len(COMPANY_INSIGHTS)],
    }

def format_text(data):
    lines = []
    lines.append("=" * 60)
    lines.append(f"💼 前端求职情报日报 - {data['date']} {data['weekday']}")
    lines.append("=" * 60)
    lines.append("\n▶ 💼 上海热门岗位")
    lines.append("-" * 60)
    for job in data["jobs"]:
        lines.append(f"  【{job['company']}】{job['position']}")
        lines.append(f"    {job['salary']} | {job['location']}")
        lines.append(f"    技术栈: {job['stack']}")
        lines.append("")
    lines.append("\n▶ 📊 技术栈需求")
    lines.append("-" * 60)
    for tech in data["tech_trends"]:
        lines.append(f"  {tech['name']}: {tech['demand']} {tech['trend']}")
    lines.append("\n▶ 📝 今日真题")
    lines.append("-" * 60)
    q = data["question"]
    lines.append(f"  【{q['category']}】{q['q']}")
    lines.append(f"  答: {q['a']}")
    lines.append("  追问:")
    for i, f in enumerate(q['follow'], 1):
        lines.append(f"    {i}. {f}")
    lines.append("\n▶ 🏢 今日目标公司")
    lines.append("-" * 60)
    c = data["company"]
    lines.append(f"  【{c['name']}】{c['culture']}")
    lines.append(f"    面试风格: {c['style']}")
    lines.append(f"    💡 备考: {c['tip']}")
    lines.append("\n▶ 💡 求职锦囊")
    lines.append("-" * 60)
    lines.append("  【简历】突出架构设计能力，用数据说话")
    lines.append("  【面试】准备3个版本自我介绍(30s/1m/3m)")
    lines.append("  【谈薪】10年经验市场价45-70K，看总包")
    lines.append("\n" + "=" * 60)
    lines.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("💬 十年磨一剑，愿你找到心仪团队！")
    return "\n".join(lines)

def format_html(data):
    html = ['''
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
body{font-family:-apple-system,Arial,sans-serif;background:#1a1a2e;padding:20px;color:#333}
.container{max-width:650px;margin:0 auto;background:#fff;border-radius:12px}
.header{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:25px;text-align:center}
.section{padding:15px 20px;border-bottom:1px solid #eee}
.section-title{font-size:16px;font-weight:bold;color:#667eea;margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid #667eea}
.job-card{background:#f8f9fa;padding:12px;border-radius:6px;margin:8px 0;border-left:3px solid #667eea}
.job-header{display:flex;justify-content:space-between;font-weight:bold;margin-bottom:5px}
.company{color:#667eea}.salary{color:#e74c3c}
.tech-item{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #f5f5f5}
.question-box{background:#fff8e1;padding:12px;border-radius:6px}
.follow{margin-top:10px;padding-top:10px;border-top:1px dashed #ddd}
.company-box{background:linear-gradient(135deg,#f5f7fa,#c3cfe2);padding:12px;border-radius:6px}
.tip{background:#e8f4fd;padding:10px;border-left:3px solid #667eea;margin:10px 0;border-radius:4px}
.footer{padding:20px;text-align:center;color:#999;font-size:12px}
</style></head>
<body><div class="container">
''']
    html.append(f'<div class="header"><h1>💼 前端求职情报日报</h1><p>{data["date"]} {data["weekday"]}</p></div>')
    html.append('<div class="section"><div class="section-title">💼 上海热门岗位</div>')
    for job in data["jobs"]:
        html.append(f'''
        <div class="job-card">
            <div class="job-header"><span class="company">{job["company"]}</span><span class="salary">{job["salary"]}</span></div>
            <div>{job["position"]} | {job["location"]}</div>
            <div style="color:#666;margin-top:5px">技术栈: {job["stack"]}</div>
        </div>''')
    html.append('</div>')
    html.append('<div class="section"><div class="section-title">📊 技术栈需求</div>')
    for tech in data["tech_trends"]:
        color = "#27ae60" if "↑" in tech["trend"] else "#666"
        html.append(f'<div class="tech-item"><span>{tech["name"]}</span><span>{tech["demand"]} <span style="color:{color}">{tech["trend"]}</span></span></div>')
    html.append('</div>')
    q = data["question"]
    html.append(f'''
    <div class="section"><div class="section-title">📝 今日真题</div>
    <div class="question-box">
        <div style="color:#667eea;font-weight:bold">【{q["category"]}】</div>
        <div style="margin:10px 0;font-weight:bold">{q["q"]}</div>
        <div style="color:#555">{q["a"]}</div>
        <div class="follow">
            <div style="font-weight:bold;color:#667eea">追问:</div>
            {''.join([f'<div style="padding:3px 0 3px 15px">{f}</div>' for f in q['follow']])}
        </div>
    </div>
    </div>''')
    c = data["company"]
    html.append(f'''
    <div class="section"><div class="section-title">🏢 今日目标公司</div>
    <div class="company-box">
        <div style="font-weight:bold;font-size:18px;margin-bottom:8px">{c["name"]}</div>
        <div>文化: {c["culture"]}</div>
        <div>风格: {c["style"]}</div>
        <div class="tip">💡 备考建议: {c["tip"]}</div>
    </div>
    </div>''')
    html.append('''
    <div class="section"><div class="section-title">💡 求职锦囊</div>
    <div class="tip">📝 简历: 突出架构设计能力，用数据说话</div>
    <div class="tip">🎤 面试: 准备3个版本自我介绍(30s/1m/3m)</div>
    <div class="tip">💰 谈薪: 10年经验市场价45-70K，看总包</div>
    </div>''')
    html.append(f'<div class="footer">⏰ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 💬 十年磨一剑，愿你找到心仪团队！</div>')
    html.append('</div></body></html>')
    return "\n".join(html)

def send_email(text, html):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['receiver_email']
        msg['Subject'] = Header(f"💼 前端求职情报日报 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['receiver_email'], msg.as_string())
        print("✅ 邮件发送成功")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def main():
    print(f"开始生成求职日报... {datetime.now()}")
    if not EMAIL_CONFIG['sender_password']:
        print("❌ 未配置邮箱授权码")
        return False
    data = get_daily_data()
    text = format_text(data)
    html = format_html(data)
    print(text)
    success = send_email(text, html)
    with open('job_push.log', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n{datetime.now().isoformat()}\n{text}\n状态: {'成功' if success else '失败'}\n")
    return success

if __name__ == "__main__":
    main()