# 巴哈姆特動畫瘋評分 Dashboard - PRD

**目標**: 給 Claude Code 實現  
**更新**: 2025-12-02

---

## 1. 產品定義

### 做什麼
一個個人使用的巴哈姆特動畫瘋動畫評分 Dashboard，上面有所有巴哈姆特動畫瘋動畫上架的作品，整合巴哈姆特、IMDb、豆瓣、MyAnimeList 四個平台的評分數據，提供多維度過濾和排序，幫助快速找到值得看的動畫，並且讓用戶可以迅速點及連結到動畫瘋觀看。

### 不做什麼
- ❌ 播放功能
- ❌ 社交/評論
- ❌ 用戶帳號
- ❌ 推薦算法
- ❌ 歷史評分追蹤
- ❌ 地區過濾（基本都是日本）

---

## 2. 數據結構

### 存儲格式
使用 JSON 文件：`/data/animes.json`

### 數據來源
- **主要**: 巴哈姆特動畫瘋（動畫信息 + 評分）
- **次要**: IMDb / 豆瓣 / MyAnimeList（跨平台評分）

### 必需字段
```javascript
{
  id: string,                    // 唯一識別
  title: string,                 // 中文標題
  thumbnail: string,             // 縮圖 URL
  year: number,                  // 播出年份
  genres: string[],              // 類型（多個）
  episodes: number,              // 集數
  bahamutUrl: string,            // 觀看連結
  
  ratings: {
    bahamut: { score: number, votes: number },      // 1-5 分制
    imdb: { score: number, votes: number },         // 0-10，可選
    douban: { score: number, votes: number },       // 0-10，可選
    myanimelist: { score: number, members: number } // 0-10，可選
  },
  
  popularity: number             // 觀看人數
}
```

### 可選字段
- `titleOriginal`: 日文原標題
- `tags`: 特殊標籤（**僅使用巴哈原始標籤**）

---

## 3. 核心業務邏輯

### 3.1 過濾邏輯

**主要使用場景**: 先按年份+類型篩選，再看不同排序結果

#### 過濾條件

1. **類型過濾（多選）**
   - 邏輯: OR（選 Action + Comedy = 找有 Action 或 Comedy 的）
   - 空選 = 全選

2. **年份過濾（預設選項）**
   - **介面語言**: 繁體中文
   - **選項**:
     - 所有時間
     - 2025
     - 2024
     - 2023
     - 2022
     - 2021
     - 2020
     - 2010-2019
     - 2000-2009
     - 1980-1999

3. **評分人數過濾（可選）**
   - 隱藏評分人數太少的動畫
   - 例: 只顯示巴哈評分人數 >= 100 的

4. **全文搜尋**
   - 搜尋動畫標題（中文 + 日文原標題）
   - **重要**: 搜尋時清空其他過濾條件，只顯示搜尋結果

### 3.2 排序邏輯

**UI 語言**: 必須使用**繁體中文**顯示所有選項和標籤。


**排序選項**（按優先級）:
1. 巴哈評分最高
2. IMDb 評分最高
3. 豆瓣評分最高
4. MyAnimeList 評分最高
5. 綜合評分最高（用戶可自定義加權）

**缺失評分處理**:
- 沒有該平台評分的動畫 → 排在最後
- 最後再按巴哈評分次級排序

**範例**: 按 IMDb 排序
```
1. IMDb 8.5 (巴哈 4.8)
2. IMDb 8.3 (巴哈 4.7)
3. IMDb 8.3 (巴哈 4.5)  ← 同 IMDb 分數，巴哈高的在前
---
100. 無 IMDb (巴哈 4.9)  ← 無 IMDb 評分，放最後
101. 無 IMDb (巴哈 4.2)
```

### 3.3 綜合評分計算

**用戶可自定義加權參數**:
- 巴哈權重: 0-100%
- IMDb 權重: 0-100%
- 豆瓣權重: 0-100%
- MAL 權重: 0-100%
- 總和需 = 100%

**計算公式**:
1. 先標準化到 0-10（巴哈 1-5 → 乘 2）
2. 加權平均（只計算有評分的平台）

**範例**:
```
設定權重: 巴哈 40% / IMDb 30% / 豆瓣 20% / MAL 10%

某動畫:
- 巴哈 4.5 → 標準化 9.0
- IMDb 8.5
- 豆瓣 無
- MAL 8.0

綜合評分 = (9.0 × 0.4 + 8.5 × 0.3 + 8.0 × 0.1) / (0.4 + 0.3 + 0.1)
         = (3.6 + 2.55 + 0.8) / 0.8
         = 8.69
```

**預設權重**: 25% / 25% / 25% / 25%（平均）

---

## 4. UI 交互邏輯

### 4.1 卡片顯示

**動畫卡片包含**:
- 縮圖
- 標題
- 年份 · 類型 · 集數
- **4 個評分並排顯示**:
  ```
  ⭐ 4.8 (1.2K)    ← 巴哈
  🎬 8.5 (5K)      ← IMDb
  🎭 8.7 (3K)      ← 豆瓣
  📺 8.6 (10K)     ← MAL
  ```
- 「觀看」按鈕 → 跳轉巴哈動畫瘋

**評分顯示規則**:
- 有評分: 顯示分數 + 評分人數
- 無評分: **隱藏該欄位**（不顯示「無評分」）

**Grid 佈局**:
- Desktop: 4 列
- Tablet: 3 列
- Mobile: 2 列

### 4.2 過濾器（側邊欄）

**固定在左側，包含**:
1. 搜尋框（全文搜尋）
2. 類型多選（15 種巴哈類型）
3. 年份選擇
4. 評分人數最低門檻（滑桿）
5. 排序下拉選單
6. 綜合評分加權設定（摺疊面板）

**即時過濾**: 選擇後立即更新結果（無需點擊「搜尋」按鈕）

**顯示結果數**: 「找到 87 部動畫」

### 4.3 搜尋行為

**觸發搜尋時**:
1. 清空所有過濾條件（類型、年份、評分門檻）
2. 只顯示標題匹配的動畫
3. 保留排序設定

**清空搜尋時**:
1. 恢復之前的過濾條件
2. 或直接顯示全部動畫

### 4.4 綜合評分設定

**UI 元素**:
- 4 個滑桿（巴哈 / IMDb / 豆瓣 / MAL）
- 即時顯示總和（需 = 100%）
- 「重置為預設」按鈕

**互動邏輯**:
- 調整任一滑桿 → 自動重新計算所有動畫的綜合評分
- 切換到「綜合評分排序」時才生效

---

## 5. 爬蟲數據規格

### 5.1 巴哈姆特動畫瘋

**爬取目標**:
- 所有上架動畫（預估 ~1800 部）
- 數據更新頻率: 每兩週

**必需字段**:
- 標題、縮圖、年份、類型、集數
- 巴哈評分 + 評分人數
- 觀看人數
- 動畫連結

**類型標籤**（15 種）:
```
奇幻冒險、科幻未來、青春校園、幽默搞笑、戀愛、
溫馨、靈異神怪、推理懸疑、料理美食、社會寫實、
運動競技、歷史傳記、其他、電影版、OVA
```

**特殊標籤**（如果巴哈原始有）:
- 改編自漫畫
- 改編自輕小說
- 改編自遊戲
- 其他巴哈原生標籤

### 5.2 跨平台評分

**來源**: 第三方 API / 網頁爬取

**必需字段**:
- IMDb: score (0-10), votes (使用 Suggestion API 查找 ID + JSON-LD 抓取評分)
- 豆瓣: score (0-10), votes  
- MyAnimeList: score (0-10), members

---

## 6. 數據工程架構（重點！）

### 6.1 數據對齊策略（Data Mapping Pipeline）

**核心問題**: 
- 巴哈用中文標題「葬送的芙莉蓮」
- MAL 用英文/羅馬拼音「Sousou no Frieren」
- IMDb 用英文「Frieren: Beyond Journey's End」
- 豆瓣用中文「葬送的芙莉蓮」

**❌ 錯誤做法**: 直接用中文標題去搜 IMDb API（根本搜不到）

**✅ 正確流程**: 使用「日文原名」作為橋樑

```
Step 1: 爬巴哈姆特
├─ 抓取字段: 中文標題、日文原名、年份、巴哈評分
└─ 關鍵: 必須抓「日文原名」(例: 葬送のフリーレン)

Step 2: 用日文原名查 MyAnimeList
├─ MAL API: 搜尋日文原名 → 拿到 MAL ID
├─ MAL 頁面通常有 IMDb ID (在 External Links)
└─ 拿到: MAL評分 + IMDb ID

Step 3: 獲取 IMDb 評分
├─ 優先: 使用 MAL 提供的 IMDb ID
├─ 備案: 若 MAL 無 ID，使用 IMDb Suggestion API 搜尋 (用日文原名或 MAL 英文名)
└─ 拿到: IMDb評分 (解析頁面 JSON-LD)

Step 4: 豆瓣匹配（最難）
├─ 方案A: 用中文標題 + 年份搜豆瓣 (準確率 ~60%)
├─ 方案B: 用 IMDb ID 反查豆瓣 (需要第三方 API)
└─ 拿到: 豆瓣評分 (能拿到就拿，拿不到留空)
```

**實施重點**:
1. 巴哈頁面必須能抓到「日文原名」
2. MAL 搜尋 API 用日文原名去查
3. 豆瓣最難對齊，不強求 100% 覆蓋率（70% 就很好）

### 6.2 爬蟲實施細節

#### Rate Limiting（限速）
```python
# 巴哈姆特
每抓一頁休息 2-3 秒
建議: time.sleep(random.uniform(2, 4))

# MAL API
官方限制: 每秒 1 次請求
建議: 每次 API 呼叫後 sleep(1.5)

# 豆瓣
反爬最嚴格，每次請求後 sleep(5)
或者用第三方 API 避開反爬
```

#### Error Handling（容錯機制）
```python
# 原則: 抓不到不要 Crash，留空繼續跑

try:
    anime_data = scrape_bahamut_page(url)
except Exception as e:
    print(f"抓取失敗: {url}, 錯誤: {e}")
    continue  # 跳過這部，繼續下一部
    
# 對於跨平台評分
if mal_id:
    try:
        mal_rating = fetch_mal_rating(mal_id)
    except:
        mal_rating = None  # 抓不到留空
```

#### User-Agent 輪換
```python
# 避免被識別為爬蟲
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
    # 準備 5-10 個
]

headers = {
    'User-Agent': random.choice(USER_AGENTS)
}
```

### 6.3 資料更新策略（Pipeline）

**推薦方案: Flat Data 模式**

```
專案結構:
├── /crawler
│   ├── bahamut_scraper.py     # 爬巴哈
│   ├── cross_platform.py      # 跨平台對齊
│   └── generate_json.py       # 生成 JSON
├── /data
│   └── animes.json            # 靜態資料
└── /app (Next.js)
```

**運行方式**:

**Phase 1: 初始爬取（手動）**
```bash
# 本地運行 Python Script
cd crawler
python bahamut_scraper.py      # 爬巴哈 ~1800 部
python cross_platform.py       # 對齊跨平台評分
python generate_json.py        # 生成 animes.json

# 預計耗時: 1-2 小時
# 產出: data/animes.json (~2MB)
```

**Phase 2: 定期更新（兩週一次）**

**方案A: 手動更新（簡單）**
```bash
# 每兩週手動跑一次
python update_latest.py   # 只爬最新動畫
git add data/animes.json
git commit -m "Update anime data"
git push
```

**方案B: GitHub Actions 自動化（進階）**
```yaml
# .github/workflows/update-data.yml
name: Update Anime Data
on:
  schedule:
    - cron: '0 0 */14 * *'  # 每兩週運行
  workflow_dispatch:         # 手動觸發

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python crawler/update_latest.py
      - run: |
          git config user.name github-actions
          git add data/animes.json
          git commit -m "Auto-update anime data"
          git push
```

**推薦**: 先用方案A（手動），穩定後再考慮方案B

### 6.4 數據品質控制

**必需檢查**:
```python
# 生成 JSON 後的驗證
def validate_data(animes):
    print(f"總動畫數: {len(animes)}")
    
    # 檢查必需字段
    missing_title = [a for a in animes if not a.get('title')]
    print(f"缺少標題: {len(missing_title)}")
    
    # 檢查評分覆蓋率
    has_imdb = sum(1 for a in animes if a['ratings'].get('imdb'))
    has_douban = sum(1 for a in animes if a['ratings'].get('douban'))
    has_mal = sum(1 for a in animes if a['ratings'].get('myanimelist'))
    
    print(f"IMDb 覆蓋率: {has_imdb / len(animes) * 100:.1f}%")
    print(f"豆瓣覆蓋率: {has_douban / len(animes) * 100:.1f}%")
    print(f"MAL 覆蓋率: {has_mal / len(animes) * 100:.1f}%")
    
    # 目標: 總數 >= 1500, 跨平台覆蓋 >= 70%
```

### 6.5 實施建議

**給 Claude Code 的指示**:

1. **先寫驗證 Script**: 
   - 只爬 10 部動畫測試整個 Pipeline
   - 確保日文原名 → MAL → IMDb 的路通了
   - 再開始大量爬取

2. **分階段實施**:
   ```
   Week 1: 只爬巴哈 + 存 CSV
   Week 2: 加上 MAL 對齊
   Week 3: 加上 IMDb/豆瓣
   Week 4: 生成最終 JSON + 前端整合
   ```

3. **容忍不完美**:
   - 跨平台覆蓋率 70% 就算成功
   - 豆瓣最難對齊，能拿到 50% 就很好
   - 不要為了 100% 卡住整個專案

4. **備用方案**:
   - 如果自動對齊失敗率太高 (>30%)
   - 可以手動補充熱門動畫的 ID mapping
   - 建立一個 `manual_mapping.json`:
   ```json
   {
     "143722": {  // 巴哈 ID
       "mal_id": "39535",
       "imdb_id": "tt13146488",
       "douban_id": "34895145"
     }
   }
   ```

---

## 7. 邊界情況處理

### 7.1 評分缺失

**情境**: 動畫沒有 IMDb/豆瓣/MAL 評分

**處理**:
- 卡片顯示: 隱藏該評分欄位
- 排序: 放在最後 + 巴哈次級排序
- 綜合評分: 只用有評分的平台計算

### 7.2 評分人數過少

**情境**: 巴哈評分只有 10 人

**處理**:
- 預設顯示所有動畫
- 提供「最低評分人數」過濾選項
- 建議預設值: >= 50 人

### 7.3 搜尋無結果

**情境**: 搜尋「XXX」找不到

**處理**:
- 顯示「找不到符合的動畫」
- 提供「清空搜尋」按鈕
- 建議相似標題（可選）

### 7.4 綜合評分權重不合法

**情境**: 4 個權重加起來 ≠ 100%

**處理**:
- 即時提示「總和需為 100%」
- 禁用「套用」按鈕
- 或自動調整其他權重（進階）

### 7.5 數據對齊失敗

**情境**: 某部動畫抓不到 MAL/IMDb/豆瓣

**處理**:
- 只顯示巴哈評分（其他留空）
- 不影響動畫顯示
- Log 記錄失敗的動畫以便後續手動補充

---

## 8. 用戶流程

### 主要使用場景 1: 找最新高分動畫
```
1. 進入 Dashboard
2. 選擇年份: 2024
3. 選擇類型: 奇幻冒險
4. 排序: 巴哈評分最高
→ 看到 2024 年奇幻冒險動畫按巴哈評分排序
```

### 主要使用場景 2: 比較不同平台評價
```
1. 已選年份 2023 + 類型科幻
2. 切換排序:
   - 巴哈評分最高 → 看結果
   - IMDb 評分最高 → 看結果
   - 豆瓣評分最高 → 看結果
→ 觀察同一批動畫在不同平台的排名差異
```

### 主要使用場景 3: 自定義綜合評分
```
1. 打開「綜合評分設定」
2. 調整權重:
   - 巴哈 50%（更信任台灣評分）
   - IMDb 30%
   - 豆瓣 10%
   - MAL 10%
3. 排序: 綜合評分最高
→ 看到按我的偏好計算的排名
```

### 次要使用場景: 搜尋特定動畫
```
1. 搜尋框輸入「進擊的巨人」
2. 其他過濾條件清空
3. 看到所有標題包含「進擊的巨人」的動畫
4. 點擊「觀看」→ 跳轉巴哈
```

---

## 9. 設計參考

**awwrated.com**
- 側邊欄固定過濾器
- 卡片式佈局
- 即時過濾（無需點擊按鈕）
- 簡潔乾淨的 UI

**不要複製的部分**:
- 社交功能
- 評論區
- 用戶帳號

---

## 10. 成功標準

### 功能完整性
- ✅ 初始數據量 >= 1500 部動畫
- ✅ 跨平台評分覆蓋率 >= 70%
- ✅ 過濾響應時間 < 1 秒

### 使用體驗
- ✅ 從進入網站到找到目標動畫 < 30 秒
- ✅ 過濾器直覺易用（無需說明）
- ✅ 評分顯示清晰（一眼看懂）

---

## END

**給 Claude Code 的話**: 
- 技術實現自己決定
- 重點是把上面的商業邏輯和交互規則做對
- 有疑問的話再問我