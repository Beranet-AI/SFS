export class HttpError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
  }
}

export async function http<T>(
  input: RequestInfo,
  init?: RequestInit,
): Promise<T> {
  const res = await fetch(input, {
    credentials: 'include',
    ...init,
  })

  if (!res.ok) {
    throw new HttpError(res.status, `HTTP ${res.status} error`)
  }

  return res.json() as Promise<T>
}
