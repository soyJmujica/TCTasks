from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import UnderContract
from .forms import UnderContractForm, UnderContractProcessing, UnderContractClosing
from django.core.mail import send_mail, EmailMessage
from TestEmail.settings import EMAIL_HOST_USER
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

def Home(request):
    return render(request,"home.html", {"encabezado":"Home"})


def signup(request):
    correos = ["master1495@gmail.com", "joseblack1495@hotmail.com"]
    if request.method=="POST":
        if request.POST["email"] in correos:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            password = request.POST["password"]
            email = request.POST["email"]
            user = User.objects.create_user(
				first_name = first_name,
				last_name = last_name,
				username = username,
				password = password,
				email = email
				)
            login(request, user)
            subject = "Welcome to the Emails App"
            message = f"Hi {username}, this is a message to Welcome you in our team."
            email_from = EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail(subject, message, email_from, recipient_list)
            print(f"Email sent to {username} - {email}")
            return redirect('/')
        else:
            #print(f"a vaina {request.POST["first_name"]} tu no tienes permitido registrate")
            return redirect("signup")
      
    return redirect('ingreso')

def	signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            message = "Incorrect username or password"
            return redirect('ingreso', message = message, form=AuthenticationForm())
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {"form":form, "encabezado":'Log In'})
        
def ingreso(request):
    login = AuthenticationForm()
    return render(request, 'ingreso.html', {'login':login, "encabezado": "Sign Up  |  Log In"})

def not_logged(request):
    return render(request, "no.html", {'encabezado':"Not Today Baby"})

@login_required     
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def undercontract(request):
    if request.method == "POST":
        form = UnderContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = UnderContractForm()
    return render(request, "input.html",{'form':form,"encabezado":"Add Properties"})

@login_required
def tasks(request):
    properties = UnderContract.objects.filter(completed = False).order_by("closing_date")
    return render(request, "tasks.html", {'properties':properties,"encabezado":"Pendings"})

@login_required
def DA(request):
    properties = UnderContract.objects.filter(da_requested = False).order_by("closing_date")
    return render(request, "DA.html", {'properties':properties, "encabezado":"DA list"})

@login_required
def checklist(request, property_id):
    if request.method == "GET":
        property=get_object_or_404(UnderContract, pk = property_id)
        form = UnderContractProcessing(instance=property)
        return render(request, "checklist.html", {"property":property,'form':form ,'encabezado':property.address})
    elif request.method == "POST":
        property=get_object_or_404(UnderContract, pk = property_id)
        form = UnderContractProcessing(request.POST,instance=property)
        form.save()
        return render(request, "checklist.html", {"property":property,'form':form ,'encabezado':property.address})
    

@login_required
def congrats_completed(request, property_id):
    property = get_object_or_404(UnderContract, pk=property_id)
    if request.method =="POST":
        property.congratulations = True
        property.save()
        return redirect('checklist', property_id = property_id)
    return render(request,"checklist.html", {'property':property, 'encabezado':property.address})
@login_required
def congrast_incompleted(request, property_id):
    property = get_object_or_404(UnderContract, pk=property_id)
    if request.method == "POST":
        property.congratulations = False
        property.save()
        return redirect('checklist', property_id = property_id)
    return render(request, "checklist.html",{'property':property, 'encabezado':property.address})

@login_required
def da_completed(request, property_id):
    property = get_object_or_404(UnderContract, pk = property_id)
    if request.method == "POST":
        property.da_requested = True
        property.save()
        return redirect('DA')
    return render(request, "DA.html", {'encabezado':"DA list"})

@login_required
def da_incompleted(request, property_id):
    property = get_object_or_404(UnderContract, pk = property_id)
    if request.method == "POST":
        property.da_requested = False
        property.save()
        return redirect('DA')
    return render(request, "DA.html",{'encabezado': "DA list"})

@login_required
def properties(request):
    filtro = request.GET.get('filtro',)
    if filtro == None:
        pendings = UnderContract.objects.filter(closed = False).order_by("closing_date")
        closed = UnderContract.objects.filter(closed = True).order_by("closing_date")
        properties = UnderContract.objects.all().order_by("closing_date")
    else:
        pendings = UnderContract.objects.filter(closed = False, address__contains=filtro)
        closed = UnderContract.objects.filter(closed = True, address__contains=filtro)
        properties = UnderContract.objects.filter(address__contains=filtro)
    
    return render(request, "properties.html",{"encabezado":"Tab Views",
                                              "properties":properties,
                                              "pendings":pendings,
                                              "closed":closed})

@login_required    

@login_required
def details(request, property_id):
    property = get_object_or_404(UnderContract, pk = property_id)
    if property.category == "Buyer":
        commission = (property.price * (property.commission/100)) - property.mls_fee
    else:
        commission = (property.price * (property.commission/100)) + property.mls_fee
    if property.da_requested == False:
        hoy = datetime.now().date()
        diferencia = (property.closing_date - hoy).days
        if diferencia <=10:
            alert = f"The closing is in {diferencia} days, please request DA"
        else:
            dia = property.closing_date - timedelta(days=10)
            dia = dia.strftime("%B %d, %Y")
            alert = f"DA must be requested on {dia}"            
    else:
        alert = "DA has been requested"
    
    return render(request, "detalles.html", {'encabezado': property.address,'property':property,"commission":commission, "alert":alert})


def congratulations(request, property_id):
    property = get_object_or_404(UnderContract, pk=property_id)
    
    return render(request, "congratulations.html", {'encabezado':f"Congratulations email of {property.address}",'property':property})

def closing(request, property_id):
    if request.method == "GET":
        property=get_object_or_404(UnderContract, pk = property_id)
        form = UnderContractClosing(instance=property)
        return render(request, "closing.html", {"property":property,'form':form ,'encabezado':property.address})
    elif request.method == "POST":
        property=get_object_or_404(UnderContract, pk = property_id)
        form = UnderContractClosing(request.POST,instance=property)
        form.save()
        return render(request, "closing.html", {"property":property,'form':form ,'encabezado':property.address})
    
    
def edit(request, property_id):
    if request.method == "GET":
        property = get_object_or_404(UnderContract, pk = property_id)
        form = UnderContractForm(instance=property)
        return render(request, "editar.html", {"property":property,'form':form ,'encabezado':property.address})
    elif request.method == "POST":
        property = get_object_or_404(UnderContract, pk = property_id)
        form = UnderContractForm(request.POST,instance=property)
        form.save()
        return render(request, "editar.html", {"property":property,'form':form ,'encabezado':property.address})
    
    
    