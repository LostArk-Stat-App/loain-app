'use client'

import { useState } from 'react'

export default function Home() {
  const [characterName, setCharacterName] = useState('')
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!characterName.trim()) return

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const res = await fetch(`/api/v1/characters/${encodeURIComponent(characterName)}`)
      if (!res.ok) {
        if (res.status === 404) throw new Error('캐릭터를 찾을 수 없습니다.')
        throw new Error('검색 중 오류가 발생했습니다.')
      }
      const data = await res.json()
      setResult(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold mb-2 text-yellow-400">로아인</h1>
      <p className="text-gray-400 mb-8">로스트아크 캐릭터 검색 서비스</p>

      <form onSubmit={handleSearch} className="flex gap-2 w-full max-w-md">
        <input
          type="text"
          value={characterName}
          onChange={(e) => setCharacterName(e.target.value)}
          placeholder="캐릭터 이름 입력"
          className="flex-1 px-4 py-2 rounded-lg bg-gray-800 border border-gray-600 focus:outline-none focus:border-yellow-400 text-white"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-2 bg-yellow-400 text-gray-900 font-bold rounded-lg hover:bg-yellow-300 disabled:opacity-50 transition"
        >
          {loading ? '검색 중...' : '검색'}
        </button>
      </form>

      {error && (
        <p className="mt-4 text-red-400">{error}</p>
      )}

      {result && (
        <div className="mt-8 w-full max-w-md bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-xl font-bold text-yellow-400 mb-2">{result.CharacterName}</h2>
          <p className="text-gray-400">서버: {result.ServerName}</p>
          <p className="text-gray-400">직업: {result.CharacterClassName}</p>
          <p className="text-gray-400">아이템 레벨: {result.ItemAvgLevel}</p>
        </div>
      )}
    </main>
  )
}
