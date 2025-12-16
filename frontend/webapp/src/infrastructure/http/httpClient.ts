// src/infrastructure/http/httpClient.ts

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE'

async function request<T>(
  method: HttpMethod,
  url: string,
  body?: unknown,
): Promise<T> {
  const response = await fetch(url, {
    method,
    headers: {
      'Content-Type': 'application/json',
      // بعداً اینجا token اضافه می‌شود
    },
    body: body ? JSON.stringify(body) : undefined,
  })

  if (!response.ok) {
    const errorText = await response.text()
    throw new Error(errorText || 'HTTP request failed')
  }

  // اگر response body نداشت (مثلاً acknowledge)
  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export const httpClient = {
  get<T>(url: string) {
    return request<T>('GET', url)
  },

  post<T>(url: string, body?: unknown) {
    return request<T>('POST', url, body)
  },

  put<T>(url: string, body?: unknown) {
    return request<T>('PUT', url, body)
  },

  delete<T>(url: string) {
    return request<T>('DELETE', url)
  },
}
