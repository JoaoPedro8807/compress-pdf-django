import aspose.words as aw
from typing import Any
import os
from pathlib import Path
import io

class Compress:
    def __init__(self, *args, **kwargs) -> None:
        ...

    def set_pdf_page_size(self, page_setup: Any, width: int, height: int) -> None:
        """ set size for any image in PDF """
        page_setup.page_width = width
        page_setup.page_height = height

    def compact(self,  
                file: bytes, 
                max_width: int = 1500, 
                max_height: int = 1500, 
                quality: int = 50,
                *args,
                **kwargs
                ) -> bytes:
        
        """ build the compact pdf, with quality params """
        
        pdf_read_options = aw.pdf2word.fixedformats.PdfFixedOptions()
        pdf_read_options.image_format = aw.pdf2word.fixedformats.FixedImageFormat.JPEG
        pdf_read_options.jpeg_quality = quality
        
        renderer = aw.pdf2word.fixedformats.PdfFixedRenderer()
        print('Compactando ....')
        #with open(file, 'rb') as pdf_stream: #open with write binary
        pdf_stream = io.BytesIO(file)
        aspose_image = renderer.save_pdf_as_images(pdf_stream, pdf_read_options)

        for i in range(0, len(aspose_image)): # loop for all pages in PDF, and rewrite 
            page_setup = self.builder.page_setup
            self.set_pdf_page_size(page_setup, max_width, max_height) #set the image size in current page

            page_image = self.builder.insert_image(aspose_image[i])

            self.set_pdf_page_size(page_setup, page_image.width, page_image.height) 
           
            page_setup.top_margin = 0 #clean all margins from image
            page_setup.left_margin = 0
            page_setup.bottom_margin = 0
            page_setup.right_margin = 0

            if i != len(aspose_image) - 1: # break increment in the last page 
                self.builder.insert_break(aw.BreakType.SECTION_BREAK_NEW_PAGE)

        pdf_output = io.BytesIO()
        self.builder.document.save(pdf_output, aw.SaveFormat.PDF)
        pdf_output.seek(0)

        return pdf_output
    



        