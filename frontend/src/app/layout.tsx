import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: '로아인 - 로스트아크 캐릭터 검색',
  description: '로스트아크 캐릭터 정보를 빠르게 검색하세요.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  )
}
