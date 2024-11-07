from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import todo_table , customersResetsId
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage



# Create your views here.
@login_required
def indexPage(req):
    all_todo = todo_table.objects.filter(user=req.user).order_by('-time_created') 
    completed_todo = todo_table.objects.filter(user=req.user, todo_status=True)
    uncompleted_todo = todo_table.objects.filter(user=req.user, todo_status=False)
    print(completed_todo)
    print(uncompleted_todo) 
    if req.method == 'POST':
        task = req.POST.get('task')
        create_todo = todo_table.objects.create(todo_name=task, user=req.user)
        create_todo.save()
        return redirect('home')
        
    return render(req , 'index.html' , {"all_todo" : all_todo})

def registerPage(req):
    if req.method == "POST":
        first_name = req.POST.get('first_name')
        last_name = req.POST.get('last_name')
        username = req.POST.get('username')
        email  = req.POST.get('email')
        password = req.POST.get('password')
        cpassword = req.POST.get('cpassword')

        duplicate_username = User.objects.filter(username=username)
        duplicate_email = User.objects.filter(email=email)

        if duplicate_username or duplicate_email:
            messages.error(req , 'user Already Exists')
            return redirect('login')
        elif password != cpassword:
            messages.error(req , 'Password are not the same')
        else:
            create_new_user = User.objects.create_user(first_name=first_name,last_name=last_name , username=username,email=email ,password=password)
            create_new_user.save()
            messages.success(req , 'Account Created succesfully')
            return redirect('login')            
    return render(req, 'register.html' ,{})

def loginPage(req):
    # get users input
    if req.method == 'POST':
        usernames = req.POST.get('username')
        password = req.POST.get('password')
    # confirm the user input with what we have in our database
        confirm_user = authenticate(username=usernames , password=password)
        if confirm_user is not None:
            login(req , confirm_user)
            return redirect('home')
        else:
            messages.error(req , 'Account does not Exist or Invalid User details')
    return render(req, 'login.html' ,{})

@login_required
def deleteView(req,todo_id):
    selected_todo = todo_table.objects.get(user=req.user,todo_id=todo_id)
    selected_todo.delete()
    return redirect('home')

@login_required
def updateStatus(req, todo_id):
    all_todo = todo_table.objects.filter(user=req.user).order_by('-time_created') 
    select_todo = todo_table.objects.get(user=req.user, todo_id=todo_id)
    if select_todo.todo_status == False:
        select_todo.todo_status = True
    else:
        select_todo.todo_status = False
    select_todo.save()    
    return redirect('home')       


def logoutView(req):
    logout(req)
    return redirect('login')


def ForgetPassword(req):
# check if the user exisist in our system
    if req.method == "POST":
        try:
            get_entred_email = req.POST.get('forget_password_email')
            check_user  =  User.objects.get(email=get_entred_email)
            new_password = customersResetsId(user=check_user)
            new_password.save()

            # create anew url that will be sent to teh user email adress
            password_reset_url =  reverse('resetpassword' , kwargs={"reset_id" : str(new_password.reset_id)})

            generate_full_url = f"{req.scheme}://{req.get_host()}{password_reset_url}"

            email_body = f"Kindly Use the Link below to Reset Your Password it Expires In Ten minutes \n\n\n {generate_full_url}"

            email_init_generator = EmailMessage(
                  "Reset Your Password",
                  email_body , 
                  settings.EMAIL_HOST_USER,
                  [get_entred_email],
            )

# incase you have an error let the mail fial without causeing issues to yoru code
            email_init_generator.fail_silently = True
            email_init_generator.send()

            return redirect("passwordresetsent" , reset_id=new_password.reset_id )
        except User.DoesNotExist:
            messages.error(req, "Invalid User")
            return redirect('forgetpassword')
    return render(req, 'forget_password.html')

def passwordResetSent(req , reset_id):
    # go to our datatbase and serch for a reset ID
    if customersResetsId.objects.filter(reset_id=reset_id):
        return render(req, 'password_reset_sent.html')
    else:
        messages.error(req, 'Invalid Request ID')
        return redirect('forgetpassword')


def resetPassword(req, reset_id):
    if req.method == "POST":
        user_password_reset_id = customersResetsId.objects.get(reset_id=reset_id)
        pasword = req.POST.get('password')
        confirm_password = req.POST.get('confirm_password')

        if pasword != confirm_password:     
            messages.error(req, "Your Passords do not Match")
            return redirect('resetpassword')
        if len(pasword) < 5:
            messages.error(req, "Pasword length is too chort")
            return redirect('resetpassword')
        
        # let check if the time it was created has expired
        # add ten minuted to the time from when it was created

        expire_time = user_password_reset_id.created + timezone.timedelta(minutes=10)  
        # 7:10  => 7:20


        if timezone.now() > expire_time:
            messages.error(req, "YOur Reset Id has Expired Try Gain")
            return redirect("forgetpassword")
        else:
            get_user = user_password_reset_id.user
            get_user.set_password(pasword)
            get_user.save()

            user_password_reset_id.delete()
            messages.success(req, "Congrats You can login now")
            return redirect('login')
    return render(req, 'reset_password.html')

def test(req):
    return render(req , "hello.html")


def edittask(req , todo_id):
    current_user = get_object_or_404(todo_table , user=req.user , todo_id=todo_id  )
    if req.method == "POST":
        new_todo_name = req.POST.get('todotask')

        # update the input with the one in the databse
        current_user.todo_name = new_todo_name
        current_user.save()
        return redirect('home')

