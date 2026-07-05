<template>
  <section class="works-page">
    <div v-if="status === 'loading'" class="state-card">
      <p class="state-label">LOADING</p>
      <p>正在加载 Works...</p>
    </div>

    <div v-else-if="status === 'error'" class="state-card error-card">
      <p class="state-label">ERROR</p>
      <p>{{ errorMessage }}</p>
      <button class="pop-button" type="button" @click="loadWorks">重新加载</button>
    </div>

    <template v-else>
      <article class="hero-panel">
        <div class="hero-copy">
          <p class="eyebrow">{{ isEditing ? 'EDIT WORKS!' : title }}</p>

          <template v-if="!isEditing">
            <h1>{{ title }}</h1>
            <p class="subtitle">{{ subtitle }}</p>
            <p class="description">{{ description }}</p>
          </template>

          <div v-else class="page-form">
            <label>
              <span>Title</span>
              <input v-model="draftTitle" type="text" />
            </label>
            <label>
              <span>Subtitle</span>
              <input v-model="draftSubtitle" type="text" />
            </label>
            <label>
              <span>Description</span>
              <textarea v-model="draftDescription" />
            </label>
          </div>
        </div>

        <div v-if="isAdmin" class="admin-strip" aria-live="polite">
          <button
            v-if="status === 'view' || status === 'saved'"
            class="pop-button"
            type="button"
            @click="startEditing"
          >
            编辑
          </button>
          <span v-if="status === 'saving'">保存中...</span>
          <span v-else-if="status === 'saved'">SAVED!</span>
          <span v-else-if="saveError">{{ saveError }}</span>
        </div>
      </article>

      <section class="projects-panel">
        <div class="projects-heading">
          <div>
            <p class="eyebrow">PROJECTS</p>
            <p>点击卡片查看详情！</p>
          </div>

          <button v-if="isEditing" class="pop-button" type="button" @click="addProject">
            新增项目
          </button>
        </div>

        <div v-if="!isEditing" class="project-grid">
          <a
            v-for="(project, index) in projects"
            :key="`${project.name}-${index}`"
            class="project-card"
            :class="projectColorClass(project, index)"
            :href="project.github"
            target="_blank"
            rel="noreferrer"
          >
            <h2>{{ project.name }}</h2>
            <p class="project-tech">{{ project.tech }}</p>
            <p class="project-desc">{{ project.desc }}</p>
            <span class="project-status">{{ project.status }}</span>
            <span class="github-link">VIEW GITHUB →</span>
          </a>
        </div>

        <div v-else class="project-editor-list">
          <article
            v-for="(project, index) in draftProjects"
            :key="project.id ?? `new-${index}`"
            class="project-editor"
          >
            <header>
              <strong>PROJECT {{ index + 1 }}</strong>
              <button class="ghost-button small-button" type="button" @click="removeProject(index)">
                删除
              </button>
            </header>

            <div class="project-fields">
              <label>
                <span>Name</span>
                <input v-model="project.name" type="text" />
              </label>
              <label>
                <span>Tech</span>
                <input v-model="project.tech" type="text" />
              </label>
              <label>
                <span>Status</span>
                <input v-model="project.status" type="text" />
              </label>
              <label>
                <span>Color</span>
                <input v-model="project.color" type="text" />
              </label>
              <label>
                <span>Order</span>
                <input v-model.number="project.sort_order" type="number" />
              </label>
              <label>
                <span>GitHub</span>
                <input v-model="project.github" type="url" />
              </label>
              <label class="wide-field">
                <span>Description</span>
                <textarea v-model="project.desc" />
              </label>
            </div>
          </article>
        </div>

        <footer v-if="isEditing" class="editor-actions">
          <button class="ghost-button" type="button" :disabled="status === 'saving'" @click="cancelEditing">
            取消
          </button>
          <button class="pop-button" type="button" :disabled="status === 'saving'" @click="saveWorks">
            保存
          </button>
        </footer>
      </section>
    </template>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

type PageStatus = 'loading' | 'view' | 'editing' | 'saving' | 'saved' | 'error'

interface WorkProject {
  id?: number
  name: string
  tech: string
  desc: string
  status: string
  github: string
  color: string
  sort_order: number
}

interface WorksResponse {
  title: string
  subtitle: string
  description: string
  projects: WorkProject[]
  updated_at?: string
}

const status = ref<PageStatus>('loading')
const title = ref('WORKS!')
const subtitle = ref('CREATE · BUILD · SHOW')
const description = ref('展示项目、作品、练习和创造过程。')
const projects = ref<WorkProject[]>([])

const draftTitle = ref('')
const draftSubtitle = ref('')
const draftDescription = ref('')
const draftProjects = ref<WorkProject[]>([])
const errorMessage = ref('')
const saveError = ref('')

const token = computed(() => localStorage.getItem('adminToken') ?? localStorage.getItem('access_token') ?? '')
const isAdmin = computed(() => Boolean(token.value))
const isEditing = computed(() => status.value === 'editing' || status.value === 'saving')

onMounted(() => {
  loadWorks()
})

async function loadWorks() {
  status.value = 'loading'
  errorMessage.value = ''
  saveError.value = ''

  try {
    applyWorksData(await fetchWorksData())
    status.value = 'view'
  } catch {
    errorMessage.value = '暂时无法加载 Works，请稍后再试。'
    status.value = 'error'
  }
}

async function fetchWorksData() {
  const response = await fetch('/api/works')
  if (!response.ok) {
    throw new Error('Failed to load Works')
  }

  return (await response.json()) as WorksResponse
}

function applyWorksData(data: WorksResponse) {
  title.value = data.title || 'WORKS!'
  subtitle.value = data.subtitle || 'CREATE · BUILD · SHOW'
  description.value = data.description || '展示项目、作品、练习和创造过程。'
  projects.value = cloneProjects(data.projects || []).sort((a, b) => a.sort_order - b.sort_order)
  resetDrafts()
}

function resetDrafts() {
  draftTitle.value = title.value
  draftSubtitle.value = subtitle.value
  draftDescription.value = description.value
  draftProjects.value = cloneProjects(projects.value)
}

function cloneProjects(source: WorkProject[]) {
  const fallbackColors = ['yellow', 'blue', 'pink', 'green']

  return source.map((project, index) => ({
    ...project,
    color: project.color || fallbackColors[index % fallbackColors.length] || 'yellow',
    sort_order: Number.isFinite(project.sort_order) ? project.sort_order : index + 1,
  }))
}

function startEditing() {
  resetDrafts()
  saveError.value = ''
  status.value = 'editing'
}

function cancelEditing() {
  resetDrafts()
  saveError.value = ''
  status.value = 'view'
}

function addProject() {
  draftProjects.value.push({
    name: 'NEW PROJECT!',
    tech: 'Vue · FastAPI',
    desc: '项目简介',
    status: 'BUILDING',
    github: 'https://github.com/xxx/new-project',
    color: 'green',
    sort_order: draftProjects.value.length + 1,
  })
}

function removeProject(index: number) {
  draftProjects.value.splice(index, 1)
}

async function saveWorks() {
  const nextTitle = draftTitle.value.trim()
  const nextSubtitle = draftSubtitle.value.trim()
  const nextDescription = draftDescription.value.trim()
  const nextProjects = draftProjects.value.map((project) => ({
    id: project.id,
    name: project.name.trim(),
    tech: project.tech.trim(),
    desc: project.desc.trim(),
    status: project.status.trim(),
    github: project.github.trim(),
    color: project.color.trim() || 'yellow',
    sort_order: Number.isFinite(project.sort_order) ? project.sort_order : 0,
  }))

  if (!nextTitle || !nextSubtitle || !nextDescription) {
    saveError.value = '标题、副标题和描述不能为空。'
    return
  }

  if (!nextProjects.length || nextProjects.some((project) => !project.name || !project.github)) {
    saveError.value = '至少保留一个项目，并填写项目名称和 GitHub。'
    return
  }

  status.value = 'saving'
  saveError.value = ''

  try {
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token.value}`,
    }

    const settingsResponse = await fetch('/api/admin/works/settings', {
      method: 'PUT',
      headers,
      body: JSON.stringify({
        title: nextTitle,
        subtitle: nextSubtitle,
        description: nextDescription,
      }),
    })

    if (!settingsResponse.ok) {
      throw new Error('Failed to save Works settings')
    }

    const draftIds = new Set(nextProjects.flatMap((project) => project.id ?? []))
    const deleteIds = projects.value.flatMap((project) =>
      project.id !== undefined && !draftIds.has(project.id) ? [project.id] : [],
    )

    await Promise.all(
      deleteIds.map(async (id) => {
        const response = await fetch(`/api/admin/works/${id}`, {
          method: 'DELETE',
          headers,
        })

        if (!response.ok) {
          throw new Error('Failed to delete Work')
        }
      }),
    )

    for (const project of nextProjects) {
      const response = await fetch(project.id ? `/api/admin/works/${project.id}` : '/api/admin/works', {
        method: project.id ? 'PUT' : 'POST',
        headers,
        body: JSON.stringify({
          name: project.name,
          tech: project.tech,
          desc: project.desc,
          status: project.status,
          github: project.github,
          color: project.color,
          sort_order: project.sort_order,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to save Work')
      }
    }

    applyWorksData(await fetchWorksData())
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

function projectColorClass(project: WorkProject, index: number) {
  if (['yellow', 'blue', 'pink', 'green'].includes(project.color)) {
    return `project-${project.color}`
  }

  const name = project.name.toLowerCase()
  if (name.includes('mylog')) return 'project-yellow'
  if (name.includes('market')) return 'project-blue'
  if (name.includes('research') || name.includes('ai')) return 'project-pink'
  if (name.includes('vue')) return 'project-green'

  return ['project-yellow', 'project-blue', 'project-pink', 'project-green'][index % 4]
}
</script>

<style scoped>
.works-page {
  position: relative;
  display: grid;
  gap: 32px;
  color: #111111;
}

.works-page::before {
  content: '';
  position: absolute;
  top: -20px;
  right: -120px;
  z-index: -1;
  width: 300px;
  height: 210px;
  opacity: 0.3;
  background-image: radial-gradient(#00a6fb 3px, transparent 3px);
  background-size: 18px 18px;
  border-radius: 50%;
}

.works-page::after {
  content: 'WOW!';
  position: absolute;
  left: -54px;
  bottom: 90px;
  z-index: 2;
  padding: 10px 14px;
  border: 3px solid #111111;
  border-radius: 999px;
  background: #f25f5c;
  font-weight: 900;
  line-height: 1;
  box-shadow: 5px 5px 0 #111111;
  transform: rotate(-10deg);
  pointer-events: none;
}

.state-card,
.hero-panel,
.projects-panel {
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

.state-card p {
  margin: 0;
  font-size: 18px;
  line-height: 1.7;
}

.error-card {
  box-shadow: 8px 8px 0 #f25f5c;
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

.hero-panel {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 24px;
  padding: 32px;
}

.hero-copy {
  display: grid;
  gap: 14px;
  min-width: 0;
}

.hero-copy h1 {
  margin: 0;
  font-size: 48px;
  font-weight: 900;
  line-height: 1;
}

.subtitle,
.description,
.projects-heading p {
  margin: 0;
  color: #111111;
  font-size: 18px;
  line-height: 1.7;
}

.subtitle {
  font-weight: 900;
}

.admin-strip {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 18px;
  font-weight: 900;
}

.projects-panel {
  padding: 32px;
}

.projects-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 24px;
}

.projects-heading > div {
  display: grid;
  gap: 12px;
}

.project-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 22px;
}

.project-card {
  display: grid;
  align-content: start;
  min-height: 230px;
  padding: 22px;
  border: 4px solid #111111;
  border-radius: 8px;
  color: #111111;
  text-decoration: none;
  box-shadow: 7px 7px 0 #111111;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease;
}

.project-card:hover {
  transform: translate(-4px, -4px);
  box-shadow: 11px 11px 0 #111111;
}

.project-card h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 900;
  line-height: 1.05;
}

.project-tech,
.project-desc {
  margin: 14px 0 0;
  color: #111111;
  line-height: 1.55;
}

.project-tech {
  font-weight: 900;
}

.project-status {
  display: inline-flex;
  width: fit-content;
  margin-top: 18px;
  padding: 5px 8px;
  border: 3px solid #111111;
  border-radius: 999px;
  background: #ffffff;
  font-size: 13px;
  font-weight: 900;
}

.github-link {
  margin-top: 18px;
  font-weight: 900;
}

.project-yellow {
  background: #ffd23f;
}

.project-blue {
  background: #00a6fb;
}

.project-pink {
  background: #f25f5c;
}

.project-green {
  background: #4ecdc4;
}

.page-form,
.project-editor-list {
  display: grid;
  gap: 18px;
}

.page-form label,
.project-fields label {
  display: grid;
  gap: 8px;
}

.page-form span,
.project-fields span {
  font-size: 13px;
  font-weight: 900;
  text-transform: uppercase;
}

input,
textarea {
  width: 100%;
  border: 3px solid #111111;
  border-radius: 8px;
  background: #fff4d6;
  color: #111111;
  font: inherit;
  outline: none;
  box-shadow: 4px 4px 0 #4ecdc4;
}

input {
  min-height: 42px;
  padding: 8px 10px;
}

textarea {
  min-height: 88px;
  padding: 10px;
  resize: vertical;
}

input:focus,
textarea:focus {
  box-shadow: 5px 5px 0 #f25f5c;
}

.project-editor {
  padding: 20px;
  border: 3px solid #111111;
  border-radius: 8px;
  background: #fff4d6;
}

.project-editor header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.project-editor strong {
  font-size: 18px;
  font-weight: 900;
}

.project-fields {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.wide-field {
  grid-column: 1 / -1;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
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
  box-shadow: 4px 4px 0 #111111;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background-color 0.18s ease;
}

.pop-button {
  background: #4ecdc4;
}

.ghost-button {
  background: #ffffff;
}

.small-button {
  min-height: 34px;
  padding: 0 12px;
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

.pop-button:disabled,
.ghost-button:disabled {
  cursor: not-allowed;
  opacity: 0.68;
  transform: none;
}

@media (max-width: 900px) {
  .project-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 720px) {
  .works-page::before,
  .works-page::after {
    display: none;
  }

  .hero-panel,
  .projects-heading,
  .editor-actions {
    align-items: stretch;
    flex-direction: column;
  }

  .hero-copy h1 {
    font-size: 36px;
  }

  .project-grid,
  .project-fields {
    grid-template-columns: 1fr;
  }
}
</style>
