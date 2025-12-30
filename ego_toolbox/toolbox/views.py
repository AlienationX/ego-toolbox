from django.shortcuts import redirect, render
from django.conf import settings
from django.utils.translation import activate, get_language
from .models import Todo


def index(request):
    """首页视图"""
    # 示例工具数据
    example_tools = [
        {
            'id': 'todo',
            'title': '待办事项',
            'description': '简单高效的待办事项管理工具，帮助你组织任务和提高效率。',
            'icon': '📝',
            'tags': ['效率工具'],
            'featured': True
        },
        {
            'id': 'calculator',
            'title': '计算器',
            'description': '功能齐全的在线计算器，支持基本运算和科学计算。',
            'icon': '🧮',
            'tags': ['实用工具'],
            'featured': True
        },
        {
            'id': 'notes',
            'title': '便签',
            'description': '快速记录灵感和想法的便签工具，支持实时保存。',
            'icon': '📄',
            'tags': ['效率工具'],
            'featured': False
        },
        {
            'id': 'timer',
            'title': '计时器',
            'description': '精确的计时器和倒计时工具，适用于各种场景。',
            'icon': '⏱️',
            'tags': ['实用工具'],
            'featured': False
        },
        {
            'id': 'converter',
            'title': '单位转换',
            'description': '支持多种单位之间的转换，包括长度、重量、温度等。',
            'icon': '🔄',
            'tags': ['实用工具'],
            'featured': True
        },
        {
            'id': 'password',
            'title': '密码生成',
            'description': '安全的密码生成器，帮助你创建强密码。',
            'icon': '🔐',
            'tags': ['安全工具'],
            'featured': False
        }
    ]
    
    # 分类数据
    categories = ['全部', '效率工具', '实用工具', '安全工具', '开发工具']
    
    # 获取当前分类和搜索关键词
    current_category = request.GET.get('category', '全部')
    search_query = request.GET.get('q', '')
    
    # 筛选工具
    filtered_tools = []
    for tool in example_tools:
        # 分类筛选
        if current_category != '全部' and current_category not in tool['tags']:
            continue
        # 搜索筛选
        if search_query:
            if search_query.lower() not in tool['title'].lower() and search_query.lower() not in tool['description'].lower():
                continue
        filtered_tools.append(tool)
    
    # 精选工具
    featured_tools = [tool for tool in example_tools if tool['featured']]
    
    # 总工具数和总使用次数（示例数据）
    total_tools = len(example_tools)
    total_usage = 12345
    
    context = {
        'featured_tools': featured_tools,
        'tools': filtered_tools,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'total_tools': total_tools,
        'total_usage': total_usage
    }
    
    return render(request, 'toolbox/index.html', context)


def tool_detail(request, tool_id):
    """工具详情视图"""
    # 示例工具数据（与index视图保持一致）
    example_tools = [
        {
            'id': 'todo',
            'title': '待办事项',
            'description': '简单高效的待办事项管理工具，帮助你组织任务和提高效率。',
            'icon': '📝',
            'tags': ['效率工具'],
            'featured': True
        },
        {
            'id': 'calculator',
            'title': '计算器',
            'description': '功能齐全的在线计算器，支持基本运算和科学计算。',
            'icon': '🧮',
            'tags': ['实用工具'],
            'featured': True
        },
        {
            'id': 'notes',
            'title': '便签',
            'description': '快速记录灵感和想法的便签工具，支持实时保存。',
            'icon': '📄',
            'tags': ['效率工具'],
            'featured': False
        },
        {
            'id': 'timer',
            'title': '计时器',
            'description': '精确的计时器和倒计时工具，适用于各种场景。',
            'icon': '⏱️',
            'tags': ['实用工具'],
            'featured': False
        },
        {
            'id': 'converter',
            'title': '单位转换',
            'description': '支持多种单位之间的转换，包括长度、重量、温度等。',
            'icon': '🔄',
            'tags': ['实用工具'],
            'featured': True
        },
        {
            'id': 'password',
            'title': '密码生成',
            'description': '安全的密码生成器，帮助你创建强密码。',
            'icon': '🔐',
            'tags': ['安全工具'],
            'featured': False
        }
    ]
    
    # 根据tool_id查找工具
    tool = next((t for t in example_tools if t['id'] == tool_id), None)
    
    if not tool:
        # 如果没有找到工具，重定向到首页
        return redirect('toolbox:index')
    
    return render(request, 'toolbox/tool_detail.html', {'tool': tool})


def todo_detail(request):
    """待办事项应用首页"""
    # 获取所有待办事项
    todos = Todo.objects.all()
    
    # 待办事项工具信息
    todo_tool = {
        'id': 'todo',
        'title': '待办事项',
        'description': '简单高效的待办事项管理工具，帮助你组织任务和提高效率。',
        'icon': '📝',
        'tags': ['效率工具'],
        'featured': True
    }
    
    return render(request, 'toolbox/todo_detail.html', {
        'tool': todo_tool,
        'todos': todos
    })


def todo_add(request):
    """添加待办事项"""
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title)
            
            # 获取最新的待办事项（用于HTMX响应）
            todo = Todo.objects.latest('id')
            return render(request, 'toolbox/partials/todo_item.html', {'todo': todo})
    return redirect('toolbox:todo_detail')


def todo_toggle(request, todo_id):
    """切换待办事项状态"""
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.completed = not todo.completed
        todo.save()
        return render(request, 'toolbox/partials/todo_item.html', {'todo': todo})
    except Todo.DoesNotExist:
        pass
    return redirect('toolbox:todo_detail')


def todo_delete(request, todo_id):
    """删除待办事项"""
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return render(request, 'toolbox/partials/todo_item.html', {'todo': todo, 'deleted': True})
    except Todo.DoesNotExist:
        pass
    return redirect('toolbox:todo_detail')


def custom_set_language(request):
    """自定义语言切换视图"""
    if request.method == 'POST':
        # 获取语言代码和跳转路径
        language = request.POST.get('language')
        next_path = request.POST.get('next', '/')
        
        # 激活选定的语言
        if language in [lang[0] for lang in settings.LANGUAGES]:
            activate(language)
            
        # 构建正确的跳转URL
        if language == 'zh-hans':
            # 切换到中文 - 移除/en/前缀
            if next_path.startswith('/en/'):
                next_path = next_path[4:]
        else:
            # 切换到英文 - 添加/en/前缀（如果没有的话）
            if not next_path.startswith('/en/'):
                next_path = f'/en{next_path}'
        
        # 重定向到正确的URL
        return redirect(next_path)
    
    # 如果是GET请求，直接重定向到首页
    return redirect('/')