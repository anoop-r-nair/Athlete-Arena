from datetime import datetime, timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
import firebase_admin
from firebase_admin import auth, credentials, firestore, storage
import os
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_control



# Initialize Firebase Admin SDK
cred_path = os.path.join(os.path.dirname(__file__), 'C:/Users/Anoop/sports_team_management/sports_team_management/athletarena-firebase-adminsdk-q957f-b59ba119bd.json')
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Home view
def index(request):
    return render(request, 'accounts/index.html')

# Signup view
def signup(request):
    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')  # Ensure passwords match
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        userType = request.POST.get('userType')  # Ensure to get 'userType' from the form

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')

        try:
            # Create a new user in Firebase Authentication
            user = auth.create_user(email=email, password=password)
            
            # Save the user's details in Firestore
            user_ref = db.collection('users').document(user.uid)
            user_ref.set({
                'email': email,
                'userType': userType,
                'phone': phone,
                'name': name,
            })

            messages.success(request, 'User created successfully.')
            return redirect('login')

        except Exception as e:
            # Log the error (optional)
            print(f"Error creating user: {str(e)}")
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'accounts/signup.html')

    return render(request, 'accounts/signup.html')

def signupcoach(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        
        try:
            # Create a new user in Firebase Authentication
            user = auth.create_user(email=email, password=password)
            
            # Save the user's details in Firestore with 'uid' as document ID
            user_ref = db.collection('coaches').document(user.uid)
            user_ref.set({
                'email': email,
                'uid': user.uid,  # Store uid
                'address': address,
                'phone': phone,
                'name': name,
            })
            messages.success(request, 'Coach created successfully')
            return redirect('login')  # Ensure 'login' is a valid URL name
        except Exception as e:
            # Log the exception (optional)
            print(f"Error creating coach: {e}")
            messages.error(request, f"Error: {str(e)}")
            return redirect('signupcoach')  # Redirect back to signup on error
    else:
        return render(request, 'accounts/signupcoach.html')
    
def signupparent(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        name = request.POST.get('name')
        
        try:
            # Create a new user in Firebase Authentication
            user = auth.create_user(email=email, password=password)
            
            # Save the user's details in Firestore with 'uid' as document ID
            user_ref = db.collection('parent').document(user.uid)
            user_ref.set({
                'email': email,
                'uid': user.uid,  # Store uid
                'address': address,
                'phone': phone,
                'name': name,
            })
            messages.success(request, 'Coach created successfully')
            return redirect('login')  # Ensure 'login' is a valid URL name
        except Exception as e:
            # Log the exception (optional)
            print(f"Error creating coach: {e}")
            messages.error(request, f"Error: {str(e)}")
            return redirect('signupparent')  # Redirect back to signup on error
    else:
        return render(request, 'accounts/signupparent.html')    

# Login view

# def coach_login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
        
#         try:
#             user = auth.get_user_by_email(email)
#             coach_ref = db.collection('coaches').document(user.uid)
#             coach_doc = coach_ref.get()
            
#             if coach_doc.exists:
#                 # Coach exists, proceed to login
#                 # Your logic to render dashboard or homepage for coach
#                 return render(request, 'accounts/manage_team.html', {'coach': coach_doc.to_dict()})
#             else:
#                 return JsonResponse({'error': 'You are not registered as a coach.'})
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
    
#     return render(request, 'login.html')

# Admin login view (optional, depending on how you handle admin login)
def admin_login(request):
    return render(request, 'accounts/admin_login.html')

# Admin dashboard view

def admin_dashboard(request):
    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.stream()]
    return render(request, 'accounts/admin_dashboard.html', {'users': users})

def create(request):
    if request.method == 'POST':
        coachname = request.POST.get('coachname')
        players = request.POST.get('players').split(',')
        teamname = request.POST.get('teamname')

        try:
            # Save the team details in Firestore
            team_ref = db.collection('teams').document()
            team_ref.set({
                'coachname': coachname,
                'players': players,
                'teamname': teamname,
            })
            messages.success(request, 'Team created successfully')
            return redirect('manage_team')  # Replace with the actual URL name for managing teams
        except Exception as e:
            messages.error(request, f"Error creating team: {str(e)}")

    return render(request, 'accounts/manage_team.html')

# def manage_teams(request):
#     return render(request, 'teams.html')

# def get_teams(request):
#     try:
#         teams_ref = db.collection('teams')
#         teams = []
#         for doc in teams_ref.stream():
#             team = doc.to_dict()
#             team['id'] = doc.id
#             teams.append(team)
#         return JsonResponse({'teams': teams}, status=200)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)


# def delete_team(request, team_id):
#     if request.method == 'DELETE':
#         try:
#             db.collection('teams').document(team_id).delete()
#             return JsonResponse({'message': 'Team deleted successfully'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

# def update_team(request, team_id):
#     if request.method == 'POST':
#         data = request.POST
#         try:
#             team_data = {
#                 'teamname': data.get('teamname'),
#                 'coachname': data.get('coachname'),
#                 'players': data.get('players').split(',')
#             }
#             db.collection('teams').document(team_id).update(team_data)
#             return JsonResponse({'message': 'Team updated successfully'}, status=200)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request method'}, status=405)


# Delete user view (only for admin)
@staff_member_required
def delete_user(request, email):
    try:
        # Fetch the user by email
        user = auth.get_user_by_email(email)
        # Delete the user from Firebase Authentication
        auth.delete_user(user.uid)
        # Delete the user document from Firestore
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).stream()
        for doc in query:
            doc.reference.delete()
        messages.success(request, 'User deleted successfully')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('admin_dashboard')

# Update user view (only for admin)
@staff_member_required
def update_user(request, email):
    try:
        # Fetch user details from Firestore
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).stream()
        user_doc = None
        doc_reference = None
        for doc in query:
            user_doc = doc.to_dict()
            doc_reference = doc.reference
            break
        
        if request.method == 'POST':
            name = request.POST.get('name')
            email= request.POST.get('email')
            userType = request.POST.get('userType')
            users = request.POST.get('users')
            
            # Update user details in Firestore
            if user_doc:
                doc_reference.update({
                    'name': name,
                    'email': email,
                    'userType': userType,
                    'users': users,
                })
                messages.success(request, 'User updated successfully')
                return redirect('admin_dashboard')
        
        return render(request, 'accounts/update_user.html', {'user': user_doc})

    except Exception as e:
        messages.error(request, str(e))
        return redirect('admin_dashboard')
    
# def coaches_view(request):
#     try:
#         coaches_ref = db.collection('coaches')
#         docs = coaches_ref.stream()

#         coaches_list = []
#         for doc in docs:
#             coach_data = doc.to_dict()
#             print(coach_data)  # This will print the coach data in the console
#             coaches_list.append(coach_data)

#         return render(request, 'accounts/coaches.html', {'coaches': coaches_list})

#     except Exception as e:
#         print("Error:", str(e))
#         return render(request, 'accounts/coaches.html', {'error': str(e), 'coaches': []})


def update_coach_by_email(request, email):
    coaches_ref = db.collection('coaches')
    query = coaches_ref.where('email', '==', email).limit(1).get()

    if not query:
        return render(request, 'accounts/error.html', {'message': 'Coach not found'})

    coach_ref = query[0].reference  # Get the document reference

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Get the uploaded files, if any
        profile_picture = request.FILES.get('profilePicture')
        resume = request.FILES.get('resume')

        # Create a dictionary for fields to update
        updated_data = {
            'name': name,
            'address': address,
            'phone': phone,
        }

        # If profile picture was uploaded, upload to Firebase storage
        if profile_picture:
            # Assuming you have Firebase storage configured
            bucket = storage.bucket()
            blob = bucket.blob(f'coaches/{email}/profile_picture.jpg')
            blob.upload_from_file(profile_picture)
            # Get the public URL for the uploaded profile picture
            updated_data['profilePicture'] = blob.public_url

        # If resume was uploaded, upload to Firebase storage
        if resume:
            blob = bucket.blob(f'coaches/{email}/resume.pdf')
            blob.upload_from_file(resume)
            updated_data['resume'] = blob.public_url

        # Update the Firestore document with new data
        coach_ref.update(updated_data)

        return redirect('coaches')  # Redirect back to the coaches list

    # For GET request, display the current coach data
    coach = coach_ref.get().to_dict()
    return render(request, 'accounts/update_coach.html', {'coach': coach})


def delete_coach_by_email(request, email):
    coaches_ref = db.collection('coaches')
    query = coaches_ref.where('email', '==', email).limit(1).get()

    if not query:
        return render(request, 'accounts/error.html', {'message': 'Coach not found'})

    coach_ref = query[0].reference  # Get the document reference
    coach_ref.delete()
    return redirect('coaches')  # Redirect back to the coaches list

def update_parent_by_email(request, email):
    parents_ref = db.collection('parents')
    query = parents_ref.where('email', '==', email).limit(1).get()

    if not query:
        return render(request, 'accounts/error.html', {'message': 'Parent not found'})

    parent_ref = query[0].reference  # Get the document reference

    if request.method == 'POST':
        # Get data from the form
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Update the Firestore document
        parent_ref.update({
            'name': name,
            'address': address,
            'phone': phone,
        })
        return redirect('parents')  # Redirect back to the parents list

    # For GET request, display the current parent data
    parent = parent_ref.get().to_dict()
    return render(request, 'accounts/update_parent.html', {'parent': parent})

def delete_parent_by_email(request, email):
    parents_ref = db.collection('parents')
    query = parents_ref.where('email', '==', email).limit(1).get()

    if not query:
        return render(request, 'accounts/error.html', {'message': 'Parent not found'})

    parent_ref = query[0].reference  # Get the document reference
    parent_ref.delete()
    return redirect('parents')  # Redirect back to the parents list



@staff_member_required
def manage_teams(request):
    try:
        # Retrieve all coaches
        coaches_ref = db.collection('coaches')
        coaches_docs = coaches_ref.stream()
        coaches = [{'email': doc.id, **doc.to_dict()} for doc in coaches_docs]

        # Retrieve all players
        players_ref = db.collection('users').where('role', '==', 'player')
        players_docs = players_ref.stream()
        players = [{'email': doc.id, **doc.to_dict()} for doc in players_docs]

        # Retrieve all teams
        teams_ref = db.collection('teams')
        teams_docs = teams_ref.stream()
        teams = [{'id': doc.id, **doc.to_dict()} for doc in teams_docs]

        return render(request, 'manage_team.html', {
            'coaches': coaches,
            'players': players,
            'teams': teams,
        })
    except Exception as e:
        messages.error(request, f'Error retrieving data: {e}')
        return redirect('manage_team')

@staff_member_required
def edit_team_by_email(request, coach_email):
    teams_ref = db.collection('teams')
    team_query = teams_ref.where('coach_email', '==', coach_email).stream()
    team_doc = next(team_query, None)

    if not team_doc:
        messages.error(request, 'Team not found')
        return redirect('manage_teams')

    team = team_doc.to_dict()

    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.stream()]
    coaches = [user for user in users if user.get('role') == 'coach']
    players = [user for user in users if user.get('role') == 'player']

    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        new_coach_email = request.POST.get('coach_email')
        player_emails = request.POST.getlist('player_emails')

        team_doc.reference.update({
            'team_name': team_name,
            'coach_email': new_coach_email,
            'players': player_emails,
        })

        messages.success(request, 'Team updated successfully')
        return redirect('manage_teams')

    return render(request, 'accounts/edit_team.html', {
        'team': team,
        'coaches': coaches,
        'players': players,
    })


@staff_member_required
def delete_team_by_email(request, coach_email):
    try:
        # Find the team document where the coach_email matches
        teams_ref = db.collection('teams')
        team_query = teams_ref.where('coach_email', '==', coach_email).stream()
        team_doc = next(team_query, None)

        if not team_doc:
            messages.error(request, 'Team not found')
            return redirect('manage_teams')

        # Delete the team document
        team_doc.reference.delete()
        messages.success(request, 'Team deleted successfully')
    except Exception as e:
        messages.error(request, str(e))

    return redirect('manage_teams')

def manage_schedules(request):
    if request.method == 'POST':
        schedule_type = request.POST.get('schedule_type')
        title = request.POST.get('title')
        description = request.POST.get('description')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')

        try:
            schedule_data = {
                'schedule_type': schedule_type,
                'title': title,
                'description': description,
                'start_time': start_time,
                'end_time': end_time,
                'location': location,
                'created_at': timezone.now(),
                'updated_at': timezone.now(),
            }

            # Add the schedule to Firestore
            db.collection('schedules').add(schedule_data)
            
            # Print success message if saved successfully
            messages.success(request, 'Schedule successfully saved.')

            return redirect('manage_schedules')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('manage_schedules')

    try:
        # Fetch schedules from Firestore
        schedules_ref = db.collection('schedules')
        schedules = schedules_ref.stream()
        schedule_list = [schedule.to_dict() for schedule in schedules]

        return render(request, 'manage_schedules.html', {'schedules': schedule_list})
    
    except Exception as e:
        messages.error(request, f'An error occurred while fetching schedules: {str(e)}')
        return render(request, 'manage_schedules.html', {'schedules': []})

# Role-specific dashboard views

def coach_dashboard(request):
    return render(request, 'accounts/coach_dashboard.html')


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)

def playerprofile(request):
    return render(request, 'accounts/playerprofile.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)

def playerprofile(request):
    return render(request, 'accounts/playerprofile.html')


def player_dashboard(request):
    return render(request, 'accounts/player_dashboard.html')

def playerprofile(request):
    return render(request, 'accounts/playerprofile.html')

def lineups(request):
    users_ref = db.collection('users')
    users = [doc.to_dict() for doc in users_ref.stream()]
    return render(request, 'accounts/lineups.html', {'users': users})


def registration(request):
    return render(request, 'accounts/registration.html')

def managecoachprofile(request):
    return render(request, 'accounts/managecoachprofile.html')


def team_players(request):
    return render(request, 'accounts/team_players.html')


def formation1(request):
    return render(request, 'accounts/formation1.html')


def formation2(request):
    return render(request, 'accounts/formation2.html')

def viewplayerimage(request):
    return render(request, 'accounts/viewplayerimage.html')








def approvedcoaches(request):
    return render(request, 'accounts/approvedcoaches.html')

def approvedplayers(request):
    return render(request, 'accounts/approvedplayers.html')


def viewplayerdetails(request):
    return render(request, 'accounts/viewplayerdetails.html')



def fanpage(request):
    return render(request, 'accounts/fanpage.html')

def playerdevelopment(request):
    return render(request, 'accounts/playerdevelopment.html')

def fanviewprofile(request):
    return render(request, 'accounts/fanviewprofile.html')

def viewassessment(request):
    return render(request, 'accounts/viewassessment.html')


def practicechange(request):
    return render(request, 'accounts/practicechange.html')


def gameresult(request):
    return render(request, 'accounts/gameresult.html')


def announcement(request):
    return render(request, 'accounts/announcement.html')


def fanviewresult(request):
    return render(request, 'accounts/fanviewresult.html')

def addcoachprofile(request):
    return render(request, 'accounts/addcoachprofile.html')

def updates1(request):
    return render(request, 'accounts/updates1.html')


def schedulefans(request):
    return render(request, 'accounts/schedulefans.html')

def viewprofile(request):
    return render(request, 'accounts/viewprofile.html')

def giveassessment(request):
    return render(request, 'accounts/giveassessment.html')

def medical_staff_dashboard(request):
    return render(request, 'accounts/medical_staff_dashboard.html')

def sports_psychologist_dashboard(request):
    return render(request, 'accounts/sports_psychologist_dashboard.html')

def analytics_expert_dashboard(request):
    return render(request, 'accounts/analytics_expert_dashboard.html')

# Additional views for the app's features
def modules(request):
    return render(request, 'accounts/modules.html')

def schedules(request):
    return render(request, 'accounts/schedules.html')

def teams(request):
    return render(request, 'accounts/teams.html')
def teamupdate(request):
    return render(request, 'accounts/teamupdate.html')
def viewteamcoach(request):
    return render(request, 'accounts/viewteamcoach.html')


def players(request):
    return render(request, 'accounts/players.html')

def manage_schedules(request):
    # Your logic here
    return render(request, 'accounts/manage_schedules.html')

def communicate_with_players(request):
    # Your logic here
    return render(request, 'accounts/communicate_with_players.html')

def workouts(request):
    return render(request, 'accounts/workouts.html') 

def viewworkouts(request):
    return render(request, 'accounts/viewworkouts.html') 

def viewschedules(request):
    return render(request, 'accounts/viewschedules.html') 

def viewupdates(request):
    return render(request, 'accounts/viewupdates.html') 

def updates(request):
    return render(request, 'accounts/updates.html') 

def coachprofile(request):
    return render(request, 'accounts/coachprofile.html') 
def managerdasboard(request):
    return render(request, 'accounts/managerdasboard.html')


# def edit_coach_profile(request, email):
#     # Reference to the coach document in Firestore
#     coach_ref = db.collection('coaches').document(email)
    
#     if request.method == 'POST':
#         # Get updated data from the form
#         updated_name = request.POST.get('name')
#         updated_address = request.POST.get('address')
#         updated_phone = request.POST.get('phone')

#         # Update the coach's data in Firestore
#         coach_ref.update({
#             'name': updated_name,
#             'address': updated_address,
#             'phone': updated_phone
#         })
        
#         return redirect('view_profile')  # Redirect to the desired page after update

#     # Get the current coach data
#     coach = coach_ref.get()
    
#     if coach.exists:
#         coach_data = coach.to_dict()
#         return render(request, 'edit_coach_profile.html', {'coach': coach_data})
#     else:
#         return render(request, 'edit_coach_profile.html', {'error': 'Coach not found'})

def edit_coach_profile(request):
     return render(request, 'accounts/edit_coach_profile.html')


# def logout_view(request):
#     # Log out the user and clear the session
#     logout(request)
#     request.session.flush()
#     # Redirect to login page or any other page
#     return redirect('index')

def logout_view(request):  
    request.session.delete()
    logout(request)
    return redirect('login')


def parents(request):
    parents_ref = db.collection('parents')
    parents_docs = parents_ref.stream()

    # Collecting parent data into a list
    parents = []
    for doc in parents_docs:
        parent = doc.to_dict()
        parents.append(parent)

    return render(request, 'accounts/parents.html', {'parents': parents})

def manage_team(request):
    # Your logic here
    return render(request, 'accounts/manage_team.html') 

def viewlineups(request):
    return render(request, 'accounts/viewlineups.html') 


def attendance(request):
    return render(request, 'accounts/attendance.html')

def markattendance(request):
    return render(request, 'accounts/markattendance.html')

def viewattendance(request):
    return render(request, 'accounts/viewattendance.html')

def payment(request):
    return render(request, 'accounts/payment.html')

def paymentplayer(request):
    return render(request, 'accounts/paymentplayer.html')



def session(request):
    return render(request, 'accounts/session.html')

def assigncoach(request):
    return render(request, 'accounts/assigncoach.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = auth.get_user_by_email(email)  # Fetch user by email
            # Here you can add your password verification logic.
            # Since you are using Firebase, you may need to handle password verification in the frontend as you've done.

            # Assuming user verification is successful
            doc = db.collection("users").document(user.uid).get()
            if doc.exists:
                user_data = doc.to_dict()
                user_type = user_data.get('userType')

                # Set session variables
                request.session['user_id'] = user.uid
                request.session['user_email'] = email
                request.session['user_type'] = user_type

                return JsonResponse({'success': True, 'user_type': user_type})
            else:
                return JsonResponse({'success': False, 'error': 'User not found in database.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return render(request, 'accounts/login.html')

def coaches(request):
    try:
        # Fetch all coaches from Firestore
        coaches_ref = db.collection('coaches')
        coaches = [doc.to_dict() for doc in coaches_ref.stream()]
        print(coaches)  # For debugging: Print the coaches data
        return render(request, 'accounts/coaches.html', {'coaches': coaches})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'accounts/coaches.html', {'coaches': []})
    
def editcoachprofile(request):
    try:
        # Fetch all coaches from Firestore
        coaches_ref = db.collection('coaches')
        coaches = [doc.to_dict() for doc in coaches_ref.stream()]
        print(coaches)  # For debugging: Print the coaches data
        return render(request, 'accounts/editcoachprofile.html', {'coaches': coaches})
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'accounts/editcoachprofile.html',  {'coaches': []})    
    

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Admin login check
#         if email == 'admin@gmail.com' and password == 'admin@123':
#             return redirect('modules')  # Redirect to admin dashboard

#         try:
#             # Sign in the user with Firebase Authentication
#             user = auth.get_user_by_email(email)
            
#             # Simulate Firebase Authentication sign-in process
#             # Use Firebase Client SDK for actual user authentication on the client side

#             # Retrieve user details from Firestore
#             user_ref = db.collection('users').document(user.uid)
#             user_data = user_ref.get().to_dict()
            
#             if user_data is None:
#                 messages.error(request, 'User not found in the database.')
#                 return redirect('login')

#             # Check user type and redirect to appropriate dashboard
#             userType = user_data.get('userType')
#             if userType == 'Player':
#                 return redirect('player_dashboard')  # Define URL for player dashboard
#             elif userType == 'Coach':
#                 return redirect('coach_dashboard')  # Define URL for coach dashboard
#             elif userType == 'Admin':
#                 return redirect('admin_dashboard')  # Define URL for admin dashboard
#             else:
#                 messages.error(request, 'User type not recognized.')
#                 return redirect('login')

#         except Exception as e:
#             messages.error(request, f"Login error: {str(e)}")
#             return redirect('login')

#     return render(request, 'accounts/login.html')

# def login(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Admin login check
#         if email == 'admin@gmail.com' and password == 'admin@123':
#             return redirect('modules')  # Redirect to admin dashboard

#         try:
#             # Sign in the user with Firebase Authentication
#             user = auth.get_user_by_email(email)
            
#             # Simulate Firebase Authentication sign-in process
#             # Use Firebase Client SDK for actual user authentication on the client side

#             # Retrieve user details from Firestore
#             user_ref = db.collection('users').document(user.uid)
#             user_data = user_ref.get().to_dict()
            
#             if user_data is None:
#                 messages.error(request, 'User not found in the database.')
#                 return redirect('login')

#             # Check user type and redirect to appropriate dashboard
#             userType = user_data.get('userType')
#             if userType == 'Player':
#                 return redirect('player_dashboard')  # Define URL for player dashboard
#             elif userType == 'Coach':
#                 return redirect('coach_dashboard')  # Define URL for coach dashboard
#             elif userType == 'Admin':
#                 return redirect('admin_dashboard')  # Define URL for admin dashboard
#             else:
#                 messages.error(request, 'User type not recognized.')
#                 return redirect('login')

#         except Exception as e:
#             messages.error(request, f"Login error: {str(e)}")
#             return redirect('login')

#     return render(request, 'accounts/login.html')

def send_message(request):
    if request.method == 'POST':
        sender_id = request.POST.get('sender_id')
        receiver_id = request.POST.get('receiver_id')
        message_content = request.POST.get('message')

        # Add message to Firestore
        message_data = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message_content,
            'timestamp': datetime.datetime.now()
        }
        db.collection('messages').add(message_data)

        return JsonResponse({'status': 'Message sent successfully'})

def get_messages(request, user_id):
    # Fetch messages from Firestore for the given user_id
    messages = db.collection('messages').where('receiver_id', '==', user_id).stream()
    message_list = [{'sender_id': message.get('sender_id'), 'message': message.get('message'), 'timestamp': message.get('timestamp')} for message in messages]


    return JsonResponse({'messages': message_list})    


    return JsonResponse({'messages': message_list})  

    return JsonResponse({'messages': message_list})    


    return JsonResponse({'messages': message_list})  






