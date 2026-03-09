import uuid
import zipfile
from pathlib import Path

import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .catalog import get_nav_categories, get_tool_catalog


def excel_splitter_view(request):
    """Excel拆分工具主视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "excel_splitter"][-1]

    if request.method == "GET":
        context = {
            "tool": tool,
            "nav_categories": get_nav_categories(all_tools),
        }
        return render(request, "toolbox/pages/excel_splitter.html", context)

    # POST 请求处理文件拆分
    try:
        if "file" not in request.FILES:
            return JsonResponse({"success": False, "error": _("请上传Excel文件")})

        uploaded_file = request.FILES["file"]
        split_field = request.POST.get("split_field", "")
        split_mode = request.POST.get("split_mode", "files")
        sheet_name_prefix = request.POST.get("sheet_name_prefix", "数据")

        # 验证文件类型
        if not uploaded_file.name.endswith((".xlsx", ".xls")):
            return JsonResponse({"success": False, "error": _("请上传Excel文件(.xlsx或.xls)")})

        # 验证拆分字段
        if not split_field:
            return JsonResponse({"success": False, "error": _("请选择拆分字段")})

        # 读取Excel文件
        df = pd.read_excel(uploaded_file)

        # 验证拆分字段是否存在
        if split_field not in df.columns:
            return JsonResponse({"success": False, "error": _("拆分字段不存在")})

        # 创建工作目录
        work_dir = Path(settings.MEDIA_ROOT) / "excel_splitter"
        work_dir.mkdir(parents=True, exist_ok=True)

        # 生成唯一ID
        unique_id = str(uuid.uuid4())[:8]

        if split_mode == "files":
            # 拆分为多个文件
            zip_path = _split_to_files(df, split_field, work_dir, unique_id)
        else:
            # 拆分为多个sheet
            zip_path = _split_to_sheets(df, split_field, work_dir, unique_id, sheet_name_prefix)

        # 读取ZIP文件内容并返回
        with open(zip_path, "rb") as f:
            from django.http import HttpResponse

            response = HttpResponse(f.read(), content_type="application/zip")
            response["Content-Disposition"] = f'attachment; filename="拆分文件_{unique_id}.zip"'
            return response

    except Exception as e:
        return JsonResponse({"success": False, "error": f"{_('处理失败')}: {str(e)}"})


def _split_to_files(df, split_field, work_dir, unique_id):
    """拆分为多个Excel文件，返回ZIP文件路径"""
    # 按字段分组
    grouped = df.groupby(split_field, sort=False)

    # 创建ZIP文件
    zip_filename = f"split_files_{unique_id}.zip"
    zip_path = work_dir / zip_filename

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for field_value, group_df in grouped:
            # 清理文件名（移除非法字符）
            safe_name = str(field_value).replace("/", "_").replace("\\", "_")[:50]
            excel_filename = f"{safe_name}.xlsx"
            excel_path = work_dir / excel_filename

            # 保存为Excel
            group_df.to_excel(excel_path, index=False, engine="openpyxl")

            # 添加到ZIP
            zf.write(excel_path, excel_filename)

            # 删除临时文件
            excel_path.unlink()

    return zip_path


def _split_to_sheets(df, split_field, work_dir, unique_id, sheet_name_prefix):
    """拆分为多个Sheet页，返回ZIP文件路径"""
    # 按字段分组
    grouped = df.groupby(split_field, sort=False)

    # 创建Excel文件，包含多个sheet
    excel_filename = f"split_sheets_{unique_id}.xlsx"
    excel_path = work_dir / excel_filename

    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        for field_value, group_df in grouped:
            # 清理sheet名称（Excel限制31字符，且不能包含某些字符）
            safe_name = (
                str(field_value)
                .replace("/", "_")
                .replace("\\", "_")
                .replace("?", "")
                .replace("*", "")
                .replace("[", "")
                .replace("]", "")[:31]
            )
            sheet_name = f"{sheet_name_prefix}_{safe_name}" if sheet_name_prefix else safe_name

            # 写入sheet
            group_df.to_excel(writer, sheet_name=sheet_name, index=False)

    # 创建ZIP文件（包含单个Excel文件）
    zip_filename = f"split_sheets_{unique_id}.zip"
    zip_path = work_dir / zip_filename

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(excel_path, excel_filename)

    # 删除临时Excel文件
    excel_path.unlink()

    return zip_path


@csrf_exempt
@require_http_methods(["POST"])
def excel_splitter_preview(request):
    """预览Excel文件内容"""
    try:
        if "file" not in request.FILES:
            return JsonResponse({"success": False, "error": _("请上传Excel文件")})

        uploaded_file = request.FILES["file"]

        # 验证文件类型
        if not uploaded_file.name.endswith((".xlsx", ".xls")):
            return JsonResponse({"success": False, "error": _("请上传Excel文件(.xlsx或.xls)")})

        # 读取Excel文件
        df = pd.read_excel(uploaded_file)

        # 获取表头
        headers = list(df.columns)

        # 获取前5行数据
        preview_data = []
        for idx, row in df.head(5).iterrows():
            row_dict = {"index": idx}
            for col in headers:
                value = row[col]
                # 处理NaN值
                if pd.isna(value):
                    row_dict[col] = ""
                else:
                    row_dict[col] = str(value)[:100]  # 限制长度
            preview_data.append(row_dict)

        # 获取sheet名称
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_name = excel_file.sheet_names[0] if excel_file.sheet_names else "Sheet1"

        return JsonResponse(
            {
                "success": True,
                "headers": headers,
                "preview": preview_data,
                "sheet_name": sheet_name,
                "total_rows": len(df),
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": f"{_('解析失败')}: {str(e)}"})
