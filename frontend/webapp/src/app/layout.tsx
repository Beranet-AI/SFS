import "./globals.css";
import { I18nProvider } from "@/i18n/I18nProvider";
import { LanguageSwitcher } from "@/ui/components/LanguageSwitcher";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="app-body">
        <I18nProvider>
          <div className="app-shell">
            <LanguageSwitcher />
            {children}
          </div>
        </I18nProvider>
      </body>
    </html>
  );
}
