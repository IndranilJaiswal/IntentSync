"""
Coverage Gap Models

Purpose:
---------
Represents assurance gaps where the platform
does not yet possess an executable claim.

Coverage gaps differ from evidence gaps.

Evidence Gap:
-------------
A claim exists but required evidence
is missing.

Coverage Gap:
-------------
No executable claim definition exists.

Author:
-------
Indranil Jaiswal
AI Assurance Platform
"""

from dataclasses import dataclass


@dataclass
class CoverageGap:
    """
    Represents a claim that cannot currently
    be assured by the platform.
    """

    claim_id: str
    reason: str
