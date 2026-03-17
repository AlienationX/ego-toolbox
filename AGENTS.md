# toolbox 项目自定义规则

Django + HTMX（django-htmx） + Alpine.js  + daisyUI（tailwind） 前后端一体全栈开发

## 项目概述

本项目是一个基于 django 开发的在线工具箱的WEB应用，支持用户注册登录，提供在线的工具箱功能，如：Excel转CSV、CSV转Excel等

htmx：处理服务端驱动的交互，通过 AJAX 获取 HTML 片段并局部更新 DOM，减少 JavaScript 代码
Alpine.js：处理客户端状态和交互，提供响应式数据、条件显示、事件处理等客户端逻辑

## 技术栈

- 框架：django（Python 3.12 + Django 6）
- 状态管理：django-session
- 网络请求：django-htmx
- 样式：SCSS，采用 BEM 命名规范
- UI组件库：daisyUI（tailwind）

## 代码规范

- 组件文件名使用 PascalCase，如 `GoodsList.vue`
- 页面文件放在 `pages/` 目录，按模块分子目录
- htmx交互的代码片段放在 `partials/` 目录下的对应页面文件中
- 公共组件放在 `components/` 目录
- 使用Pathlib处理文件路径，而不是os.path

## 注意事项

- 优先使用toolbox/static目录下的静态文件
- 优先纯前端实现功能。除了性能考虑和比较复杂的功能，其他功能都应在前端实现
- 前端布局采用daisyUI（tailwind）组件库，保持一致的外观和交互体验
- 前端布局采用响应式设计，适配不同屏幕尺寸
