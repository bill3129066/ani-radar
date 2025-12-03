import type { Metadata } from "next";
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
  title: "Ani-Radar - Anime Rating Dashboard",
  description: "Discover the best anime with multi-platform ratings",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-TW">
      <body className={`${notoSansTC.className} ${inter.variable} antialiased`}>{children}</body>
    </html>
  );
}