import base64
import logging
import os
import tempfile

from django.shortcuts import render
from django.utils.translation import gettext as _

from .catalog import get_nav_categories, get_tool_catalog

logger = logging.getLogger(__name__)


def excel_merger_view(request):
    """Excel文件合并工具视图"""
    all_tools = get_tool_catalog()
    tool = [x for x in all_tools if x["id"] == "excel_merger"][-1]

    if request.method == "GET":
        context = {
            "tool": tool,
            "nav_categories": get_nav_categories(all_tools),
        }
        return render(request, "toolbox/pages/excel_merger.html", context)

    if request.htmx:
        action = request.POST.get("action")
        merge_mode = request.POST.get("merge_mode", "horizontal")

        if action == "merge":
            import pandas as pd
            from openpyxl import load_workbook
            from io import BytesIO

            files = request.FILES.getlist("excel_files")

            if not files:
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("输入为空"), "error_message": _("请上传至少一个Excel文件")},
                )

            if len(files) < 2:
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("文件数量不足"), "error_message": _("请至少上传两个Excel文件进行合并")},
                )

            try:
                dfs = []
                sheet_name = request.POST.get("sheet_name", "0")

                for file in files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                        for chunk in file.chunks():
                            temp_file.write(chunk)
                        temp_file_path = temp_file.name

                    try:
                        df = pd.read_excel(temp_file_path, sheet_name=sheet_name)
                        dfs.append(df)
                    finally:
                        if os.path.exists(temp_file_path):
                            os.unlink(temp_file_path)

                if not dfs:
                    return render(
                        request,
                        "toolbox/components/alert.html",
                        {
                            "error_title": _("处理失败"),
                            "error_message": _("无法读取Excel文件数据"),
                        },
                    )

                if merge_mode == "horizontal":
                    merged_df = pd.concat(dfs, axis=1)
                else:
                    merged_df = pd.concat(dfs, axis=0, ignore_index=True)

                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    merged_df.to_excel(writer, index=False, sheet_name="Merged")

                output.seek(0)
                excel_data = output.getvalue()
                excel_data_base64 = base64.b64encode(excel_data).decode("utf-8")

                context = {
                    "excel_data": excel_data_base64,
                    "row_count": len(merged_df),
                    "column_count": len(merged_df.columns),
                    "file_count": len(files),
                    "merge_mode": merge_mode,
                }
                return render(request, "toolbox/partials/excel_merger_result.html", context)

            except ImportError as e:
                logger.error(f"缺少必要的库: {str(e)}")
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {
                        "error_title": _("服务器配置错误"),
                        "error_message": "服务器缺少必要的库，请联系管理员安装pandas和openpyxl",
                    },
                )
            except Exception as e:
                logger.error(f"Excel合并失败: {str(e)}")
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {
                        "error_title": _("合并失败"),
                        "error_message": f"Excel合并失败: {str(e)}",
                    },
                )

    return render(request, "toolbox/pages/excel_merger.html", context)
