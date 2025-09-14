
# Create your views here.
import fitz  # PyMuPDF
from django.http import HttpResponse
from django.shortcuts import render
from io import BytesIO




def compress_pdf(request):
    if request.method == "POST":
        uploaded_pdf = request.FILES['pdf']

        # Load the PDF into PyMuPDF
        pdf_document = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")

        # Create an in-memory output stream for the compressed PDF
        compressed_pdf = BytesIO()
        new_pdf_document = fitz.open()  # Create a new PDF document

        # Iterate through each page of the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # Render the page as a lower quality image
            pix = page.get_pixmap(matrix=fitz.Matrix(0.3, 0.3), alpha=False)  # Further reduce resolution
            
            # Convert Pixmap to JPEG bytes with lower quality
            jpeg_bytes = pix.tobytes("jpeg")  # Get the JPEG bytes
            
            # Create a new page in the new PDF and insert the JPEG image
            new_page = new_pdf_document.new_page(width=pix.width, height=pix.height)
            new_page.insert_image(new_page.rect, stream=jpeg_bytes)

        # Save the compressed PDF
        new_pdf_document.save(compressed_pdf, garbage=4, deflate=True)
        new_pdf_document.close()
        pdf_document.close()

        compressed_pdf.seek(0)  # Move to the beginning of the file

        # Send the compressed PDF as a downloadable response
        response = HttpResponse(compressed_pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="compressed_output.pdf"'
        return response

    return render(request, 'upload_pdf.html')





