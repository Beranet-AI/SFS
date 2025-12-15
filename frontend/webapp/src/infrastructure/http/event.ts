export async function http<T>(
  url: string,
  options: RequestInit = {},
): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    credentials: 'include', // اگر auth/session داری
  })

  // اگر پاسخ OK نیست
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    const error = new Error(`HTTP ${res.status} ${res.statusText}: ${text}`)
    // @ts-expect-error – attach status for debugging
    error.status = res.status
    throw error
  }

  // اگر پاسخ بدون body بود (204)
  if (res.status === 204) {
    return null as T
  }

  return (await res.json()) as T
}
