# uploader/views.py

import pandas as pd
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.conf import settings
import os

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)

        
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        try:
            if filename.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif filename.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                return render(request, 'upload.html', {
                    'message': 'Invalid file format. Please upload an Excel or CSV file.'
                })

            
            summary = df.describe()  
            summary_report = summary.to_string()  

            
            send_mail(
                subject=f'Python Assignment - Likesh barve',
                message=summary_report,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['tech@themedius.ai'],
                fail_silently=False,
            )

            return render(request, 'upload.html', {
                'file_url': file_url,
                'message': 'File uploaded and summary report emailed successfully!'
            })

        except Exception as e:
            return render(request, 'upload.html', {
                'message': f'Error processing file: {str(e)}'
            })
    return render(request, 'upload.html')
