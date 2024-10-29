from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..forms import FileFieldForm
from django.utils.decorators import method_decorator
from compress import PDFCompression
from compress.main import GenericFileType
from typing import List
import io
import zipfile
import asyncio
from asgiref.sync import sync_to_async

@method_decorator(csrf_exempt, name='dispatch')
class CompressView(View):


    @sync_to_async
    def compress_file(self, file: GenericFileType) -> None:
        pass


    def get(self, request):
        return HttpResponse('get no compress')
    
    async def post(self, request):
        print('POST: ', request.POST, 'FILES: ', request.FILES, 'TESTE: ', request.FILES.get('file'))
        form = FileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data['file']
            files_compressed: List[GenericFileType] = []
            corrutines = []

            with PDFCompression() as compress:
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for f in files:
                        pdf_stream = compress.build(file=f.read(), quality=50, name=f.name)
                        files_compressed.append(pdf_stream)
                        zip_file.writestr(f"{f.name}.pdf", pdf_stream.getvalue())
                zip_buffer.seek(0)

            response = HttpResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="files_compressed.zip"'    
        
            return response
        return HttpResponse(f'error: {form.errors}')