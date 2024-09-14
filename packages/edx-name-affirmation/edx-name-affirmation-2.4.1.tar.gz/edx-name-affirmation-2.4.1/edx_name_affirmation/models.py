"""
Database models for edx_name_affirmation.
"""

from config_models.models import ConfigurationModel
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from edx_name_affirmation.statuses import VerifiedNameStatus

try:
    from lms.djangoapps.verify_student.models import SoftwareSecurePhotoVerification
except ImportError:
    SoftwareSecurePhotoVerification = None

User = get_user_model()


class VerifiedName(TimeStampedModel):
    """
    This model represents a verified name for a user, with a link to the source
    through `verification_attempt_id` or `proctored_exam_attempt_id` if applicable.

    .. pii: Contains name fields.
    .. pii_types: name
    .. pii_retirement: local_api
    """
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    verified_name = models.CharField(max_length=255, db_index=True)

    # Snapshot of the user's UserProfile `name` upon creation
    profile_name = models.CharField(max_length=255, null=True)

    # Reference to an external ID verification or proctored exam attempt
    verification_attempt_id = models.PositiveIntegerField(null=True, blank=True)
    proctored_exam_attempt_id = models.PositiveIntegerField(null=True, blank=True)

    status = models.CharField(
        max_length=32,
        choices=[(st.value, st.value) for st in VerifiedNameStatus],
        default=VerifiedNameStatus.PENDING.value,
    )
    history = HistoricalRecords()

    class Meta:
        """ Meta class for this Django model """
        db_table = 'nameaffirmation_verifiedname'
        verbose_name = 'verified name'

    @property
    def verification_attempt_status(self):
        "Returns the status associated with its SoftwareSecurePhotoVerification with verification_attempt_id if any."

        if not self.verification_attempt_id or not SoftwareSecurePhotoVerification:
            return None

        try:
            verification = SoftwareSecurePhotoVerification.objects.get(id=self.verification_attempt_id)
            return verification.status

        except ObjectDoesNotExist:
            return None


class VerifiedNameConfig(ConfigurationModel):
    """
    This model provides various configuration fields for users regarding their
    verified name.
    .. no_pii: This model has no PII.
    """
    KEY_FIELDS = ('user',)

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='verified_name_config')
    use_verified_name_for_certs = models.BooleanField(default=False)

    class Meta:
        """ Meta class for this Django model """
        db_table = 'nameaffirmation_verifiednameconfig'
        verbose_name = 'verified name config'
