import cv2
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
import os
import pickle
import face_recognition
import numpy as np
from datetime import datetime
import concurrent.futures
import json
from .models import Student
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz
import time
from .models import Student
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import pygame
pygame.mixer.init()
# Load encoding file once
print("Loading Encode File ...")
file_path = os.path.join('..', 'attendance', 'EncodeFile.p')
with open(file_path, 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")
latest_detected_person_image_url = None 
latest_detected_person_id = None
time_gap_in_seconds = None
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_view')
        else:
            # Handle invalid login
            return render(request, 'login_admin.html', {'error_message': 'Invalid login credentials'})
    else:
        # Handle GET request
        return render(request, 'login_admin.html')
def logout_admin(request):
    logout(request)
    return redirect('login_admin')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})
def view_report(request):
    students = Student.objects.all()
    return render(request, 'view_report.html', {'students': students})
def update_student(request, student_id):
    # Retrieve the specific student object by its ID
    student = get_object_or_404(Student, pk=student_id)
    
    if request.method == 'POST':
        # Populate the form with the existing student data and update it
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render a success message
            return redirect('sent_success')  # Replace 'success' with the name of your success URL
    else:
        # Populate the form with the existing student data
        form = StudentForm(instance=student)
    
    return render(request, 'update_student.html', {'form': form})
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to a success page or render a success message
            return redirect('sent_success')  # Replace 'success' with the name of your success URL
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

# def login_student(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         # Check if a student with the provided email exists
#         try:
#             student = Student.objects.get(email=email)
#             if student is not None:
                
#                 student = Student.objects.filter(email=email,password=password)
#                 if student.exists():
#                     print("Yeah")
#                     # return redirect('student_view')
#                     # id=Student.object.filter(email=email)
#                     student = Student.objects.all()
    
#                     return render(request, 'student_view.html',{'student':student})
#                 else:
#                     # If authentication fails, display an error message
#                     messages.error(request, 'Invalid email or password.')
#                     return render(request, 'login_student.html')

#             else:
#                 # If student does not exist, display an error message
#                 messages.error(request, 'Student with provided email does not exist.')
#                 return render(request, 'login_student.html')
                
#         except Student.DoesNotExist:
#             student = None

#         # If student exists, attempt to authenticate
        

#     else:
#         # If it's a GET request, render the login page
#         print("zele1")
#         return render(request, 'login_student.html')
    
def detect_faces(frame):
    global latest_detected_person_image_url, latest_detected_person_id, time_gap_in_seconds
    imgS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    
    detected_faces = []
    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            student_id = studentIds[matchIndex]
            student = get_object_or_404(Student, id=studentIds[matchIndex])

            detected_faces.append({
                'location': faceLoc,
                'student_id': studentIds[matchIndex],
                'image_url': student.image.url,
                'name': student.name,
          
            })
            # # from datetime import datetime, timedelta
            # attendance_start_time = datetime.strptime('07:00:00', '%H:%M:%S').time()
            # last_recorded_time = student.last_attendance_time.time()
            # # time_now = datetime.now().time()
            # last_attendance_diff = datetime.combine(datetime.today(), last_recorded_time) - datetime.combine(datetime.today(), attendance_start_time)
            # time_gap_in_seconds = last_attendance_diff.total_seconds()
            # if  time_gap_in_seconds< 86400:
            #     print('alredy')
            #     latest_detected_person_image_url = student.image.url
            #     latest_detected_person_id = student_id
            #     play_sound_failur()
            #     print("person already detected")
            # else:
            #     print('success')
            #     student.last_attendance_time = timezone.now().astimezone(pytz.timezone('Africa/Nairobi'))
            #     # Update the previous_detection_times field with the new datetime
            #     student.previous_detection_times.insert(0, timezone.now().astimezone(pytz.timezone('Africa/Nairobi')).isoformat())
            #     # Keep only the last 7 detection times
            #     student.previous_detection_times = student.previous_detection_times[:30]
            #     student.save()
            #     latest_detected_person_image_url = student.image.url
            #     latest_detected_person_id = student_id
            #     play_sound_success()
            #     print("Known Face Detected")
            #     print(studentIds[matchIndex])
            #     print("Image URL:", student.image.url)
            #     print("Student Name:", student.name)
            #     print("Time:", student.last_attendance_time)
            #     print("person detected successfuly")
                
            print(student.last_attendance_time)
            last_recorded_time = student.last_attendance_time
            time_now = timezone.now()
            print(time_now)
            time_gap = time_now - last_recorded_time
            time_gap_in_seconds = time_gap.total_seconds()
            print(time_gap_in_seconds)
            if time_gap_in_seconds <= 120:
                latest_detected_person_image_url = student.image.url
                latest_detected_person_id = student_id
                play_sound_failur()
                print("person already detected")
            else:
                student.last_attendance_time = timezone.now().astimezone(pytz.timezone('Africa/Nairobi'))
                # Update the previous_detection_times field with the new datetime
                student.previous_detection_times.insert(0, timezone.now().astimezone(pytz.timezone('Africa/Nairobi')).isoformat())
                # Keep only the last 7 detection times
                student.previous_detection_times = student.previous_detection_times[:30]
                student.save()
                latest_detected_person_image_url = student.image.url
                latest_detected_person_id = student_id
                play_sound_success()
                print("Known Face Detected")
                print(studentIds[matchIndex])
                print("Image URL:", student.image.url)
                print("Student Name:", student.name)
                print("Time:", student.last_attendance_time)
                print("person detected successfuly")
            
          
 
    return detected_faces

def generate_frames():
    cap = cv2.VideoCapture('https://192.168.0.2:8080/video')#'https://192.168.0.6:8080/video'
    # cap = cv2.VideoCapture(f'http://{ip_address}:8080/video')
    start_time = time.time()
    interval = 10  # Interval for face detection
    detect_faces_flag = True

    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                elapsed_time = time.time() - start_time

                if elapsed_time < 10:
                    resized_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                    ret, jpeg = cv2.imencode('.jpg', resized_frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
                    continue

                if detect_faces_flag:
                    # Resize frame and submit face detection task
                    resized_frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                    future = executor.submit(detect_faces, resized_frame)

                    # Wait for face detection result
                    detected_faces = future.result()

                    # Draw rectangles around detected faces
                    for face_details in detected_faces:
                        y1, x2, y2, x1 = face_details['location']
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)

                # Encode frame and yield it
                ret, jpeg = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

                # Toggle face detection every 10 seconds
                if elapsed_time % interval < 0.3:  # A small buffer for time discrepancy
                    detect_faces_flag = not detect_faces_flag

    finally:
        cap.release()
            
            
@csrf_exempt
def update_detected_person_image(request):
    global latest_detected_person_image_url, latest_detected_person_id,time_gap_in_seconds
    

    if latest_detected_person_id is not None:
        try:
            student = Student.objects.get(id=latest_detected_person_id)
            data = {
                'image_url': latest_detected_person_image_url,
                'name': student.name,
                'attendance_status': True if time_gap_in_seconds > 120 else False,
            }
        except Student.DoesNotExist:
            data = {
                'image_url': latest_detected_person_image_url,
                'name': 'Unknown'  # Provide a default name or handle the case when the student is not found
            }
    else:
        data = {
            'image_url': '',
            'name': 'Unknown'
        }

    return JsonResponse(data)
def play_sound_success():
    pygame.mixer.music.load('static/audio/success.mp3')
    pygame.mixer.music.play()
def play_sound_failur():
    pygame.mixer.music.load('static/audio/already_detected.mp3')
    pygame.mixer.music.play()
# def report_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None and user.is_superuser:
#             login(request, user)
#             return redirect('send_all_reports')
#         else:
#             # Handle invalid login
#             return render(request, 'report_login.html', {'error_message': 'Invalid login credentials'})

#     # Handle 'GET' request by rendering the login page
#     return render(request, 'report_login.html')

def generate_student_report(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    pdf_filename = student.generate_student_report_pdf()
    
    # Send the report via email
    

    with open(pdf_filename, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={student.name}_report.pdf'

    return response


def send_all_reports(request):
    all_students = Student.objects.all()
    
    # Use the send_report_email method to send reports for all students to one email
    student = all_students[0]  # Use any student to access the method
    student.send_report_email(all_students)

    return redirect('sent_success')

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type="multipart/x-mixed-replace;boundary=frame")
# def connect_webcam(request):
#     if request.method == 'POST':
#         ip_address = request.POST.get('ip_address')
#         # Redirect to index.html with the IP address as a query parameter
#         return render(request, 'index.html', {'ip_address': ip_address})
#     else:
#         return render(request, 'connect_webcam.html')
# def video_feed(request):
#     ip_address = request.GET.get('ip_address')  # Get IP address from query parameter
#     if ip_address:
#         # cap = cv2.VideoCapture(f'http://{ip_address}:8080/video')
#         # # Rest of your video processing logic
#         return StreamingHttpResponse(generate_frames(ip_address), content_type="multipart/x-mixed-replace;boundary=frame")
#     else:
#         return HttpResponse("IP address not provided!")
# def cam_connect(request):
    
#     return render(request, 'connect_webcam.html')  
    
def index(request):
    if request.user.is_authenticated:
        # ip_address = request.GET.get('ip_address')  # Get the IP address from the query string
        return render(request, 'index.html')  
    else:
        return render(request, 'login_admin.html')
def admin_view(request):
    user = request.user
    if request.user.is_authenticated:
        return render(request, 'admin_view.html')
    else:
        return render(request, 'login_admin.html')
def home(request):
    return render(request, 'home.html')
def sent_success(request):
    return render(request, 'successfully_sent.html')    
    
      
    