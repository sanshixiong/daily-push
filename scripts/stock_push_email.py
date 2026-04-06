#!/usr/bin/env python3
"""
股市信息推送脚本 - GitHub Actions 版本
"""
import os
import smtplib
from datetime import datetime
import urllib.request
import re
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

def fetch_url(url, headers=None, timeout=10):
    if headers is None:
        headers = {
            'Referer': 'https://finance.sina.com.cn',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('gbk')
    except:
        return None

def get_index_data(code, name):
    try:
        url = f"https://hq.sinajs.cn/list={code}"
        data = fetch_url(url)
        if data:
            match = re.search(r'var hq_str_[^"]+="(.+?)";', data)
            if match:
                parts = match.group(1).split(',')
                if len(parts) >= 10:
                    price = float(parts[3])
                    prev_close = float(parts[2])
                    change = price - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                    amount = float(parts[9])
                    return {
                        "name": name,
                        "price": f"{price:.2f}",
                        "change": f"{change:+.2f}",
                        "change_pct": f"{change_pct:+.2f}%",
                        "amount": f"{amount/100000000:.0f}亿",
                        "color": "red" if change >= 0 else "green"
                    }
    except:
        pass
    return {"name": name, "error": "获取失败"}

def get_stock_detail(code, name):
    try:
        url = f"https://hq.sinajs.cn/list={code}"
        data = fetch_url(url)
        if data:
            match = re.search(r'var hq_str_[^"]+="(.+?)";', data)
            if match:
                parts = match.group(1).split(',')
                if len(parts) >= 30:
                    price = float(parts[3])
                    prev_close = float(parts[2])
                    change = price - prev_close
                    change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
                    high = float(parts[4])
                    low = float(parts[5])
                    amount = float(parts[9])
                    return {
                        "name": name,
                        "price": f"{price:.2f}",
                        "change": f"{change:+.2f}",
                        "change_pct": f"{change_pct:+.2f}%",
                        "amplitude": f"{((high-low)/prev_close)*100:.2f}%",
                        "amount": f"{amount/100000000:.2f}亿",
                        "color": "red" if change >= 0 else "green"
                    }
    except:
        pass
    return {"name": name, "error": "获取失败"}

def get_all_data():
    data = {
        "date": datetime.now().strftime("%Y年%m月%d日"),
        "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][datetime.now().weekday()],
        "sections": []
    }
    
    indices_section = {"title": "📊 大盘风向标", "content": []}
    indices = [("sh000001", "上证指数"), ("sz399001", "深证成指"), ("sz399006", "创业板指"), ("sh000016", "上证50"), ("sh000905", "中证500")]
    for code, name in indices:
        indices_section["content"].append(get_index_data(code, name))
    data["sections"].append(indices_section)
    
    sectors_section = {"title": "🔥 热门赛道", "content": []}
    sectors = [("sh512480", "半导体"), ("sh515030", "新能源车"), ("sh515790", "光伏"), ("sh512760", "芯片"), ("sh561160", "锂电池"), ("sh515070", "AI智能")]
    for code, name in sectors:
        sectors_section["content"].append(get_stock_detail(code, name))
    data["sections"].append(sectors_section)
    
    leaders_section = {"title": "👑 龙头股", "content": []}
    leaders = [("sh600519", "贵州茅台"), ("sz300750", "宁德时代"), ("sz002594", "比亚迪"), ("sh600036", "招商银行"), ("sh688981", "中芯国际")]
    for code, name in leaders:
        leaders_section["content"].append(get_stock_detail(code, name))
    data["sections"].append(leaders_section)
    
    rules_section = {"title": "📝 交易纪律", "content": ["① 买入前先想好止损位", "② 不追高，只低吸", "③ 盈利5%以上分批止盈", "④ 单票亏损不超过总资金2%", "⑤ 新手仓位不超过5成"]}
    data["sections"].append(rules_section)
    
    lessons = [{"topic": "量价关系", "points": ["放量上涨=资金进场", "缩量上涨=筹码锁定"]}, {"topic": "均线系统", "points": ["5日线=短线生命线", "10日线=止损参考"]}, {"topic": "换手率", "points": ["1-3%=正常", "3-7%=活跃"]}]
    lesson = lessons[datetime.now().weekday() % len(lessons)]
    learn_section = {"title": "📚 每日一学", "content": [f"{lesson['topic']}: {', '.join(lesson['points'])}"]}
    data["sections"].append(learn_section)
    
    return data

def format_text(data):
    lines = []
    lines.append("=" * 60)
    lines.append(f"📈 中短线学徒日报 - {data['date']} {data['weekday']}")
    lines.append("=" * 60)
    for section in data["sections"]:
        lines.append(f"\n▶ {section['title']}")
        lines.append("-" * 60)
        for item in section["content"]:
            if isinstance(item, dict):
                if "error" in item:
                    lines.append(f"  {item['name']}: {item.get('error', '获取失败')}")
                else:
                    symbol = "↑" if not item['change'].startswith('-') else "↓"
                    lines.append(f"  {item['name']}: {item['price']} {symbol} {item['change_pct']} | {item['amount']}")
            else:
                lines.append(f"  {item}")
    lines.append("\n" + "=" * 60)
    lines.append(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 数据: 新浪财经")
    return "\n".join(lines)

def format_html(data):
    html = ['''
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><style>
body{font-family:-apple-system,Arial,sans-serif;background:#f5f5f5;padding:20px;color:#333}
.container{max-width:600px;margin:0 auto;background:#fff;border-radius:12px}
.header{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:25px;text-align:center}
.section{padding:15px 20px;border-bottom:1px solid #eee}
.section-title{font-size:16px;font-weight:bold;color:#667eea;margin-bottom:12px}
.item{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f5f5f5}
.name{font-weight:500}.price{font-weight:bold}
.up{color:#e74c3c}.down{color:#27ae60}
.rule{padding:5px 0 5px 10px;color:#555}
.footer{padding:20px;text-align:center;color:#999;font-size:12px}
</style></head>
<body><div class="container">
''']
    html.append(f'<div class="header"><h1>📈 中短线学徒日报</h1><p>{data["date"]} {data["weekday"]}</p></div>')
    for section in data["sections"]:
        html.append(f'<div class="section"><div class="section-title">{section["title"]}</div>')
        for item in section["content"]:
            if isinstance(item, dict):
                if "error" in item:
                    html.append(f'<div class="item"><span class="name">{item["name"]}</span><span style="color:#999">{item.get("error","获取失败")}</span></div>')
                else:
                    css = "up" if not item['change'].startswith('-') else "down"
                    symbol = "↑" if not item['change'].startswith('-') else "↓"
                    html.append(f'<div class="item"><span class="name">{item["name"]}</span><span class="price {css}">{item["price"]} {symbol} {item["change_pct"]}</span></div>')
            else:
                html.append(f'<div class="rule">{item}</div>')
        html.append('</div>')
    html.append(f'<div class="footer">⏰ {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 数据: 新浪财经</div>')
    html.append('</div></body></html>')
    return "\n".join(html)

def send_email(text, html):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['receiver_email']
        msg['Subject'] = Header(f"📈 中短线学徒日报 - {datetime.now().strftime('%Y-%m-%d')}", 'utf-8')
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
    print(f"开始生成股市日报... {datetime.now()}")
    if not EMAIL_CONFIG['sender_password']:
        print("❌ 未配置邮箱授权码")
        return False
    data = get_all_data()
    text = format_text(data)
    html = format_html(data)
    print(text)
    success = send_email(text, html)
    with open('stock_push.log', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n{datetime.now().isoformat()}\n{text}\n状态: {'成功' if success else '失败'}\n")
    return success

if __name__ == "__main__":
    main()