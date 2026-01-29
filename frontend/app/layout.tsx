import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Todo Chatbot - Phase III',
  description: 'AI-powered todo management chatbot',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
