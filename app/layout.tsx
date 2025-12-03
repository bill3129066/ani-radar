import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/next"
import { Inter, Noto_Sans_TC } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const notoSansTC = Noto_Sans_TC({ 
  subsets: ["latin"], 
  weight: ["300", "400", "500", "700"],
  variable: "--font-noto-sans-tc",
  preload: false
});

export const metadata: Metadata = {
  title: "Ani-Radar - 巴哈姆特動畫瘋評分 Dashboard",
  description: "聚合巴哈姆特、IMDb、豆瓣、MyAnimeList 四大平台動畫評分，快速找到值得看的動畫。提供多維度篩選與自定義權重排序。",
  keywords: ["動畫瘋", "巴哈姆特", "動畫評分", "IMDb", "MyAnimeList", "豆瓣", "新番推薦"],
  openGraph: {
    title: "Ani-Radar - 巴哈姆特動畫瘋評分 Dashboard",
    description: "聚合四大平台評分，發現優質動畫。",
    type: "website",
  }
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-TW">
      <body className={`${notoSansTC.className} ${inter.variable} antialiased`}>{children}
      <Analytics />
      </body>
    </html>
  );
}