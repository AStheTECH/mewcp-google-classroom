#!/usr/bin/env python3
"""
MCP Server for Google Classroom API
Provides access to Google Classroom operations through Model Context Protocol

Documentation referred : https://googleapis.github.io/google-api-python-client/docs/dyn/classroom_v1.html
"""

import json
import logging
import argparse
from typing import Dict

from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Google Classroom API scopes
SCOPES = [
    "https://www.googleapis.com/auth/classroom.addons.student",  # 	See and update its own attachments to posts in Google Classroom
    "https://www.googleapis.com/auth/classroom.addons.teacher",  # 	See, create, and update its own attachments to posts in classes you teach in Google Classroom
    "https://www.googleapis.com/auth/classroom.announcements",  # 	View and manage announcements in Google Classroom
    "https://www.googleapis.com/auth/classroom.announcements.readonly",  # 	View announcements in Google Classroom
    "https://www.googleapis.com/auth/classroom.courses",  # 	See, edit, create, and permanently delete your Google Classroom classes
    "https://www.googleapis.com/auth/classroom.courses.readonly",  # 	View your Google Classroom classes
    "https://www.googleapis.com/auth/classroom.coursework.me",  # 	See, create and edit coursework items including assignments, questions, and grades
    "https://www.googleapis.com/auth/classroom.coursework.me.readonly",  # 	View your course work and grades in Google Classroom
    "https://www.googleapis.com/auth/classroom.coursework.students",  # 	Manage course work and grades for students in the Google Classroom classes you teach and view the course work and grades for classes you administer
    "https://www.googleapis.com/auth/classroom.coursework.students.readonly",  # 	View course work and grades for students in the Google Classroom classes you teach or administer
    "https://www.googleapis.com/auth/classroom.courseworkmaterials",  # 	See, edit, and create classwork materials in Google Classroom
    "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",  # 	See all classwork materials for your Google Classroom classes
    "https://www.googleapis.com/auth/classroom.guardianlinks.me.readonly",  # 	View your Google Classroom guardians
    "https://www.googleapis.com/auth/classroom.guardianlinks.students",  # 	View and manage guardians for students in your Google Classroom classes
    "https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly",  # 	View guardians for students in your Google Classroom classes
    "https://www.googleapis.com/auth/classroom.profile.emails",  # 	View the email addresses of people in your classes
    "https://www.googleapis.com/auth/classroom.profile.photos",  # 	View the profile photos of people in your classes
    "https://www.googleapis.com/auth/classroom.push-notifications",  # 	Receive notifications about your Google Classroom data
    "https://www.googleapis.com/auth/classroom.rosters",  # 	Manage your Google Classroom class rosters
    "https://www.googleapis.com/auth/classroom.rosters.readonly",  # 	View your Google Classroom class rosters
    "https://www.googleapis.com/auth/classroom.student-submissions.me.readonly",  # 	View your course work and grades in Google Classroom
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",  # 	View course work and grades for students in the Google Classroom classes you teach or administer
    "https://www.googleapis.com/auth/classroom.topics",  # 	See, create, and edit topics in Google Classroom
    "https://www.googleapis.com/auth/classroom.topics.readonly",  # 	View topics in Google Classroom
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("google-meet-mcp-server")

# Create FastMCP instance
mcp = FastMCP("CL Google Classroom MCP Server")

# Global service instance
_service = None


def _get_token_data(token_data: str) -> Dict:
    """Decode access token JSON string to dictionary"""
    try:
        token_data = json.loads(token_data)
        auth_data = {
            "token": token_data.get("token"),
            "refresh_token": token_data.get("refresh_token"),
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": token_data.get("client_id"),
            "client_secret": token_data.get("client_secret"),
            "scopes": token_data.get("scopes"),
        }
        return auth_data
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode access token: {e}")
        return {}


def _get_service(token_data: str):
    """Create Google Classroom service with provided access token"""
    auth_data = _get_token_data(token_data)
    logger.info("Creating Google Classroom API service with provided access token")
    creds = Credentials(**auth_data)
    service = build("classroom", "v1", credentials=creds)
    logger.info("Google Classroom API service created successfully")
    return service


# =======================================================================================
#                       MCP TOOLS START
# =======================================================================================


@mcp.tool()
def list_courses(token_data: str, student_id: str = None, teacher_id: str = None, course_states: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of courses that the requesting user is permitted to view, restricted to those that match the criteria.

    :param token_data: The JSON string of the user's access token.
    :param student_id: Restricts returned courses to those having a student with the specified identifier.
    :param teacher_id: Restricts returned courses to those having a teacher with the specified identifier.
    :param course_states: Restricts returned courses to those in one of the specified states.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned.
    :return: A JSON string of the list of courses.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().list(
            studentId=student_id,
            teacherId=teacher_id,
            courseStates=course_states,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list courses: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_course(token_data: str, id: str) -> str:
    """
    Returns a course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to return.
    :return: A JSON string of the course.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().get(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course(token_data: str, body: str) -> str:
    """
    Creates a course.

    :param token_data: The JSON string of the user's access token.
    :param body: A JSON string representing the course to create.
    :return: A JSON string of the created course.
    """
    try:
        service = _get_service(token_data)
        course = json.loads(body)
        response = service.courses().create(body=course).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def update_course(token_data: str, id: str, body: str) -> str:
    """
    Updates a course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to update.
    :param body: A JSON string representing the updated course.
    :return: A JSON string of the updated course.
    """
    try:
        service = _get_service(token_data)
        course = json.loads(body)
        response = service.courses().update(id=id, body=course).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to update course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_course(token_data: str, id: str, update_mask: str, body: str) -> str:
    """
    Updates a course. This method is an alias for update(), but only fields specified in updateMask are updated.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to update.
    :param update_mask: Mask that identifies which fields on the course to update.
    :param body: A JSON string representing the updated course.
    :return: A JSON string of the updated course.
    """
    try:
        service = _get_service(token_data)
        course = json.loads(body)
        response = service.courses().patch(id=id, updateMask=update_mask, body=course).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course(token_data: str, id: str) -> str:
    """
    Deletes a course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().delete(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course_alias(token_data: str, course_id: str, body: str) -> str:
    """
    Creates an alias for a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: The identifier of the course.
    :param body: A JSON string representing the alias to create.
    :return: A JSON string of the created alias.
    """
    try:
        service = _get_service(token_data)
        alias = json.loads(body)
        response = service.courses().aliases().create(courseId=course_id, body=alias).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course alias for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_course_aliases(token_data: str, course_id: str, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of aliases for a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: The identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned.
    :return: A JSON string of the list of aliases.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().aliases().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list course aliases for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course_alias(token_data: str, course_id: str, alias: str) -> str:
    """
    Deletes an alias of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: The identifier of the course.
    :param alias: The alias to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().aliases().delete(courseId=course_id, alias=alias).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course alias '{alias}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_announcement(token_data: str, course_id: str, body: str) -> str:
    """
    Creates an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the announcement to create.
    :return: A JSON string of the created announcement.
    """
    try:
        service = _get_service(token_data)
        announcement = json.loads(body)
        response = service.courses().announcements().create(courseId=course_id, body=announcement).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create announcement for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_announcements(token_data: str, course_id: str, announcement_states: str = None, order_by: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of announcements that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param announcement_states: Restriction on the work status to return.
    :param order_by: Sort order for results.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of announcements.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().announcements().list(
            courseId=course_id,
            announcementStates=announcement_states,
            orderBy=order_by,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list announcements for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_announcement(token_data: str, course_id: str, id: str) -> str:
    """
    Returns an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement to return.
    :return: A JSON string of the announcement.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().announcements().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_announcement(token_data: str, course_id: str, id: str, update_mask: str, body: str) -> str:
    """
    Updates an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement to update.
    :param update_mask: Mask that identifies which fields on the announcement to update.
    :param body: A JSON string representing the updated announcement.
    :return: A JSON string of the updated announcement.
    """
    try:
        service = _get_service(token_data)
        announcement = json.loads(body)
        response = service.courses().announcements().patch(courseId=course_id, id=id, updateMask=update_mask, body=announcement).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_announcement(token_data: str, course_id: str, id: str) -> str:
    """
    Deletes an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().announcements().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def modify_announcement_assignees(token_data: str, course_id: str, id: str, body: str) -> str:
    """
    Modifies assignee mode and options of an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement.
    :param body: A JSON string with the modifications.
    :return: A JSON string of the modified announcement.
    """
    try:
        service = _get_service(token_data)
        modifications = json.loads(body)
        response = service.courses().announcements().modifyAssignees(courseId=course_id, id=id, body=modifications).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to modify assignees for announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course_work(token_data: str, course_id: str, body: str) -> str:
    """
    Creates course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the course work to create.
    :return: A JSON string of the created course work.
    """
    try:
        service = _get_service(token_data)
        course_work = json.loads(body)
        response = service.courses().courseWork().create(courseId=course_id, body=course_work).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course work for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_course_work(token_data: str, course_id: str, course_work_states: str = None, order_by: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of course work that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_states: Restriction on the work status to return.
    :param order_by: Sort order for results.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of course work.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().list(
            courseId=course_id,
            courseWorkStates=course_work_states,
            orderBy=order_by,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list course work for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_course_work(token_data: str, course_id: str, id: str) -> str:
    """
    Returns course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work to return.
    :return: A JSON string of the course work.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_course_work(token_data: str, course_id: str, id: str, update_mask: str, body: str) -> str:
    """
    Updates course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work to update.
    :param update_mask: Mask that identifies which fields on the course work to update.
    :param body: A JSON string representing the updated course work.
    :return: A JSON string of the updated course work.
    """
    try:
        service = _get_service(token_data)
        course_work = json.loads(body)
        response = service.courses().courseWork().patch(courseId=course_id, id=id, updateMask=update_mask, body=course_work).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course_work(token_data: str, course_id: str, id: str) -> str:
    """
    Deletes course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def modify_course_work_assignees(token_data: str, course_id: str, id: str, body: str) -> str:
    """
    Modifies assignee mode and options of a course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work.
    :param body: A JSON string with the modifications.
    :return: A JSON string of the modified course work.
    """
    try:
        service = _get_service(token_data)
        modifications = json.loads(body)
        response = service.courses().courseWork().modifyAssignees(courseId=course_id, id=id, body=modifications).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to modify assignees for course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_student_submission(token_data: str, course_id: str, course_work_id: str, id: str) -> str:
    """
    Returns a student submission.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :return: A JSON string of the student submission.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_student_submissions(token_data: str, course_id: str, course_work_id: str, user_id: str = None, states: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of student submissions that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param user_id: Optional argument to restrict returned student submissions to those owned by the student with the specified user ID.
    :param states: Requested submission states.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of student submissions.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().studentSubmissions().list(
            courseId=course_id,
            courseWorkId=course_work_id,
            userId=user_id,
            states=states,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list student submissions for course work '{course_work_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_student_submission(token_data: str, course_id: str, course_work_id: str, id: str, update_mask: str, body: str) -> str:
    """
    Updates a student submission.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :param update_mask: Mask that identifies which fields on the student submission to update.
    :param body: A JSON string representing the updated student submission.
    :return: A JSON string of the updated student submission.
    """
    try:
        service = _get_service(token_data)
        submission = json.loads(body)
        response = service.courses().courseWork().studentSubmissions().patch(
            courseId=course_id,
            courseWorkId=course_work_id,
            id=id,
            updateMask=update_mask,
            body=submission
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def return_student_submission(token_data: str, course_id: str, course_work_id: str, id: str) -> str:
    """
    Returns a student submission.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().studentSubmissions().return_conflict(courseId=course_id, courseWorkId=course_work_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to return student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def reclaim_student_submission(token_data: str, course_id: str, course_work_id: str, id: str) -> str:
    """
    Reclaims a student submission on behalf of the student that owns it.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWork().studentSubmissions().reclaim(courseId=course_id, courseWorkId=course_work_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to reclaim student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course_work_material(token_data: str, course_id: str, body: str) -> str:
    """
    Creates course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the course work material to create.
    :return: A JSON string of the created course work material.
    """
    try:
        service = _get_service(token_data)
        material = json.loads(body)
        response = service.courses().courseWorkMaterials().create(courseId=course_id, body=material).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course work material for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_course_work_materials(token_data: str, course_id: str, material_drive_id: str = None, material_link: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of course work materials that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param material_drive_id: Google Drive item ID.
    :param material_link: URL of the material.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of course work materials.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWorkMaterials().list(
            courseId=course_id,
            materialDriveId=material_drive_id,
            materialLink=material_link,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list course work materials for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_course_work_material(token_data: str, course_id: str, id: str) -> str:
    """
    Returns a course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work material.
    :return: A JSON string of the course work material.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWorkMaterials().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get course work material '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_course_work_material(token_data: str, course_id: str, id: str, update_mask: str, body: str) -> str:
    """
    Updates a course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work material.
    :param update_mask: Mask that identifies which fields on the course work material to update.
    :param body: A JSON string representing the updated course work material.
    :return: A JSON string of the updated course work material.
    """
    try:
        service = _get_service(token_data)
        material = json.loads(body)
        response = service.courses().courseWorkMaterials().patch(courseId=course_id, id=id, updateMask=update_mask, body=material).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch course work material '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course_work_material(token_data: str, course_id: str, id: str) -> str:
    """
    Deletes a course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work material to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().courseWorkMaterials().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course work material '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_student(token_data: str, course_id: str, enrollment_code: str, body: str) -> str:
    """
    Adds a user as a student of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course to create the student in.
    :param enrollment_code: Enrollment code of the course to create the student in.
    :param body: A JSON string representing the student to create.
    :return: A JSON string of the created student.
    """
    try:
        service = _get_service(token_data)
        student = json.loads(body)
        response = service.courses().students().create(courseId=course_id, enrollmentCode=enrollment_code, body=student).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create student for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_students(token_data: str, course_id: str, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of students of this course that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of students.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().students().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list students for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_student(token_data: str, course_id: str, user_id: str) -> str:
    """
    Returns a student of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the student.
    :return: A JSON string of the student.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().students().get(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get student '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_student(token_data: str, course_id: str, user_id: str) -> str:
    """
    Deletes a student of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the student to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().students().delete(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete student '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_teacher(token_data: str, course_id: str, body: str) -> str:
    """
    Creates a teacher in a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the teacher to create.
    :return: A JSON string of the created teacher.
    """
    try:
        service = _get_service(token_data)
        teacher = json.loads(body)
        response = service.courses().teachers().create(courseId=course_id, body=teacher).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create teacher for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_teachers(token_data: str, course_id: str, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of teachers of this course that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of teachers.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().teachers().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list teachers for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_teacher(token_data: str, course_id: str, user_id: str) -> str:
    """
    Returns a teacher of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the teacher.
    :return: A JSON string of the teacher.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().teachers().get(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get teacher '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_teacher(token_data: str, course_id: str, user_id: str) -> str:
    """
    Deletes a teacher of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the teacher to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().teachers().delete(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete teacher '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_topic(token_data: str, course_id: str, body: str) -> str:
    """
    Creates a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the topic to create.
    :return: A JSON string of the created topic.
    """
    try:
        service = _get_service(token_data)
        topic = json.loads(body)
        response = service.courses().topics().create(courseId=course_id, body=topic).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create topic for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_topics(token_data: str, course_id: str, page_size: int = None, page_token: str = None) -> str:
    """
    Returns the list of topics that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of topics.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().topics().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list topics for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_topic(token_data: str, course_id: str, id: str) -> str:
    """
    Returns a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the topic.
    :return: A JSON string of the topic.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().topics().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get topic '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_topic(token_data: str, course_id: str, id: str, update_mask: str, body: str) -> str:
    """
    Updates a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the topic.
    :param update_mask: Mask that identifies which fields on the topic to update.
    :param body: A JSON string representing the updated topic.
    :return: A JSON string of the updated topic.
    """
    try:
        service = _get_service(token_data)
        topic = json.loads(body)
        response = service.courses().topics().patch(courseId=course_id, id=id, updateMask=update_mask, body=topic).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch topic '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_topic(token_data: str, course_id: str, id: str) -> str:
    """
    Deletes a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the topic to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.courses().topics().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete topic '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_invitation(token_data: str, body: str) -> str:
    """
    Creates an invitation. Only course teachers are permitted to create invitations.

    :param token_data: The JSON string of the user's access token.
    :param body: A JSON string representing the invitation to create.
    :return: A JSON string of the created invitation.
    """
    try:
        service = _get_service(token_data)
        invitation = json.loads(body)
        response = service.invitations().create(body=invitation).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create invitation: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_invitations(token_data: str, user_id: str = None, course_id: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of invitations that the requesting user is permitted to view, restricted to those that match the list request.

    :param token_data: The JSON string of the user's access token.
    :param user_id: Restricts returned invitations to those for a specific user.
    :param course_id: Restricts returned invitations to those for a specific course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of invitations.
    """
    try:
        service = _get_service(token_data)
        response = service.invitations().list(
            userId=user_id,
            courseId=course_id,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list invitations: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_invitation(token_data: str, id: str) -> str:
    """
    Returns an invitation.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the invitation to return.
    :return: A JSON string of the invitation.
    """
    try:
        service = _get_service(token_data)
        response = service.invitations().get(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get invitation '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_invitation(token_data: str, id: str) -> str:
    """
    Deletes an invitation.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the invitation to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.invitations().delete(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete invitation '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def accept_invitation(token_data: str, id: str) -> str:
    """
    Accepts an invitation, removing it and adding the invited user to the teachers or students (as appropriate) of the specified course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the invitation to accept.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.invitations().accept(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to accept invitation '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_registration(token_data: str, body: str) -> str:
    """
    Creates a `Registration`.

    :param token_data: The JSON string of the user's access token.
    :param body: A JSON string representing the registration to create.
    :return: A JSON string of the created registration.
    """
    try:
        service = _get_service(token_data)
        registration = json.loads(body)
        response = service.registrations().create(body=registration).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create registration: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_registration(token_data: str, registration_id: str) -> str:
    """
    Deletes a `Registration`.

    :param token_data: The JSON string of the user's access token.
    :param registration_id: The `registration_id` of the `Registration` to be deleted.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.registrations().delete(registrationId=registration_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete registration '{registration_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_user_profile(token_data: str, user_id: str) -> str:
    """
    Returns a user profile.

    :param token_data: The JSON string of the user's access token.
    :param user_id: The identifier of the user.
    :return: A JSON string of the user profile.
    """
    try:
        service = _get_service(token_data)
        response = service.userProfiles().get(userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get user profile '{user_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_guardian_invitation(token_data: str, student_id: str, body: str) -> str:
    """
    Creates a guardian invitation, and sends an email to the guardian asking them to confirm that they are the student's guardian.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The ID of the student (the user) for whom to create a guardian invitation.
    :param body: A JSON string representing the guardian invitation to create.
    :return: A JSON string of the created guardian invitation.
    """
    try:
        service = _get_service(token_data)
        invitation = json.loads(body)
        response = service.userProfiles().guardianInvitations().create(studentId=student_id, body=invitation).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create guardian invitation for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_guardian_invitation(token_data: str, student_id: str, invitation_id: str) -> str:
    """
    Returns a specific guardian invitation.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The ID of the student whose guardian invitation is being requested.
    :param invitation_id: The `id` field of the `GuardianInvitation` being requested.
    :return: A JSON string of the guardian invitation.
    """
    try:
        service = _get_service(token_data)
        response = service.userProfiles().guardianInvitations().get(studentId=student_id, invitationId=invitation_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get guardian invitation '{invitation_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_guardian_invitation(token_data: str, student_id: str, invitation_id: str, update_mask: str, body: str) -> str:
    """
    Modifies a guardian invitation.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The ID of the student whose guardian invitation is to be modified.
    :param invitation_id: The `id` field of the `GuardianInvitation` to be modified.
    :param update_mask: Mask that identifies which fields on the guardian invitation to update.
    :param body: A JSON string representing the updated guardian invitation.
    :return: A JSON string of the updated guardian invitation.
    """
    try:
        service = _get_service(token_data)
        invitation = json.loads(body)
        response = service.userProfiles().guardianInvitations().patch(
            studentId=student_id,
            invitationId=invitation_id,
            updateMask=update_mask,
            body=invitation
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch guardian invitation '{invitation_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_guardian(token_data: str, student_id: str, guardian_id: str) -> str:
    """
    Returns a specific guardian.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The student whose guardian is being requested.
    :param guardian_id: The `id` field of the `Guardian` being requested.
    :return: A JSON string of the guardian.
    """
    try:
        service = _get_service(token_data)
        response = service.userProfiles().guardians().get(studentId=student_id, guardianId=guardian_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get guardian '{guardian_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_guardians(token_data: str, student_id: str, invited_email_address: str = None, page_size: int = None, page_token: str = None) -> str:
    """
    Returns a list of guardians that the requesting user is permitted to view, restricted to those that match the request.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The student whose guardians are to be returned.
    :param invited_email_address: If specified, only results with the specified `invited_email_address` are returned.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of guardians.
    """
    try:
        service = _get_service(token_data)
        response = service.userProfiles().guardians().list(
            studentId=student_id,
            invitedEmailAddress=invited_email_address,
            pageSize=page_size,
            pageToken=page_token
        ).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list guardians for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_guardian(token_data: str, student_id: str, guardian_id: str) -> str:
    """
    Deletes a guardian.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The student whose guardian is to be deleted.
    :param guardian_id: The `id` of the guardian to be deleted.
    :return: An empty JSON string if successful.
    """
    try:
        service = _get_service(token_data)
        response = service.userProfiles().guardians().delete(studentId=student_id, guardianId=guardian_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete guardian '{guardian_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})


# =======================================================================================
#                       MCP TOOLS END
# =======================================================================================


# Function for parsing the cmd-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Google Classroom MCP Server")
    parser.add_argument(
        "-t",
        "--transport",
        help="Transport method for MCP (Allowed Values: 'stdio', 'sse', or 'streamable-http')",
        default=None,
    )
    parser.add_argument("--host", help="Host to bind the server to", default=None)
    parser.add_argument(
        "--port", type=int, help="Port to bind the server to", default=None
    )
    return parser.parse_args()


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("Google Classroom MCP Server Starting")
    logger.info("=" * 60)

    args = parse_args()

    # Build kwargs for mcp.run() only with provided values
    run_kwargs = {}
    if args.transport:
        run_kwargs["transport"] = args.transport
        logger.info(f"Transport: {args.transport}")
    if args.host:
        run_kwargs["host"] = args.host
        logger.info(f"Host: {args.host}")
    if args.port:
        run_kwargs["port"] = args.port
        logger.info(f"Port: {args.port}")

    try:
        # Start the MCP server with optional transport/host/port
        mcp.run(**run_kwargs)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server crashed: {e}", exc_info=True)
        raise
