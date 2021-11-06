from django.shortcuts import render, redirect
from .models import Album,Photo


def gallery(request):
    user=request.user
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
        else:
            print("Nope")
        


    context = {'albums':albums, 'photos':photos, 'user':user}
    #print(context)
    return render(request,'photos/gallery.html',context)


def photo(request,pk):
    photo = request.user.photo_set.get(id=pk)
    return render(request,'photos/photo.html', {'photo':photo})


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

