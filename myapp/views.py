# import os
# import subprocess
# from django.shortcuts import render
# from django.conf import settings
# from django.http import HttpResponse
# from .forms import PDFUploadForm
# from datetime import datetime
# import re

# def safe_filename(original_filename):
#     """
#     Generates a safe filename based on the current date and time.
#     """
#     # Extract the file extension
#     extension = os.path.splitext(original_filename)[1]
    
#     # Get the current date and time
#     now = datetime.now()
#     timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
    
#     # Generate a safe filename
#     safe_name = f"up_{timestamp}{extension}"
    
#     return safe_name

# def handle_upload(request):
#     if request.method == 'POST':
#         form = PDFUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             pdf_file = form.cleaned_data['pdf_file']
#             split_size = form.cleaned_data['split_size']
#             dpi = form.cleaned_data['dpi']

#             upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
#             if not os.path.isdir(upload_dir):
#                 os.makedirs(upload_dir)

#             # Generate a safe filename
#             safe_pdf_filename = safe_filename(pdf_file.name)
#             pdf_path = os.path.join(upload_dir, safe_pdf_filename)
#             with open(pdf_path, 'wb+') as destination:
#                 for chunk in pdf_file.chunks():
#                     destination.write(chunk)

#             output_dir = os.path.join(settings.MEDIA_ROOT, 'output', os.path.splitext(safe_pdf_filename)[0])
#             if not os.path.isdir(output_dir):
#                 os.makedirs(output_dir)

#             python_executable = os.path.join(settings.BASE_DIR, 'Scripts', 'python.exe')

#             # Execute split.py
#             split_command = [
#                 python_executable,
#                 os.path.join(settings.BASE_DIR, 'myapp', 'scripts', 'split.py'),
#                 pdf_path,
#                 output_dir,
#                 str(split_size)
#             ]
#             result = subprocess.run(split_command, capture_output=True, text=True)
#             if result.returncode != 0:
#                 return HttpResponse(f"Error: {result.stderr}")

#             # Execute convert2img.py
#             convert_command = [
#                 python_executable,
#                 os.path.join(settings.BASE_DIR, 'myapp', 'scripts', 'convert2img.py'),
#                 output_dir,
#                 os.path.join(output_dir, 'img_output'),
#                 str(dpi)
#             ]
#             result = subprocess.run(convert_command, capture_output=True, text=True)
#             if result.returncode != 0:
#                 return HttpResponse(f"Error: {result.stderr}")

#             # Execute extractVision.py
#             vision_command = [
#                 python_executable,
#                 os.path.join(settings.BASE_DIR, 'myapp', 'scripts', 'extractVision.py'),
#                 os.path.join(output_dir, 'img_output'),
#                 os.path.join(output_dir, 'fromvision')
#             ]
#             result = subprocess.run(vision_command, capture_output=True, text=True)
#             if result.returncode != 0:
#                 return HttpResponse(f"Error: {result.stderr}")

#             # Execute txt2word.py
#             word_command = [
#                 python_executable,
#                 os.path.join(settings.BASE_DIR, 'myapp', 'scripts', 'txt2word.py'),
#                 os.path.join(output_dir, 'fromvision'),
#                 os.path.join(output_dir, os.path.splitext(safe_pdf_filename)[0] + '.docx')
#             ]
#             result = subprocess.run(word_command, capture_output=True, text=True)
#             if result.returncode != 0:
#                 return HttpResponse(f"Error: {result.stderr}")

#             return HttpResponse(f"Processing complete. Download your document <a href='{output_dir}/{os.path.splitext(safe_pdf_filename)[0]}.docx'>here</a>.")
#     else:
#         form = PDFUploadForm()

#     return render(request, 'upload.html', {'form': form})
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os
import subprocess
from .forms import PDFUploadForm
from datetime import datetime

def safe_filename(original_filename):
    """
    Generates a safe filename based on the current date and time.
    """
    extension = os.path.splitext(original_filename)[1]
    now = datetime.now()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")
    safe_name = f"up_{timestamp}{extension}"
    return safe_name

def handle_upload(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            split_size = form.cleaned_data['split_size']
            dpi = form.cleaned_data['dpi']

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            safe_pdf_filename = safe_filename(pdf_file.name)
            pdf_path = os.path.join(upload_dir, safe_pdf_filename)
            with open(pdf_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            output_dir = os.path.join(settings.MEDIA_ROOT, 'output', os.path.splitext(safe_pdf_filename)[0])
            os.makedirs(output_dir, exist_ok=True)

            python_executable = os.path.join(settings.BASE_DIR, 'Scripts', 'python.exe')

            # Run scripts and capture output
            scripts = [
                ('split.py', [pdf_path, output_dir, str(split_size)]),
                ('convert2img.py', [output_dir, os.path.join(output_dir, 'img_output'), str(dpi)]),
                ('extractVision.py', [os.path.join(output_dir, 'img_output'), os.path.join(output_dir, 'fromvision')]),
                ('txt2word.py', [os.path.join(output_dir, 'fromvision'), os.path.join(output_dir, safe_filename(pdf_file.name).replace('.pdf', '.docx'))])
            ]

            for script, args in scripts:
                command = [python_executable, os.path.join(settings.BASE_DIR, 'myapp', 'scripts', script)] + args
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode != 0:
                    return HttpResponse(f"Error in {script}: {result.stderr}")

            # Construct media URL
            docx_filename = safe_pdf_filename.replace('.pdf', '.docx')
            docx_file = os.path.join(output_dir, docx_filename)
            
            if not os.path.exists(docx_file):
                return HttpResponse("Error: The processed document was not found.")

            media_url = os.path.join(settings.MEDIA_URL, 'output', os.path.splitext(safe_pdf_filename)[0], docx_filename)
            
            return render(request, 'finished.html', {'media_url': media_url})
    else:
        form = PDFUploadForm()

    return render(request, 'upload.html', {'form': form})
