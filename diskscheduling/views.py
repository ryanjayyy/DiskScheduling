from django.shortcuts import render

# Create your views here.

def home(request):

    return render(request, 'diskscheduling/home.html')


def calculate_fcfs(jobs):
    # First-Come, First-Served (FCFS) scheduling algorithm
    return jobs

def calculate_sstf(jobs):
    # Shortest Seek Time First (SSTF) scheduling algorithm
    return jobs

