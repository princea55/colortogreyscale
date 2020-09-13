from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from zipfile import ZipFile
from PIL import Image
import datetime 
from os import makedirs
import os
import shutil
# import glob
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        # files = glob.glob('/media')
        # for f in files:
        #     os.remove(f)
        # shutil.rmtree("media/")
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        
        with ZipFile(myfile, 'r') as zip:
            os.mkdir(os.path.join(os.getcwd()+"/media", 'ctg'))
            print('Extracting all the files now.............................')
            zip.extractall(path="media/ctg")
            print("Extracting done..........................")
            os.remove("media/"+myfile.name)
            print("upload file deleted..........................")
            
        def get_all_file_paths(directory):
            file_paths = []
            for root, directory, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_paths.append(file_path)
            print("ok..........................")
            return file_paths


        def rgb_to_greyscale(directory):
            os.mkdir(os.path.join(os.getcwd()+"/media", 'greyscale')) 
            for root, directory, files in os.walk("media/"+directory):
                print(root)
                print("root 6 ",root[6:])
                print("root 10 ",root[10:])
                makedirs("media/greyscale/"+root[10:], exist_ok=True) 
                for filename in files:
                    img = Image.open(root+"/"+filename).convert('LA').convert('RGB')
                    img.save("media/greyscale/"+root[10:]+"/"+filename)
            
        def main():
            
            directory = 'ctg/'
            rgb_to_greyscale(directory)
            zippath = 'media/greyscale/'
            filePaths = get_all_file_paths(zippath)
            
            with ZipFile("media/"+myfile.name,'w')as zip:
                for file in filePaths:
                    zip.write(file)
            
            print("zip created!!!..........................")
            shutil.rmtree(os.path.join(os.getcwd()+'/media', 'ctg'))
            shutil.rmtree(os.path.join(os.getcwd()+'/media', 'greyscale'))
            
            
        main()
        # filename = fs.save("custome"+myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'fileupload/fileupload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'fileupload/fileupload.html')