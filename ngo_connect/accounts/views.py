from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

from .models import Profile, NGO


# ---------------- HOME ----------------
def home(request):
    return render(request, 'frontpage.html')


# ---------------- LOGIN + REGISTER ----------------
def login_page(request):

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # ---------- LOGIN ----------
        if form_type == "login":

            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)

                # ADMINS → DASHBOARD
                if user.is_staff or user.is_superuser:
                    return redirect('/dashboard/')

                # NORMAL USERS → HOME
                return redirect('/')

            return render(request, 'login.html', {
                "error": "Invalid credentials"
            })

        # ---------- REGISTER ----------
        elif form_type == "register":

            username = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            phone = request.POST.get("phone")

            dob_input = request.POST.get("dob")
            dob = None

            if dob_input:
                try:
                    dob = datetime.strptime(
                        dob_input,
                        "%Y-%m-%d"
                    ).date()
                except ValueError:
                    dob = None

            if User.objects.filter(username=username).exists():
                return render(request, 'login.html', {
                    "error": "User already exists"
                })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            Profile.objects.create(
                user=user,
                phone=phone or "",
                dob=dob
            )

            return redirect('/login/')

    return render(request, 'login.html')


# ---------------- LOGOUT ----------------
def logout_user(request):
    logout(request)
    return redirect('/')


# ---------------- PROFILE ----------------
@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        profile.phone = request.POST.get("phone") or ""

        dob_input = request.POST.get("dob")

        if dob_input:
            try:
                profile.dob = datetime.strptime(
                    dob_input,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                profile.dob = None

        profile.skills = request.POST.get("skills") or ""
        profile.interests = request.POST.get("interests") or ""

        if request.FILES.get("profile_pic"):
            profile.profile_pic = request.FILES.get("profile_pic")

        profile.save()

    skills_list = (
        profile.skills.split(",")
        if profile.skills else []
    )

    interests_list = (
        profile.interests.split(",")
        if profile.interests else []
    )

    return render(request, 'profile.html', {
        "profile": profile,
        "skills_list": skills_list,
        "interests_list": interests_list
    })


# ---------------- ACTIVITIES ----------------
@login_required
def activities(request):
    return render(request, 'activities.html')


# ---------------- EVENTS ----------------
def events(request):
    return render(request, 'events.html')


# ---------------- NGOS ----------------
def ngos(request):

    # ==========================
    # ADMIN NGO MANAGEMENT
    # ==========================
    if request.user.is_authenticated and request.user.is_staff:

        if request.method == "POST":

            action = request.POST.get("action")
            ngo_id = request.POST.get("ngo_id")

            if action and ngo_id:

                ngo = get_object_or_404(NGO, id=ngo_id)

                if action == "approve":
                    ngo.status = "Approved"
                    ngo.save()

                elif action == "reject":
                    ngo.status = "Rejected"
                    ngo.save()

                elif action == "delete":
                    ngo.delete()

                return redirect('ngos')

        ngos_list = NGO.objects.all().order_by('-created_at')

        return render(request, 'ngos.html', {
            "ngos": ngos_list,
            "is_admin": True,
            "total_ngos": NGO.objects.count(),
            "approved_ngos": NGO.objects.filter(
                status="Approved"
            ).count(),
            "pending_ngos": NGO.objects.filter(
                status="Pending"
            ).count(),
            "rejected_ngos": NGO.objects.filter(
                status="Rejected"
            ).count(),
        })

    # ==========================
    # NORMAL USER NGO SUBMISSION
    # ==========================
    if request.method == "POST":

        NGO.objects.create(
            name=request.POST.get("ngo_name"),
            contact_person=request.POST.get("contact_person"),
            contact_email=request.POST.get("email"),
            description=request.POST.get("description"),
            status="Pending"
        )

        return redirect('ngos')

    # ==========================
    # NORMAL USER VIEW
    # ==========================
    ngos_list = NGO.objects.filter(
        status="Approved"
    ).order_by('-created_at')

    return render(request, 'ngos.html', {
        "ngos": ngos_list,
        "is_admin": False,
    })

# ---------------- ADMIN DASHBOARD ----------------
@login_required
@staff_member_required
def dashboard(request):

    total_users = User.objects.count()
    total_ngos = NGO.objects.count()

    context = {
        "total_users": total_users,
        "total_ngos": total_ngos,
    }

    return render(request, 'dashboard.html', context)