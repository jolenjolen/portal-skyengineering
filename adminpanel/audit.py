"""
Author: Jolen Mascarenhas (w2078969)
Description: Helper to write audit log entries.
             Import and call log_action() from any view.
"""

from django.utils import timezone
from core.models import TblAudit, TblUser


def log_action(request, action: str):
    """
    Writes one row to tbl_audit.
    action — a plain-English description, e.g. "Created user jsmith"
    """
    user_id = request.session.get('user_id')
    user = None
    if user_id:
        try:
            user = TblUser.objects.get(id=user_id)
        except TblUser.DoesNotExist:
            pass

    TblAudit.objects.create(
        user=user,
        action=action,
        datetime=timezone.now(),
    )