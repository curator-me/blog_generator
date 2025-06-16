from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import Blog, Profile
from blogGenerator import settings
from groq import Groq

import assemblyai as aai
import yt_dlp, os, uuid, re


@login_required
def home(request):
    return render(request, "home.html")


def register_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            user = User.objects.create_user(
                username=username, email=email, password=password1
            )
            user.save()
            messages.success(request, "User created successfully!")
            login(request, user=user)
            return redirect("home")
        else:
            messages.error(request, "Passwords do not match.")
            render(request, "register.html")
    else:
        return render(request, "register.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            messages.success(request, "Login successfully")
            return redirect("home")
        else:
            messages.error(request, "Wrong Credential Info.")
            messages.error(request, "Please Try Again!")
            return render(request, "login.html")
    return render(request, "login.html")


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logout.../")
        return redirect("home")
    else:
        return redirect("home")
    

# blog views
def format_the_text(text):
    blog = new_text = re.sub(r'\*\*(.*?)\*\*', r'</p><h5>\1</h5><p>', text)
    return blog[4:-3]

def download_audio(url, user):
    filename = f"{user.username}_{uuid.uuid4().hex[:8]}"
    output_path = os.path.join(settings.MEDIA_ROOT, filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Downloaded file to:", output_path)
    return filename + ".mp3", output_path + ".mp3"


def generate_text(audiofile):
    filename = os.path.join(settings.MEDIA_ROOT, audiofile)
    aai.settings.api_key = "3779d873ea8c40e582e46c836fc721ec"
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(filename)

    return transcript.text


def generate_blog_from_text(text):  # used groq api
    prompt = f"Based on the following transcript from a YouTube video, \
        write a comprehensive blog article, write it based on the transcript, \
        but dont make it look like a youtube video, \
        make it look like a proper blog article:\n\n{text}\n\nArticle:\
            \n\n*note: After that edit the blog:\
            wrap each title or subtitle with <strong> </strong>\
            wrap each para with <p> </p>"
            
    # api_key = os.getenv("MY_KEY")
    client = Groq(api_key="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")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )
    generated_blog = chat_completion.choices[0].message.content
    return generated_blog


@login_required
def generate_blog(request):
    if request.method == "POST":
        yt_url = request.POST["youtube_url"]
        print("link to video ", yt_url)
        print(type(yt_url))
        

        with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
            info = ydl.extract_info(url=yt_url, download=False)
        title = info['title']

        filename, path_to_file = download_audio(yt_url, request.user)
        print("file name ", filename)
        
        transcripted_text = generate_text(path_to_file)
        if not transcripted_text:
            return JsonResponse({"error": "Faild to get transcript"}, status=509)
        blog = generate_blog_from_text(transcripted_text)
        blog = format_the_text(blog)
        new_blog = Blog.objects.create(
            title=title,
            blog=blog,
            created_by=request.user.username,
            author=request.user,
            url_link=yt_url,
            url_title=title,
        )
        new_blog.save()
        
        # print("here is the generated blog:")
        # print(blog)
        print(new_blog.title)
        print(new_blog.url_link)
        print("here the ", type(new_blog.url_link))

        data = {
            'title':title,
            'blog':blog,
        }

        return JsonResponse(data=data)
    else:
        return JsonResponse({"error": "Invalid request"}, status=409)


@login_required
def saved_blog(request, pk):
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=pk)
        return render(request, "blogs.html", {"blogs": blogs})
    return redirect("home")

@login_required
def show_blog(request, pk):
    blog = Blog.objects.get(id = pk);
    return render(request,'blog.html', {"blog":blog})

@login_required
def delete_blog(request, pk):
    pass


# profile views and edit
@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    print("info ")
    print(profile.first_name)
    return render(request, "profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.phone = request.POST['phone']
        user.email = request.POST['email']
        # profile.bio = request.POST['bio']
        profile.bio = request.POST.get('bio', '')

        user.save()
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    else:
        print("not post method")
    
    return render(request, 'edit.html', {"profile":profile})


def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if email == request.user.email:
            # send-password()
            return render(request, 'sent-done.html')
        else:
            messages(request, 'Please enter the correct email!!')
    return render(request, 'new_password.html', {'action' : 'reset'})


def new_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            request.user.password = password1
            # send email notification
            messages.success(request, 'Password change successfull')
            return redirect('login_user')
        else:
            messages.error(request, 'Password didn\'t match')

    return render(request, 'new_password')


@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['password']
        new_password1 = request.POST['password1']
        new_password2 = request.POST['password2']

        user = request.user

        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')

        if new_password1 != new_password2:
            messages.error(request, "New passwords do not match.")
            return redirect('change_password')

        user.set_password(new_password1)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Your password was successfully updated.")
        return redirect('profile') 

    return render(request, 'new_password.html', {'action': 'change'})


