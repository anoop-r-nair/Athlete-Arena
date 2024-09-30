from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signupcoach/', views.signupcoach, name='signupcoach'),
    path('login/', views.login, name='login'),
    #  path('coach/login/', views.coach_login, name='coach_login'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('delete_user/<str:email>/', views.delete_user, name='delete_user'),
    path('update_user/<str:email>/', views.update_user, name='update_user'),
    #  path('coaches/', views.coaches_view, name='coaches'),
    path('coaches/update/<str:email>/', views.update_coach_by_email, name='update_coach_by_email'),
    path('coaches/delete/<str:email>/', views.delete_coach_by_email, name='delete_coach_by_email'),
    path('coach_dashboard/', views.coach_dashboard, name='coach_dashboard'),
    path('player_dashboard/', views.player_dashboard, name='player_dashboard'),
    path('signupparent/', views.signupparent, name='signupparent'),
    path('medical_staff_dashboard/', views.medical_staff_dashboard, name='medical_staff_dashboard'),
    path('sports_psychologist_dashboard/', views.sports_psychologist_dashboard, name='sports_psychologist_dashboard'),
    path('analytics_expert_dashboard/', views.analytics_expert_dashboard, name='analytics_expert_dashboard'),
    path('modules/', views.modules, name='modules'),
    path('schedules/', views.schedules, name='schedules'),
    path('teams/', views.teams, name='teams'),
    # path('manage-teams/', views.manage_teams, name='manage_teams'),
    # path('get-teams/', views.get_teams, name='get_teams'),
    # path('delete-team/<str:team_id>/', views.delete_team, name='delete_team'),
    # path('update-team/<str:team_id>/', views.update_team, name='update_team'),
    path('players/', views.players, name='players'),
    path('parents/', views.parents, name='parents'),
    path('parents/update/<str:email>/', views.update_parent_by_email, name='update_parent_by_email'),
    path('parents/delete/<str:email>/', views.delete_parent_by_email, name='delete_parent_by_email'),
    path('coaches/', views.coaches, name='coaches'),
    path('manage_team/', views.manage_team, name='manage_team'),
    # path('edit_team_by_email/<str:coach_email>/', views.edit_team_by_email, name='edit_team_by_email'),
    # path('delete_team_by_email/<str:coach_email>/', views.delete_team_by_email, name='delete_team_by_email'),
    path('create/',views.create,name='create'),
    path('manage-schedules/', views.manage_schedules, name='manage_schedules'),
    path('communicate_with_players/',views.communicate_with_players, name='communicate_with_players'),
     path('send_message/', views.send_message, name='send_message'),
    path('get_messages/<str:user_id>/', views.get_messages, name='get_messages'),
    path('editcoachprofile/', views.editcoachprofile, name='editcoachprofile'),
    path('playerprofile/', views.playerprofile, name='playerprofile'),
    path('workouts/',views.workouts, name='workouts'),
    path('viewworkouts/',views.viewworkouts, name='viewworkouts'),
    path('viewschedules/',views.viewschedules, name='viewschedules'), 
    path('viewupdates/',views.viewupdates, name='viewupdates'),
    path('updates/',views.updates, name='updates'),
    path('coachprofile/',views.coachprofile, name='coachprofile'),
    path('edit-coach/<str:email>/', views.edit_coach_profile, name='edit_coach_profile'),
    path('edit_coach_profile/',views.edit_coach_profile, name='edit_coach_profile'),
    path('managerdasboard/',views.managerdasboard, name='managerdasboard'), 
    path('teamupdate/',views.teamupdate, name='teamupdate'),
    path('viewteamcoach/',views.viewteamcoach, name='viewteamcoach'),
    path('logout/', views.logout_view, name='logout'),
    path('lineups/',views.lineups, name='lineups'),
    path('payment/',views.payment, name='payment'),
    path('attendance/',views.attendance, name='attendance'),
    path('viewlineups/',views.viewlineups, name='viewlineups'),
    path('session/',views.session, name='session'),
    path('markattendance/',views.markattendance, name='markattendance'),
    path('viewattendance/',views.viewattendance, name='viewattendance'),


]

