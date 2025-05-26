from django.http import HttpResponse, Http404
from .models import BinaryDocument


def admin_download_file(request, pk):
    try:
        doc = BinaryDocument.objects.get(pk=pk)
    except BinaryDocument.DoesNotExist:
        raise Http404("Файл не найден")

    content_type = _guess_content_type(doc.expansion)
    response = HttpResponse(doc.file_data, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{doc.name}.{doc.expansion}"'
    return response


def _guess_content_type(ext: str):
    mapping = {
        'txt': 'text/plain',
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }
    return mapping.get(ext.lower(), 'application/octet-stream')
