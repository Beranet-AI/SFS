let audio: HTMLAudioElement | null = null

export function playCriticalAlertSound() {
  if (!audio) {
    audio = new Audio('/sounds/critical.mp3')
    audio.volume = 0.8
  }

  audio.currentTime = 0
  audio.play().catch(() => {
    // autoplay policy
  })
}
