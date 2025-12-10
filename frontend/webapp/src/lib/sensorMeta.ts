// sensorMeta.ts
export type SensorMeta = {
  name: string // English name, e.g., "Temperature"
  faLabel?: string // فارسی: مثلاً "دما"
  unit?: string // مثلاً "°C"
  color?: string // رنگ اصلی برای نمودار یا نمایش کارت
  icon?: string // آیکون اختیاری (مثلاً emoji یا نام کلاس)
}

export const sensorMetaMap: Record<string, SensorMeta> = {
  temperature: {
    name: 'Temperature',
    faLabel: 'دمــا',
    unit: '°C',
    color: '#facc15', // yellow
    icon: '🌡️',
  },
  ammonia: {
    name: 'Ammonia',
    faLabel: 'آمونیاک',
    unit: 'ppm',
    color: '#4ade80', // green
    icon: '🧪',
  },
  humidity: {
    name: 'Humidity',
    faLabel: 'رطوبت',
    unit: '%',
    color: '#38bdf8', // blue
    icon: '💧',
  },
  co2: {
    name: 'CO₂',
    faLabel: 'دی‌اکسید کربن',
    unit: 'ppm',
    color: '#f87171',
    icon: '🌫️',
  },
  light: {
    name: 'Light',
    faLabel: 'نور',
    unit: 'lux',
    color: '#fde68a',
    icon: '💡',
  },
  // سنسورهای جدید را به همین صورت اضافه کن
}
