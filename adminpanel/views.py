"""
Author: Muhammed Hasan (w1689191), Jolen Mascarenhas (w2078969)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.utils import timezone
from core.models import TblUser, TblTeam, TblDepartment, TblProject, TblDependencies
from accounts.views import is_logged_in
import secrets
import string


def is_admin(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return False
    try:
        return TblUser.objects.get(id=user_id).role == 'Admin'
    except TblUser.DoesNotExist:
        return False


def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


# ─── DASHBOARD ──────────────────────────────────────────

def admin_dashboard(request):
    if not is_admin(request):
        return redirect("home")
    context = {
        "is_admin_user": is_admin(request),
    }
    return render(request, "adminpanel/dashboard.html", context)


def admin_panel_view(request):
    if not is_admin(request):
        return redirect('login')
    context = {
        'users': TblUser.objects.all(),
        'teams': TblTeam.objects.all(),
        'departments': TblDepartment.objects.all(),
        'projects': TblProject.objects.all(),
        'dependencies': TblDependencies.objects.all(),
        'current_user_id': request.session.get('user_id'),
    }
    return render(request, 'admin_panel/index.html', context)


# ─── MANAGE PAGES ───────────────────────────────────────

def manage_users(request):
    if not is_admin(request):
        return redirect("home")
    users = TblUser.objects.select_related("team").all()
    teams = TblTeam.objects.all()
    return render(request, "adminpanel/manage_users.html", {
        "users": users,
        "teams": teams,
    })


def manage_teams(request):
    if not is_admin(request):
        return redirect("home")
    return render(request, "adminpanel/manage_teams.html", {
        "teams": TblTeam.objects.all(),
        "users": TblUser.objects.all(),
        "departments": TblDepartment.objects.all(),
    })


def manage_departments(request):
    if not is_admin(request):
        return redirect("home")
    return render(request, "adminpanel/manage_departments.html", {
        "departments": TblDepartment.objects.all(),
        "users": TblUser.objects.all(),
    })


def manage_projects(request):
    if not is_admin(request):
        return redirect("home")
    return render(request, "adminpanel/manage_projects.html", {
        "projects": TblProject.objects.all(),
        "teams": TblTeam.objects.all(),
    })


def manage_dependencies(request):
    if not is_admin(request):
        return redirect("home")
    return render(request, "adminpanel/manage_dependencies.html", {
        "dependencies": TblDependencies.objects.all(),
        "teams": TblTeam.objects.all(),
    })


# ─── LEGACY USER MANAGEMENT (kept for existing URL references) ──

def reset_user_password(request, user_id):
    if not is_admin(request):
        return redirect("home")
    if request.method == "POST":
        user = TblUser.objects.get(id=user_id)
        if user.id == request.session.get("user_id"):
            return redirect("manage_users")
        user.password = make_password("Password123")
        user.save(update_fields=["password"])
    return redirect("manage_users")


def toggle_user_active(request, user_id):
    if not is_admin(request):
        return redirect("home")
    if request.method == "POST":
        user = TblUser.objects.get(id=user_id)
        user.active = not user.active
        user.save(update_fields=["active"])
    return redirect("manage_users")


def change_user_role(request, user_id):
    if not is_admin(request):
        return redirect("home")
    if request.method == "POST":
        user = TblUser.objects.get(id=user_id)
        new_role = request.POST.get("role")
        if new_role in ["User", "Admin", "Team Leader", "Department Head"]:
            user.role = new_role
            user.save(update_fields=["role"])
    return redirect("manage_users")


def add_user(request):
    if not is_admin(request):
        return redirect("home")
    if request.method == "POST":
        TblUser.objects.create(
            fname=request.POST.get("fname"),
            sname=request.POST.get("sname"),
            uname=request.POST.get("uname"),
            email=request.POST.get("email"),
            role=request.POST.get("role"),
            active=True,
            created=timezone.now(),
            password=make_password("Password123"),
        )
    return redirect("manage_users")


def delete_user(request, user_id):
    if not is_admin(request):
        return redirect("home")
    if request.method == "POST":
        user = TblUser.objects.get(id=user_id)
        if user.id != request.session.get("user_id"):
            user.delete()
    return redirect("manage_users")


# ─── USER ───────────────────────────────────────────────

def user_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        team_id = request.POST.get("team")
        error = None
        if TblUser.objects.filter(uname=uname).exists():
            error = "Username already exists"
        elif TblUser.objects.filter(email=email).exists():
            error = "Email already exists"
        if error:
            return redirect(f"{request.META.get('HTTP_REFERER', '/admin-panel/users/')}?error={error}")
    
        if team_id:
            team = TblTeam.objects.get(id=team_id)
        else:
            team = None
        raw_password = generate_password()
        TblUser.objects.create(
            fname=request.POST.get('fname'),
            sname=request.POST.get('sname'),
            uname=uname,
            email=email,
            password=make_password(raw_password),
            role=request.POST.get('role'),
            team=team,
            created=timezone.now(),
            active=True
        )
        return redirect(f"/admin-panel/users/?created_password={raw_password}&created_uname={uname}")
    return redirect('manage_users')


def user_edit_view(request, user_id):
    if not is_admin(request):
        return redirect('login')
    user = get_object_or_404(TblUser, id=user_id)
    team_id = request.POST.get('team')
    if team_id:
            team = TblTeam.objects.get(id=team_id)
    else:
        team = None
    if request.method == 'POST':
        user.fname = request.POST.get('fname')
        user.sname = request.POST.get('sname')
        user.email = request.POST.get('email')
        user.role = request.POST.get('role')
        user.team = team
        user.active = request.POST.get('active') == 'on'
        user.save()
    return redirect('manage_users')


def user_delete_view(request, user_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        user = get_object_or_404(TblUser, id=user_id)
        if user.id != request.session.get('user_id'):
            user.delete()
    return redirect('manage_users')


# ─── TEAM ───────────────────────────────────────────────

def team_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        TblTeam.objects.create(
            name=request.POST.get('name'),
            team_leader_id=request.POST.get('team_leader') or None,
            department_id=request.POST.get('department') or None,
            description=request.POST.get('description'),
            skills_and_tech=request.POST.get('skills_and_tech'),
            slack=request.POST.get('slack'),
            wiki=request.POST.get('wiki'),
        )
    return redirect('manage_teams')


def team_edit_view(request, team_id):
    if not is_admin(request):
        return redirect('login')
    team = get_object_or_404(TblTeam, id=team_id)
    if request.method == 'POST':
        team.name = request.POST.get('name')
        team.team_leader_id = request.POST.get('team_leader') or None
        team.department_id = request.POST.get('department') or None
        team.description = request.POST.get('description')
        team.skills_and_tech = request.POST.get('skills_and_tech')
        team.slack = request.POST.get('slack')
        team.wiki = request.POST.get('wiki')
        team.save()
    return redirect('manage_teams')


def team_delete_view(request, team_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        get_object_or_404(TblTeam, id=team_id).delete()
    return redirect('manage_teams')


# ─── DEPARTMENT ─────────────────────────────────────────

def department_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        TblDepartment.objects.create(
            name=request.POST.get('name'),
            department_head_id=request.POST.get('department_head') or None,
        )
    return redirect('manage_departments')


def department_edit_view(request, dept_id):
    if not is_admin(request):
        return redirect('login')
    dept = get_object_or_404(TblDepartment, id=dept_id)
    if request.method == 'POST':
        dept.name = request.POST.get('name')
        dept.department_head_id = request.POST.get('department_head') or None
        dept.save()
    return redirect('manage_departments')


def department_delete_view(request, dept_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        get_object_or_404(TblDepartment, id=dept_id).delete()
    return redirect('manage_departments')


# ─── PROJECT ────────────────────────────────────────────

def project_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        TblProject.objects.create(
            name=request.POST.get('name'),
            team_id=request.POST.get('team') or None,
            description=request.POST.get('description'),
            codebase=request.POST.get('codebase'),
            jira_board=request.POST.get('jira_board'),
            created=timezone.now(),
            status=request.POST.get('status'),
        )
    return redirect('manage_projects')


def project_edit_view(request, project_id):
    if not is_admin(request):
        return redirect('login')
    project = get_object_or_404(TblProject, id=project_id)
    if request.method == 'POST':
        project.name = request.POST.get('name')
        project.team_id = request.POST.get('team') or None
        project.description = request.POST.get('description')
        project.codebase = request.POST.get('codebase')
        project.jira_board = request.POST.get('jira_board')
        project.status = request.POST.get('status')
        project.save()
    return redirect('manage_projects')


def project_delete_view(request, project_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        get_object_or_404(TblProject, id=project_id).delete()
    return redirect('manage_projects')


# ─── DEPENDENCY ─────────────────────────────────────────

def dependency_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        TblDependencies.objects.create(
            upstream=request.POST.get('upstream') == 'on',
            downstream=request.POST.get('downstream') == 'on',
            team_id=request.POST.get('team') or None,
            type=request.POST.get('type'),
        )
    return redirect('manage_dependencies')


def dependency_edit_view(request, dep_id):
    if not is_admin(request):
        return redirect('login')
    dep = get_object_or_404(TblDependencies, id=dep_id)
    if request.method == 'POST':
        dep.upstream = request.POST.get('upstream') == 'on'
        dep.downstream = request.POST.get('downstream') == 'on'
        dep.team_id = request.POST.get('team') or None
        dep.type = request.POST.get('type')
        dep.save()
    return redirect('manage_dependencies')


def dependency_delete_view(request, dep_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        get_object_or_404(TblDependencies, id=dep_id).delete()
    return redirect('manage_dependencies')