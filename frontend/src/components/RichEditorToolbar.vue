<!-- 
  RichEditorToolbar.vue — 富文本编辑器工具栏组件

  配合 RichEditor.vue 使用，提供可视化操作按钮：
    - 块级样式：段落、标题 H1/H2/H3
    - 行内样式：加粗（B）、斜体（I）
    - 列表：无序列表（UL）、有序列表（OL）
    - 引用（“”）
    - 插入：链接（Link）、图片（Img）
    - 历史：撤销（↶）、重做（↷）

  按钮状态同步 editor 实例的选区状态，自动高亮当前生效的样式。
-->

<template>
  <!-- 
    role="toolbar" 增强无障碍语义
    aria-label 提供屏幕阅读器描述
  -->
  <div class="rich-editor-toolbar" role="toolbar" aria-label="富文本编辑工具栏">

    <!-- ============ 块级样式按钮组：段落 / H1 / H2 / H3 ============ -->
    <button
      v-for="item in blockItems"
      :key="item.label"
      class="toolbar-button"
      :class="{ 'is-active': item.active() }"
      type="button"
      :disabled="isDisabled"
      :title="item.title"
      @click="item.action"
    >
      {{ item.label }}
    </button>

    <!-- 分隔线 -->
    <span class="toolbar-divider" aria-hidden="true" />

    <!-- ============ 行内样式按钮组：加粗 / 斜体 ============ -->
    <button
      class="toolbar-button"
      :class="{ 'is-active': isActive('bold') }"
      type="button"
      :disabled="isDisabled"
      title="加粗"
      @click="runCommand(() => editor?.chain().focus().toggleBold().run())"
    >
      B
    </button>

    <button
      class="toolbar-button"
      :class="{ 'is-active': isActive('italic') }"
      type="button"
      :disabled="isDisabled"
      title="斜体"
      @click="runCommand(() => editor?.chain().focus().toggleItalic().run())"
    >
      I
    </button>

    <!-- ============ 列表按钮组：无序 / 有序 / 引用 ============ -->
    <button
      class="toolbar-button"
      :class="{ 'is-active': isActive('bulletList') }"
      type="button"
      :disabled="isDisabled"
      title="无序列表"
      @click="runCommand(() => editor?.chain().focus().toggleBulletList().run())"
    >
      UL
    </button>

    <button
      class="toolbar-button"
      :class="{ 'is-active': isActive('orderedList') }"
      type="button"
      :disabled="isDisabled"
      title="有序列表"
      @click="runCommand(() => editor?.chain().focus().toggleOrderedList().run())"
    >
      OL
    </button>

    <button
      class="toolbar-button"
      :class="{ 'is-active': isActive('blockquote') }"
      type="button"
      :disabled="isDisabled"
      title="引用"
      @click="runCommand(() => editor?.chain().focus().toggleBlockquote().run())"
    >
      “”
    </button>

    <!-- 分隔线 -->
    <span class="toolbar-divider" aria-hidden="true" />

    <!-- ============ 插入按钮组：链接 / 图片 ============ -->
    <button
      class="toolbar-button"
      type="button"
      :disabled="isDisabled"
      title="插入链接"
      @click="setLink"
    >
      Link
    </button>

    <button
      class="toolbar-button"
      type="button"
      :disabled="isDisabled"
      title="插入图片"
      @click="setImage"
    >
      Img
    </button>

    <!-- 分隔线 -->
    <span class="toolbar-divider" aria-hidden="true" />

    <!-- ============ 历史操作按钮组：撤销 / 重做 ============ -->
    <button
      class="toolbar-button"
      type="button"
      :disabled="isDisabled || !editor?.can().undo()"
      title="撤销"
      @click="runCommand(() => editor?.chain().focus().undo().run())"
    >
      ↶
    </button>

    <button
      class="toolbar-button"
      type="button"
      :disabled="isDisabled || !editor?.can().redo()"
      title="重做"
      @click="runCommand(() => editor?.chain().focus().redo().run())"
    >
      ↷
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Editor } from '@tiptap/core'

/* ================================================================
   Props — 接收父组件（RichEditor）传入的 editor 实例
   ================================================================ */

const props = withDefaults(
  defineProps<{
    editor: Editor | null   // TipTap Editor 实例，由 RichEditor 传入
    disabled?: boolean      // 是否禁用工具栏
  }>(),
  {
    disabled: false,
  },
)

/**
 * 计算属性：当没有 editor 实例或 disabled 为 true 时，
 * 所有按钮均应禁用。
 */
const isDisabled = computed(() => props.disabled || !props.editor)

/* ================================================================
   块级样式按钮配置
   ================================================================ */

/**
 * blockItems 定义了段落和 H1 ~ H3 四个块级样式按钮。
 * 每个按钮包含：
 *   label   — 按钮显示文字
 *   title   — 鼠标悬浮提示
 *   active  — 判断当前选区是否命中该样式
 *   action  — 点击执行的命令
 */
const blockItems = computed(() => [
  {
    label: 'P',
    title: '段落',
    active: () => isActive('paragraph'),
    action: () => runCommand(() => props.editor?.chain().focus().setParagraph().run()),
  },
  {
    label: 'H1',
    title: '一级标题',
    active: () => props.editor?.isActive('heading', { level: 1 }) || false,
    action: () => runCommand(() => props.editor?.chain().focus().toggleHeading({ level: 1 }).run()),
  },
  {
    label: 'H2',
    title: '二级标题',
    active: () => props.editor?.isActive('heading', { level: 2 }) || false,
    action: () => runCommand(() => props.editor?.chain().focus().toggleHeading({ level: 2 }).run()),
  },
  {
    label: 'H3',
    title: '三级标题',
    active: () => props.editor?.isActive('heading', { level: 3 }) || false,
    action: () => runCommand(() => props.editor?.chain().focus().toggleHeading({ level: 3 }).run()),
  },
])

/* ================================================================
   通用工具函数
   ================================================================ */

/**
 * 检查当前选区是否应用了指定名称的样式。
 * 例如 isActive('bold')、isActive('bulletList')。
 */
function isActive(name: string) {
  return props.editor?.isActive(name) || false
}

/**
 * 安全执行编辑器命令。
 * 如果已禁用则跳过执行。
 */
function runCommand(action: () => boolean | undefined) {
  if (isDisabled.value) {
    return
  }

  action()
}

/* ================================================================
   插入图片
   ================================================================ */

/**
 * 通过 prompt 弹窗让用户输入图片 URL。
 * 输入后调用 editor.chain().setImage() 插入图片。
 * 取消或空输入则不执行任何操作。
 */
function setImage() {
  if (isDisabled.value) {
    return
  }

  const url = window.prompt('请输入图片 URL')

  if (!url) {
    return
  }

  props.editor?.chain().focus().setImage({ src: url.trim() }).run()
}

/* ================================================================
   插入 / 移除链接
   ================================================================ */

/**
 * 通过 prompt 弹窗让用户输入链接 URL。
 *   - 如果已有链接，prompt 默认值显示当前链接 URL
 *   - 如果输入为空且原链接存在 → 移除链接
 *   - 如果输入不为空 → 设置/更新链接
 *   - 如果用户取消 (url === null) → 不操作
 */
function setLink() {
  if (isDisabled.value) {
    return
  }

  const previousUrl = props.editor?.getAttributes('link').href as string | undefined
  const url = window.prompt('请输入链接 URL。留空可移除当前链接。', previousUrl || '')

  if (url === null) {
    return
  }

  if (!url.trim()) {
    // 输入为空 → 移除链接
    props.editor?.chain().focus().extendMarkRange('link').unsetLink().run()
    return
  }

  // 输入有效 URL → 设置链接
  props.editor?.chain().focus().extendMarkRange('link').setLink({ href: url.trim() }).run()
}
</script>

<style scoped>
/* ——— 工具栏容器：flex 水平排列，黄色背景 ——— */
.rich-editor-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  padding: 12px;
  border-bottom: 4px solid #111111;
  background: #ffd23f;
}

/* ——— 工具按钮通用样式 ——— */
.toolbar-button {
  min-width: 40px;
  height: 36px;
  padding: 0 10px;
  border: 3px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  color: #111111;
  font-size: 14px;
  font-weight: 900;
  line-height: 1;
  cursor: pointer;
  box-shadow: 3px 3px 0 #111111;
}

/* 悬浮高亮 & 当前激活的样式按钮 */
.toolbar-button:hover:not(:disabled),
.toolbar-button.is-active {
  background: #2ec4b6;
  transform: translate(-1px, -1px);
  box-shadow: 4px 4px 0 #111111;
}

/* 禁用状态 */
.toolbar-button:disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

/* ——— 分隔线 ——— */
.toolbar-divider {
  width: 3px;
  height: 28px;
  margin: 0 2px;
  background: #111111;
}

/* ——— 移动端适配 ——— */
@media (max-width: 720px) {
  .rich-editor-toolbar {
    gap: 6px;
    padding: 10px;
  }

  .toolbar-button {
    min-width: 36px;
    height: 34px;
    padding: 0 8px;
    font-size: 13px;
  }
}
</style>