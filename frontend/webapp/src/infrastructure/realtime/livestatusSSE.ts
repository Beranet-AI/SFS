export function connectLiveStatus(
  livestockId: string,
  onMessage: (data: any) => void
) {
  const es = new EventSource(
    `${process.env.NEXT_PUBLIC_MONITORING_BASE_URL}/monitoring/livestatus/stream?livestock_id=${livestockId}`
  )

  es.onmessage = (event) => {
    onMessage(JSON.parse(event.data))
  }

  return () => es.close()
}
