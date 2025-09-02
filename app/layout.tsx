import './globals.css'
import '../styles/tokens.css'
import type { ReactNode } from 'react'
export const metadata = { title: 'ThemeExtractor Preview', description: 'Extract → Tokenize → Synthesize' }
export default function RootLayout({ children }: { children: ReactNode }) {
  return (<html lang="ko"><body>{children}</body></html>)
}