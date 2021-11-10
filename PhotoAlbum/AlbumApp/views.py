import os
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from wsgiref.util import FileWrapper
from AlbumApp.models import Album,Photo
import magic

def gallery(request):
    user=request.user
    if user.is_authenticated:
        album = request.GET.get('album')
        print('album:',album)

        if album == None:
            photos = request.user.photo_set.all()
        else:
            photos = request.user.photo_set.filter(album__name=album)

        albums = request.user.album_set.all()

        if request.method == 'POST':
            data = request.POST
            print(data)
            if 'DeletePic' in data:
                print(data['DeletePic'])
                print(request.user.photo_set.get(id=data['DeletePic']).delete())
            elif 'DeleteAlbum' in data:
                print(data['DeleteAlbum'])
                print(request.user.album_set.get(id=data['DeleteAlbum']).delete())
            elif 'searchDesc' in data:
                #print(data['searchDesc'])
                photos = request.user.photo_set.filter(description__icontains=data['searchDesc'])
                
                print(photos)#if data['searchDesc'] in 
                #print(request.user.photo_set.get(id=27))
            else:
                print("Nope")
        

    if user.is_authenticated:
        context = {'albums':albums, 'photos':photos, 'user':user}
        return render(request,'photos/gallery.html',context)
    #print(context)
    return render(request,'photos/gallery.html')


def photo(request,pk):
    photo = request.user.photo_set.get(id=pk)
    allUsers = get_user_model().objects.all()
    print(allUsers)
    usersVis = []
    usersNotVis = []
    print(photo.user.all())
    #print(data['PhotoDescEdit'])
    if request.method == 'POST':
        data=request.POST
        photo.description=data['PhotoDescEdit']
        photo.save()
        print(data)

    for user in allUsers:
        if user != request.user:
            if user in photo.user.all():
                print("Vis:" ,user)
                usersVis.append(user)
            else:
                usersNotVis.append(user)
                print("Not vis:",user)
    
    for user in usersVis:
        if request.method == 'POST':
            if user.username in request.POST:
                print(user)


    for user in usersNotVis:
        if request.method == 'POST':
            if user.username in request.POST:
                if data[user.username] == 'on':
                    print(photo.user.add(user))


    context = {'usersVis':usersVis,'usersNotVis':usersNotVis,'photo':photo}
    return render(request,'photos/photo.html', context)


def add(request):
    albums = request.user.album_set.all()
    print(albums)
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')
        print('data:' , data)
        print('image:' , images)
        #print(request.user.album_set.create(name="Created in code 1"))
        #print(request.user.album_set.get(id=2))
        #print(request.user.photo_set.all())

        if data['album'] != 'none':
            album=request.user.album_set.get(id=data['album'])
        elif data['album'] != "":
            album , created = request.user.album_set.get_or_create(name = data['album_new'])
        else:
            album = None
        
        for image in images:
            photo = request.user.photo_set.create(
                album = album,
                description = data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'albums':albums}
    return render(request,'photos/add.html', context)

def download_file(request,pk):
    # fill these variables with real values
    photo = request.user.photo_set.get(id=pk)
    #print(photo.image.url)
    image_buffer = open('static'+photo.image.url, "rb").read()
    content_type = magic.from_buffer(image_buffer, mime=True)
    response = HttpResponse(image_buffer, content_type=content_type);
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename('static'+photo.image.url)
    return response