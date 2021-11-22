import os,magic,datetime,logging
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import get_user_model
from AlbumApp.models import Album,Photo
from PIL import Image

logger = logging.getLogger(__name__)

def gallery(request):
    user=request.user
    if user.is_authenticated:
        album = request.GET.get('album')

        if album == None:
            photos = request.user.photo_set.all()
        else:
            photos = request.user.photo_set.filter(album__name=album)

        albums = request.user.album_set.all()

        if request.method == 'POST':
            data = request.POST
            if 'DeletePic' in data:
                request.user.photo_set.get(id=data['DeletePic']).delete()
            elif 'DeleteAlbum' in data:
                request.user.album_set.get(id=data['DeleteAlbum']).delete()
            elif 'searchDesc' in data:
                photos = request.user.photo_set.filter(description__icontains=data['searchDesc'])
    else:
        logger.error("User was not authenticated")

    if user.is_authenticated:
        context = {'albums':albums, 'photos':photos, 'user':user}
        return render(request,'photos/gallery.html',context)
    else:
        logger.error("User was not authenticated")
    return render(request,'photos/gallery.html')

def photo(request,pk):
    photo = request.user.photo_set.get(id=pk)
    allUsers = get_user_model().objects.all()
    #print(allUsers)
    usersVis = []
    usersNotVis = []
    #print(photo.user.all())
    #print(data['PhotoDescEdit'])
    if request.method == 'POST':
        data=request.POST
        photo.description=data['PhotoDescEdit']
        photo.geolocation = data['GeolocationEdit']
        photo.tags = data['TagsEdit']
        if(data['captureDateEdit']!=''):
            date = datetime.date(int(data["captureDateEdit"][0:4]),int(data["captureDateEdit"][5:7]),int(data["captureDateEdit"][8:10]))
            photo.captureDate = date
        photo.capturedBy = data['CaptuedByEdit']
        photo.save()
        #print(data)

    for user in allUsers:
        if user != request.user:
            if user in photo.user.all():
                #print("Vis:" ,user)
                usersVis.append(user)
            else:
                usersNotVis.append(user)
                #print("Not vis:",user)
    
    #print("User set: ", photo.user.get(id=3))
    for user in usersVis:
        if request.method == 'POST':
            if user.username not in request.POST:
                photo.user.remove(user)
                return redirect('gallery')

    for user in usersNotVis:
        if request.method == 'POST':
            if user.username in request.POST:
                if data[user.username] == 'on':
                    photo.user.add(user)
                    return redirect('gallery')
    
    context = {'usersVis':usersVis,'usersNotVis':usersNotVis,'photo':photo}
    return render(request,'photos/photo.html', context)

def add(request):
    albums = request.user.album_set.all()
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['album'] != 'none':
            album=request.user.album_set.get(id=data['album'])
        elif data['album'] != "":
            album , created = request.user.album_set.get_or_create(name = data['album_new'])
            pass
        else:
            album = None
        
        date = datetime.date(int(data["captureDate"][0:4]),int(data["captureDate"][5:7]),int(data["captureDate"][8:10]))
        for image in images:
            try:
                im = Image.open(image)
                photo = request.user.photo_set.create(
                album = album,
                image=image,
                description = data['description'],
                geolocation = data['cityName'],
                tags = data['tags'],
                captureDate = date,
                capturedBy = data['capturedBy']
                )
            except:
                logger.error("The file format is not correct!")

        return redirect('gallery')

    context = {'albums':albums}
    return render(request,'photos/add.html', context)

def download_file(request,pk):
    try:
        logger.warning("Photo is being downloaded")
        photo = request.user.photo_set.get(id=pk)
        image_buffer = open('static'+photo.image.url, "rb").read()
        content_type = magic.from_buffer(image_buffer, mime=True)
        response = HttpResponse(image_buffer, content_type=content_type);
        response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename('static'+photo.image.url)
    except:
        logger.error("Photo failed to download")

    return response