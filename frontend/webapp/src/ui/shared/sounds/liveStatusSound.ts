let audio: HTMLAudioElement | null = null

export function playCriticalLiveStatusSound() {
  // Guard for SSR
  if (typeof window === 'undefined') return

  if (!audio) {
    audio = new Audio('/sounds/critical.mp3')
  }

  audio.currentTime = 0
  audio.play().catch(() => {
    // autoplay ممکن است بلاک شود؛ عمداً ignore
  })
}
