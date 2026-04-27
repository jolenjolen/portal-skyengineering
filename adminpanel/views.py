"""
Author: Muhammed Hasan (w1689191), Jolen Mascarenhas (w2078969)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from core.models import TblUser, TblTeam, TblDepartment, TblProject, TblDependencies, TblAudit
from accounts.views import is_logged_in
from .audit import log_action
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
        return redirect('home')
    logs = TblAudit.objects.select_related('user').order_by('-datetime')[:100]
    context = {
        'is_admin_user': True,
        'audit_logs': logs,
    }
    return render(request, 'adminpanel/dashboard.html', context)


def admin_panel_view(request):
    if not is_admin(request):
        return redirect('login')
    logs = TblAudit.objects.select_related('user').order_by('-datetime')[:100]
    context = {
        'users':           TblUser.objects.all(),
        'teams':           TblTeam.objects.all(),
        'departments':     TblDepartment.objects.all(),
        'projects':        TblProject.objects.all(),
        'dependencies':    TblDependencies.objects.all(),
        'current_user_id': request.session.get('user_id'),
        'audit_logs':      logs,
    }
    return render(request, 'admin_panel/index.html', context)


# ─── MANAGE PAGES ───────────────────────────────────────

def manage_users(request):
    if not is_admin(request):
        return redirect('home')
    return render(request, 'adminpanel/manage_users.html', {
        'users': TblUser.objects.all(),
        'teams': TblTeam.objects.all(),
    })


def manage_teams(request):
    if not is_admin(request):
        return redirect('home')
    return render(request, 'adminpanel/manage_teams.html', {
        'teams':       TblTeam.objects.all(),
        'users':       TblUser.objects.all(),
        'departments': TblDepartment.objects.all(),
    })


def manage_departments(request):
    if not is_admin(request):
        return redirect('home')
    return render(request, 'adminpanel/manage_departments.html', {
        'departments': TblDepartment.objects.all(),
        'users':       TblUser.objects.all(),
    })


def manage_projects(request):
    if not is_admin(request):
        return redirect('home')
    return render(request, 'adminpanel/manage_projects.html', {
        'projects': TblProject.objects.all(),
        'teams':    TblTeam.objects.all(),
    })


def manage_dependencies(request):
    if not is_admin(request):
        return redirect('home')
    return render(request, 'adminpanel/manage_dependencies.html', {
        'dependencies': TblDependencies.objects.all(),
        'teams':        TblTeam.objects.all(),
    })


# ─── LEGACY USER MANAGEMENT ─────────────────────────────

def reset_user_password(request, user_id):
    if not is_admin(request):
        return redirect('home')
    if request.method == 'POST':
        user = TblUser.objects.get(id=user_id)
        if user.id == request.session.get('user_id'):
            return redirect('manage_users')
        user.password = make_password('Password123')
        user.save(update_fields=['password'])
        log_action(request, f"Reset password for user '{user.uname}' (ID {user.id})")
    return redirect('manage_users')


def toggle_user_active(request, user_id):
    if not is_admin(request):
        return redirect('home')
    if request.method == 'POST':
        user = TblUser.objects.get(id=user_id)
        user.active = not user.active
        user.save(update_fields=['active'])
        status = 'activated' if user.active else 'deactivated'
        log_action(request, f"User '{user.uname}' (ID {user.id}) {status}")
    return redirect('manage_users')


def change_user_role(request, user_id):
    if not is_admin(request):
        return redirect('home')
    if request.method == 'POST':
        user = TblUser.objects.get(id=user_id)
        old_role = user.role
        new_role = request.POST.get('role')
        if new_role in ['User', 'Admin', 'Team Leader', 'Department Head']:
            user.role = new_role
            user.save(update_fields=['role'])
            log_action(request, f"Changed role of '{user.uname}' from '{old_role}' to '{new_role}'")
    return redirect('manage_users')


def add_user(request):
    if not is_admin(request):
        return redirect('home')
    if request.method == 'POST':
        uname = request.POST.get('uname')
        TblUser.objects.create(
            fname=request.POST.get('fname'),
            sname=request.POST.get('sname'),
            uname=uname,
            email=request.POST.get('email'),
            role=request.POST.get('role'),
            active=True,
            created=timezone.now(),
            password=make_password('Password123'),
        )
        log_action(request, f"Created user '{uname}' with default password")
    return redirect('manage_users')


def delete_user(request, user_id):
    if not is_admin(request):
        return redirect('home')
    if request.method == 'POST':
        user = TblUser.objects.get(id=user_id)
        if user.id != request.session.get('user_id'):
            log_action(request, f"Deleted user '{user.uname}' (ID {user.id})")
            user.delete()
    return redirect('manage_users')


# ─── USER (new views) ────────────────────────────────────

def user_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        error = None
        if TblUser.objects.filter(uname=uname).exists():
            error = 'Username already exists'
        elif TblUser.objects.filter(email=email).exists():
            error = 'Email already exists'
        if error:
            return redirect(
                f"{request.META.get('HTTP_REFERER', '/admin-panel/users/')}?error={error}"
            )
        raw_password = generate_password()
        TblUser.objects.create(
            fname=request.POST.get('fname'),
            sname=request.POST.get('sname'),
            uname=uname,
            email=email,
            password=make_password(raw_password),
            role=request.POST.get('role'),
            team_id=request.POST.get('team') or None,
            created=timezone.now(),
            active=True,
        )
        log_action(request, f"Created user '{uname}' (email: {email})")
        return redirect(
            f"/admin-panel/users/?created_password={raw_password}&created_uname={uname}"
        )
    return redirect('manage_users')


def user_edit_view(request, user_id):
    if not is_admin(request):
        return redirect('login')
    user = get_object_or_404(TblUser, id=user_id)
    if request.method == 'POST':
        old = f"{user.fname} {user.sname}, role={user.role}, active={user.active}"
        user.fname   = request.POST.get('fname')
        user.sname   = request.POST.get('sname')
        user.email   = request.POST.get('email')
        user.role    = request.POST.get('role')
        user.team_id = request.POST.get('team') or None
        user.active  = request.POST.get('active') == 'on'
        user.save()
        log_action(request, f"Edited user '{user.uname}' (ID {user.id}) — was: {old}")
    return redirect('manage_users')


def user_delete_view(request, user_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        user = get_object_or_404(TblUser, id=user_id)
        if user.id != request.session.get('user_id'):
            log_action(request, f"Deleted user '{user.uname}' (ID {user.id})")
            user.delete()
    return redirect('manage_users')


# ─── TEAM ────────────────────────────────────────────────

def team_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        team = TblTeam.objects.create(
            name=name,
            team_leader_id=request.POST.get('team_leader') or None,
            department_id=request.POST.get('department') or None,
            description=request.POST.get('description'),
            skills_and_tech=request.POST.get('skills_and_tech'),
            slack=request.POST.get('slack'),
            wiki=request.POST.get('wiki'),
        )
        log_action(request, f"Created team '{name}' (ID {team.id})")
    return redirect('manage_teams')


def team_edit_view(request, team_id):
    if not is_admin(request):
        return redirect('login')
    team = get_object_or_404(TblTeam, id=team_id)
    if request.method == 'POST':
        old_name = team.name
        team.name           = request.POST.get('name')
        team.team_leader_id = request.POST.get('team_leader') or None
        team.department_id  = request.POST.get('department') or None
        team.description    = request.POST.get('description')
        team.skills_and_tech = request.POST.get('skills_and_tech')
        team.slack          = request.POST.get('slack')
        team.wiki           = request.POST.get('wiki')
        team.save()
        log_action(request, f"Edited team '{old_name}' → '{team.name}' (ID {team.id})")
    return redirect('manage_teams')


def team_delete_view(request, team_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        team = get_object_or_404(TblTeam, id=team_id)
        log_action(request, f"Deleted team '{team.name}' (ID {team.id})")
        team.delete()
    return redirect('manage_teams')


# ─── DEPARTMENT ──────────────────────────────────────────

def department_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        dept = TblDepartment.objects.create(
            name=name,
            department_head_id=request.POST.get('department_head') or None,
        )
        log_action(request, f"Created department '{name}' (ID {dept.id})")
    return redirect('manage_departments')


def department_edit_view(request, dept_id):
    if not is_admin(request):
        return redirect('login')
    dept = get_object_or_404(TblDepartment, id=dept_id)
    if request.method == 'POST':
        old_name = dept.name
        dept.name               = request.POST.get('name')
        dept.department_head_id = request.POST.get('department_head') or None
        dept.save()
        log_action(request, f"Edited department '{old_name}' → '{dept.name}' (ID {dept.id})")
    return redirect('manage_departments')


def department_delete_view(request, dept_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        dept = get_object_or_404(TblDepartment, id=dept_id)
        log_action(request, f"Deleted department '{dept.name}' (ID {dept.id})")
        dept.delete()
    return redirect('manage_departments')


# ─── PROJECT ─────────────────────────────────────────────

def project_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        proj = TblProject.objects.create(
            name=name,
            team_id=request.POST.get('team') or None,
            description=request.POST.get('description'),
            codebase=request.POST.get('codebase'),
            jira_board=request.POST.get('jira_board'),
            created=timezone.now(),
            status=request.POST.get('status'),
        )
        log_action(request, f"Created project '{name}' (ID {proj.id})")
    return redirect('manage_projects')


def project_edit_view(request, project_id):
    if not is_admin(request):
        return redirect('login')
    project = get_object_or_404(TblProject, id=project_id)
    if request.method == 'POST':
        old_name = project.name
        project.name        = request.POST.get('name')
        project.team_id     = request.POST.get('team') or None
        project.description = request.POST.get('description')
        project.codebase    = request.POST.get('codebase')
        project.jira_board  = request.POST.get('jira_board')
        project.status      = request.POST.get('status')
        project.save()
        log_action(request, f"Edited project '{old_name}' → '{project.name}' (ID {project.id})")
    return redirect('manage_projects')


def project_delete_view(request, project_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        project = get_object_or_404(TblProject, id=project_id)
        log_action(request, f"Deleted project '{project.name}' (ID {project.id})")
        project.delete()
    return redirect('manage_projects')


# ─── DEPENDENCY ──────────────────────────────────────────

def dependency_create_view(request):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        dep = TblDependencies.objects.create(
            upstream=request.POST.get('upstream') == 'on',
            downstream=request.POST.get('downstream') == 'on',
            team_id=request.POST.get('team') or None,
            type=request.POST.get('type'),
        )
        team_name = dep.team.name if dep.team else 'no team'
        log_action(request, f"Created dependency (ID {dep.id}) for team '{team_name}', type '{dep.type}'")
    return redirect('manage_dependencies')


def dependency_edit_view(request, dep_id):
    if not is_admin(request):
        return redirect('login')
    dep = get_object_or_404(TblDependencies, id=dep_id)
    if request.method == 'POST':
        dep.upstream   = request.POST.get('upstream') == 'on'
        dep.downstream = request.POST.get('downstream') == 'on'
        dep.team_id    = request.POST.get('team') or None
        dep.type       = request.POST.get('type')
        dep.save()
        team_name = dep.team.name if dep.team else 'no team'
        log_action(request, f"Edited dependency (ID {dep.id}) — team '{team_name}', type '{dep.type}'")
    return redirect('manage_dependencies')


def dependency_delete_view(request, dep_id):
    if not is_admin(request):
        return redirect('login')
    if request.method == 'POST':
        dep = get_object_or_404(TblDependencies, id=dep_id)
        log_action(request, f"Deleted dependency (ID {dep.id}), type '{dep.type}'")
        dep.delete()
    return redirect('manage_dependencies')