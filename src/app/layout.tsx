import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NextERA - Danışmanlık Platformu",
  description: "Online danışmanlık ve seans yönetim platformu",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
        <link rel="manifest" href="/manifest.json" />
        <link rel="icon" href="/logo.png" />
        <link rel="apple-touch-icon" href="/logo.png" />
        <meta name="theme-color" content="#0891B2" />
      </head>
      <body>
        <div
          style={{
            maxWidth: 480,
            margin: "0 auto",
            minHeight: "100vh",
            background: "#F8FAFC",
            boxShadow: "0 0 60px rgba(0,0,0,0.08)",
          }}
        >
          {children}
        </div>
      </body>
    </html>
  );
}
