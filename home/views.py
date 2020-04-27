from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from django.contrib.auth.models import User
from blog.models import Post



# Html Pages

def home(request):
    return render(request,'home/home.html')


def about(request):
    return render(request ,'home/about.html')


def contact(request):
    if request.method=="POST":
        name =request.POST['name']
        email =request.POST['email']
        phone =request.POST['phone']
        content =request.POST['content']
        print(name,email,phone,content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<5 :
            messages.error(request,"Plese fill the form Correctly")
        else:
           contact =Contact(name=name ,email=email ,phone=phone, content=content)
           contact.save()
           messages.success(request,'Your message has been successfully sent')
    return render(request, 'home/contact.html')


def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsaddContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsaddContent)

    if allPosts.count() == 0:
        messages.warning(request, "No search results found.please refine Your query ")
    prams={'allPosts': allPosts , 'query':query}
    return render(request,'home/search.html',prams)


## Authencation APIS
def handlesignup(request):
    if request.method=="POST":
        ### get the post parameetar
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if len(username) >10:
            messages.error(request, " username must be under 10 characters ")
            return redirect('home')

        if  not username.isalunm():
            messages.error(request, " username should only contain latter and Number ")
            return redirect('home')

        if pass1 !=pass2:
            messages.error(request, " Password do not match")
            return redirect('home')


        ## Check for error news input
        ## Check for error news input
        ## create the user

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request , " Your AshuTechStudy Account has been successfully Created")
        return redirect('home')

    else:
        return HttpResponse("404 page not Found")


def handleLogin(request):
    if request.method =="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user =authenticate(username=loginusername , password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request,"succesfully logged In")
            return redirect('home')
        else:
            messages.error(request," invalid Credentials , Please try again")
            return redirect('home')


    return HttpResponse('404 :page not found')


def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully Logged Out")
    return redirect('home')






