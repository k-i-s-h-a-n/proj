from django.shortcuts import render
from django.contrib.auth import logout,authenticate,login
from django.shortcuts import redirect
import os



import cv2
import numpy as np
from Teachers import utlis
from Teachers import new_utils
from Teachers import read_qr_and_scan
import glob



from django.contrib.auth.decorators import login_required


# Create your views here.

def bulana():
    import os
    import uuid
    from django.conf import settings
    unique_omrfolder_name = uuid.uuid4().hex
    upload_folder = os.path.join(settings.MEDIA_ROOT, unique_omrfolder_name)
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
            
                # print("!!!!!!!!!!! : ",upload_folder)
                # path = r"C:\Users\kishf\OneDrive\Desktop\OMR\env\Scripts\ExamSystem\media\c4c2d01773974a829e23a83a0772fc35"
    filename = upload_folder.split('\\')[-1]
                # print("@@@@@@@@@@@ ",filename)
            # print("K I S H A N     B H A I   F U N C T I O N    K     A N D H A R")

    return filename






# ___________________________________________________

# S I G N U P
from .forms import SignUpForm
def sign_up(request):
    if request.method=="POST":
        fm=SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account Created Successfully !! ')
            fm.save()
            return redirect('/login')
    else:
        # print("else----------------")
        fm=SignUpForm()
    return render(request,'enroll/signup.html',{'form':fm})


# L O G I N
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
def teachers_login(request):
    if not  request.user.is_authenticated:
        if request.method=="POST":
            fm=AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                teachers_username=fm.cleaned_data['username']
                teachers_password=fm.cleaned_data['password']
                user=authenticate(username=teachers_username,password=teachers_password)
                if user is not None:
                    login(request,user)
                    if request.GET.get('next',None):
                        return redirect(request.GET['next'])
                        
                    # messages.success(request,'Logged in successfully !! ')
                    request.session['teacher_id']=user.id
                    request.session['teacher_username']=user.username
                    return redirect("/")
        else:
            # print("else----------------")
            fm=AuthenticationForm()
        return render(request,'enroll/teacherslogin.html',{'form':fm})
    else:
        return redirect('/')




# L O G O U T
def teachers_logout(request):
    logout(request)
    return redirect('/login')



def index(request):
    if request.user.is_authenticated:
        print('HHH you are : ',request.session.get('teacher_username'))
        return render(request,'index.html')
    else:
        return redirect("/login")


# ___________________________________________________






# def loginuser(request):
#     if request.method=="POST":
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:            
#             # A backend authenticated the credentials
#             login(request,user)
#             return redirect('/')
#         else:
#             # No backend authenticated the credentials
#             return render(request,'login.html')

#     return render(request,'login.html')


# def questions(request):
#     return render(request,'questions.html')


# def logoutuser(request):
#     logout(request)
#     return redirect("/login")



# --------------------QUESTION PAPER DOWNLOAD------------------------
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO


@login_required(login_url="/login")
def generate_pdf(request):
    # Render the HTML template to a string
    html = render_to_string('questions.html')

    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Generate the PDF using the buffer
    pisa.CreatePDF(html, dest=buffer)

    # Use the buffer content to create a PDF response
    pdf = buffer.getvalue()
    buffer.close()

    # Set the content type of the response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="questions.pdf"'
    return response






# --------------------OMR PAPER UPLOAD------------------------
from django.shortcuts import redirect, render  
from .forms import ImageForm
from .models import Image  

@login_required(login_url="/login")
def upload_image(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = ImageForm()
    return render(request, "upload_image.html", {"form": form})










@login_required(login_url="/login")
def success(request):
    return HttpResponse("Image uploaded successfully")



@login_required(login_url="/login")
def omr(request):
    return render(request,"omr_generation.html")


from django.contrib import messages
def search(request):
    if request.method == 'POST':
        exam_center = request.POST['exam_center']
        Exam_name = request.POST['exam_name']
        classes = request.POST['classes']
        subject = request.POST['subject']
        if not (exam_center or classes or subject or Exam_name):
            messages.error(request, 'Please provide Details')
            return redirect('search')
        elif not Exam_name:
            messages.error(request, 'Please provide Exam name')
            return redirect('search')
        elif not exam_center:
            messages.error(request, 'Please provide Exam center')
            return redirect('search')
        elif not classes:
            messages.error(request, 'Please provide Class')
            return redirect('search')
        elif not subject:
            messages.error(request, 'Please provide Subject')
            return redirect('search')
        return redirect('search_results', exam_center=exam_center,Exam_name=Exam_name,classes=classes,subject=subject)
    return render(request, 'search.html')









######################################
####################################
###################################




from django.contrib import messages
@login_required(login_url="/login")
def scan_search(request):
    if request.method == 'POST':
        exam_center = request.POST['exam_center']
        classes = request.POST['classes']
        subject = request.POST['subject']
        exam_name=request.POST['exam_name']
        if not (exam_center or classes or subject or exam_name):
            messages.error(request, 'Please provide Details')
            return redirect('scan_search')
        elif not exam_center:
            messages.error(request, 'Please provide Exam center')
        elif not exam_name:
            messages.error(request, 'Please provide Exam name')
            return redirect('scan_search')
        elif not classes:
            messages.error(request, 'Please provide Class')
            return redirect('scan_search')
        elif not subject:
            messages.error(request, 'Please provide Subject')
            return redirect('scan_search')
        return redirect('rrr', exam_center=exam_center,exam_name=exam_name,classes=classes,subject=subject)
    return render(request, 'scan_omr/scan_search.html')




@login_required(login_url="/login")
def scan_search_results(request, exam_center,exam_name,classes,subject):
    # perform search based on exam_center an classes
    data = Qr.objects.filter(center_code=exam_center,Exam_name=exam_name,classes=classes,subject=subject)
    
   
    # print(data)
    url = f"/upload/{exam_center}/{exam_name}/{classes}/{subject}"
    context={
        "data":data,
        "url":url
    }

    if not data:
        # return HttpResponse("NO data found")
        return render(request,"no_data_found.html")
        
    return render(request, 'upload.html',context)


######################################
####################################
###################################









@login_required(login_url="/login")
def search_results(request, exam_center,Exam_name,classes,subject):
    # perform search based on exam_center an classes
    data = Qr.objects.filter(center_code=exam_center,Exam_name=Exam_name,classes=classes,subject=subject)
    
   
    # print(data)
    url = f"/omr_gen_dow/{exam_center}/{Exam_name}/{classes}/{subject}"
    context={
        "data":data,
        "url":url
    }

    if not data:
        # return HttpResponse("NO data found")
        return render(request,"no_data_found.html")
        
    return render(request, 'search_results.html',context)












############# A D D I N G    D A T A  ################
@login_required(login_url="/login")
def add_data(request):
    if request.method=="POST":
        Exam_name=request.POST.get('exam_name')
        Exam_id=request.POST.get('exam_id')
        Name=request.POST.get('name')
        Roll_no=request.POST.get('roll_no')
        classes=request.POST.get('classes')
        section=request.POST.get('section')
        center_code=request.POST.get('center_code')
        subject=request.POST.get('subject')
        add_data=Qr(Exam_name=Exam_name,Exam_id=Exam_id,Name=Name,Roll_no=Roll_no,classes=classes,section=section,center_code=center_code,subject=subject)
        add_data.save()
        messages.success(request, 'Your response has been recorded!')
        
    return render(request,'add_data.html')

##############################################







############### D O W N L O A D I N G ############





#################### O M R   G E N E R A T I O N ####################################

from .models import Qr
@login_required(login_url="/login")


def     omr_gen_dow(request,center_code,Exam_name,classes,subject):
    try:      
        import qrcode
        from PIL import Image
        import img2pdf
        import os
        import shutil
        print("OMR GENERATION")
        
        # deleting the media/media path contents as to clear all the previous generated pdf's

        # Specify the path of the folder
        # folder_path = "media/media"
        folder_path="ExamSystem/media/media"
        print("3 8 9")
        

        # Iterate over the contents of the folder
        for filename in os.listdir(folder_path):
            print("3 9 4")
            file_path = os.path.join(folder_path, filename)
            print("3 9 5")
            if os.path.isfile(file_path):
                # Delete individual files
                os.remove(file_path)
                print("3 9 9")
            elif os.path.isdir(file_path):
                # Recursively delete subfolders
                shutil.rmtree(file_path)
        print("K I S H A N ")
        # Create a dictionary of the fields and their values
        qr_objects = Qr.objects.filter(center_code=center_code,Exam_name=Exam_name,classes=classes,subject=subject)
        print('4 0 7')

        qr_only=bulana()
        
        omrs=bulana()
        


        for student in qr_objects:
            fields = {
                'Exam name':student.Exam_name,
                'Exam ID':student.Exam_id,
                'Name': student.Name,
                'Roll No':student.Roll_no,
                'Class': student.classes,
                'Section': student.section,
                'Exam code':student.center_code,
                'Subject':student.subject,
            }

            # Convert the dictionary to a string
            data = '\n'.join([f"{key}: {value}" for key, value in fields.items()])
            print('4 2 9')

            # print("D A T A = ",data)

            # Generate the QR code
            qr_img = qrcode.make(data)

            # Load the qr_template image
            # bg_img = Image.open('omr24april.jpg')
            bg_img = Image.open('ExamSystem/omr24april.jpg')
            
            print('4 3 8')


            # Resize the QR code image to fit the student image
            qr_img = qr_img.resize((250, 250))

            # Calculate the position to paste the QR code image onto the student image
            x = bg_img.width - qr_img.width - 1000
            y = bg_img.height - qr_img.height - 90

            # Paste the QR code image onto the student image
            bg_img.paste(qr_img, (x, y))

            
            
            
            
            
            # Save the QR code as a PNG file with the name of the class name and student roll number
            # filename = f"media/qr_only/{student.Exam_name}_{student.Roll_no}.jpg"
            print("K I S H A N     B H A I")
            new_qr_only=qr_only.split("/")
            qr_only=new_qr_only[-1]
            # print(qr_only)
            filename = f"ExamSystem/media/{qr_only}/{student.Exam_name}_{student.Roll_no}.jpg"
            bg_img.save(filename)


            print("K I S H A N    4 5 1")
            #Printing Name and Roll no
            # from PIL import Image
            from PIL import ImageFont
            from PIL import ImageDraw 

            # Open the image file
            print(" 4 6 0")
            img = Image.open(filename)
            print(" 4 6 1")
            # Create a drawing context
            draw = ImageDraw.Draw(img)
            print("4 6 5")
            
            
            # Define the font to use          
            # font = ImageFont.truetype("arial.ttf", 30)
         
            print("4 6 8")

           

            # Draw the name on the image
            x=760
            y=1700
            draw.text((x, y), student.Name, font=None, fill=(0,0,0))

            # Draw the name on the image
            roll_x=780
            roll_y=1740
            draw.text((roll_x, roll_y), student.Roll_no, font=None, fill=(0,0,0))

            # Save the modified image
            # s=f"media/omrs/{student.Exam_name}_{student.Roll_no}.jpg"
            # omrs=bulana()
            print(" 4 8 5")
            new_omrs=omrs.split("/")
            omrs=new_omrs[-1]
            # print(omrs)
            s=f"ExamSystem/media/{omrs}/{student.Exam_name}_{student.Roll_no}.jpg"
            print("4 8 7")
            img.save(s)
            
            
            
            ######  A L L   J P G   T O   P D F ########
            import glob, PIL.Image
            import uuid
            # L = [PIL.Image.open(f) for f in glob.glob(f'media/omrs/*.jpg')]
            L = [PIL.Image.open(f) for f in glob.glob(f'ExamSystem/media/{omrs}/*.jpg')]
            a=uuid.uuid4().hex
            L[0].save(f'ExamSystem/media/media/{a}_OMR.pdf', "PDF" ,resolution=100.0, save_all=True, append_images=L[1:])

            
            from django.http import StreamingHttpResponse
            from django.conf import settings
            import os
            
            file_path=f'media/{a}_OMR.pdf'
            file_abs_path = os.path.join(settings.MEDIA_ROOT, file_path)

        
            def file_iterator(file_path, chunk_size=8192):
                with open(str(file_path), 'rb') as pdf:
                    while True:
                        data = pdf.read(chunk_size)
                        if not data:
                            break
                        yield data          
                os.remove(file_path)      
            
            # Use the StreamingHttpResponse class to serve the file as a stream
            response = StreamingHttpResponse(file_iterator(file_abs_path))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_abs_path)}"'
            response['Content-Type'] = 'application/pdf'   

        # deleteing the folder contents after been used
        import shutil    
        # print(qr_only)
        qr_only_folder_path = f"ExamSystem/media/{qr_only}"
        omr_folder_path = f"ExamSystem/media/{omrs}"
        shutil.rmtree(qr_only_folder_path)
        shutil.rmtree(omr_folder_path)
        return response
    
    except:
        return render(request,"somethingwentwrong.html")  
    


    
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
############################################################################################
        
             
   
@login_required(login_url="/login")
def scan_download(request):
    return render(request,"scan_omr/download_generation.html")


    
# @login_required(login_url="/login")
# def search_scan_results(request, exam_center):
#     # perform search based on exam_center an classes
#     data = Qr.objects.filter(center_code=exam_center)
    
   
#     # print(data)
#     url = f"/omr_scan_dow/{exam_center}"
#     context={
#         "data":data,
#         "url":url
#     }

#     if not data:
#         # return HttpResponse("NO data found")
#         return render(request,"no_data_found.html")
        
#     return render(request, 'scan_omr/search_scan_results.html',context)
   
    
    
    
################ U P L O A D   M U L T I P L E   I M A G E S  ########### 
  

import os
from django.conf import settings
from django.http import JsonResponse
import datetime
from .models import ExamScore,studentLogs
import uuid
from django.utils import timezone




import cv2
import glob
from django.shortcuts import render
from pyzbar.pyzbar import decode
from PIL import Image


data=[]
# import threading





# Create a lock object
# processing_lock = threading.Lock()
@login_required(login_url="/login")
def upload_file(request, exam_center, exam_name,classes, subject):
    if request.method == 'POST':
        files = request.FILES.getlist('images')

        if not files:
            return render(request,'pleaseuploadimages.html')
        
            # return render(request, 'upload.html')

        folder_name = bulana()
        folder_path = os.path.join('media', folder_name)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(folder_path, file.name)

            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

      

        try:
            # P R O C E S S I N G
            # path = f"media/{folder_name}/*.jpg"
            # print("6 5 3")
            old_path = f"{folder_name}/*.jpeg"
            # old_path = f"{folder_name}/*.jpeg"


            # RUNSERVER
            # # print("6 5 5")
            # np=old_path.split("ExamSystem")
            # print(np)    #['/home/kishan/', '/media/fb03f63bd55a47bfbac89a6a2f171fe5/*.jpeg']
            # # print("6 5 7")
            # npa=np[-1]
            # # npa=np[1]
            # path=npa[1:]
            # print(path)     #media/75edf11832634e019464098a24b800df/*.jpeg           
            # # path=f"media/{folder_name}/*.jpg"
            # print("i am 683")
            # k = glob.glob(old_path)    #['media/1f1aa65e94b946f991fd3f3a38131e46/1.jpeg']
            # print(k)
            # print("i am 685")


            images = [cv2.imread(images) for images in glob.glob(old_path)]
            # print("i am 687")
            # print(images)
            image_paths = glob.glob(old_path)
            # print("i am 689")
            images = []
            for image_path in image_paths:
                img = cv2.imread(image_path)
                images.append(img)
            # print("going to print images")
            # print("images = ",images)

            # mar=[]
            
            fin = []
            c = 0
            answers=[]
            for img in images:
                # print("i  m  g  = ",img)
                p = read_qr_and_scan.display_barcode(img)
                # print("pppppppp: ",p)
                answers=p[-1]
                # print(answers)
                # print(p[0][c])
                i = p[0][c] + f"\nscore: {p[1]}\nRESPONSE: {p[2]}"
                # i=p[0][c]
                fin.append(i)
                c += 1
            c = 0
            p[0].clear()
        
            

            qr_result = []
            qr_result.clear()
            for item in fin:
                parts = item.split('\n')
                temp_dict = {}
                for part in parts:
                    key, value = part.split(': ')
                    temp_dict[key] = value

                # print(temp_dict)

                # temp_dict["score"] = score
                # print(temp_dict['score'])
                qr_result.append(temp_dict)
            # print(qr_result)
            
            # print("7 1 2")
            for d in qr_result:
                d['Exam_ID'] = d.pop('Exam ID')
                d['Exam_name'] = d.pop('Exam name')
                d['Roll_no'] = d.pop('Roll No')
                d['exam_code'] =d.pop('Exam code')
            # print(qr_result)

            # for i in qr_result:
            #     print(i)

            # for removing duplicates

            new_list = []
            for item in qr_result:
                if item not in new_list:
                    new_list.append(item)
            
            # print(new_list)
            data = new_list
            # print("data = ",data)
            previous_scanned = studentLogs.objects.filter(center_code=exam_center,exam_name=exam_name,classes=classes,subject=subject)

            from Teachers.models import Answers

            # Assuming 'answers' is the value you want to check
            if not Answers.objects.filter(answer=answers).exists():
                answ = Answers(answer=answers)
                answ.save()



            for result_data in data:
                if not ExamScore.objects.filter(exam_id=int(result_data['Exam_ID']), roll_no=result_data['Roll_no'],
                                               section=result_data['Section'], name=result_data['Name']).exists():
                    result = ExamScore(
                        name=result_data['Name'],
                        subject=result_data['Subject'],
                        center_code=result_data['exam_code'],
                        classes=result_data['Class'],
                        section=result_data['Section'],
                        score=float(result_data['score']),
                        exam_id=int(result_data['Exam_ID']),
                        exam_name=result_data['Exam_name'],
                        roll_no=result_data['Roll_no']
                    )
                    result.save()
            import json
            for logs_data in data:
                if not studentLogs.objects.filter(exam_id=int(logs_data['Exam_ID']), roll_no=logs_data['Roll_no'],
                                               section=logs_data['Section'], name=logs_data['Name']).exists():
                    
                    logs = studentLogs(
                        name=logs_data['Name'],
                        subject=logs_data['Subject'],
                        center_code=logs_data['exam_code'],
                        classes=logs_data['Class'],
                        section=logs_data['Section'],
                        score=float(logs_data['score']),
                        exam_id=int(logs_data['Exam_ID']),
                        exam_name=logs_data['Exam_name'],
                        roll_no=logs_data['Roll_no'],
                        # studentResponses= studentLogs(studentResponses=json.dumps(studentResponses)),
                        studentResponses=logs_data['RESPONSE'],
                    )
                    logs.save()

            context = {
                'qr_data': new_list,
                'previous_scanned':previous_scanned,
                'exam_center':exam_center,
                'exam_name':exam_name,
                'classes':classes,
                'subject':subject,
                 
                   

                # 'score':mar,
                # 'variable2': 'value2',

            }

            fin.clear()


            
            
            # print("@@@@@@@@@@@@@@@@@@@@@@",classes,subject,exam_center)
            
            
            



            # print(" 8 1 1")
            # Deleting all the folders which were created
            import shutil                
            new_folder_name=folder_name.split("/")
            folder_name=new_folder_name[-1]           
            temp_folder = f"ExamSystem/media/{folder_name}"
            shutil.rmtree(temp_folder)
            


            
           
            
            
           
            return render(request, 'result_scan.html', context)
        except:
            return render(request,"somethingwentwrong.html")  



    
# automatically saving to excel
import pandas as pd
from django.http import StreamingHttpResponse
from django.conf import settings
import os
def save_to_excel(data_list, file_path):
    df = pd.DataFrame(data_list)
    df.to_excel(file_path, index=False)
    file_abs_path=os.path.join(settings.MEDIA_ROOT, file_path)
    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as excel_file:
            while True:
                data = excel_file.read(chunk_size)
                if not data:
                    break
                yield data
        os.remove(file_path)
        # Use the StreamingHttpResponse class to serve the file as a stream
        response = StreamingHttpResponse(file_iterator(file_abs_path))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_abs_path)}"'
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response




# RESULTS VIEWS

@login_required(login_url="/login")
def view_results(request):
    return render(request,"view_results/entry_details.html")


@login_required(login_url="/login")
def view_results_search(request):
    if request.method == 'POST':
        exam_center = request.POST['exam_center']
        exam_name = request.POST['exam_name']
        classes = request.POST['classes']
        subject = request.POST['subject']
        if not (exam_center or classes or subject or exam_name):
            messages.error(request, 'Please provide Details')
            return redirect('view_results_search')
        elif not exam_center:
            messages.error(request, 'Please provide Exam center')
            return redirect('view_results_search')
        elif not exam_name:
            messages.error(request, 'Please provide Exam name')
            return redirect('view_results_search')
        elif not classes:
            messages.error(request, 'Please provide Class')
            return redirect('view_results_search')
        elif not subject:
            messages.error(request, 'Please provide Subject')
            return redirect('view_results_search')
        return redirect('results', exam_center=exam_center,exam_name=exam_name,classes=classes,subject=subject)
    return render(request, 'view_results/view_results_search.html')


@login_required(login_url="/login")
def results(request, exam_center,exam_name,classes,subject):
    # perform search based on exam_center an classes
    data = ExamScore.objects.filter(center_code=exam_center,exam_name=exam_name,classes=classes,subject=subject)
    
   
    # print(data)
    url = f"/view_results_search/{exam_center}/{exam_name}/{classes}/{subject}"
    context={
        "data":data,
        "url":url
    }

    if not data:
        # return HttpResponse("NO data found")
        return render(request,"view_results/no_data_found.html")
   
        
    return render(request, 'view_results/results.html',context)







import pandas as pd
from django.http import HttpResponse
from .models import ExamScore 

def download_excel(request, exam_center, exam_name, classes, subject):
    # Fetch the data from the database or any other source
    data = ExamScore.objects.filter(center_code=exam_center, exam_name=exam_name, classes=classes, subject=subject)  
    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data.values())

    # Create the response object with the appropriate headers
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={exam_center}-{exam_name}-{classes}-{subject}.xlsx'

    # Save the DataFrame to the response as an Excel file
    df.to_excel(response, index=False, sheet_name='Exam Scores')

    return response





from django.shortcuts import render
from .models import studentLogs,Answers
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def log(request, exam_code, Exam_name, Class, Subject, Name):
    filtered_data = studentLogs.objects.filter(center_code=exam_code, exam_name=Exam_name, classes=Class,  subject=Subject, name=Name)
    
    student_logs = []
    for log in filtered_data:
        responses = eval(log.studentResponses)  # Parse the string representation of the list
        student_logs.append(responses)
        break

    answ = Answers.objects.all()
    ans_values = [ans.answer for ans in answ]
    data = {'student_logs': student_logs, 'ans': ans_values[-1]}

    
    # data={'student_logs': student_logs,'ans':answ}
    # print(data)

    return render(request, 'student_logs.html', data)



# class UserMainCode(object):
#     @classmethod
#     def paint(cls, input1, input2):
#         def cf(num):
#             if num <= 1:
#                 return 1
#             return num * cf(num - 1)
            
#         def ccc(input1, input2):
#             n = cf(input1 + input2 - 1)
#             d = cf(input2) * cf(input1 - 1)
#             com = n // d
#             return com
            
#         com = ccc(input1, input2)
#         return com
#         pass
