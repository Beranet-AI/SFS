import "./globals.css";
import { I18nProvider } from "@/i18n/I18nProvider";
import { Inter, Vazirmatn } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const vazirmatn = Vazirmatn({
  subsets: ["arabic"],
  variable: "--font-vazir",
  display: "swap",
});

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`app-body ${inter.variable} ${vazirmatn.variable}`}>
        <I18nProvider>
          <div className="app-shell">{children}</div>
        </I18nProvider>
      </body>
    </html>
  );
}
