from django.shortcuts import render,redirect
from Student.models import StudentSection
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.utils import timezone
from datetime import datetime

from datetime import datetime

# dates in string format
str_d1 = '2023/5/20'
str_d2 = datetime.now()

# convert string to date object
d1 = datetime.strptime(str_d1, "%Y/%m/%d")
#d2 = datetime.strptime(str_d2, "%Y/%m/%d")

# difference between dates in timedelta
delta = str_d2 - d1
if delta.days > 30:
    print(f"Above One Mounth {delta.days}")
else:
    print(f"Under One Mounth {delta.days}")
# Create your views here.
def home_view(request):
    user = request.user
    
    #context ={"users":users}
    #user = request.user
    if user.is_authenticated: 
        users = StudentSection.objects.get(id=user.id)
        #last_login = request.session.get('last_login')
        #ul=StudentSection.objects.get('last_login')
        print(users.date_joined)
        st1 =users.date_joined
        #st2 = datetime.now().astimezone()
        st2 = timezone.now()
        t1= st1 
        #t11 = datetime.strptime(t1,"%Y/%m/%d %H:%M:%S")
    
        print("Last Login",t1.time())
        #t2 = datetime.strptime(st2,"%Y/%m/%d %H:%M:%S")
        t2=st2
        #t22 = datetime.strptime(t2,"%Y/%m/%d %H:%M:%S")
        print("Now time",t2.time())
        h= t2 - t1
        kt=h.total_seconds()  
        #kt=h.total_minute()
        print("total Seconed",kt)
        if kt <= 60:
            print("Note allwed")
            na = "አልተፈቀዳም"
            print(kt)
            check = 0
            context ={'na':na,'check':check}
            #if delta.days > 30:
                #print(f"Above One Mounth {delta.days}")
            #return render(request,'contact.html',context)
            #else:
            return render(request,'index.html',context)
                
    
        else:
            print("allwed")
            print(kt)
            na = "ተፈቅዶዋል"
            check = 1
            context ={'na':na,'check':check}
            #if delta.days > 30:
            #print(f"Above One Mounth {delta.days}")
            #return render(request,'contact.html',context)
            #else:
            return render(request,'index.html',context)
       
        
       
    else:
        
      return redirect("Student:newstudent")
 
def login_view(request, *args, **kwargs):
  context = {}

  user = request.user
        
  if user.is_authenticated:

    return redirect("Student:home")
    

  destination = get_redirect_if_exists(request)
  print("destination: " + str(destination))

  if request.POST:
    form = StudentAuthenticationForm(request.POST)
    if form.is_valid():

      student_id = request.POST['student_id']
      
      studentsection = authenticate(student_id=student_id,password=student_id)
           
      print("login",studentsection.student_id) 
            

      if studentsection:
        login(request, studentsection)
                
    
        if destination:
          if 'next' in request.POST:
            return redirect(request.POST.get('next'))
          else:
                  
            return redirect(destination)
            
        return redirect("Student:home")


  else:
    form = StudentAuthenticationForm()

  context['form']=form

  return render(request, "login.html", context)


def get_redirect_if_exists(request):
  redirect = None
  if request.GET:
    if request.GET.get("next"):
      redirect = str(request.GET.get("next"))
  return redirect

def logout_View(request):
    user = request.user.student_id
    StudentSection.objects.filter(student_id=user).update(date_joined=timezone.now())
    
   
   
   
    logout(request)
    return redirect("Student:home")