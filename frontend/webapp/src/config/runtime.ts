export const runtimeConfig = {
  env: process.env.NEXT_PUBLIC_ENV,
  enableRealtime: process.env.NEXT_PUBLIC_ENABLE_REALTIME === "true",

  monitoringApi: process.env.NEXT_PUBLIC_MONITORING_API,

  realtime: {
    mode: process.env.NEXT_PUBLIC_REALTIME_MODE,
    endpoint: process.env.NEXT_PUBLIC_REALTIME_ENDPOINT,
    reconnect: process.env.NEXT_PUBLIC_REALTIME_RECONNECT === "true",
    reconnectDelay: Number(process.env.NEXT_PUBLIC_REALTIME_RECONNECT_DELAY),
  },
}
