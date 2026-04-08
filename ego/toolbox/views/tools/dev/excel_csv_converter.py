import base64
import logging
import os
import tempfile
from io import StringIO

from django.shortcuts import render
from django.utils.translation import gettext as _

from toolbox.views.core.context import build_tool_context

logger = logging.getLogger(__name__)


def excel_csv_converter_view(request):
    """Excel和CSV转换工具视图"""
    if request.method == "GET":
        return render(
            request,
            "toolbox/pages/tools/dev/excel_csv_converter.html",
            build_tool_context("excel_csv_converter"),
        )

    if request.htmx:
        action = request.POST.get("action")

        if action == "excel_to_csv":
            import pandas as pd

            if not request.FILES.get("excel_file"):
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("输入为空"), "error_message": _("请上传Excel文件")},
                )

            excel_file = request.FILES["excel_file"]
            sheet_name = request.POST.get("sheet_name", "0")

            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_file:
                    for chunk in excel_file.chunks():
                        temp_file.write(chunk)
                    temp_file_path = temp_file.name

                try:
                    df = pd.read_excel(temp_file_path, sheet_name=sheet_name)

                    csv_output = df.to_csv(index=False).encode("utf-8-sig")

                    os.unlink(temp_file_path)

                    context = {
                        "csv_output": csv_output.decode("utf-8-sig"),
                        "row_count": len(df),
                        "column_count": len(df.columns),
                    }
                    return render(request, "toolbox/partials/excel/excel_csv_result.html", context)

                except Exception as e:
                    if os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                    logger.error(f"Excel处理失败: {str(e)}")
                    return render(
                        request,
                        "toolbox/components/alert.html",
                        {
                            "error_title": _("Excel处理失败"),
                            "error_message": f"Excel处理失败: {str(e)}",
                        },
                    )

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
                logger.error(f"Excel处理错误: {str(e)}")
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {
                        "error_title": _("处理失败"),
                        "error_message": _("处理失败，请稍后重试"),
                    },
                )

        elif action == "csv_to_excel":
            from io import BytesIO

            import pandas as pd

            csv_input = request.POST.get("csv_input", "").strip()

            if not csv_input:
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {"error_title": _("输入为空"), "error_message": _("请输入CSV数据")},
                )

            try:
                df = pd.read_csv(StringIO(csv_input))

                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Sheet1")

                output.seek(0)
                excel_data = output.getvalue()

                excel_data_base64 = base64.b64encode(excel_data).decode("utf-8")

                context = {
                    "excel_data": excel_data_base64,
                    "row_count": len(df),
                    "column_count": len(df.columns),
                }
                return render(request, "toolbox/partials/excel/csv_excel_result.html", context)

            except Exception as e:
                logger.error(f"CSV处理失败: {str(e)}")
                return render(
                    request,
                    "toolbox/components/alert.html",
                    {
                        "error_title": _("CSV处理失败"),
                        "error_message": f"CSV处理失败: {str(e)}",
                    },
                )

    return render(
        request,
        "toolbox/pages/tools/dev/excel_csv_converter.html",
        build_tool_context("excel_csv_converter"),
    )


ROUTES = [
    ("excel-csv-converter/", excel_csv_converter_view, "excel_csv_converter", "excel_csv_converter"),
]
