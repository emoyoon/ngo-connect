from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.db import IntegrityError
from .models import Activity, Enrollment


@login_required
def activities(request):

    # ---------- ENROLL ACTION ----------
    if request.method == "POST":
        activity_id = request.POST.get("activity_id")

        if not activity_id:
            print("❌ No activity ID received")
            return redirect('activities')

        activity = get_object_or_404(Activity, id=activity_id)

        # check if already enrolled
        already_enrolled = Enrollment.objects.filter(
            user=request.user,
            activity=activity
        ).exists()

        # ---------- CONDITIONS ----------
        if activity.date < now().date():
            print("⚠️ Cannot enroll in past activity")

        elif activity.status != "Open":
            print("⚠️ Activity not open")

        elif activity.seats <= 0:
            print("⚠️ No seats left")
            activity.status = "Closed"
            activity.save()

        elif already_enrolled:
            print("⚠️ User already enrolled")

        # ---------- SUCCESS ----------
        else:
            try:
                Enrollment.objects.create(
                    user=request.user,
                    activity=activity
                )

                activity.seats -= 1

                if activity.seats == 0:
                    activity.status = "Closed"

                activity.save()

                print("✅ ENROLLED SUCCESSFULLY")

            except IntegrityError:
                print("⚠️ Duplicate enrollment prevented (DB level)")

        return redirect('activities')


    # ---------- FETCH DATA ----------
    activities = Activity.objects.all().order_by('date')

    user_enrollments = Enrollment.objects.filter(
        user=request.user
    ).select_related('activity')

    # faster lookup
    enrolled_ids = set(
        user_enrollments.values_list('activity_id', flat=True)
    )

    return render(request, 'activities.html', {
        "activities": activities,
        "enrolled_ids": enrolled_ids,
        "user_enrollments": user_enrollments
    })