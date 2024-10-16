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
<<<<<<< HEAD

=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 46d1897297df01375989a552f6ec599eaf15b63a
>>>>>>> 9ea7a12c623032af2a641b10172abf8ebae95c5e
    path('logout/', views.logout_view, name='logout'),
    path('lineups/',views.lineups, name='lineups'),
    path('payment/',views.payment, name='payment'),
    path('attendance/',views.attendance, name='attendance'),
    path('viewlineups/',views.viewlineups, name='viewlineups'),
    path('session/',views.session, name='session'),
    path('markattendance/',views.markattendance, name='markattendance'),
    path('viewattendance/',views.viewattendance, name='viewattendance'),
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 9ea7a12c623032af2a641b10172abf8ebae95c5e
    path('fanpage/',views.fanpage, name='fanpage'),
    path('schedulefans/',views.schedulefans, name='schedulefans'),
    path('viewprofile/',views.viewprofile, name='viewprofile'),
    path('playerdevelopment/',views.playerdevelopment, name='playerdevelopment'),
    path('giveassessment/',views.giveassessment, name='giveassessment'),
    path('viewassessment/',views.viewassessment, name='viewassessment'),
    path('fanviewprofile/',views.fanviewprofile, name='fanviewprofile'),
    path('fanviewresult/',views.fanviewresult, name='fanviewresult'),
    path('addcoachprofile/',views.addcoachprofile, name='addcoachprofile'),
    path('updates1/',views.updates1, name='updates1'),
    path('practicechange/',views.practicechange, name='practicechange'),
    path('gameresult/',views.gameresult, name='gameresult'),
    path('announcement/',views.announcement, name='announcement'),
<<<<<<< HEAD
    path('registration/',views.registration, name='registration'),
    path('viewplayerdetails/',views.viewplayerdetails, name='viewplayerdetails'),
    path('approvedcoaches/',views.approvedcoaches, name='approvedcoaches'),
    path('approvedplayers/',views.approvedplayers, name='approvedplayers'),
    path('managecoachprofile/',views.managecoachprofile, name='managecoachprofile'),
    path('team_players/',views.team_players, name='team_players'),


=======



=======

=======
>>>>>>> 9b8fda4e33aea8a09a1cbbdf622aa63b4ff1f31a
>>>>>>> 03012c97d16d6b4ed142a47da138b4166c1dff1c
>>>>>>> 46d1897297df01375989a552f6ec599eaf15b63a
>>>>>>> 9ea7a12c623032af2a641b10172abf8ebae95c5e

]

