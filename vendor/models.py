from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import *

# Create your models here.
class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=255)
    vendor_slug = models.SlugField(max_length=255, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            original = Vendor.objects.get(pk=self.pk)
            if original.is_approved != self.is_approved:
                if self.is_approved == True:
                    # Send notification email : Approved
                    mail_subject = 'Congradulation!!! You account has been approved.'
                    mail_template = 'accounts/emails/admin_approval_emai.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
                    send_notification(mail_subject, mail_template, context=context)
                else:
                    # Send notification email : Approve is panding
                    mail_subject = 'Sorry!!! You account has been approved.'
                    mail_template = 'accounts/emails/admin_approval_emai.html'
                    context = {
                        'user': self.user,
                        'is_approved': self.is_approved,
                    }
        return super(Vendor, self).save(*args, **kwargs)
    
