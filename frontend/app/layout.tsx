import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Complaint Management",
  description: "Customer complaint management dashboard"
};

export default function RootLayout({
  children
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

