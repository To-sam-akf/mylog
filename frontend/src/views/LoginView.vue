<template>
  <section class="login-page">
    <article class="login-panel">
      <header class="login-header">
        <p class="eyebrow">ADMIN</p>
        <h1>Login</h1>
        <p>登录后可以编辑 Life Notes 和 Works。</p>
      </header>

      <form class="login-form" @submit.prevent="login">
        <label>
          <span>Username</span>
          <input v-model.trim="username" type="text" autocomplete="username" />
        </label>

        <label>
          <span>Password</span>
          <input v-model="password" type="password" autocomplete="current-password" />
        </label>

        <p v-if="message" class="login-message" :class="{ 'is-error': hasError }">
          {{ message }}
        </p>

        <div class="login-actions">
          <button class="pop-button" type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? '登录中...' : '登录' }}
          </button>
          <button
            v-if="isLoggedIn"
            class="ghost-button"
            type="button"
            :disabled="isSubmitting"
            @click="logout"
          >
            退出登录
          </button>
        </div>
      </form>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

interface LoginResponse {
  access_token: string
  token_type: string
}

const router = useRouter()

const username = ref('admin')
const password = ref('')
const isSubmitting = ref(false)
const message = ref('')
const hasError = ref(false)

const isLoggedIn = computed(() =>
  Boolean(localStorage.getItem('access_token') || localStorage.getItem('adminToken')),
)

async function login() {
  if (!username.value || !password.value) {
    showMessage('请输入用户名和密码。', true)
    return
  }

  isSubmitting.value = true
  showMessage('', false)

  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {  // 请求的元信息
        'Content-Type': 'application/json', // 告诉后端，我发送的数据是json格式
      },
      body: JSON.stringify({ // 解析成json格式，随请求发送的实际数据
        username: username.value,
        password: password.value,
      }),
    })

    if (!response.ok) {
      throw new Error('Login failed')
    }

    const data = (await response.json()) as LoginResponse

    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('adminToken', data.access_token)
    showMessage('登录成功，正在进入 Life Notes。', false)
    await router.push('/life-notes')
  } catch {
    showMessage('登录失败，请检查用户名或密码。', true)
  } finally {
    isSubmitting.value = false
  }
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('adminToken')
  password.value = ''
  showMessage('已退出登录。', false)
}

function showMessage(nextMessage: string, isError: boolean) {
  message.value = nextMessage
  hasError.value = isError
}
</script>

<style scoped>
.login-page {
  display: grid;
  justify-items: center;
}

.login-panel {
  width: min(520px, 100%);
  padding: 32px;
  border: 4px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 8px 8px 0 #111111;
}

.login-header {
  display: grid;
  gap: 12px;
  margin-bottom: 28px;
}

.eyebrow {
  display: inline-block;
  justify-self: start;
  margin: 0;
  padding: 6px 12px;
  border: 3px solid #111111;
  background: #ffd23f;
  color: #111111;
  font-size: 16px;
  font-weight: 900;
  line-height: 1;
}

.login-header h1 {
  margin: 0;
  color: #111111;
  font-size: 44px;
  font-weight: 900;
  line-height: 1.1;
}

.login-header p {
  margin: 0;
  color: #5f6b7a;
  font-size: 17px;
  line-height: 1.7;
}

.login-form {
  display: grid;
  gap: 18px;
}

.login-form label {
  display: grid;
  gap: 8px;
  color: #111111;
  font-weight: 900;
}

.login-form span {
  font-size: 14px;
  font-weight: 900;
  text-transform: uppercase;
}

.login-form input {
  width: 100%;
  min-height: 48px;
  padding: 8px 12px;
  border: 3px solid #111111;
  border-radius: 8px;
  background: #fff4d6;
  color: #111111;
  font: inherit;
  outline: none;
  box-shadow: 4px 4px 0 #4ecdc4;
}

.login-form input:focus {
  box-shadow: 5px 5px 0 #f25f5c;
}

.login-message {
  margin: 0;
  color: #111111;
  font-weight: 900;
}

.login-message.is-error {
  color: #b91c1c;
}

.login-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.pop-button,
.ghost-button {
  min-height: 42px;
  padding: 0 16px;
  border: 3px solid #111111;
  border-radius: 8px;
  color: #111111;
  font-weight: 900;
  cursor: pointer;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background-color 0.18s ease;
}

.pop-button {
  background: #4ecdc4;
  box-shadow: 4px 4px 0 #111111;
}

.ghost-button {
  background: #ffffff;
  box-shadow: 4px 4px 0 #111111;
}

.pop-button:hover:not(:disabled),
.ghost-button:hover:not(:disabled) {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #111111;
}

.pop-button:disabled,
.ghost-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

@media (max-width: 720px) {
  .login-panel {
    padding: 24px;
  }

  .login-header h1 {
    font-size: 34px;
  }
}
</style>
