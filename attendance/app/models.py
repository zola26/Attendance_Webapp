from django.db import models 
from django.db.models import JSONField
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.conf import settings
import os
import shutil
import traceback
from django.contrib.auth.models import User
import random
import string
from django.contrib.auth.hashers import make_password

class Student(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    starting_year = models.IntegerField()
    # total_attendance = models.IntegerField()
    # standing = models.CharField(max_length=1)
    year = models.IntegerField()
    last_attendance_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    # attendance_flag = models.BooleanField(default=True)
    previous_detection_times = JSONField(default=list) 
    email = models.EmailField()
    password = models.CharField(max_length=128, blank=True)  # Assuming a maximum length of 128 characters for the password
    # def save(self, *args, **kwargs):
           
    #     self.password = make_password(self.password)
     
    #     super().save(*args, **kwargs)
    
    

    def generate_student_report_pdf(self):
        pdf_filename = os.path.join('media', f"{self.name}_report.pdf")

        # Open the PDF file for writing
        with open(pdf_filename, 'wb') as pdf_file:
            pdf = canvas.Canvas(pdf_file)

            pdf.drawString(100, 800, f"Student Name: {self.name}")
            pdf.drawString(100, 780, "Previous Detection Times:")

            # Add previous detection times to the PDF
            for index, detection_time in enumerate(self.previous_detection_times):
                pdf.drawString(120, 760 - (index * 20), f"{index + 1}. {detection_time}")

            # Save the PDF file
            pdf.save()

        return pdf_filename
    

    def send_report_email(self, all_students):
        # Create a temporary directory to store individual PDF reports
        temp_dir = 'temp_reports'
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # Generate and save PDF reports for all students
            for student in all_students:
                pdf_filename = student.generate_student_report_pdf()

                # Ensure that the source file exists before copying
                if os.path.exists(pdf_filename):
                    student_pdf_path = os.path.join(temp_dir, f"{student.name}_report.pdf")

                    # Copy the generated PDF to the temp directory
                    shutil.copy(pdf_filename, student_pdf_path)

            # Compose the email
            subject = "Attendance Reports for All Students"
            message = "Please find the attached PDF reports for the attendance of all students."
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = ['ethiozele4443@gmail.com']  # Replace with the actual email address

            email = EmailMessage(subject, message, from_email, to_email)

            # Attach all individual PDF reports to the email
            for student in all_students:
                student_pdf_path = os.path.join(temp_dir, f"{student.name}_report.pdf")

                # Ensure that the source file exists before attaching
                if os.path.exists(student_pdf_path):
                    email.attach_file(student_pdf_path)

            email.send()

        finally:
            # Clean up: Remove the temporary directory and its contents
            shutil.rmtree(temp_dir)
    def __str__(self):
        return self.name

