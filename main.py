import time
import os
import sys
import locale
from openai import OpenAI
from openai._utils import convert_to_openai_object

# ===================== 1. 彻底修复中文编码（关键！） =====================
# 1.1 设置系统locale为UTF-8
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    locale.setlocale(locale.LC_ALL, 'C.UTF-8')

# 1.2 强制Python全环节UTF-8
os.environ.update({
    'PYTHONIOENCODING': 'utf-8',
    'LC_ALL': 'en_US.UTF-8',
    'LANG': 'en_US.UTF-8',
    'LC_CTYPE': 'en_US.UTF-8'
})
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ===================== 2. 基础配置（替换为你的实际值） =====================
API_KEY = "你的Gemini/OpenAI API密钥"
BASE_URL = "https://generativelanguage.googleapis.com/v1"  # Gemini的base_url
model_name = "gemini-2.5-flash"
GEMINI_REQUEST_DELAY = 2
TODAY_STR = time.strftime("%Y年%m月%d日", time.localtime())
CURRENT_YEAR = int(time.strftime("%Y", time.localtime()))
TARGET_COMPANIES = "威高集团、三角轮胎、威海广泰、荣成华泰、文登威力工具"

# ===================== 3. 初始化客户端（强制UTF-8请求头） =====================
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    default_headers={
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json; charset=utf-8"
    }
)

# ===================== 4. 搜索函数（模拟/替换为真实逻辑） =====================
def search_info(keywords):
    """模拟搜索，返回非空UTF-8字符串"""
    mock_data = {
        f"{TARGET_COMPANIES} 威海 涉外业务 近7天": "威高集团获中东1亿美元医疗设备订单；三角轮胎海外工厂产能扩建30%；威海广泰拿下拉美机场设备订单；荣成华泰新能源汽车出口中亚；文登威力工具获欧盟专利认证",
        "威海 荣成 文登 乳山 政经 外贸 招商 近7天": "威海发布2026外贸新政：中亚贸易通道补贴提升20%；荣成海洋经济产业园签约3个亿元项目；文登家纺产业对接中东经贸走廊；乳山海产品出口欧盟关税下调",
        "威海 工程承包 橡胶轮胎 医疗器械 油气装备 机器人 行业动向 近7天": "医疗器械出口欧盟绿色壁垒升级：新增3项检测标准；轮胎行业原材料橡胶价格下跌5%；海洋工程装备出口东南亚增长15%",
        "LPR 存款准备金率 美联储利率 汇率 威海银行 跨境结算 出口信贷 近7天": "2月LPR下调5个基点：1年期3.45%；美元兑人民币汇率中间价6.89；威海银行推出跨境结算手续费减免50%政策",
        "国内国际政治经济 贸易局势 大宗商品价格 威海 近7天": "日韩自贸协定更新：威海汽配出口关税再降3%；中亚五国关税同盟利好威海农机出口；橡胶期货价格上涨3%；海产品国际价格波动+2%",
        "大语言模型 AI 机器人 新能源 全球前沿科技 近7天": "大语言模型助力威海跨境电商AI翻译：效率提升40%；医疗AI在威高集团质检环节落地；深海装备AI检测技术突破；全球新能源电池技术迭代：成本降10%"
    }
    # 强制转为UTF-8编码字符串
    result = mock_data.get(keywords, "默认素材内容，确保不为空")
    return result.encode('utf-8').decode('utf-8')

# ===================== 5. 生成周报函数（修复API调用编码） =====================
def generate_briefing():
    """生成周报，彻底解决中文编码问题"""
    try:
        # 1. 搜索素材（确保UTF-8）
        comp_raw = search_info(f"{TARGET_COMPANIES} 威海 涉外业务 近7天")
        weihai_raw = search_info("威海 荣成 文登 乳山 政经 外贸 招商 近7天")
        ind_context = search_info("威海 工程承包 橡胶轮胎 医疗器械 油气装备 机器人 行业动向 近7天")
        finance_raw = search_info("LPR 存款准备金率 美联储利率 汇率 威海银行 跨境结算 出口信贷 近7天")
        macro_raw = search_info("国内国际政治经济 贸易局势 大宗商品价格 威海 近7天")
        tech_raw = search_info("大语言模型 AI 机器人 新能源 全球前沿科技 近7天")

        # 2. 构建prompt（强制UTF-8）
        prompt_template = """
【全局核心设定】
    1. 角色：顶尖投行研究所首席经济师。无修辞，无客套，极端客观。今天是{TODAY_STR}。
    2. 辖区绝对定义：下文中所有提到"大威海地区"、"威海市辖区"、"威海本地"的概念，均【严格且仅包含】威海、荣成、文登、乳山四个区域。
    3. 严格审查每条素材的时间与真实性:
       - 如果内容事件发生时间涉及{TODAY_STR}之前一周以上的旧闻，绝对不予采纳！
       - 严禁拿旧闻（{CURRENT_YEAR - 1}年及以前的内容）凑数，或伪造虚假URL。
    4. 【反摆烂绝对红线】：严禁在正文中输出任何诸如"受限于素材密度"、"未搜索到相关信息"等借口或声明性文字。必须竭尽全力从下方庞大的素材池中挖掘信息，严格满足各板块要求的数量！
    5. 一个来源链接（URL）最多只能对应生成一条新闻，严格禁止一个素材反复使用。
    6. 【新增：价值挖掘核心规则】：
       - 核心必保：所有板块优先筛选"领导重点关注"的高价值信息（如目标企业重大订单、威海核心外贸政策、关键金融指标变动），确保"想看的能看到"；
       - 惊喜挖掘：主动从素材池边缘/冷门素材中，识别"非预期但有长期价值"的信息（如威海中小企业冷门市场突破、新兴赛道试点、隐藏政策红利），确保"意想不到的也能看到"；
       - 分析要求：每条新闻的"三句话梗概"中，第三句话必须为【价值分析句】——核心信息分析"直接商业影响"，惊喜信息分析"隐藏价值/长远意义"，不得仅陈述事实。
    
    【极度严厉的排版与格式指令】
    1. 必须首先生成【目录】，严格照抄以下 HTML 格式：
       <h3 style="color: #1a365d; font-size: 18px; font-weight: normal; margin-top: 20px; margin-bottom: 10px;">一、 重点企业动态</h3>
       <div style="font-size: 14px; color: #333; line-height: 1.8;">
       1. [新闻标题1]<br>
       2. [新闻标题2]<br>
       </div>
    2. 正文部分格式指令：
       正文所有板块的每一条新闻，【绝对禁止使用 Markdown 列表(* 或 -)】，必须严格使用以下 HTML 结构框定，以确保字号精确递减：
       <div style="margin-bottom: 20px;">
         <div style="font-size: 14px; font-weight: bold; color: #333;">[序号]. [标题]</div>
         <div style="font-size: 14px; color: #333; line-height: 1.6; margin-top: 4px;">[用三句话精确概括核心事件、商业动作及影响]</div>
         <div style="font-size: 12px; color: #666; margin-top: 4px;">关键词：[词1] | [词2]</div>
         <div style="font-size: 10px; color: #999; margin-top: 4px;">来源：<a href="[URL]" style="color: #3498db; text-decoration: none;">[URL]</a></div>
       </div>

    【六大板块内容架构（基于下方素材池）】
    一、 重点企业动态（强制生成 15 条）：
        【收录标准】：必须且只能是具体的实体企业。企业必须有明确的涉外属性（国际业务、海外投资、出口订单、外贸潜力）或重大的实体产能扩建。优先包含给定目标企业（{TARGET_COMPANIES}）的动态。
        【核心必保筛选】：
          1. 优先筛选{TARGET_COMPANIES}的重大涉外动作（如大额海外订单、海外工厂落地、国际认证获取），至少占8条；
          2. 优先筛选威海龙头企业（威高、三角轮胎、威海广泰等）的产能扩建/跨境合作，至少占4条；
        【惊喜挖掘筛选】：
          1. 挖掘威海中小微企业的非传统市场突破（如中亚/中东/拉美订单、小众领域国际专利），至少占2条；
          2. 挖掘威海企业在新兴赛道（低空经济、合成生物、深海装备）的涉外布局，至少占1条；
        【绝对排除红线】：严格排除以下4类内容，若素材属于此类，直接抛弃，宁可从素材池深挖也不得用其凑数：
          1. 绝对禁止包含任何银行、金融机构（此类应归入第四部分）。
          2. 绝对禁止包含区域宏观经济、政府招商会议、工作动员大会（此类应归入第二部分）。
          3. 绝对禁止包含任何形式的"股价动态"、"股票价格"、"涨跌幅"新闻。
          4. 绝对禁止包含纯国内本地生活服务类企业（如国内客运、饭店、国内文旅、学校、本地商店等）。
        注意，企业必须严格限制在威海辖区内，绝对禁止纳入非威海的全国性科技公司！必须凑够15条，严禁写借口。
        【关键词规则升级】：词1为"事实标签"（如"海外订单"），词2为"价值标签"（如"中东市场突破"），不得仅标注通用词汇。
    
    二、 威海本地政经（强制生成 8 条）：
        【收录与配比标准】：必须严格凑够 8 条，且内部结构必须执行以下硬性配比，绝对不许越界：
        1. 核心政经与产业（6至8条）：必须聚焦威海市辖区的产业发展、外经外贸、重大招商引资、新质生产力、地方政府债务、重大会议与工作部署。
        2. 民生与消费（最高限额 2 条）：国内消费市场、文旅活动、人才招聘等社会民生新闻【严格限制在 2 条以内】。
        若民生消费类素材不足，剩余名额全部由"核心政经与产业"补齐。绝对排斥社会奇闻、恶性事件。严禁写借口。
        【核心必保筛选】：
          1. 优先筛选威海市级层面发布的外贸/招商政策、重大产业项目签约，至少占4条；
          2. 优先筛选荣成/文登/乳山的核心产业升级动态，至少占2条；
        【惊喜挖掘筛选】：
          1. 挖掘威海对接非传统合作区域的政策（如中亚自贸区对接、中东经贸走廊），至少占1条；
          2. 挖掘威海细分产业（渔具/家纺/海洋食品）的隐藏政策红利，至少占1条；
        【关键词规则升级】：词1为"事实标签"（如"招商引资"），词2为"价值标签"（如"新质生产力布局"）。
    
    三、 行业风向（每个行业 2 条）：
        禁止聚焦单一企业公关稿。每个行业配齐一内一外共两条新闻。新闻内容须为行业内最新突破、重大利好或利空、可能影响行业的重要事件及其影响。
        【核心必保筛选】：优先筛选威海支柱产业（医疗器械、轮胎、海洋经济）的行业动向，至少覆盖3个行业；
        【惊喜挖掘筛选】：挖掘威海小众优势行业（渔具、家纺、高端装备）的国际行业规则变动（如欧盟绿色壁垒、东南亚市场标准），至少覆盖1个行业；
        【关键词规则升级】：词1为"行业标签"（如"医疗器械"），词2为"影响标签"（如"出口壁垒升级"）。
    
    四、 金融与银行（强制生成 8 条）：
        1. 金融宏观（5条）：LPR、存款准备金率、美联储利率、汇率等发生重大变化或其他有出海需求的中国大陆企业应当关注的其他新闻。
        2. 本地银行（3条）：严格限制在威海市辖区内开展业务的银行，关于跨境结算、对公业务、出口信贷等方面出台新优惠政策或其他领域的新闻，不包括银行股价变动等出口企业进行海外业务不需要的信息。
        3. 每个指标一条新闻，绝对禁止一个指标的变动占用3条新闻额度。
        4. 当素材池内有一个指标在一周内多次变化的多条新闻时，仅采用最新的一条。（例如当美元汇率每天都公布最新中间价时，只用最近一天的那一条新闻。）
        【核心必保筛选】：优先筛选对威海出口企业影响最大的金融指标（如美元汇率、出口信贷利率），至少占5条；
        【惊喜挖掘筛选】：挖掘小众金融工具（如跨境人民币结算、海外仓融资）在威海的落地动态，至少占1条；
        【关键词规则升级】：词1为"指标标签"（如"LPR"），词2为"影响标签"（如"出口企业融资成本"）。
    
    五、 宏观与全球重点局势（强制生成 7 条）：
        国内与国际政治经济、贸易局势、突发事件重大新闻。其中国内6条，国际4条。
        新闻内容要限制在会影响产业发展、大宗商品价格、经贸局势的新闻。
        【核心必保筛选】：优先筛选影响威海核心贸易伙伴（日韩、欧盟）的局势，至少占4条；
        【惊喜挖掘筛选】：挖掘影响威海非传统贸易区（中亚、中东）的局势、小众大宗商品（橡胶、海产品）价格变动，至少占2条；
        【关键词规则升级】：词1为"区域标签"（如"日韩贸易"），词2为"影响标签"（如"威海出口成本"）。
    
    六、 科技前沿与大语言模型（强制生成 9 条）：
        全面汇总4条大语言模型最新焦点、2条中国科技进展（AI或者机器人或者新能源）及3条全球前沿动向。发布时间须为{TODAY_STR}的三日内，消息内事件的发生时间也须为{TODAY_STR}的三日内，严格审核。
        【核心必保筛选】：优先筛选与威海产业结合的科技进展（如医疗AI、轮胎智能制造），至少占3条；
        【惊喜挖掘筛选】：挖掘可能颠覆威海传统产业的前沿科技（如深海AI检测、跨境电商AI翻译），至少占2条；
        【关键词规则升级】：词1为"科技标签"（如"大语言模型"），词2为"应用标签"（如"威海外贸效率提升"）。

    【素材池】
    一/重点企业: {comp_raw}
    二/大威海政经: {weihai_raw}
    三/行业: {ind_context}
    四/金融与银行: {finance_raw}
    五/宏观: {macro_raw}
    六/科技: {tech_raw}

    【输出框架】：
    # 威海营业部超级周报
    **报告日期：** {TODAY_STR} | 来自您的超级智能新闻官🤖
    ---
    ## 目录
    （目录 HTML 代码）
    ---
    ## 一、 重点企业动态
    （正文 HTML 代码）
    ## 二、 威海本地政经
    （正文 HTML 代码）
    ## 三、 行业风向
    （正文 HTML 代码）
    ## 四、 金融与银行
    （正文 HTML 代码）
    ## 五、 宏观与全球重点局势
    （正文 HTML 代码）
    ## 六、 科技前沿与大语言模型
    （正文 HTML 代码）
    ---
    <p style="text-align: center;"><strong>以上为本周新闻，均为自动收集并由AI生成</strong></p>
    <p style="text-align: center;">🤖我们下周再见🤖</p>
        """
        # 格式化prompt并强制UTF-8
        prompt = prompt_template.format(
            TODAY_STR=TODAY_STR,
            CURRENT_YEAR=CURRENT_YEAR,
            TARGET_COMPANIES=TARGET_COMPANIES,
            comp_raw=comp_raw,
            weihai_raw=weihai_raw,
            ind_context=ind_context,
            finance_raw=finance_raw,
            macro_raw=macro_raw,
            tech_raw=tech_raw
        ).encode('utf-8').decode('utf-8')

        time.sleep(GEMINI_REQUEST_DELAY)
        
        # 调用API（强制UTF-8请求体）
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            # 强制返回UTF-8编码
            extra_headers={"Content-Type": "application/json; charset=utf-8"}
        )
        
        # 处理响应（确保UTF-8）
        result = response.choices[0].message.content.strip()
        return result if result else "生成的周报内容为空，请检查素材或API配置"
    
    except Exception as e:
        error_msg = f"生成简报失败：{str(e)}"
        print(error_msg)
        # 确保错误信息也是UTF-8
        return error_msg.encode('utf-8').decode('utf-8')

# ===================== 6. 邮件发送函数（保留空值防护） =====================
def send_email(subject, markdown_content):
    """发送邮件，增加空值检查和字符处理"""
    if not markdown_content:
        markdown_content = "【警告】周报内容为空，生成失败"
    
    try:
        markdown_content = markdown_content.replace("```html", "").replace("```", "")
    except Exception as e:
        print(f"处理邮件内容失败：{e}")
        markdown_content = f"【内容处理失败】{markdown_content}"
    
    # 示例：打印邮件内容（替换为你的SMTP发送逻辑）
    try:
        print(f"===== 准备发送邮件 =====")
        print(f"标题：{subject}")
        print(f"内容：{markdown_content[:500]}...")  # 打印前500字符
        return True
    except Exception as e:
        print(f"发送邮件失败：{e}")
        return False

# ===================== 7. 主函数 =====================
if __name__ == "__main__":
    print(f"-> 启动报告生成器，当前日期：{TODAY_STR} ...")
    print(f"-> 系统编码：{sys.getdefaultencoding()} | Locale：{locale.getlocale()}")
    print(f"-> 正在使用 {model_name} 接口...")
    
    # 生成周报
    briefing = generate_briefing()
    print(f"-> 周报生成完成，长度：{len(briefing)} 字符")
    
    # 发送邮件
    email_subject = f"【威海商业情报】{TODAY_STR}"
    send_result = send_email(email_subject, briefing)
    
    if send_result:
        print("-> 邮件发送成功！")
    else:
        print("-> 邮件发送失败！")
