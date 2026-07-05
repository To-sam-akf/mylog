<template>
    <section class="home-page">
  <p class="side-slogan" aria-hidden="true">RECORD · CREATE · GROW</p>
  <p class="wow-sticker" aria-hidden="true">WOW!</p>

  <div class="hero">
    <div class="hero-content">
      <p class="eyebrow">MYLOG!</p>
      <h1>记录生活，展示作品</h1>
      <p class="intro">
        这里是我的个人空间，用文字、图像和作品记录成长。
      </p>

      <div class="hero-actions">
        <RouterLink class="primary-action" to="/life-notes">进入 Life Notes</RouterLink>
        <RouterLink class="secondary-action" to="/works">查看 Works</RouterLink>
      </div>
    </div>

    <aside class="profile-card">
      <p class="profile-title">IMAGINE</p>
      <img class="glasses-icon" :src="glassesUrl" alt="Round glasses" />
      <p class="profile-tags">AI / LIFE / WORKS</p>
      <p class="profile-slogan">PEACE · CREATE</p>
      <img class="album-icon" :src="albumUrl" alt="Album" />
    </aside>
  </div>

  <div class="entry-grid">
    <RouterLink class="entry-card life-card" to="/life-notes">
      <span>LIFE NOTES!</span>
      <p>记录日常、想法、片段和成长轨迹。</p>
    </RouterLink>

    <RouterLink class="entry-card works-card" to="/works">
      <span>WORKS!</span>
      <p>展示项目、作品、练习和创造过程。</p>
    </RouterLink>
  </div>
    </section>
</template>

<style scoped>
.home-page {
  position: relative;
  isolation: isolate;
  display: grid;
  gap: 40px;
  color: #111111;
}

.home-page::before,
.home-page::after {
  content: '';
  position: absolute;
  z-index: -1;
  pointer-events: none;
}

.home-page::before {
  top: 12px;
  left: -150px;
  width: 360px;
  height: 260px;
  opacity: 0.34;
  background-image: radial-gradient(#f25f5c 3px, transparent 3px);
  background-size: 18px 18px;
  border-radius: 50%;
}

.home-page::after {
  top: 280px;
  right: -140px;
  width: 260px;
  height: 180px;
  background:
    radial-gradient(circle at 72% 28%, #ffd23f 0 22px, transparent 23px),
    linear-gradient(135deg, rgba(0, 166, 251, 0.28), rgba(78, 205, 196, 0.28));
  transform: rotate(-9deg);
}

.side-slogan {
  position: absolute;
  top: 50%;
  left: -210px;
  z-index: 1;
  margin: 0;
  padding: 8px 14px;
  border: 3px solid #111111;
  background: #ffffff;
  color: #111111;
  font-size: 14px;
  font-weight: 900;
  line-height: 1;
  letter-spacing: 0;
  box-shadow: 5px 5px 0 #f25f5c;
  transform: translateY(-50%) rotate(-90deg);
  transform-origin: center;
  pointer-events: none;
}

.wow-sticker {
  position: absolute;
  left: -72px;
  bottom: 38px;
  z-index: 2;
  margin: 0;
  padding: 12px 18px;
  border: 3px solid #111111;
  border-radius: 999px;
  background: #f25f5c;
  color: #111111;
  font-size: 20px;
  font-weight: 900;
  line-height: 1;
  letter-spacing: 0;
  box-shadow: 5px 5px 0 #111111;
  transform: rotate(-8deg);
  pointer-events: none;
}

.wow-sticker::after {
  content: '';
  position: absolute;
  right: 16px;
  bottom: -11px;
  width: 18px;
  height: 18px;
  border-right: 3px solid #111111;
  border-bottom: 3px solid #111111;
  background: #f25f5c;
  transform: rotate(45deg);
}

.hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 36px;
  align-items: center;
  padding: 56px 0;
}

.hero::before {
  content: '';
  position: absolute;
  top: -40px;
  left: -64px;
  z-index: -1;
  width: 280px;
  height: 200px;
  opacity: 0.4;
  background-image: radial-gradient(#f25f5c 3px, transparent 3px);
  background-size: 18px 18px;
  border-radius: 50%;
}

.eyebrow {
  display: inline-block;
  margin: 0 0 16px;
  padding: 6px 12px;
  border: 3px solid #111111;
  background: #ffd23f;
  color: #111111;
  font-size: 18px;
  font-weight: 900;
}

.hero h1 {
  max-width: 680px;
  margin: 0;
  color: #111111;
  font-size: 52px;
  font-weight: 900;
  line-height: 1.12;
}

.intro {
  max-width: 620px;
  margin: 20px 0 0;
  color: #333333;
  font-size: 18px;
  line-height: 1.8;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
  margin-top: 30px;
}

.primary-action,
.secondary-action {
  display: inline-flex;
  align-items: center;
  min-height: 46px;
  padding: 0 20px;
  border: 3px solid #111111;
  border-radius: 8px;
  color: #111111;
  font-weight: 900;
  text-decoration: none;
  box-shadow: 5px 5px 0 #111111;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background-color 0.18s ease;
}

.primary-action {
  background: #f25f5c;
}

.secondary-action {
  background: #4ecdc4;
}

.primary-action:hover,
.secondary-action:hover {
  transform: translate(-3px, -3px);
  box-shadow: 8px 8px 0 #111111;
}

.primary-action:hover {
  background: #ffd23f;
}

.secondary-action:hover {
  background: #00a6fb;
}

.primary-action:active,
.secondary-action:active {
  transform: translate(2px, 2px);
  box-shadow: 2px 2px 0 #111111;
}

.profile-card {
  position: relative;
  min-height: 360px;
  padding: 28px;
  border: 4px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 8px 8px 0 #00a6fb;
  overflow: hidden;
}

.profile-title {
  margin: 0;
  font-size: 34px;
  font-weight: 900;
  line-height: 1;
}

.glasses-icon {
  display: block;
  width: 150px;
  height: 90px;
  object-fit: contain;
  margin: 32px auto 24px;
}

.profile-tags {
  margin: 0;
  font-size: 18px;
  font-weight: 900;
  text-align: center;
}

.profile-slogan {
  margin: 12px 0 0;
  color: #f25f5c;
  font-size: 20px;
  font-weight: 900;
  text-align: center;
}

.album-icon {
  position: absolute;
  right: -18px;
  bottom: -18px;
  width: 96px;
  height: 96px;
  border: 3px solid #111111;
  border-radius: 50%;
  object-fit: cover;
  background: #ffd23f;
}
.entry-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.entry-card {
  position: relative;
  z-index: 0;
  min-height: 180px;
  padding: 28px;
  border: 4px solid #111111;
  border-radius: 8px;
  color: #111111;
  text-decoration: none;
  box-shadow: 7px 7px 0 #111111;
  isolation: isolate;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background-color 0.18s ease;
}

.entry-card::before {
  content: '';
  position: absolute;
  z-index: -1;
  pointer-events: none;
}

.entry-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 11px 11px 0 #111111;
}

.entry-card:hover span {
  text-decoration: underline;
  text-decoration-thickness: 4px;
  text-underline-offset: 6px;
}

.life-card:hover {
  background: #f25f5c;
}

.works-card:hover {
  background: #4ecdc4;
}

.life-card {
  background: #ffd23f;
}

.life-card::before {
  top: -48px;
  right: 42px;
  width: 132px;
  height: 132px;
  border: 3px solid #111111;
  background: #ffd23f;
  clip-path: polygon(
    50% 0%,
    61% 30%,
    94% 14%,
    74% 45%,
    100% 50%,
    72% 61%,
    86% 94%,
    55% 74%,
    50% 100%,
    39% 70%,
    6% 86%,
    26% 55%,
    0% 50%,
    28% 39%,
    14% 6%,
    45% 26%
  );
  opacity: 0.72;
  transform: rotate(12deg);
  box-shadow: 8px 8px 0 rgba(242, 95, 92, 0.45);
}

.works-card {
  background: #00a6fb;
}

.works-card::before {
  right: -30px;
  bottom: -38px;
  width: 84%;
  height: 104px;
  border: 3px solid rgba(17, 17, 17, 0.22);
  background: rgba(0, 166, 251, 0.32);
  transform: rotate(-4deg);
}

.entry-card span {
  display: block;
  font-size: 30px;
  font-weight: 900;
}

.entry-card p {
  max-width: 360px;
  margin: 16px 0 0;
  color: #111111;
  font-size: 17px;
  line-height: 1.7;
}

@media (max-width: 720px) {
  .side-slogan,
  .wow-sticker {
    display: none;
  }

  .home-page::before {
    left: -190px;
  }

  .home-page::after {
    top: 520px;
    right: -190px;
  }

  .hero {
    grid-template-columns: 1fr;
    padding: 32px 0;
  }

  .hero h1 {
    font-size: 36px;
  }

  .intro {
    font-size: 16px;
  }

  .profile-card {
    min-height: 300px;
  }

  .entry-grid {
    grid-template-columns: 1fr;
  }

  .entry-card span {
    font-size: 26px;
  }
}
</style>

<script setup lang="ts">
import glassesUrl from '@/assets/home/round glasses.jpg'
import peaceUrl from '@/assets/home/peace.jpg'
import albumUrl from '@/assets/home/album.jpg'
</script>
