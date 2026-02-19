import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Toaster } from "sonner";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Article Reputation Analyzer",
  description:
    "FSE Technical Challenge - Analyze the reputation of news articles",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen bg-slate-50`}
      >
        <header className="bg-slate-900 px-8 py-4 flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-blue-400" />
            <span className="text-white font-semibold tracking-tight">
              Reputation Analyzer
            </span>
          </div>
          <span className="text-slate-500 text-sm"></span>
        </header>
        {children}
        <footer className="mt-16 py-6 border-t border-slate-200 text-center text-xs text-slate-400">
          FSE Technical Challenge
        </footer>
        <Toaster richColors position="top-right" />
      </body>
    </html>
  );
}
