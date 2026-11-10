"""MewCP Google Classroom tool registration."""

from fastmcp import FastMCP

from .aliases_tools import register_aliases_tools
from .announcements_tools import register_announcements_tools
from .courses_tools import register_courses_tools
from .coursework_tools import register_coursework_tools
from .coursework_materials_tools import register_coursework_materials_tools
from .guardian_invitations_tools import register_guardian_invitations_tools
from .guardians_tools import register_guardians_tools
from .invitations_tools import register_invitations_tools
from .registrations_tools import register_registrations_tools
from .rubrics_tools import register_rubrics_tools
from .student_group_members_tools import register_student_group_members_tools
from .student_groups_tools import register_student_groups_tools
from .student_submissions_tools import register_student_submissions_tools
from .students_tools import register_students_tools
from .teachers_tools import register_teachers_tools
from .topics_tools import register_topics_tools
from .user_profiles_tools import register_user_profiles_tools


def register_tools(mcp: FastMCP) -> None:
    register_aliases_tools(mcp)
    register_announcements_tools(mcp)
    register_courses_tools(mcp)
    register_coursework_tools(mcp)
    register_coursework_materials_tools(mcp)
    register_guardian_invitations_tools(mcp)
    register_guardians_tools(mcp)
    register_invitations_tools(mcp)
    register_registrations_tools(mcp)
    register_rubrics_tools(mcp)
    register_student_group_members_tools(mcp)
    register_student_groups_tools(mcp)
    register_student_submissions_tools(mcp)
    register_students_tools(mcp)
    register_teachers_tools(mcp)
    register_topics_tools(mcp)
    register_user_profiles_tools(mcp)
