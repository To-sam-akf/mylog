<template>
  <section class="life-notes-page">
    <p class="page-sticker" aria-hidden="true">LIFE!</p>

    <div v-if="status === 'loading'" class="state-card">
      <p class="state-label">LOADING</p>
      <p>正在加载 Life Notes...</p>
    </div>

    <div v-else-if="status === 'error'" class="state-card error-card">
      <p class="state-label">ERROR</p>
      <p>{{ errorMessage }}</p>
      <button class="pop-button" type="button" @click="loadLifeNotes">重新加载</button>
    </div>

    <article v-else class="note-panel">
      <header class="note-header">
        <div class="note-heading">
          <p class="eyebrow">LIFE NOTES!</p>
          <!-- 普通文本标题 -->
          <h1 v-if="status !== 'editing'">{{ title }}</h1>

          <!-- 编辑模式下的单行输入框 -->
          <input
            v-else
            v-model="draftTitle"
            class="title-input"
            type="text"
            aria-label="Life Notes title"
          />
        </div>

        <button
          v-if="isAdmin && status !== 'editing' && status !== 'saving'"
          class="pop-button edit-button"
          type="button"
          @click="startEditing"
        >
          编辑
        </button>
      </header>

      <div v-if="status !== 'editing'" class="note-content">
        <p v-if="content">{{ content }}</p>
        <p v-else class="empty-text">这里还没有内容。</p>
      </div>

      <!-- ↑ 取代 <h1>，变成一个文本输入框，多行文本输入控件  -->
      <!-- `v-model` 的存在，会直接修改 `draftTitle` / `draftContent`，而 `title` / `content` __保持不变__。
 -->
      <textarea
        v-else
        v-model="draftContent"
        class="note-editor"
        aria-label="Life Notes content"
      />

      <footer v-if="isAdmin" class="admin-footer">
        <div class="save-message" aria-live="polite">
          <span v-if="status === 'saving'">保存中...</span>
          <span v-else-if="status === 'saved'">已保存</span>
          <span v-else-if="saveError">{{ saveError }}</span>
          <span v-else>管理员模式</span>
        </div>

        <div v-if="status === 'editing'" class="admin-actions">
          <button class="ghost-button" type="button" @click="cancelEditing">取消</button>
          <button class="pop-button" type="button" @click="saveLifeNotes">保存</button>
        </div>
      </footer>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type PageStatus = 'loading' | 'view' | 'editing' | 'saving' | 'saved' | 'error'

interface LifeNoteResponse {
  id: number
  title: string
  content: string
  content_markdown?: string | null
  updated_at?: string
}

const status = ref<PageStatus>('loading')
const title = ref('')
const content = ref('')
const draftTitle = ref('')
const draftContent = ref('')
const errorMessage = ref('')
const saveError = ref('')

const token = computed(() => localStorage.getItem('adminToken') ?? localStorage.getItem('access_token') ?? '')
const isAdmin = computed(() => Boolean(token.value))

onMounted(() => {
  loadLifeNotes()
})

async function loadLifeNotes() {
  status.value = 'loading'
  errorMessage.value = ''
  saveError.value = ''

  try {
    const response = await fetch('/api/life-notes')

    if (!response.ok) {
      throw new Error('Failed to load Life Notes')
    }

    const data = (await response.json()) as LifeNoteResponse

    title.value = data.title || 'Life Notes'
    content.value = data.content || ''
    draftTitle.value = title.value
    draftContent.value = content.value
    status.value = 'view'
  } catch {
    errorMessage.value = '暂时无法加载 Life Notes，请稍后再试。'
    status.value = 'error'
  }
}

function startEditing() {
  draftTitle.value = title.value
  draftContent.value = content.value
  saveError.value = ''
  status.value = 'editing'  // ★ 关键：将状态切换为 'editing'
}

function cancelEditing() {
  draftTitle.value = title.value
  draftContent.value = content.value
  saveError.value = ''
  status.value = 'view'
}

async function saveLifeNotes() {
  const nextTitle = draftTitle.value.trim()
  const nextContent = draftContent.value.trim()

  if (!nextTitle || !nextContent) {
    saveError.value = '标题和内容不能为空。'
    return
  }

  status.value = 'saving'
  saveError.value = ''

  try {
    const response = await fetch('/api/admin/life-notes', {
      method: 'PUT',
      // HTTP 请求的"元信息
      headers: {
        'Content-Type': 'application/json',     // ← 告诉后端："我发的内容是 JSON 格式"
        Authorization: `Bearer ${token.value}`,  // ← 告诉后端："这是我的身份凭证"
      },
      // 随请求发送的实际数据
      body: JSON.stringify({               // ← 把 JavaScript 对象转成 JSON 字符串
        title: nextTitle,                  // ← 用户编辑后的新标题
        content: nextContent,              // ← 用户编辑后的新内容
      }),
    })

    if (!response.ok) {
      throw new Error('Failed to save Life Notes')
    }

    const data = (await response.json()) as LifeNoteResponse

    title.value = data.title || nextTitle // 优先使用后端返回的标题，如果没有则使用用户编辑后的标题
    content.value = data.content || nextContent
    draftTitle.value = title.value // 保持草稿与保存后的内容一致 
    draftContent.value = content.value
    status.value = 'saved'

    window.setTimeout(() => {
      if (status.value === 'saved') {
        status.value = 'view'
      }
    }, 1200)
  } catch {
    saveError.value = '保存失败，请稍后再试。'
    status.value = 'editing'
  }
}
</script>

<style scoped>
.life-notes-page {
  position: relative;
  display: grid;
  color: #111111;
}

.life-notes-page::before {
  content: '';
  position: absolute;
  top: -24px;
  right: -90px;
  z-index: -1;
  width: 260px;
  height: 180px;
  opacity: 0.32;
  background-image: radial-gradient(#f25f5c 3px, transparent 3px);
  background-size: 18px 18px;
  border-radius: 50%;
}

.page-sticker {
  position: absolute;
  top: 40px;
  left: -44px;
  z-index: 2;
  margin: 0;
  padding: 10px 14px;
  border: 3px solid #111111;
  border-radius: 999px;
  background: #ffd23f;
  font-size: 18px;
  font-weight: 900;
  line-height: 1;
  box-shadow: 5px 5px 0 #f25f5c;
  transform: rotate(-10deg);
  pointer-events: none;
}

.state-card,
.note-panel {
  border: 4px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 8px 8px 0 #111111;
}

.state-card {
  display: grid;
  gap: 16px;
  justify-items: start;
  padding: 32px;
}

.state-label,
.eyebrow {
  display: inline-block;
  margin: 0;
  padding: 6px 12px;
  border: 3px solid #111111;
  background: #ffd23f;
  font-size: 16px;
  font-weight: 900;
  line-height: 1;
}

.state-card p {
  margin: 0;
  color: #111111;
  font-size: 18px;
  line-height: 1.7;
}

.error-card {
  box-shadow: 8px 8px 0 #f25f5c;
}

.error-card .state-label {
  background: #f25f5c;
}

.note-panel {
  position: relative;
  overflow: hidden;
  padding: 36px;
}

.note-panel::after {
  content: '';
  position: absolute;
  right: -56px;
  bottom: -50px;
  z-index: 0;
  width: 220px;
  height: 96px;
  border: 3px solid rgba(17, 17, 17, 0.22);
  background: rgba(0, 166, 251, 0.24);
  transform: rotate(-6deg);
  pointer-events: none;
}

.note-header,
.note-content,
.note-editor,
.admin-footer {
  position: relative;
  z-index: 1;
}

.note-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.note-heading {
  display: grid;
  gap: 16px;
  min-width: 0;
}

.note-heading h1 {
  margin: 0;
  color: #111111;
  font-size: 46px;
  font-weight: 900;
  line-height: 1.1;
}

.note-content {
  min-height: 320px;
  padding: 24px;
  border: 3px solid #111111;
  border-radius: 8px;
  background: #fff4d6;
  white-space: pre-wrap;
}

.note-content p {
  margin: 0;
  color: #111111;
  font-size: 18px;
  line-height: 1.9;
}

.empty-text {
  color: #555555;
}

.title-input,
.note-editor {
  width: 100%;
  border: 3px solid #111111;
  border-radius: 8px;
  background: #fff4d6;
  color: #111111;
  font: inherit;
  outline: none;
  box-shadow: 4px 4px 0 #4ecdc4;
}

.title-input:focus,
.note-editor:focus {
  box-shadow: 5px 5px 0 #f25f5c;
}

.title-input {
  min-height: 58px;
  padding: 8px 12px;
  font-size: 34px;
  font-weight: 900;
}

.note-editor {
  min-height: 360px;
  padding: 20px;
  resize: vertical;
  font-size: 17px;
  line-height: 1.8;
}

.admin-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-top: 24px;
}

.admin-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.save-message {
  color: #111111;
  font-weight: 900;
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

.pop-button:hover,
.ghost-button:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #111111;
}

.pop-button:active,
.ghost-button:active {
  transform: translate(1px, 1px);
  box-shadow: 2px 2px 0 #111111;
}

@media (max-width: 720px) {
  .life-notes-page::before,
  .page-sticker {
    display: none;
  }

  .note-panel {
    padding: 24px;
  }

  .note-header,
  .admin-footer {
    align-items: stretch;
    flex-direction: column;
  }

  .note-heading h1 {
    font-size: 34px;
  }

  .title-input {
    font-size: 26px;
  }
}
</style>
