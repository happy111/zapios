from django.db import models
from django.contrib.auth.models import User
from UserRole.models import ManagerProfile
from Brands.models import Company
from Outlet.models import OutletProfile

# Create your models here.

class StaffAttendance(models.Model):
    status_choice = (
        ("present", "Present"),
        ("lwp", "Leave without pay"),
        ("cl", "Casual leave"),
        ("el", "Earned leave"),
        ("weeklyoff", "Weekly Off"),
    )
    auth_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_attendance",
        null=True,
        blank=True,
    )

    profile = models.ForeignKey(
        ManagerProfile,
        related_name="staff_attendance",
        on_delete=models.CASCADE,
        verbose_name="Staff",
        limit_choices_to={"active_status": "1"},
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        verbose_name="Staff Member Name"
    )
    time_in = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Time In")
    time_out = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Time Out")
    status = models.CharField(
        choices=status_choice,
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Status",
    )
    is_billprint = models.BooleanField(
        default=0, 
        verbose_name="Is Bill print")
    company = models.ForeignKey(
        Company,
        related_name="company_attendance",
        on_delete=models.CASCADE,
        verbose_name="Company",
        limit_choices_to={"active_status": "1"},
        null=True,
        blank=True,
    )
    outlet = models.ForeignKey(
        OutletProfile,
        related_name="outlet_attendance",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    temperature = models.CharField(
        max_length=50, 
        null=True, 
        blank=True, 
        verbose_name="Staff Name"
    )
    active_status = models.BooleanField(
        default=0, 
        verbose_name="Login/Logout")
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Creation Date & Time"
    )
    updated_at = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Updation Date & Time"
    )

    class Meta:
        verbose_name = "Staff Attendance"
        verbose_name_plural = "Staff Attendance"

    def __str__(self):
        return str(self.name)



class AttendanceTime(models.Model):
    status_choice = (
        ("present", "Present"),
        ("lwp", "Leave without pay"),
        ("cl", "Casual leave"),
        ("el", "Earned leave"),
        ("weeklyoff", "Weekly Off"),
    )
    attendance_id = models.ForeignKey(StaffAttendance,
     related_name='AttendanceTime_attendance_id',
     on_delete=models.CASCADE,
     verbose_name='attendance_id')
    time_in = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Time In")
    time_out = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Time Out")
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Creation Date & Time"
    )
    status = models.CharField(
        choices=status_choice,
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Status",
    )

    class Meta:
        verbose_name = "Staff AttendanceTime"
        verbose_name_plural = "Staff AttendanceTime"

    def __str__(self):
        return str(self.attendance_id)



