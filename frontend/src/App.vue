<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-shell">
    <header class="site-header">
      <RouterLink class="brand" to="/">MYLOG!</RouterLink>

      <nav class="nav">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/life-notes">Life Notes</RouterLink>
        <RouterLink to="/works">Works</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
      </nav>
    </header>

    <main class="main-content">
      <RouterView />
    </main>

    <button class="agent-button" type="button" aria-label="Open Agent">
      Ask me!
    </button>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: #fff4d6;
  color: #111111;
}

.site-header {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  padding: 18px 40px;
  border-bottom: 4px solid #111111;
  background: #fff4d6;
}

.brand {
  color: #111111;
  font-size: 24px;
  font-weight: 900;
  text-decoration: none;
  text-transform: uppercase;
}

.nav {
  display: flex;
  align-items: center;
  gap: 28px;
}

.nav a {
  border: 3px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  color: #111111;
  font-size: 16px;
  font-weight: 700;
  /* padding: 4px 0; */
}

.nav a.router-link-active {
  color: #111827;
  font-weight: 700;
}



.main-content {
  width: min(960px, calc(100% - 32px));
  margin: 0 auto;
  padding: 48px 0 96px;
}

.agent-button {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 20;

  min-width: 112px;
  height: 56px;
  padding: 0 20px;

  border: 4px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  color: #111111;

  font-size: 18px;
  font-weight: 900;
  cursor: pointer;

  box-shadow: 6px 6px 0 #f25f5c;
}

.agent-button::after {
  content: '';
  position: absolute;
  right: 22px;
  bottom: -13px;

  width: 18px;
  height: 18px;

  border: 4px solid #111111;
  border-radius: 50%;
  background: #ffd23f;
}

.agent-button:hover {
  transform: translate(-2px, -2px);
  box-shadow: 8px 8px 0 #f25f5c;
}

@media (max-width: 720px) {
  .site-header {
    align-items: flex-start;
    flex-direction: column;
    gap: 14px;
    padding: 16px 20px;
  }

  .nav {
    width: 100%;
    flex-wrap: wrap;
    gap: 16px;
  }
}

@media (max-width: 720px) {
  .agent-button {
    right: 16px;
    bottom: 16px;
    min-width: 96px;
    height: 50px;
    font-size: 16px;
  }

  .agent-button::after {
    right: 18px;
    bottom: -12px;
    width: 16px;
    height: 16px;
  }
}
</style>