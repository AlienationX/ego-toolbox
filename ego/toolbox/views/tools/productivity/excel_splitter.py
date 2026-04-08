import logging
import time
import traceback
import zipfile
from pathlib import Path
from urllib.parse import quote

import pandas as pd
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext as _

from toolbox.views.core.context import build_tool_context

logger = logging.getLogger(__name__)


def excel_splitter_view(request):
    """Excel拆分工具主视图"""
    if request.method == "GET":
        return render(
            request,
            "toolbox/pages/tools/productivity/excel_splitter.html",
            build_tool_context("excel_splitter"),
        )

    # POST 请求处理文件拆分
    try:
        timestamp_seconds = int(time.time())
        # 设置并创建工作目录
        work_dir = Path(settings.MEDIA_ROOT) / "excel_splitter"
        work_dir.mkdir(parents=True, exist_ok=True)

        if request.htmx:
            # 处理文件预览
            uploaded_file = request.FILES.get("file")
            logger.info(f"Received file: {uploaded_file.name}")

            # 验证文件类型
            if not uploaded_file.name.endswith((".xlsx", ".xls")):
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("文件类型错误"), "error_message": _("请上传Excel文件(.xlsx或.xls)")},
                )

            # 验证文件大小
            max_size = 10 * 1024 * 1024  # 10MB
            if uploaded_file.size > max_size:
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("文件大小错误"), "error_message": _("文件大小不能超过10MB")},
                )

            file_path = work_dir / f"{timestamp_seconds}_{uploaded_file.name}"
            with open(file_path, "wb") as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)

            df = pd.read_excel(file_path)
            headers = list(df.columns)
            # TODO 获取所有sheet名称
            sheet_names = ["Sheet1", "Sheet2"]

            # 获取前5行数据
            preview_data = []
            for idx, row in df.head(5).iterrows():
                row_list = []
                for col in headers:
                    value = row[col]
                    # 处理NaN值
                    if pd.isna(value):
                        row_list.append("")
                    else:
                        row_list.append(str(value)[:100])  # 限制长度
                preview_data.append(row_list)

            context = {
                "headers": headers,
                "preview_data": preview_data,
                "total_rows": len(df),
                "sheet_names": sheet_names,
                "file_name": uploaded_file.name,
                "file_path": file_path,
            }
            return render(request, "toolbox/partials/excel/splitter_preview.html", context)

        else:
            # POST请求，处理拆分操作
            file_path = request.POST.get("file_path")
            split_field = request.POST.get("split_field")
            split_mode = request.POST.get("split_mode")
            name_prefix = request.POST.get("name_prefix")

            # 验证文件路径是否存在
            if not Path(file_path).exists():
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("文件不存在"), "error_message": _("请重新上传文件")},
                )

            df = pd.read_excel(file_path)
            # 验证拆分字段是否存在
            if split_field not in df.columns:
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("字段不存在"), "error_message": _("拆分字段不存在")},
                )

            # 生成唯一ID
            # unique_id = str(uuid.uuid4())[:8]
            unique_id = f"{timestamp_seconds}"

            if split_mode == "files":
                # 拆分为多个文件
                zip_path = _split_to_files(df, split_field, work_dir, unique_id, name_prefix)
            else:
                # 拆分为多个sheet
                zip_path = _split_to_sheets(df, split_field, work_dir, unique_id, name_prefix)

            # 读取ZIP文件内容并返回
            # 必须使用django的POST请求触发，htmx只能返回代码片段，无法返回下载文件
            with open(zip_path, "rb") as f:
                response = HttpResponse(f.read(), content_type="application/zip")
                # 同时提供 ASCII 兜底文件名 + RFC 5987 编码，避免浏览器回退成“下载.zip”
                filename = f"{Path(file_path).stem}.zip"
                encoded_filename = quote(filename)
                ascii_fallback = f"split_{unique_id}.zip"
                response["Content-Disposition"] = (
                    f"attachment; filename=\"{ascii_fallback}\"; filename*=UTF-8''{encoded_filename}"
                )
                return response

    except Exception as e:
        error_details = traceback.format_exc() if settings.DEBUG else str(e)
        context = {
            "error_title": _("处理失败"),
            "error_message": _("系统处理您的请求时遇到了问题，请稍后重试。"),
            "error_details": error_details,
            "debug": settings.DEBUG,
        }
        return render(
            request,
            "toolbox/partials/excel/splitter_preview.html",
            context,
        )


def _split_to_files(df, split_field, work_dir, unique_id, name_prefix):
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
            excel_filename = f"{name_prefix}_{safe_name}.xlsx" if name_prefix else f"{safe_name}.xlsx"
            excel_path = work_dir / excel_filename

            # 保存为Excel
            group_df.to_excel(excel_path, index=False, engine="openpyxl")

            # 添加到ZIP
            zf.write(excel_path, excel_filename)

            # 删除临时文件
            excel_path.unlink()

    return zip_path


def _split_to_sheets(df, split_field, work_dir, unique_id, name_prefix):
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
                .replace("]", "")
            )
            sheet_name = f"{name_prefix}_{safe_name}" if name_prefix else safe_name

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


ROUTES = [
    ("excel-splitter/", excel_splitter_view, "excel_splitter", "excel_splitter"),
]
