import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { Flip } from 'gsap/Flip'
import { Observer } from 'gsap/Observer'

gsap.registerPlugin(ScrollTrigger, Flip, Observer)

gsap.defaults({ ease: 'power3.out', duration: 0.5 })
gsap.config({ nullTargetWarn: false })

// Respect prefers-reduced-motion: run all animations at near-instant speed
const mm = gsap.matchMedia()
mm.add('(prefers-reduced-motion: reduce)', () => {
  gsap.globalTimeline.timeScale(1000)
  return () => gsap.globalTimeline.timeScale(1)
})

export { gsap, ScrollTrigger, Flip, Observer }
