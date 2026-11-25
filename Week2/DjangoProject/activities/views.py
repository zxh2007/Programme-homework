from django.shortcuts import get_object_or_404, redirect, render

from .forms import ActivityForm
from .models import Activity


def activity_list(request):
    """活动列表，支持按标题搜索"""
    keyword = request.GET.get('q', '').strip()
    activities = Activity.objects.all()
    if keyword:
        activities = activities.filter(title__icontains=keyword)
    context = {
        'activities': activities,
        'keyword': keyword,
    }
    return render(request, 'activities/activity_list.html', context)


def activity_create(request):
    """添加活动"""
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('activities:activity_list')
    else:
        form = ActivityForm()
    return render(request, 'activities/activity_form.html', {
        'form': form,
        'page_title': '添加活动',
    })


def activity_update(request, pk):
    """编辑活动，复用 ModelForm"""
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activities:activity_list')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'activities/activity_form.html', {
        'form': form,
        'page_title': '编辑活动',
        'activity': activity,
    })


def activity_delete(request, pk):
    """删除活动，先确认再删除"""
    activity = get_object_or_404(Activity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        return redirect('activities:activity_list')
    return render(request, 'activities/activity_confirm_delete.html', {
        'activity': activity,
    })
