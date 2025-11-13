from django.shortcuts import render, HttpResponse
from .models import Emoloyee, Role, Department
from datetime import datetime
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request, "index.html")

def all_emp(request):
    emps = Emoloyee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, "all_emp.html", context)


def add_emp(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        salary_str = request.POST.get('salary', '').strip()
        bonus_str = request.POST.get('bonus', '').strip()
        phone = request.POST.get('phone', '').strip()
        dept_str = request.POST.get('dept', '').strip()
        role_str = request.POST.get('role', '').strip()

        # Validate required fields
        if not first_name:
            return HttpResponse('Error: First Name is required!')
        if not phone:
            return HttpResponse('Error: Phone Number is required!')
        if not dept_str:
            return HttpResponse('Error: Department is required!')
        if not role_str:
            return HttpResponse('Error: Role is required!')

        # Convert to integers with default values for empty strings
        try:
            salary = int(salary_str) if salary_str else 0
            bonus = int(bonus_str) if bonus_str else 0
            phone_int = int(phone)
        except ValueError:
            return HttpResponse('Error: Invalid number format in salary, bonus, or phone fields!')

        # Get or create Department by name
        try:
            dept_obj, created = Department.objects.get_or_create(name=dept_str)
        except Exception as e:
            return HttpResponse(f'Error: Could not process Department - {str(e)}')

        # Get or create Role by name
        try:
            role_obj, created = Role.objects.get_or_create(name=role_str)
        except Exception as e:
            return HttpResponse(f'Error: Could not process Role - {str(e)}')

        new_emp = Emoloyee(first_name=first_name, last_name=last_name, bonus=bonus, salary=salary, phone=phone_int,
                           dept=dept_obj, role=role_obj, hire_date=datetime.now())
        new_emp.save()
        return HttpResponse('Employee Added Successfully')
    elif request.method == 'GET':
        return render(request, "add_emp.html")
    else:
        return HttpResponse("An Exception Occurred !!! Employee Has Not Been Added.")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Emoloyee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully!!!")
        except:
            return HttpResponse("Please Enter A Valid Emp_ID.")

    emps = Emoloyee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, "remove_emp.html", context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Emoloyee.objects.all()

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)

        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')

    else:
        return HttpResponse("An Exception Is Occurred")
