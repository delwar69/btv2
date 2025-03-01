from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile, ClubMember
from django.utils.timezone import now

# Signal to create or update the UserProfile and ClubMember when a CustomUser is created or updated
@receiver(post_save, sender=CustomUser)
def save_user_profile_and_club_member(sender, instance, created, **kwargs):
    if created:
        # Create the UserProfile only if it does not already exist
        user_profile, created_profile = UserProfile.objects.get_or_create(user=instance)
        
        # Fetch date_of_birth from the UserProfile, if it exists
        date_of_birth = user_profile.date_of_birth if user_profile.date_of_birth else None
        
        # Create the ClubMember with default values if a new user is created
        ClubMember.objects.get_or_create(
            user=instance,
            defaults={
                'full_name': f"{instance.first_name} {instance.last_name}",
                'email': instance.email,
                'joining_date': now(),  # Default to the current date
                'date_of_birth': date_of_birth,  # Use the UserProfile's date_of_birth
            }
        )
    else:
        # Update the UserProfile if the user is updated
        if hasattr(instance, 'userprofile'):
            instance.userprofile.save()

        # Update the ClubMember if the user is updated
        if hasattr(instance, 'club_member'):
            instance.club_member.save()
