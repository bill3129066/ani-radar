# Ani-Radar - 巴哈姆特動畫瘋評分 Dashboard

一個個人使用的巴哈姆特動畫瘋動畫評分 Dashboard，整合巴哈姆特、IMDb、豆瓣、MyAnimeList 四個平台的評分數據，提供多維度過濾和排序，幫助您快速找到值得觀看的高品質動畫，並可直接連結到巴哈姆特動畫瘋觀看。

## 亮點功能

- **跨平台評分整合**: 匯集巴哈姆特、IMDb、豆瓣、MyAnimeList 四大平台的評分數據，提供全面視角。
- **直覺式頂部篩選**: 全新的頂部整合式篩選介面，包含年份、類型、最低評分人數、搜尋等功能，操作更流暢。
- **智慧權重設定**: 自定義各平台評分的權重，系統自動平衡總和 100%，打造專屬「雷達分數」。
- **動態評分徽章**: 動畫卡片右上角動態顯示當前排序依據的評分，一目瞭然。
- **完整卡片資訊**: 每張動畫卡片清晰展示所有平台的評分、年份、集數及最多兩種類型標籤。
- **直達觀看**: 一鍵點擊即可跳轉至巴哈姆特動畫瘋頁面觀看動畫。
- **響應式設計**: 無論在桌面、平板或手機上，介面均能流暢適應。

## UI/UX 設計理念

本專案採用獨特的「**Creamy Aesthetic**」視覺風格，搭配「**Top Filter Layout**」頂部篩選佈局，旨在提供一個既美觀又高效的使用體驗。設計元素包括柔和的奶油色調、圓潤的卡片、精緻的柔和陰影以及溫暖的杏色點綴，打造出舒適且引人入勝的瀏覽環境。

## 技術棧

### 前端
- **框架**: Next.js 16 (App Router)
- **樣式**: Tailwind CSS v4
- **UI 組件**: 自定義 Creamy UI Components
- **語言**: TypeScript

### 資料管線 (Data Pipeline)
- **爬蟲**: Python scripts (BeautifulSoup4, Requests)
- **資料儲存**: 靜態 JSON 檔案 (`data/animes.json`)
- **更新策略**: 定期自動更新 (GitHub Actions) 或手動更新

## 專案結構

```
ani-radar/
├── app/                    # Next.js 應用程式核心
│   ├── layout.tsx         # 根佈局
│   ├── page.tsx           # 主要儀表板頁面
│   ├── components/        # React 組件 (包含 FilterBar, AnimeCard 等)
│   │   ├── ui/            # 自定義 Creamy UI 基礎組件
│   │   └── ...            # 核心應用組件
│   └── lib/               # 工具函式、資料載入、篩選與排序邏輯
├── crawler/               # 資料收集爬蟲腳本
│   ├── bahamut_scraper.py    # 巴哈姆特動畫瘋爬蟲
│   ├── cross_platform.py     # 跨平台評分對齊邏輯
│   ├── generate_json.py      # 生成最終 JSON 資料
│   └── update_latest.py      # 增量更新腳本 (用於定期更新)
├── data/                  # 靜態資料儲存
│   └── animes.json       # 主動畫資料庫 (約 1700+ 筆)
└── public/                # 靜態資源 (圖標等)
```

## 資料結構 (Anime)

每筆動畫資料包含以下核心欄位：

```typescript
interface Anime {
  id: string;                  // 唯一識別碼
  title: string;               // 中文標題
  titleOriginal?: string;      // 日文原標題 (選填)
  thumbnail: string;           // 縮圖 URL
  year: number;                // 播出年份
  genres: string[];            // 類型 (多個)
  episodes: number;            // 集數
  bahamutUrl: string;         // 巴哈姆特動畫瘋觀看連結
  popularity: number;          // 觀看人數

  ratings: {
    bahamut: { score: number; votes: number };        // 巴哈姆特 (1-5 分制)
    imdb?: { score: number; votes: number };          // IMDb (0-10 分制, 選填)
    douban?: { score: number; votes: number };        // 豆瓣 (0-10 分制, 選填)
    myanimelist?: { score: number; members: number }; // MyAnimeList (0-10 分制, 選填)
  };
}
```

## 快速開始

### 環境要求

- Node.js 18+ (用於 Next.js 應用程式)
- Python 3.8+ (用於資料爬蟲)
- npm 或 yarn

### 安裝

1.  **複製專案**
    ```bash
    git clone https://github.com/yourusername/ani-radar.git
    cd ani-radar
    ```

2.  **安裝前端依賴**
    ```bash
    npm install
    ```

3.  **安裝爬蟲依賴**
    ```bash
    cd crawler
    pip install -r requirements.txt
    ```

### 執行應用程式 (開發模式)

```bash
npm run dev
```

接著在瀏覽器中開啟 [http://localhost:3000](http://localhost:3000) 即可查看。

### 資料收集

#### 首次資料收集 (手動)

```bash
cd crawler
python bahamut_scraper.py      # 爬取巴哈姆特動畫瘋資料
python cross_platform.py       # 對齊跨平台評分
python generate_json.py        # 生成 animes.json
```

#### 定期更新 (手動或自動化)

建議每兩週執行一次資料更新。

**選項 A: 手動更新**
```bash
cd crawler
python update_latest.py        # 僅爬取最新動畫資料
git add data/animes.json
git commit -m "Update anime data"
git push
```

**選項 B: GitHub Actions 自動化**

請參考 `.github/workflows/update-data.yml` 檔案中的配置範例，設定自動化資料更新流程。

## 貢獻

本專案主要為個人使用設計。若您有任何建議或發現錯誤，歡迎提交 Issue。

## 授權

請參閱 [LICENSE](LICENSE) 檔案以獲取詳細資訊。

## 致謝

- 資料來源：巴哈姆特動畫瘋、IMDb、豆瓣、MyAnimeList。
- 為台灣的動畫愛好者設計。
- 由 Gemini Code 協助建構。

---

**注意**: 本專案僅供個人非商業用途。請務必遵守所有資料來源的服務條款。