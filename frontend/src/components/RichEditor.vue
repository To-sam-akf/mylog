<!-- 
  RichEditor.vue — 通用富文本编辑器组件

  基于 TipTap（ProseMirror）封装，支持：
    - 标题（H1/H2/H3）、段落、加粗、斜体、列表、引用
    - 图片和链接插入
    - 撤销 / 重做
    - v-model 双向绑定，父组件通过 modelValue 传入/接收 HTML
    - 粘贴安全过滤：清理危险标签、事件属性、XSS 尝试
    - disabled 状态控制只读
-->

<template>
  <!-- 编辑器容器：disabled 时降低不透明度 -->
  <div class="rich-editor" :class="{ 'is-disabled': disabled }">
    <!-- 顶部工具栏组件 -->
    <RichEditorToolbar :editor="editor || null" :disabled="disabled" />

    <!-- 
      EditorContent 是 TipTap 提供的 Vue 组件，负责渲染编辑区域。
      editor 实例由 useEditor() 创建并暴露。
    -->
    <EditorContent class="rich-editor__content" :editor="editor" />
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { EditorContent, useEditor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'
import Link from '@tiptap/extension-link'
import Placeholder from '@tiptap/extension-placeholder'
import type { Editor } from '@tiptap/core'
import RichEditorToolbar from './RichEditorToolbar.vue'

/* ================================================================
   安全配置：白名单方式过滤粘贴/外部 HTML
   ================================================================ */

/** 允许保留的 HTML 标签 */
const allowedTags = new Set([
  'a',
  'blockquote',
  'br',
  'em',
  'h1',
  'h2',
  'h3',
  'img',
  'li',
  'ol',
  'p',
  'strong',
  'ul',
])

/** 每个标签允许保留的属性（白名单） */
const allowedAttributes: Record<string, string[]> = {
  a: ['href', 'title', 'target', 'rel'],
  img: ['src', 'alt', 'title'],
}

/* ================================================================
   Props & Emits — 组件接口定义
   ================================================================ */

const props = withDefaults(
  defineProps<{
    modelValue: string      // 当前 HTML 内容（v-model 绑定）
    placeholder?: string    // 空状态占位提示文字
    disabled?: boolean      // 是否禁用编辑（只读模式）
  }>(),
  {
    placeholder: '开始写点什么吧...',
    disabled: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]   // 内容变化时向父组件发射新 HTML
}>()

/* ================================================================
   创建 Editor 实例
   ================================================================ */

const editor = useEditor({
  // 初始内容需要经过 sanitize 过滤
  content: sanitizeHtml(props.modelValue),
  editable: !props.disabled,

  // 注册 TipTap 扩展
  extensions: [
    StarterKit.configure({
      // 只启用 H1 ~ H3，不启用 H4 ~ H6
      heading: {
        levels: [1, 2, 3],
      },
    }),
    Image.configure({
      allowBase64: false,   // 禁止 Base64 图片（防止数据量过大）
      inline: false,        // 图片块级显示
    }),
    Link.configure({
      autolink: true,               // 自动识别 URL 并转为链接
      defaultProtocol: 'https',     // 无协议时默认 https
      openOnClick: false,           // 点击不跳转（让工具栏控制编辑）
    }),
    Placeholder.configure({
      placeholder: props.placeholder,
    }),
  ],

  // 编辑器配置项
  editorProps: {
    /**
     * 粘贴外部 HTML 时先通过 sanitizeHtml 过滤，
     * 去除危险标签/属性后再注入编辑器。
     */
    transformPastedHTML(html) {
      return sanitizeHtml(html)
    },
  },

  /**
   * 编辑器内容发生变化时：
   *   1. 用 sanitizeHtml 清理后发射给父组件
   *   2. 父组件 v-model 同步更新
   */
  onUpdate({ editor }) {
    emit('update:modelValue', sanitizeHtml(editor.getHTML()))
  },
})

/* ================================================================
   响应式监听
   ================================================================ */

/**
 * 监听父组件传入的 modelValue。
 * 当外部修改内容时（例如重置、加载新数据），同步更新编辑器内容。
 * 避免循环更新：只在内容不同时 setContent，并禁止触发 emit。
 */
watch(
  () => props.modelValue,
  (value) => {
    const instance = editor.value

    if (!instance) {
      return
    }

    const nextHtml = sanitizeHtml(value)
    if (nextHtml !== sanitizeHtml(instance.getHTML())) {
      instance.commands.setContent(nextHtml, { emitUpdate: false })
    }
  },
)

/**
 * 监听 disabled 变化，动态切换编辑器是否可编辑。
 */
watch(
  () => props.disabled,
  (isDisabled) => {
    editor.value?.setEditable(!isDisabled)
  },
)

/* ================================================================
   HTML 安全过滤函数
   ================================================================ */

/**
 * 清理 HTML 字符串：
 *   1. 用 DOMParser 解析
 *   2. 递归遍历 DOM 树，删除不允许的标签/属性
 *   3. 返回安全的 HTML
 */
function sanitizeHtml(html: string) {
  if (!html || typeof window === 'undefined') {
    return ''
  }

  const template = document.createElement('template')
  template.innerHTML = html

  cleanNode(template.content)
  return template.innerHTML
}

/**
 * 递归清理 DOM 节点。
 *   - 删除注释节点
 *   - 非白名单标签 → 保留其子节点，删除标签本身（unwrap）
 *   - 白名单标签 → 清理属性后递归子节点
 */
function cleanNode(node: Node) {
  Array.from(node.childNodes).forEach((child) => {
    // 删除 HTML 注释
    if (child.nodeType === Node.COMMENT_NODE) {
      child.remove()
      return
    }

    // 只处理元素节点，文本节点直接保留
    if (child.nodeType !== Node.ELEMENT_NODE) {
      return
    }

    const element = child as HTMLElement
    const tagName = element.tagName.toLowerCase()

    // 不在白名单中的标签 → 保留子节点，删除标签外壳
    if (!allowedTags.has(tagName)) {
      element.replaceWith(...Array.from(element.childNodes))
      return
    }

    // 清理属性，再递归子节点
    cleanAttributes(element, tagName)
    cleanNode(element)
  })
}

/**
 * 清理元素属性：
 *   - 删除 on* 事件属性（如 onclick）
 *   - 只保留白名单属性
 *   - href/src 必须指向安全协议，否则移除
 *   - a 标签强制添加 target="_blank" + rel="noreferrer noopener"
 */
function cleanAttributes(element: HTMLElement, tagName: string) {
  Array.from(element.attributes).forEach((attribute) => {
    const name = attribute.name.toLowerCase()
    const value = attribute.value.trim()
    const tagAllowedAttributes = allowedAttributes[tagName] || []

    // 不在白名单中或以 on 开头的属性 → 删除
    if (!tagAllowedAttributes.includes(name) || name.startsWith('on')) {
      element.removeAttribute(attribute.name)
      return
    }

    // href 和 src 必须指向安全 URL，否则移除
    if ((name === 'href' || name === 'src') && !isSafeUrl(value)) {
      element.removeAttribute(attribute.name)
    }
  })

  // 所有链接强制新窗口打开 + 安全 rel
  if (tagName === 'a') {
    element.setAttribute('target', '_blank')
    element.setAttribute('rel', 'noreferrer noopener')
  }
}

/**
 * 检查 URL 是否安全（允许相对路径、HTTP/HTTPS/mailto）
 */
function isSafeUrl(value: string) {
  if (value.startsWith('/') || value.startsWith('#')) {
    return true
  }

  try {
    const url = new URL(value)
    return ['http:', 'https:', 'mailto:'].includes(url.protocol)
  } catch {
    return false
  }
}

/* ================================================================
   暴露内部状态和方法给父组件
   ================================================================ */

defineExpose<{
  editor: typeof editor
  getHTML: () => string
}>({
  editor,
  getHTML: () => sanitizeHtml((editor.value as Editor | null)?.getHTML() || ''),
})
</script>

<style scoped>
/* ——— 编辑器外层容器 ——— */
.rich-editor {
  overflow: hidden;
  border: 4px solid #111111;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 6px 6px 0 #111111;
}

/* 只读模式降低不透明度 */
.rich-editor.is-disabled {
  opacity: 0.7;
}

/* ——— 编辑内容区域 ——— */
.rich-editor__content {
  min-height: 260px;
}

/* ProseMirror 是 TipTap 渲染的编辑区容器 */
.rich-editor__content :deep(.ProseMirror) {
  min-height: 260px;
  padding: 20px;
  outline: none;
  color: #111111;
  font-size: 17px;
  line-height: 1.7;
}

.rich-editor__content :deep(.ProseMirror p) {
  margin: 0 0 14px;
}

/* ——— 标题样式 ——— */
.rich-editor__content :deep(.ProseMirror h1),
.rich-editor__content :deep(.ProseMirror h2),
.rich-editor__content :deep(.ProseMirror h3) {
  margin: 20px 0 12px;
  line-height: 1.15;
}
.rich-editor__content :deep(.ProseMirror h1) { font-size: 34px; }
.rich-editor__content :deep(.ProseMirror h2) { font-size: 28px; }
.rich-editor__content :deep(.ProseMirror h3) { font-size: 22px; }

/* ——— 列表 ——— */
.rich-editor__content :deep(.ProseMirror ul),
.rich-editor__content :deep(.ProseMirror ol) {
  margin: 0 0 16px;
  padding-left: 28px;
}

/* ——— 引用 ——— */
.rich-editor__content :deep(.ProseMirror blockquote) {
  margin: 0 0 16px;
  padding: 10px 14px;
  border-left: 5px solid #2ec4b6;
  background: #f2fffd;
}

/* ——— 图片 ——— */
.rich-editor__content :deep(.ProseMirror img) {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 16px 0;
  border: 3px solid #111111;
  border-radius: 8px;
}

/* ——— 链接 ——— */
.rich-editor__content :deep(.ProseMirror a) {
  color: #005fcc;
  font-weight: 700;
}

/* ——— 空状态占位文字（TipTap Placeholder 扩展注入） ——— */
.rich-editor__content :deep(.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  float: left;
  height: 0;
  color: #8a94a6;
  pointer-events: none;
}
</style>