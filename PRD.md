# 巴哈姆特動畫瘋評分 Dashboard - PRD

**目標**: 給 Claude Code 實現  
**更新**: 2025-12-03 (UI Redesign)

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

### 3.1 過濾與排序佈局 (Top Filter Layout)

**整體佈局**: 
- **上方 (Header Area)**: 放置所有過濾器、排序器、權重設定。
- **下方**: 動畫卡片 Grid。
- **無導航欄 (No Navbar)**: 頂部直接是功能區。

#### 上方控制區模塊:

1.  **搜尋模塊**
    *   全文搜尋 (中文/日文)
    *   行為: 搜尋時清空其他過濾條件

2.  **年份選擇 (Year Filter)**
    *   **UI**: 單選按鈕組 (Single-select Chips/Buttons)，**不要**下拉選單。
    *   **選項**: 全部 | 2025 | 2024 | 2023 | ... | 2010s | 2000s | 19xx

3.  **類型過濾 (Genre Filter)**
    *   UI: 多選 Chips
    *   邏輯: OR

4.  **最低評分人數 (Min Votes)**
    *   UI: 滑桿 (Slider)
    *   **最左邊 (0)**: 代表 "關閉" (Off)，不進行過濾。

5.  **綜合評分權重 (Weight Config)**
    *   UI: 獨立區塊，預設摺疊或彈出。
    *   邏輯: 4 個滑桿 (巴哈/IMDb/豆瓣/MAL)。
    *   **連動邏輯**: 拉高一個滑桿時，其他滑桿需相對降低，強制總和維持 100%。

6.  **排序方式 (Sorting)**
    *   UI: 獨立、顯眼的控制項 (Prominent Control)。
    *   **樣式**: **拿掉 emoji**，純文字標籤。
    *   **選項**: 綜合評分 (Radar Score) | 巴哈姆特 | IMDb | 豆瓣 | MAL

### 3.2 排序邏輯

**UI 語言**: 繁體中文

**排序規則**:
1.  **缺失評分處理**: 沒有該平台評分的動畫排在**最後**。
2.  **次級排序**: 巴哈評分 (當主排序分數相同時)。
3.  **綜合評分**: 根據用戶設定權重動態計算。

### 3.3 綜合評分計算

**公式**:
1.  標準化到 0-10 (巴哈 x2)。
2.  加權平均 (Sum(Score * Weight) / Sum(Weights of available sources))。

---

## 4. UI 視覺風格 (Creamy Aesthetic)

**風格關鍵字**: Cream (奶油色), Soft Shadows (柔和陰影), Rounded (圓角), Apricot (杏色點綴).
**參考**: `app/globals.css` 中的變數定義。

### 4.1 動畫卡片 (Anime Card)

**顯示內容**:
1.  **縮圖**: 高質量圖片。
2.  **綜合評分 (Radar Score)**: 顯眼展示 (例如浮動 Badge)。
3.  **標題**: 中文標題 + 日文原名 (小字)。
4.  **標籤**: 年份、集數、類型 (前2個)。
5.  **所有評分展示**:
    *   巴哈姆特 (分 + 人數)
    *   IMDb
    *   豆瓣
    *   MAL
    *   *註: 有分數才顯示，沒分數不顯示*
6.  **觀看按鈕**: 跳轉巴哈。

**排版**:
- 避免太擠，重新設計間距。
- 確保所有資訊清晰可見。

---

## 5. 爬蟲與數據工程 (已完成 Phase 1 & 2)

*參照原 PRD，此部分無變更*

---

## 6. 用戶流程

1.  進入頁面，頂部看到年份、類型、排序選項。
2.  點選 "2024"，列表即時更新。
3.  調整排序為 "IMDb"，列表重新排列。
4.  點開 "權重設定"，拉高 "巴哈" 權重，其他自動降低，列表順序改變。
5.  看到感興趣的動畫，卡片上看到四個平台分數都很高。
6.  點擊 "Watch on Bahamut"。

---

## 7. 成功標準

-   UI 符合 Creamy 風格，美觀且不擁擠。
-   Top Filter 佈局操作順手。
-   權重連動邏輯正確 (總和 100%)。
-   所有評分數據在卡片上正確顯示。
