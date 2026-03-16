from __future__ import annotations

import html
import subprocess
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parent
OUTPUT_HTML = ROOT / "travel_souvenir_guide.html"
OUTPUT_PDF = ROOT / "travel_souvenir_guide.pdf"

BROWSER_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

PAGE_TITLE = "歐洲 8 日行程實用整理"

TRIP_FACTS = [
    ("幣別", "法國、比利時、荷蘭全程使用歐元（EUR），小額零錢建議備 5€、10€。"),
    ("插頭", "以 Type C / E / F 為主，電壓 230V；手機與行動電源每天回飯店就充。"),
    ("付款", "大部分店家可刷卡，荷蘭尤其友善；市集、小吃與公廁仍可能需要零錢。"),
    ("安全", "扒手高風險區：巴黎、布魯塞爾、阿姆斯特丹。手機不要放外套口袋或桌面。"),
    ("廁所", "車站與景點公廁常需 0.5€ 到 1€，先備零錢。"),
    ("緊急", "法比荷通用緊急電話為 112。"),
]

COMMON_TIPS = [
    "護照影本與保單拍照存在手機，原件放內層拉鍊袋。",
    "歐洲春季日夜溫差大，洋蔥式穿法最實用。",
    "自來水普遍可飲用，但景點區可先買一瓶水隨身補充。",
    "退稅購物請保留護照、收據與退稅單，最後一站機場一次處理最省事。",
]

DAYS = [
    {
        "day": "D1",
        "title": "台北 → 巴黎",
        "tag": "飛行日",
        "highlights": ["桃園機場集合", "長榮 BR087 直飛巴黎", "夜宿機上"],
        "watchouts": [
            "飛行時間約 14 小時，建議穿鬆身衣物與壓力襪。",
            "入睡前先把隔天要用的牙刷、充電線、護唇膏放外層袋。",
            "抵達前機上早餐盡量吃，第一天通常步行量很大。",
        ],
        "boost": [
            "巴黎入境安檢與行李提領有時會排較久，手機先下載離線地圖。",
            "若你容易時差頭痛，機上就開始補水，咖啡和酒精不要喝太多。",
        ],
    },
    {
        "day": "D2",
        "title": "巴黎",
        "tag": "蒙馬特・塞納河・羅浮宮",
        "highlights": [
            "蒙馬特、聖心堂、畫家村、愛之牆",
            "塞納河遊船",
            "羅浮宮中文導覽",
        ],
        "watchouts": [
            "蒙馬特階梯多、坡度陡，鞋底止滑比好看重要。",
            "聖心堂周邊常見手環黨與連署搭訕，直接無視即可。",
            "塞納河遊船拍照時先綁好手機掛繩，靠欄杆拍照不要單手伸太出去。",
            "羅浮宮熱門作品區很擠，大包包不方便，能輕裝就輕裝。",
        ],
        "boost": [
            "羅浮宮官網仍公告週二休館，若行程有變動要先核對預約時段。",
            "先看《勝利女神》和《米羅的維納斯》，最後再回《蒙娜麗莎》，體感會順很多。",
            "蒙馬特與塞納河畔風偏大，薄圍巾或輕外套很有用。",
        ],
    },
    {
        "day": "D3",
        "title": "巴黎",
        "tag": "鐵塔・凱旋門・香榭麗舍",
        "highlights": [
            "艾菲爾鐵塔、凱旋門、協和廣場",
            "香榭麗舍大道、老佛爺百貨",
            "晚餐自理",
        ],
        "watchouts": [
            "艾菲爾鐵塔周邊小販很多，不要買來路不明的鐵塔模型。",
            "凱旋門必走地下道，不要直接穿越圓環。",
            "老佛爺退稅要帶護照，精品樓層與手扶梯周邊都是扒手熱區。",
        ],
        "boost": [
            "老佛爺頂樓露台免費，可補一張巴黎城市景。",
            "香榭麗舍的大型連鎖店通常可刷卡，但麵包甜點小店仍建議保留零錢。",
        ],
        "meal": {
            "city": "巴黎晚餐推薦",
            "note": "以步行可達、觀光客友善、價格相對穩定為主。",
            "restaurants": [
                {
                    "name": "Bouillon Chartier Grands Boulevards",
                    "price": "約 15€–25€",
                    "address": "7 Rue du Faubourg Montmartre, 75009 Paris",
                    "why": "巴黎經典高 CP 法式小酒館，翻桌快、份量穩。",
                    "source_label": "官方頁面",
                    "source_url": "https://www.bouillon-chartier.com/en/grands-boulevards/",
                    "dishes": [
                        ("Soupe a l'oignon gratinee", "French onion soup", "法式焗烤洋蔥湯"),
                        ("Steak-frites", "Steak and fries", "牛排薯條"),
                        ("Oeuf mayonnaise", "Egg with mayonnaise", "法式蛋佐美乃滋"),
                    ],
                },
                {
                    "name": "Bouillon Pigalle",
                    "price": "約 18€–30€",
                    "address": "22 Boulevard de Clichy, 75018 Paris",
                    "why": "如果你想吃到更完整的經典法國家常菜，這家也很穩。",
                    "source_label": "官方頁面",
                    "source_url": "https://www.bouillonlesite.com/en/bouillon-pigalle",
                    "dishes": [
                        ("Boeuf bourguignon", "Beef bourguignon", "紅酒燉牛肉"),
                        ("Confit de canard", "Duck confit", "油封鴨腿"),
                        ("Profiteroles", "Cream puffs with chocolate sauce", "巧克力泡芙"),
                    ],
                },
                {
                    "name": "Five Guys Champs-Elysees",
                    "price": "約 12€–20€",
                    "address": "49-51 Avenue des Champs-Elysees, 75008 Paris",
                    "why": "若當天已經走很多景點、只想快速補熱量，這是最穩定選項。",
                    "source_label": "官方門市",
                    "source_url": "https://restaurants.fiveguys.com/en_us/49-51-avenue-des-champs-elysees",
                    "dishes": [
                        ("Cheeseburger", "Cheeseburger", "起司漢堡"),
                        ("Little Bacon Cheeseburger", "Little Bacon Cheeseburger", "小份培根起司漢堡"),
                        ("Cajun Fries", "Cajun fries", "卡真香料薯條"),
                    ],
                },
            ],
        },
    },
    {
        "day": "D4",
        "title": "巴黎 → 布魯日",
        "tag": "古城散步日",
        "highlights": [
            "布魯日古城、愛之湖、貝居安會院",
            "市集廣場、布魯日鐘樓",
        ],
        "watchouts": [
            "石板路多而且下雨會滑，行李與推車都會比平地吃力。",
            "愛之湖天鵝很近，但不要餵食或靠太近拍照。",
            "布魯日鐘樓上塔共 366 階，若前一天已走很多可視體力保留。",
        ],
        "boost": [
            "古城區餐廳觀光價差明顯，若只是想補飲料和零食，超市會划算很多。",
            "日落前的市集廣場和運河邊最好拍，光線比中午柔和許多。",
        ],
    },
    {
        "day": "D5",
        "title": "布魯塞爾 → 鹿特丹",
        "tag": "布魯塞爾經典地標 + 鹿特丹晚餐",
        "highlights": [
            "黃金大廣場、尿尿小童、原子球塔",
            "方塊屋、Markthal 市場",
            "晚餐自理",
        ],
        "watchouts": [
            "布魯塞爾大廣場和尿尿小童周邊觀光客密度高，背包往前背。",
            "尿尿小童真的不大，拍完就走即可，不用硬卡太久。",
            "方塊屋室內斜角多，容易暈的人不要停太久。",
        ],
        "boost": [
            "Markthal 很適合直接解決晚餐，但熱門攤位傍晚會排隊，先巡一圈再決定。",
            "你原本列的 Burgertrut 已在 2025 年 12 月 24 日停業，這份已替換成目前仍營業的店。",
        ],
        "meal": {
            "city": "鹿特丹晚餐推薦",
            "note": "以當前仍營業、好找、晚餐可實際執行為主。",
            "restaurants": [
                {
                    "name": "Markthal Rotterdam",
                    "price": "約 10€–20€",
                    "address": "Dominee Jan Scharpstraat 298, 3011 GZ Rotterdam",
                    "why": "選擇最多，海鮮、披薩、Tapas、甜點都能一次解決。",
                    "source_label": "官方網站",
                    "source_url": "https://markthal.nl/en/",
                    "dishes": [
                        ("Gambas al ajillo", "Garlic shrimp", "蒜香蝦"),
                        ("Pizza margherita", "Margherita pizza", "瑪格麗特披薩"),
                        ("Croquetas", "Croquettes", "西式炸可樂餅"),
                    ],
                },
                {
                    "name": "Ter Marsch & Co Rotterdam",
                    "price": "約 15€–24€",
                    "address": "Witte de Withstraat 70, 3012 BS Rotterdam",
                    "why": "如果想吃漢堡，這家比原本的 Burgertrut 更穩，且仍營業。",
                    "source_label": "官方網站",
                    "source_url": "https://termarschco.nl/en/",
                    "dishes": [
                        ("Truffle burger", "Truffle burger", "松露漢堡"),
                        ("Cheeseburger", "Cheeseburger", "起司漢堡"),
                        ("Parmesan fries", "Parmesan fries", "帕瑪森起司薯條"),
                    ],
                },
            ],
        },
    },
    {
        "day": "D6",
        "title": "鹿特丹 → 阿姆斯特丹",
        "tag": "鬱金香花園・運河遊船",
        "highlights": [
            "鬱金香花園",
            "運河遊船、鑽石工廠、水壩廣場",
        ],
        "watchouts": [
            "鬱金香花園腹地很大，真的會走很多，先看地圖找你最想拍的區塊。",
            "運河船上體感溫度偏低，就算白天出太陽也建議帶薄外套。",
            "鑽石工廠常會有銷售介紹，喜歡再買即可，不用有壓力。",
        ],
        "boost": [
            "Keukenhof 官網已公布 2026 年開園為 3 月 19 日到 5 月 10 日，若你的出發日落在這段外要再核對實際景點安排。",
            "阿姆斯特丹水壩廣場和中央車站一帶也是扒手熱區，拍照時包包不要放地上。",
        ],
    },
    {
        "day": "D7",
        "title": "阿姆斯特丹 → 羊角村 → 風車村",
        "tag": "鄉村景觀 + 晚餐自理",
        "highlights": [
            "羊角村遊船",
            "風車村、木鞋工廠、起司工廠",
            "晚餐自理",
        ],
        "watchouts": [
            "羊角村木棧道和橋面遇水很滑，拍照不要倒退走。",
            "風車村空曠、風真的很大，帽子與圍巾要固定好。",
            "起司工廠試吃很多，但鹹味較重，記得補水。",
        ],
        "boost": [
            "如果回到阿姆斯特丹已晚，Foodhallen 會比單點餐廳更有彈性。",
            "荷蘭薯條份量通常比想像大，兩人分一份很合理。",
        ],
        "meal": {
            "city": "阿姆斯特丹晚餐推薦",
            "note": "一樣以好找、晚點到也相對容易吃得到為主。",
            "restaurants": [
                {
                    "name": "Foodhallen Amsterdam",
                    "price": "約 10€–20€",
                    "address": "Bellamyplein 51, 1053 AT Amsterdam",
                    "why": "集合多家攤位，最適合團員口味不一致時分流點餐。",
                    "source_label": "官方網站",
                    "source_url": "https://foodhallen.nl/en/venues/amsterdam/",
                    "dishes": [
                        ("Bitterballen", "Dutch beef croquettes", "荷蘭炸肉球"),
                        ("Karaage", "Japanese fried chicken", "日式炸雞"),
                        ("Oysters", "Fresh oysters", "生蠔"),
                    ],
                },
                {
                    "name": "Fabel Friet",
                    "price": "約 6€–9€",
                    "address": "Runstraat 1, 1016 GJ Amsterdam",
                    "why": "如果你只想吃一份很強的薯條，這家是目前最穩的選項之一。",
                    "source_label": "官方網站",
                    "source_url": "https://www.fabelfriet.nl/",
                    "dishes": [
                        ("Verse friet met truffelmayonaise en Parmezaanse kaas", "Fresh fries with truffle mayo and Parmesan", "松露美乃滋帕瑪森薯條"),
                        ("Verse friet met mayonaise", "Fresh fries with mayonnaise", "美乃滋薯條"),
                    ],
                },
                {
                    "name": "The Pancake Bakery",
                    "price": "約 14€–22€",
                    "address": "Prinsengracht 191, 1015 DS Amsterdam",
                    "why": "想吃荷蘭代表性主食甜鹹鬆餅，這家對旅客最友善。",
                    "source_label": "官方網站",
                    "source_url": "https://pancake.nl/en/",
                    "dishes": [
                        ("Pannenkoek met appel en spek", "Dutch pancake with apple and bacon", "蘋果培根荷蘭鬆餅"),
                        ("Pannenkoek met kaas", "Dutch pancake with cheese", "起司荷蘭鬆餅"),
                        ("Poffertjes", "Mini Dutch pancakes", "荷蘭小鬆餅"),
                    ],
                },
            ],
        },
    },
    {
        "day": "D8",
        "title": "返程日",
        "tag": "整理行李・退稅・回台",
        "highlights": ["整理行李", "確認退稅文件", "前往機場返台"],
        "watchouts": [
            "液體、巧克力醬、果醬、抹醬類請優先放托運。",
            "退稅資料請把護照、登機證、收據與商品放在同一袋，臨櫃最省時。",
            "機場安檢前先把行動電源、電子產品與外套整理好。",
        ],
        "boost": [
            "最後一天通常最容易漏東西，離開飯店前檢查保險箱、浴室、床頭與插座。",
            "若買了起司、巧克力與 Stroopwafel，盡量分散裝，避免單袋過重或壓壞。",
        ],
    },
]

SOURCES = [
    ("Louvre official hours", "https://www.louvre.fr/en"),
    ("Keukenhof 2026 season", "https://keukenhof.nl/en/"),
    ("Bouillon Chartier", "https://www.bouillon-chartier.com/en/grands-boulevards/"),
    ("Bouillon Pigalle", "https://www.bouillonlesite.com/en/bouillon-pigalle"),
    ("Five Guys Champs-Elysees", "https://restaurants.fiveguys.com/en_us/49-51-avenue-des-champs-elysees"),
    ("Markthal Rotterdam", "https://markthal.nl/en/"),
    ("Ter Marsch & Co", "https://termarschco.nl/en/"),
    ("Foodhallen Amsterdam", "https://foodhallen.nl/en/venues/amsterdam/"),
    ("Fabel Friet", "https://www.fabelfriet.nl/"),
    ("The Pancake Bakery", "https://pancake.nl/en/"),
]


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def render_list(items: list[str], cls: str = "bullet-list") -> str:
    return f'<ul class="{cls}">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def render_trip_facts() -> str:
    parts = []
    for label, text in TRIP_FACTS:
        parts.append(
            f"""
            <article class="fact-card">
              <div class="fact-label">{esc(label)}</div>
              <p>{esc(text)}</p>
            </article>
            """
        )
    return "".join(parts)


def render_restaurants(restaurants: list[dict[str, object]]) -> str:
    cards = []
    for restaurant in restaurants:
        dishes = restaurant["dishes"]
        dish_html = "".join(
            f"""
            <li>
              <strong>{esc(local)}</strong>
              <span>{esc(english)} / {esc(chinese)}</span>
            </li>
            """
            for local, english, chinese in dishes
        )
        cards.append(
            f"""
            <article class="meal-card">
              <div class="meal-top">
                <h4>{esc(restaurant["name"])}</h4>
                <div class="price-pill">{esc(restaurant["price"])}</div>
              </div>
              <p class="meal-why">{esc(restaurant["why"])}</p>
              <p class="meal-meta">{esc(restaurant["address"])}</p>
              <ul class="dish-list">{dish_html}</ul>
              <p class="source-link"><a href="{esc(restaurant["source_url"])}">{esc(restaurant["source_label"])}</a></p>
            </article>
            """
        )
    return "".join(cards)


def render_day(day: dict[str, object]) -> str:
    meal = day.get("meal")
    meal_html = ""
    if meal:
        meal_html = f"""
        <section class="meal-section">
          <div class="section-head">
            <h3>{esc(meal["city"])}</h3>
            <p>{esc(meal["note"])}</p>
          </div>
          <div class="meal-grid">
            {render_restaurants(meal["restaurants"])}
          </div>
        </section>
        """

    return f"""
    <section class="day-card">
      <div class="day-head">
        <div class="day-pill">{esc(day["day"])}</div>
        <div>
          <h2>{esc(day["title"])}</h2>
          <p class="day-tag">{esc(day["tag"])}</p>
        </div>
      </div>

      <div class="info-block">
        <h3>今日重點</h3>
        {render_list(day["highlights"])}
      </div>

      <div class="info-grid">
        <article class="info-block">
          <h3>注意事項</h3>
          {render_list(day["watchouts"])}
        </article>
        <article class="info-block accent">
          <h3>補強資訊</h3>
          {render_list(day["boost"])}
        </article>
      </div>

      {meal_html}
    </section>
    """


def build_html() -> str:
    day_sections = "".join(render_day(day) for day in DAYS)
    tips_html = render_list(COMMON_TIPS, cls="tips-list")
    sources_html = "".join(
        f'<li><a href="{esc(url)}">{esc(label)}</a></li>' for label, url in SOURCES
    )

    return dedent(
        f"""\
        <!DOCTYPE html>
        <html lang="zh-Hant">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{esc(PAGE_TITLE)}</title>
          <style>
            :root {{
              --bg: #f4efe6;
              --paper: rgba(255, 252, 247, 0.96);
              --card: #fffdfa;
              --ink: #1f2220;
              --muted: #5b635b;
              --line: #dfd2bf;
              --accent: #c45b33;
              --accent-soft: #f6e4d8;
              --olive: #7c8c52;
              --olive-soft: #eef1df;
              --shadow: 0 16px 40px rgba(88, 72, 46, 0.08);
            }}
            * {{
              box-sizing: border-box;
            }}
            html {{
              scroll-behavior: smooth;
            }}
            body {{
              margin: 0;
              color: var(--ink);
              font-family: "Segoe UI", "Noto Sans TC", "Microsoft JhengHei", sans-serif;
              background:
                radial-gradient(circle at top left, rgba(230, 197, 169, 0.55), transparent 28%),
                radial-gradient(circle at top right, rgba(196, 91, 51, 0.12), transparent 24%),
                linear-gradient(180deg, #f6f1e8 0%, #efe7da 100%);
            }}
            a {{
              color: #9c4525;
              text-decoration: none;
            }}
            .page {{
              max-width: 760px;
              margin: 0 auto;
              padding: 16px 12px 48px;
            }}
            .hero {{
              position: relative;
              overflow: hidden;
              padding: 22px 18px;
              border-radius: 28px;
              background:
                linear-gradient(135deg, rgba(255, 247, 238, 0.98), rgba(251, 246, 238, 0.95)),
                var(--paper);
              border: 1px solid rgba(196, 91, 51, 0.16);
              box-shadow: var(--shadow);
            }}
            .hero::after {{
              content: "";
              position: absolute;
              inset: auto -40px -56px auto;
              width: 180px;
              height: 180px;
              background: radial-gradient(circle, rgba(196, 91, 51, 0.18) 0%, rgba(196, 91, 51, 0) 72%);
              pointer-events: none;
            }}
            .eyebrow {{
              display: inline-flex;
              padding: 6px 10px;
              border-radius: 999px;
              background: var(--accent-soft);
              color: var(--accent);
              font-size: 12px;
              font-weight: 800;
              letter-spacing: 0.06em;
            }}
            h1 {{
              margin: 10px 0 8px;
              font-size: 32px;
              line-height: 1.12;
            }}
            .subtitle {{
              margin: 0;
              color: var(--muted);
              line-height: 1.7;
              font-size: 15px;
            }}
            .fact-grid {{
              display: grid;
              grid-template-columns: 1fr 1fr;
              gap: 10px;
              margin-top: 16px;
            }}
            .fact-card {{
              padding: 14px 14px 12px;
              border-radius: 20px;
              background: var(--card);
              border: 1px solid var(--line);
            }}
            .fact-label {{
              margin-bottom: 6px;
              color: var(--accent);
              font-size: 13px;
              font-weight: 800;
            }}
            .fact-card p,
            .day-tag,
            .meal-why,
            .meal-meta,
            .section-head p,
            .footer p {{
              margin: 0;
              color: var(--muted);
              line-height: 1.65;
            }}
            .tips-card,
            .day-card,
            .footer {{
              margin-top: 14px;
              padding: 18px 16px;
              border-radius: 24px;
              background: var(--paper);
              border: 1px solid rgba(91, 99, 91, 0.11);
              box-shadow: var(--shadow);
            }}
            .tips-card h2,
            .day-card h2,
            .footer h2 {{
              margin: 0;
            }}
            .tips-list,
            .bullet-list,
            .dish-list,
            .sources {{
              margin: 10px 0 0;
              padding-left: 18px;
            }}
            .tips-list li,
            .bullet-list li,
            .dish-list li,
            .sources li {{
              margin-bottom: 8px;
              line-height: 1.6;
            }}
            .day-head {{
              display: grid;
              grid-template-columns: auto 1fr;
              gap: 12px;
              align-items: start;
            }}
            .day-pill {{
              min-width: 52px;
              padding: 10px 0;
              border-radius: 16px;
              background: var(--olive);
              color: #fff;
              font-weight: 800;
              text-align: center;
            }}
            .day-tag {{
              margin-top: 4px;
              font-size: 14px;
            }}
            .info-grid {{
              display: grid;
              grid-template-columns: 1fr;
              gap: 12px;
              margin-top: 12px;
            }}
            .info-block {{
              margin-top: 14px;
              padding: 14px;
              border-radius: 20px;
              background: var(--card);
              border: 1px solid var(--line);
            }}
            .info-block.accent {{
              background: linear-gradient(180deg, #fbf8f1 0%, var(--olive-soft) 100%);
            }}
            .info-block h3,
            .meal-section h3,
            .meal-card h4 {{
              margin: 0;
            }}
            .meal-section {{
              margin-top: 16px;
              padding-top: 2px;
            }}
            .section-head {{
              margin-bottom: 10px;
            }}
            .section-head h3 {{
              margin-bottom: 4px;
            }}
            .meal-grid {{
              display: grid;
              grid-template-columns: 1fr;
              gap: 12px;
            }}
            .meal-card {{
              padding: 14px;
              border-radius: 20px;
              background: linear-gradient(180deg, #fff 0%, #fff8f2 100%);
              border: 1px solid var(--line);
            }}
            .meal-top {{
              display: flex;
              justify-content: space-between;
              gap: 10px;
              align-items: start;
            }}
            .price-pill {{
              flex: 0 0 auto;
              padding: 6px 10px;
              border-radius: 999px;
              background: var(--accent-soft);
              color: var(--accent);
              font-size: 12px;
              font-weight: 800;
            }}
            .meal-why {{
              margin-top: 8px;
            }}
            .meal-meta {{
              margin-top: 6px;
              font-size: 13px;
            }}
            .dish-list strong {{
              display: block;
              font-size: 14px;
            }}
            .dish-list span {{
              display: block;
              font-size: 13px;
              color: var(--muted);
            }}
            .source-link {{
              margin: 12px 0 0;
              font-size: 13px;
              font-weight: 700;
            }}
            .footer {{
              margin-bottom: 20px;
            }}
            .footer p {{
              margin-top: 8px;
              font-size: 14px;
            }}
            .sources li {{
              font-size: 13px;
              word-break: break-all;
            }}
            @media (min-width: 700px) {{
              .fact-grid {{
                grid-template-columns: repeat(3, 1fr);
              }}
              .info-grid {{
                grid-template-columns: 1fr 1fr;
              }}
              .meal-grid {{
                grid-template-columns: 1fr 1fr;
              }}
            }}
            @media print {{
              body {{
                background: #fff;
              }}
              .page {{
                max-width: none;
                padding: 9mm 8mm 12mm;
              }}
              .hero,
              .tips-card,
              .day-card,
              .footer {{
                box-shadow: none;
              }}
              .day-card,
              .meal-card,
              .info-block,
              .fact-card {{
                break-inside: avoid;
              }}
            }}
          </style>
        </head>
        <body>
          <main class="page">
            <section class="hero">
              <div class="eyebrow">MOBILE FRIENDLY PDF</div>
              <h1>{esc(PAGE_TITLE)}</h1>
              <p class="subtitle">把每天的重點、風險、自理餐與臨場會用到的補強資訊整理成手機單欄閱讀版本。餐廳招牌菜已盡量補上當地語言、英文與中文，方便你直接點餐。</p>
              <div class="fact-grid">
                {render_trip_facts()}
              </div>
            </section>

            <section class="tips-card">
              <h2>整趟最重要的提醒</h2>
              {tips_html}
            </section>

            {day_sections}

            <section class="footer">
              <h2>資料來源與補充說明</h2>
              <p>本頁以你提供的團體行程為主軸整理，並補查官方網站上的景點與餐廳資訊。餐點名稱以官方菜單、官方店家描述或餐廳代表性品項為主，實際供應仍以現場為準。</p>
              <ul class="sources">{sources_html}</ul>
            </section>
          </main>
        </body>
        </html>
        """
    )


def write_outputs() -> None:
    OUTPUT_HTML.write_text(build_html(), encoding="utf-8")


def find_browser() -> Path | None:
    for candidate in BROWSER_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def print_pdf(browser: Path) -> None:
    if OUTPUT_PDF.exists():
        OUTPUT_PDF.unlink()
    command = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-first-run",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=12000",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={OUTPUT_PDF}",
        OUTPUT_HTML.resolve().as_uri(),
    ]
    subprocess.run(command, check=True, timeout=60)


def main() -> None:
    write_outputs()
    browser = find_browser()
    if browser is None:
      raise SystemExit("No supported browser found for PDF export.")
    print_pdf(browser)
    print(f"Wrote {OUTPUT_HTML}")
    print(f"Wrote {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
