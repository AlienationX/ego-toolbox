from django.shortcuts import render


# 硬编码的工具数据
TOOLS = [
    {
        'id': 'todo',
        'title': '待办事项',
        'icon': '📝',
        'description': '管理您的待办事项列表，添加、编辑和完成任务',
        'url': 'todo',
        'color': '#4CAF50',
        'category': '效率',
        'tags': ['工具', '生产力'],
        'featured': True,
        'usage': 1234,
    },
    {
        'id': 'calculator',
        'title': '计算器',
        'icon': '🔢',
        'description': '简单易用的在线计算器，支持基本数学运算',
        'url': 'calculator',
        'color': '#2196F3',
        'category': '开发',
        'tags': ['工具', '数学'],
        'featured': False,
        'usage': 856,
    },
    {
        'id': 'timer',
        'title': '计时器',
        'icon': '⏱️',
        'description': '倒计时和正计时工具，帮助您管理时间',
        'url': 'timer',
        'color': '#FF9800',
        'category': '效率',
        'tags': ['工具', '时间管理'],
        'featured': True,
        'usage': 2341,
    },
    {
        'id': 'notes',
        'title': '笔记',
        'icon': '📄',
        'description': '快速记录和保存您的想法和笔记',
        'url': 'notes',
        'color': '#9C27B0',
        'category': '创意',
        'tags': ['工具', '记录'],
        'featured': False,
        'usage': 1892,
    },
    {
        'id': 'converter',
        'title': '单位转换',
        'icon': '🔄',
        'description': '长度、重量、温度等单位的快速转换工具',
        'url': 'converter',
        'color': '#00BCD4',
        'category': '开发',
        'tags': ['工具', '转换'],
        'featured': False,
        'usage': 567,
    },
    {
        'id': 'password',
        'title': '密码生成器',
        'icon': '🔐',
        'description': '生成安全、随机的密码',
        'url': 'password',
        'color': '#F44336',
        'category': '开发',
        'tags': ['工具', '安全'],
        'featured': True,
        'usage': 3456,
    },
    {
        'id': 'qrcode',
        'title': '二维码生成器',
        'icon': '📱',
        'description': '快速生成文本、链接的二维码',
        'url': 'qrcode',
        'color': '#795548',
        'category': '开发',
        'tags': ['工具', '二维码'],
        'featured': False,
        'usage': 1234,
    },
    {
        'id': 'color',
        'title': '颜色选择器',
        'icon': '🎨',
        'description': '选择颜色并获取对应的 HEX、RGB 值',
        'url': 'color',
        'color': '#E91E63',
        'category': '创意',
        'tags': ['工具', '设计'],
        'featured': False,
        'usage': 987,
    },
    {
        'id': 'markdown',
        'title': 'Markdown 编辑器',
        'icon': '📝',
        'description': '实时预览的 Markdown 编辑器，支持语法高亮',
        'url': 'markdown',
        'color': '#42A5F5',
        'category': '开发',
        'tags': ['工具', '编辑器'],
        'featured': False,
        'usage': 1456,
    },
    {
        'id': 'json',
        'title': 'JSON 格式化',
        'icon': '{}',
        'description': '格式化、验证和美化 JSON 数据',
        'url': 'json',
        'color': '#66BB6A',
        'category': '开发',
        'tags': ['工具', '数据'],
        'featured': False,
        'usage': 2341,
    },
    {
        'id': 'image',
        'title': '图片压缩',
        'icon': '🖼️',
        'description': '在线压缩图片，减小文件大小而不损失质量',
        'url': 'image',
        'color': '#EF5350',
        'category': '创意',
        'tags': ['工具', '图片'],
        'featured': False,
        'usage': 1876,
    },
    {
        'id': 'text',
        'title': '文本处理',
        'icon': '📋',
        'description': '文本大小写转换、去重、统计字数等实用功能',
        'url': 'text',
        'color': '#AB47BC',
        'category': '效率',
        'tags': ['工具', '文本'],
        'featured': False,
        'usage': 1123,
    },
]

def get_categories():
    """从 TOOLS 列表中提取所有唯一的分类"""
    categories = set()
    for tool in TOOLS:
        if 'category' in tool and tool['category']:
            categories.add(tool['category'])
    # 排序并加上"全部"选项
    return ['全部'] + sorted(list(categories))


def index(request):
    """首页视图，展示所有工具"""
    # 获取分类参数和搜索关键词
    category = request.GET.get('category', '全部')
    search_query = request.GET.get('q', '').strip()
    
    # 根据分类过滤工具
    if category == '全部':
        filtered_tools = TOOLS
    else:
        filtered_tools = [tool for tool in TOOLS if tool.get('category') == category]
    
    # 根据搜索关键词过滤
    if search_query:
        filtered_tools = [
            tool for tool in filtered_tools
            if search_query.lower() in tool['title'].lower() or 
               search_query.lower() in tool['description'].lower() or
               any(search_query.lower() in tag.lower() for tag in tool.get('tags', []))
        ]
    
    # 获取推荐工具（featured=True）
    featured_tools = [tool for tool in TOOLS if tool.get('featured', False)]
    
    # 获取最新工具（按 usage 排序，取前 6 个）
    latest_tools = sorted(TOOLS, key=lambda x: x.get('usage', 0), reverse=True)[:6]
    
    # 从 TOOLS 中动态获取分类列表
    categories = get_categories()
    
    # 统计信息
    total_tools = len(TOOLS)
    total_usage = sum(tool.get('usage', 0) for tool in TOOLS)
    
    context = {
        'tools': filtered_tools,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
        'featured_tools': featured_tools,
        'latest_tools': latest_tools,
        'total_tools': total_tools,
        'total_usage': total_usage,
    }
    return render(request, 'toolbox/index.html', context)


def tool_detail(request, tool_id):
    """工具详情页视图（占位页面）"""
    tool = next((t for t in TOOLS if t['id'] == tool_id), None)
    if tool is None:
        from django.http import Http404
        raise Http404("工具不存在")
    context = {
        'tool': tool,
    }
    return render(request, 'toolbox/tool_detail.html', context)
