from django.shortcuts import render, redirect
from .models import Job
from django.core.paginator import Paginator
from .filters import JobFilter
from .forms import JobForm, CandidateForm
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

'''
jobs and dashboard views almost the same and this is not professional
we can fix this problem by merging the views together with some conditions
if the current user is admin then render the dashboard else render the jobs
'''
def jobs(request):
    job_list = Job.objects.all()
    jobs_count = job_list.count()

    filter = JobFilter(request.GET, queryset=job_list)
    job_list = filter.qs

    paginator = Paginator(job_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'jobs_count': jobs_count, 'jobs': page_obj, 'filters': filter}
    return render(request, 'jobs.html', context)

def dashboard(request):
    job_list = Job.objects.all()
    jobs_count = job_list.count()

    filter = JobFilter(request.GET, queryset=job_list)
    job_list = filter.qs

    paginator = Paginator(job_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'jobs_count': jobs_count, 'jobs': page_obj, 'filters': filter}
    return render(request, 'jobs_dashboard.html', context)

def job_details(request, id):
    job_details = Job.objects.get(id=id)

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.job = job_details
            my_form.save()
            return redirect('jobs:job_details', id=id)
    else:
        form = CandidateForm()

    context = {'job': job_details, 'form': form}
    return render(request, 'job_details.html', context)

@permission_required('admin')
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.owner = request.user
            my_form.save()
            return redirect(reverse('jobs:jobs'))
    else:
        form = JobForm()
    return render(request, 'add_job.html', {'form': form})

@permission_required('admin')
def edit_job(request, id):
    job_details = Job.objects.get(id=id)
    
    if request.method == 'POST':
        job_form = JobForm(request.POST, request.FILES, instance=job_details)
        if job_form.is_valid():
            job_form.save()
            return redirect(reverse('jobs:job_dashboard'))
    else:
        form = JobForm(instance=job_details)
    
    context = {'form': form, 'job_id': job_details.id}
    return render(request, 'edit_job.html', context)

@permission_required('admin')
def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect(reverse('jobs:job_dashboard'))