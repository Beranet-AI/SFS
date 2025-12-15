import { useCallback, useEffect, useState } from 'react'

export function useAsyncList<T>(fetcher: () => Promise<T[]>) {
  const [items, setItems] = useState<T[]>([])
  const [loading, setLoading] = useState(false)

  const memoizedFetcher = useCallback(async () => {
    setLoading(true)
    try {
      const data = await fetcher()
      setItems(data)
    } finally {
      setLoading(false)
    }
  }, [fetcher])

  useEffect(() => {
    memoizedFetcher()
  }, [memoizedFetcher])

  return { items, loading }
}
