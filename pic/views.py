from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from pic.forms import UserForm,UserProfileForm,PictureForm,SearchForm
from django.contrib.auth.models import User
from pic.models import UserProfile,Photos,PhotoFollows,UserFollows,Comments
import datetime
import re
import os
import json


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
media_root = os.path.join(BASE_DIR, 'media')
static_url = os.path.join(BASE_DIR,'static')

def home(request):
    seaform=SearchForm(request.POST)
    if request.method == "POST":
      if request.POST.get("signin"):
        username = request.POST.get('username')
        password = request.POST.get('password')
        userauth = authenticate(username=username, password=password)
        if userauth:
            login(request,userauth)
            return HttpResponseRedirect("/piczzz/userhome/")
        else:
            return HttpResponse("Invalid login details supplied.")
      elif request.POST.get("search"):
        if seaform.is_valid():
            searchterm = seaform.cleaned_data["search"]
            termsplit = searchterm.split()
            picresults = []
            picobjs = Photos.objects.all()
            for term in termsplit:
                if len(term) > 1:
                    for pobj in picobjs:
                        if str(term).lower() in str(pobj.upload_photo).replace("photo/","").lower():
                            picnname = ' '.join([i.strip() for i in str(pobj.upload_photo).split('/')[-1].split('.')[:-1]])
                            pname = picnname.replace('_',' ').replace('-',' ')
                            picresults.append((pobj.upload_photo,pname))
            return render(request,"piczzz/search.html",{"media_profile":media_root,"checklog":"","picsearch":picresults})                    
            

            
    return render(request,"piczzz/home.html",{"search":seaform})


def signup(request):
    success = False
    if request.method == "POST":
        userdata  =  UserForm(data=request.POST)
        profiledata = UserProfileForm(data=request.POST)
        if userdata.is_valid() and profiledata.is_valid():
            userr=userdata.save()
            userr.set_password(userr.password)
            userr.save()
            profile = profiledata.save(commit=False)
            profile.user_id = userr
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()  
            success = True
    else:
        userdata = UserForm()
        profiledata = UserProfileForm()

    return render(request,"piczzz/signup.html",{"userdata":userdata,"success":success,"profiledata":profiledata})
    
def about(request):
    usercheck =  str(request.user)
    if usercheck != "AnonymousUser":
        checklog = "login"
    else:
        checklog = ""    
    return render(request,"piczzz/about.html",{"checklog":checklog})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/piczzz/')


def explore(request):
    usercheck =  str(request.user)
    if usercheck != "AnonymousUser":
        checklog = "login"
    else:
        checklog = ""
    popularuploads = Photos.objects.order_by('-follows','-comments_num','-date_time')[:5]
    picdatas =[]
    for eachpic in popularuploads:
        picnname = ' '.join([i.strip() for i in str(Photos.objects.get(id=eachpic.id).upload_photo).split('/')[-1].split('.')[:-1]])
        pname = picnname.replace('_',' ').replace('-',' ')
        userpic =  [Photos.objects.get(id=eachpic.id).upload_photo,pname]
        picdatas.append(userpic)
            
    return render(request,"piczzz/explore.html",{"pics":picdatas,"media_profile":media_root,"checklog":checklog})



@login_required
def userhome(request):
    seaform=SearchForm(request.POST)
    photouploads = False
    uploaded_pic = ""
    propic =UserProfile.objects.filter(user_id_id=request.user.id)
    propicfile = ""
    pname = ""
    if propic:
        propicfile = propic[0].profile_picture
    if request.method == "POST":
        picdata = PictureForm(data=request.POST)
        print request.POST
        if request.POST.get("search"):
            if seaform.is_valid():
                searchterm = seaform.cleaned_data["search"]
                termsplit = searchterm.split()
                userresults = []
                picresults = []
                userobjs = User.objects.all()
                picobjs = Photos.objects.all()
                for term in termsplit:
                    if len(term) > 1:
                        for uobj in userobjs:
                            if str(term).lower() in str(uobj.username).lower():
                                propic = UserProfile.objects.get(user_id_id=uobj.id).profile_picture
                                userresults.append((propic,uobj.username))
                        for pobj in picobjs:
                            if str(term).lower() in str(pobj.upload_photo).replace("photo/","").lower():
                                picnname = ' '.join([i.strip() for i in str(pobj.upload_photo).split('/')[-1].split('.')[:-1]])
                                pname = picnname.replace('_',' ').replace('-',' ')
                                picresults.append((pobj.upload_photo,pname))
                                
                return render(request,"piczzz/search.html",{"media_profile":media_root,"usersearch":userresults,"picsearch":picresults,"checklog":"login"})                    
        elif request.POST.get("submit"):

          if picdata.is_valid():
            picd  = picdata.save(commit=False)
                 
            
            if 'upload_photo' in request.FILES:
                picname = request.FILES['upload_photo']
                picnname = ' '.join([i.strip() for i in str(picname).split('/')[-1].split('.')[:-1]])
                pname = picnname.replace('_',' ').replace('-',' ')        
                picd.user_id = request.user
                picd.upload_photo = picname
                picd.save()
                uploaded_pic = picd.upload_photo
                photouploads=True
                return render(request,"piczzz/afterupload.html",{"media_profile":media_root,"picname":pname,"path":picd.upload_photo})
    else:
        picdata = PictureForm()
    fname = request.user.first_name
    lname = request.user.last_name
    fullname= fname+' '+lname
    email = request.user.email 
    following = len(UserFollows.objects.filter(from_user=request.user.id))
    followers = len(UserFollows.objects.filter(to_user=request.user.id))

    return render(request,"piczzz/userhome.html",{"following":following,"followers":followers,"fullname":fullname,"email":email,"media_profile":media_root,"profile_picture":propicfile,"picdata":picdata,"upload_success":photouploads,
"uploaded_pic":uploaded_pic,"search":seaform,"picname":pname})

@login_required
def youralbum(request):
        userphotos = Photos.objects.filter(user_id_id=request.user.id)
        uploadlist =[]
        if userphotos:
            uploadlist = [[i.upload_photo,' '.join([j.strip() for j in str(i.upload_photo).split('/')[-1].split('.')[:-1]]).replace('_',' ').replace('-',' ')] for i in userphotos]
            
        return render(request,"piczzz/youralbum.html",{"pics":uploadlist,"media_profile":media_root,})


def display(request,path):
        picname = path.strip('/').split('/')[-1]
        cfilename = path.strip('/')
        picinfo = Photos.objects.filter(upload_photo=cfilename)
        picfollows = picinfo[0].follows
        usercheck =  str(request.user)
        pcommentnum = picinfo[0].comments_num
        if picfollows == 1:
            follower = "follower"
        else:
            follower = "followers"
        ownerid = picinfo[0].user_id_id
        ownername = (User.objects.get(id=ownerid)).username    
        if usercheck != "AnonymousUser":          
            photofollow = PhotoFollows.objects.filter(user_id=request.user,photo_id=picinfo[0])
            if photofollow:
                followvalue = "unfollow"
            else:
                followvalue = "follow"
            
        else:
            followvalue = ""
        picnname = ' '.join([i.strip() for i in picname.split('.')[:-1]])
        pname = picnname.replace('_',' ').replace('-',' ')
        uploaddate = picinfo[0].date_time.strftime("%d-%m-%Y")                  
        return render(request,"piczzz/display.html",{"udate":uploaddate,"owner":ownername,"follower":follower,"followvalue":followvalue,"commentsnum":pcommentnum,"picfollows":picfollows,"picture":path,"picname":pname,"media_profile":media_root,"static_url":static_url})
   
@login_required
def followpic(request):
    picname=request.GET.get('iname','')
    followstatus = request.GET.get('followstats','')
    picname = picname.strip('/')
    picinfo = Photos.objects.get(upload_photo=picname)
    follownum = picinfo.follows
    if followstatus == "follow":
        
        photofollow = PhotoFollows(user_id=request.user,photo_id=picinfo)
        photofollow.save()
        newfollownum = len(PhotoFollows.objects.filter(photo_id=picinfo))
        picinfo.follows=newfollownum
        picinfo.save()
    else:
        
        photofollow = PhotoFollows.objects.filter(user_id=request.user,photo_id=picinfo)
        photofollow.delete()
        newfollownum  = len(PhotoFollows.objects.filter(photo_id=picinfo))      
        picinfo.follows=newfollownum
        picinfo.save()
    
    return HttpResponse(json.dumps({"follownum":newfollownum}))

    
@login_required
def comments(request):

    picname = request.GET.get('iname','')
    picname = picname.strip('/')
    picinfo = Photos.objects.get(upload_photo=picname)
    commenttext = request.GET.get('commentvalue')
    if commenttext:
        commentnum = picinfo.comments_num
        newcommentnum = commentnum+1
        commentsave = Comments(user_id=request.user,photo_id=picinfo)
        commentsave.save()
        datedata = commentsave.date_time.strftime("%d-%m-%Y")
        filename = str(request.user.id)+str(commentsave.date_time)
        fileopen = open(media_root+'/comment/'+filename+".txt",'w')
        fileopen.write(commenttext)
        fileopen.close()
        picinfo.comments_num = newcommentnum
        picinfo.save()
        cname = str(request.user)
        return HttpResponse(json.dumps({"commentnum":newcommentnum,"cname":cname,"datedata":datedata,"commentid":commentsave.id}))
    return HttpResponse(json.dumps({"commentnum":''}))      
    
@login_required
def loadcomments(request):
    
    picname = request.GET.get('iname','')
    picname = picname.strip('/')
    picinfo = Photos.objects.get(upload_photo=picname)
    commentpageno = request.GET.get('commentpagenumber','')
    commentnos1 = (int(commentpageno)-1)*10
    commentnos2=int(commentpageno) * 10
    commentslist = Comments.objects.filter(photo_id=picinfo).order_by('-date_time')
    commentlength =len(commentslist)
    lastflag = False
    
    selectcomments = commentslist[commentnos1:commentnos2]
    if commentlength == commentnos2 or len(selectcomments) < 10:
            lastflag = True
    else:
            lastflag = False
    commentlist = []
    
    for com in selectcomments:

        comname = com.user_id
        datedata = com.date_time.strftime("%d-%m-%Y")
        comfilename = str(com.user_id_id)+str(com.date_time).replace('+00:00','')
        comfiletext = open(media_root+'/comment/'+comfilename+".txt").read()
        if request.user.id == com.user_id_id:
            sameuser = True
        else:
            sameuser = False
        if request.user.id == picinfo.user_id_id:
            samepic = True
        else:
            samepic = False         
        comdict={"comname":str(comname),
                 "datedata":str(datedata),
                 "comtext":str(comfiletext),
                 "sameuser":sameuser,
                 "samepic":samepic,
                 "comid":com.id}
        commentlist.append(comdict)
        
    return HttpResponse(json.dumps({"commentlist":commentlist,"lastflag":lastflag}))

@login_required
def editcomment(request):
    optionto =request.GET.get('optionto','')
    if optionto == "edit":
        commentid = request.GET.get('clickid','')
        commentobj = Comments.objects.get(id=commentid)
        comfilename = str(commentobj.user_id_id)+str(commentobj.date_time).replace('+00:00','')
        comfiletext = open(media_root+'/comment/'+comfilename+".txt").read()
        changedcomment = request.GET.get('textcontent','')
        if str(comfiletext) == str(changedcomment):
            return HttpResponse(json.dumps({"changed":""}))
        else:
            datedatanew = datetime.datetime.now()
            datedatanewstr = datedatanew.strftime("%d-%m-%Y")
            fileopen = open(media_root+'/comment/'+comfilename+".txt",'w')
            fileopen.write(str(changedcomment))
            fileopen.close()    
            commentobj.date_time = datedatanew
            commentobj.save()
            newfilename = str(commentobj.user_id_id)+str(commentobj.date_time).replace('+00:00','')
            os.rename(media_root+'/comment/'+comfilename+".txt",media_root+'/comment/'+newfilename+".txt")
            return HttpResponse(json.dumps({"changed":"yes","date":datedatanewstr,"textcon":changedcomment}))
    elif optionto == "delete":
        commentid = request.GET.get('clickid','')
        commentobj = Comments.objects.get(id=commentid)
        photo_id = commentobj.photo_id_id
        comfilename = str(commentobj.user_id_id)+str(commentobj.date_time).replace('+00:00','')
        os.remove(media_root+'/comment/'+comfilename+".txt")
        commentobj.delete()
        photoobj = Photos.objects.get(id=photo_id)
        photoobj.comments_num = int(photoobj.comments_num)-1
        photoobj.save()
        return HttpResponse(json.dumps({"commentnum":str(photoobj.comments_num)}))



@login_required()
def accounts(request,path):
    userdetails = User.objects.get(username=path)
    uid = userdetails.id
    userpdetails = UserProfile.objects.get(user_id_id=uid)
    propic = userpdetails.profile_picture
    fname = userdetails.first_name
    lname = userdetails.last_name
    fullname= fname+' '+lname
    email = userdetails.email
    userphotos = Photos.objects.filter(user_id_id=uid)
    uploadlist =[]
    if userphotos:
        uploadlist = [[i.upload_photo,' '.join([i.strip() for i in str(i.upload_photo).split('/')[-1].split('.')[:-1]]).replace("_"," ").replace("-"," ")] for i in userphotos]
    following = len(UserFollows.objects.filter(from_user=uid))
    followers = len(UserFollows.objects.filter(to_user=uid))
    followvalue = UserFollows.objects.filter(from_user=request.user.id,to_user=uid)
    if followvalue:
        followval = "unfollow"
    else:            
        followval = "follow"
    if uid == request.user.id:
        visibility = "hidden"
    else:
        visibility = "visible"            
    return render(request,"piczzz/usersaccount.html",{"media_profile":media_root,"profile_picture":propic,"fullname":fullname,"email":email,"username":path,
        "uploadlist":uploadlist,"static_url":static_url,"following":following,"followers":followers,"followvalue":followval,"visibility":visibility})

@login_required
def followpeople(request):
    username=request.GET.get('uname','')
    followstatus = request.GET.get('followstats','')
    userinfo = User.objects.get(username=username.strip())
    if followstatus == "follow":
        userfollow = UserFollows(from_user=request.user.id,to_user=userinfo.id)
        userfollow.save()
    if followstatus == "unfollow":
        userfollow = UserFollows.objects.get(from_user=request.user.id,to_user=userinfo.id)
        userfollow.delete()    
    following = len(UserFollows.objects.filter(from_user=userinfo.id))
    followers = len(UserFollows.objects.filter(to_user=userinfo.id))
    return HttpResponse(json.dumps({"following":following,"followers":followers}))

@login_required
def peopleufollow(request):
    followpep = UserFollows.objects.filter(from_user=request.user.id)
    userdatas = []
    for eachpeople in followpep:
        usernam =  [User.objects.get(id=eachpeople.to_user).username,UserProfile.objects.get(user_id_id=eachpeople.to_user).profile_picture]
        userdatas.append(usernam)
    return render(request,"piczzz/followingpeople.html",{"media_profile":media_root,"userdatas":userdatas})    

@login_required
def picsufollow(request):
        followpics = PhotoFollows.objects.filter(user_id_id=request.user.id)
        picdatas =[]
        for eachpic in followpics:
            picnname = ' '.join([i.strip() for i in str(Photos.objects.get(id=eachpic.photo_id_id).upload_photo).split('/')[-1].split('.')[:-1]])
            pname = picnname.replace('_',' ').replace('-',' ')
            userpic =  [Photos.objects.get(id=eachpic.photo_id_id).upload_photo,pname]
            picdatas.append(userpic)
            
        return render(request,"piczzz/picsfollow.html",{"pics":picdatas,"media_profile":media_root,})
