import json
import logging

from fastmcp import FastMCP

from .schemas import JsonStringToolResponse
from .service import get_service

logger = logging.getLogger("google-classroom-mcp-server")

class _ToolCollector:
    def __init__(self):
        self.items = []

    def tool(self, *args, **kwargs):
        def decorator(func):
            self.items.append((args, kwargs, func))
            return func

        return decorator


mcp = _ToolCollector()


def register_tools(real_mcp: FastMCP) -> None:
    for args, kwargs, func in mcp.items:
        real_mcp.tool(*args, **kwargs)(func)


#                       MCP TOOLS START


@mcp.tool()
def list_courses(student_id: str = None, teacher_id: str = None, course_states: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def get_course(id: str) -> JsonStringToolResponse:
    """
    Returns a course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to return.
    :return: A JSON string of the course.
    """
    try:
        service = get_service()
        response = service.courses().get(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course(body: str) -> JsonStringToolResponse:
    """
    Creates a course.

    :param token_data: The JSON string of the user's access token.
    :param body: A JSON string representing the course to create.
    :return: A JSON string of the created course.
    """
    try:
        service = get_service()
        course = json.loads(body)
        response = service.courses().create(body=course).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def update_course(id: str, body: str) -> JsonStringToolResponse:
    """
    Updates a course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to update.
    :param body: A JSON string representing the updated course.
    :return: A JSON string of the updated course.
    """
    try:
        service = get_service()
        course = json.loads(body)
        response = service.courses().update(id=id, body=course).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to update course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_course(id: str, update_mask: str, body: str) -> JsonStringToolResponse:
    """
    Updates a course. This method is an alias for update(), but only fields specified in updateMask are updated.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to update.
    :param update_mask: Mask that identifies which fields on the course to update.
    :param body: A JSON string representing the updated course.
    :return: A JSON string of the updated course.
    """
    try:
        service = get_service()
        course = json.loads(body)
        response = service.courses().patch(id=id, updateMask=update_mask, body=course).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course(id: str) -> JsonStringToolResponse:
    """
    Deletes a course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the course to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().delete(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course_alias(course_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates an alias for a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: The identifier of the course.
    :param body: A JSON string representing the alias to create.
    :return: A JSON string of the created alias.
    """
    try:
        service = get_service()
        alias = json.loads(body)
        response = service.courses().aliases().create(courseId=course_id, body=alias).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course alias for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_course_aliases(course_id: str, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
    """
    Returns a list of aliases for a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: The identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call, indicating that the subsequent page of results should be returned.
    :return: A JSON string of the list of aliases.
    """
    try:
        service = get_service()
        response = service.courses().aliases().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list course aliases for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course_alias(course_id: str, alias: str) -> JsonStringToolResponse:
    """
    Deletes an alias of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: The identifier of the course.
    :param alias: The alias to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().aliases().delete(courseId=course_id, alias=alias).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course alias '{alias}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_announcement(course_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the announcement to create.
    :return: A JSON string of the created announcement.
    """
    try:
        service = get_service()
        announcement = json.loads(body)
        response = service.courses().announcements().create(courseId=course_id, body=announcement).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create announcement for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_announcements(course_id: str, announcement_states: str = None, order_by: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def get_announcement(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Returns an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement to return.
    :return: A JSON string of the announcement.
    """
    try:
        service = get_service()
        response = service.courses().announcements().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_announcement(course_id: str, id: str, update_mask: str, body: str) -> JsonStringToolResponse:
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
        service = get_service()
        announcement = json.loads(body)
        response = service.courses().announcements().patch(courseId=course_id, id=id, updateMask=update_mask, body=announcement).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_announcement(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Deletes an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().announcements().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def modify_announcement_assignees(course_id: str, id: str, body: str) -> JsonStringToolResponse:
    """
    Modifies assignee mode and options of an announcement.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the announcement.
    :param body: A JSON string with the modifications.
    :return: A JSON string of the modified announcement.
    """
    try:
        service = get_service()
        modifications = json.loads(body)
        response = service.courses().announcements().modifyAssignees(courseId=course_id, id=id, body=modifications).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to modify assignees for announcement '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course_work(course_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the course work to create.
    :return: A JSON string of the created course work.
    """
    try:
        service = get_service()
        course_work = json.loads(body)
        response = service.courses().courseWork().create(courseId=course_id, body=course_work).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course work for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_course_work(course_id: str, course_work_states: str = None, order_by: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def get_course_work(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Returns course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work to return.
    :return: A JSON string of the course work.
    """
    try:
        service = get_service()
        response = service.courses().courseWork().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_course_work(course_id: str, id: str, update_mask: str, body: str) -> JsonStringToolResponse:
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
        service = get_service()
        course_work = json.loads(body)
        response = service.courses().courseWork().patch(courseId=course_id, id=id, updateMask=update_mask, body=course_work).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course_work(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Deletes course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().courseWork().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def modify_course_work_assignees(course_id: str, id: str, body: str) -> JsonStringToolResponse:
    """
    Modifies assignee mode and options of a course work.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work.
    :param body: A JSON string with the modifications.
    :return: A JSON string of the modified course work.
    """
    try:
        service = get_service()
        modifications = json.loads(body)
        response = service.courses().courseWork().modifyAssignees(courseId=course_id, id=id, body=modifications).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to modify assignees for course work '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_student_submission(course_id: str, course_work_id: str, id: str) -> JsonStringToolResponse:
    """
    Returns a student submission.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :return: A JSON string of the student submission.
    """
    try:
        service = get_service()
        response = service.courses().courseWork().studentSubmissions().get(courseId=course_id, courseWorkId=course_work_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_student_submissions(course_id: str, course_work_id: str, user_id: str = None, states: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def patch_student_submission(course_id: str, course_work_id: str, id: str, update_mask: str, body: str) -> JsonStringToolResponse:
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
        service = get_service()
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
def return_student_submission(course_id: str, course_work_id: str, id: str) -> JsonStringToolResponse:
    """
    Returns a student submission.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().courseWork().studentSubmissions().return_conflict(courseId=course_id, courseWorkId=course_work_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to return student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def reclaim_student_submission(course_id: str, course_work_id: str, id: str) -> JsonStringToolResponse:
    """
    Reclaims a student submission on behalf of the student that owns it.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param course_work_id: Identifier of the course work.
    :param id: Identifier of the student submission.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().courseWork().studentSubmissions().reclaim(courseId=course_id, courseWorkId=course_work_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to reclaim student submission '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_course_work_material(course_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the course work material to create.
    :return: A JSON string of the created course work material.
    """
    try:
        service = get_service()
        material = json.loads(body)
        response = service.courses().courseWorkMaterials().create(courseId=course_id, body=material).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create course work material for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_course_work_materials(course_id: str, material_drive_id: str = None, material_link: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def get_course_work_material(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Returns a course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work material.
    :return: A JSON string of the course work material.
    """
    try:
        service = get_service()
        response = service.courses().courseWorkMaterials().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get course work material '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_course_work_material(course_id: str, id: str, update_mask: str, body: str) -> JsonStringToolResponse:
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
        service = get_service()
        material = json.loads(body)
        response = service.courses().courseWorkMaterials().patch(courseId=course_id, id=id, updateMask=update_mask, body=material).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch course work material '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_course_work_material(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Deletes a course work material.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the course work material to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().courseWorkMaterials().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete course work material '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_student(course_id: str, enrollment_code: str, body: str) -> JsonStringToolResponse:
    """
    Adds a user as a student of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course to create the student in.
    :param enrollment_code: Enrollment code of the course to create the student in.
    :param body: A JSON string representing the student to create.
    :return: A JSON string of the created student.
    """
    try:
        service = get_service()
        student = json.loads(body)
        response = service.courses().students().create(courseId=course_id, enrollmentCode=enrollment_code, body=student).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create student for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_students(course_id: str, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
    """
    Returns a list of students of this course that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of students.
    """
    try:
        service = get_service()
        response = service.courses().students().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list students for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_student(course_id: str, user_id: str) -> JsonStringToolResponse:
    """
    Returns a student of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the student.
    :return: A JSON string of the student.
    """
    try:
        service = get_service()
        response = service.courses().students().get(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get student '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_student(course_id: str, user_id: str) -> JsonStringToolResponse:
    """
    Deletes a student of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the student to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().students().delete(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete student '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_teacher(course_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates a teacher in a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the teacher to create.
    :return: A JSON string of the created teacher.
    """
    try:
        service = get_service()
        teacher = json.loads(body)
        response = service.courses().teachers().create(courseId=course_id, body=teacher).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create teacher for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_teachers(course_id: str, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
    """
    Returns a list of teachers of this course that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of teachers.
    """
    try:
        service = get_service()
        response = service.courses().teachers().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list teachers for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_teacher(course_id: str, user_id: str) -> JsonStringToolResponse:
    """
    Returns a teacher of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the teacher.
    :return: A JSON string of the teacher.
    """
    try:
        service = get_service()
        response = service.courses().teachers().get(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get teacher '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_teacher(course_id: str, user_id: str) -> JsonStringToolResponse:
    """
    Deletes a teacher of a course.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param user_id: Identifier of the teacher to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().teachers().delete(courseId=course_id, userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete teacher '{user_id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_topic(course_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param body: A JSON string representing the topic to create.
    :return: A JSON string of the created topic.
    """
    try:
        service = get_service()
        topic = json.loads(body)
        response = service.courses().topics().create(courseId=course_id, body=topic).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create topic for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_topics(course_id: str, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
    """
    Returns the list of topics that the requester is permitted to view.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param page_size: Maximum number of items to return.
    :param page_token: nextPageToken value returned from a previous list call.
    :return: A JSON string of the list of topics.
    """
    try:
        service = get_service()
        response = service.courses().topics().list(courseId=course_id, pageSize=page_size, pageToken=page_token).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to list topics for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_topic(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Returns a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the topic.
    :return: A JSON string of the topic.
    """
    try:
        service = get_service()
        response = service.courses().topics().get(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get topic '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_topic(course_id: str, id: str, update_mask: str, body: str) -> JsonStringToolResponse:
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
        service = get_service()
        topic = json.loads(body)
        response = service.courses().topics().patch(courseId=course_id, id=id, updateMask=update_mask, body=topic).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to patch topic '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_topic(course_id: str, id: str) -> JsonStringToolResponse:
    """
    Deletes a topic.

    :param token_data: The JSON string of the user's access token.
    :param course_id: Identifier of the course.
    :param id: Identifier of the topic to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.courses().topics().delete(courseId=course_id, id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete topic '{id}' for course '{course_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_invitation(body: str) -> JsonStringToolResponse:
    """
    Creates an invitation. Only course teachers are permitted to create invitations.

    :param token_data: The JSON string of the user's access token.
    :param body: A JSON string representing the invitation to create.
    :return: A JSON string of the created invitation.
    """
    try:
        service = get_service()
        invitation = json.loads(body)
        response = service.invitations().create(body=invitation).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create invitation: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_invitations(user_id: str = None, course_id: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def get_invitation(id: str) -> JsonStringToolResponse:
    """
    Returns an invitation.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the invitation to return.
    :return: A JSON string of the invitation.
    """
    try:
        service = get_service()
        response = service.invitations().get(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get invitation '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_invitation(id: str) -> JsonStringToolResponse:
    """
    Deletes an invitation.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the invitation to delete.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.invitations().delete(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete invitation '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def accept_invitation(id: str) -> JsonStringToolResponse:
    """
    Accepts an invitation, removing it and adding the invited user to the teachers or students (as appropriate) of the specified course.

    :param token_data: The JSON string of the user's access token.
    :param id: Identifier of the invitation to accept.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.invitations().accept(id=id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to accept invitation '{id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_registration(body: str) -> JsonStringToolResponse:
    """
    Creates a `Registration`.

    :param token_data: The JSON string of the user's access token.
    :param body: A JSON string representing the registration to create.
    :return: A JSON string of the created registration.
    """
    try:
        service = get_service()
        registration = json.loads(body)
        response = service.registrations().create(body=registration).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create registration: {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def delete_registration(registration_id: str) -> JsonStringToolResponse:
    """
    Deletes a `Registration`.

    :param token_data: The JSON string of the user's access token.
    :param registration_id: The `registration_id` of the `Registration` to be deleted.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.registrations().delete(registrationId=registration_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete registration '{registration_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_user_profile(user_id: str) -> JsonStringToolResponse:
    """
    Returns a user profile.

    :param token_data: The JSON string of the user's access token.
    :param user_id: The identifier of the user.
    :return: A JSON string of the user profile.
    """
    try:
        service = get_service()
        response = service.userProfiles().get(userId=user_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get user profile '{user_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def create_guardian_invitation(student_id: str, body: str) -> JsonStringToolResponse:
    """
    Creates a guardian invitation, and sends an email to the guardian asking them to confirm that they are the student's guardian.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The ID of the student (the user) for whom to create a guardian invitation.
    :param body: A JSON string representing the guardian invitation to create.
    :return: A JSON string of the created guardian invitation.
    """
    try:
        service = get_service()
        invitation = json.loads(body)
        response = service.userProfiles().guardianInvitations().create(studentId=student_id, body=invitation).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to create guardian invitation for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def get_guardian_invitation(student_id: str, invitation_id: str) -> JsonStringToolResponse:
    """
    Returns a specific guardian invitation.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The ID of the student whose guardian invitation is being requested.
    :param invitation_id: The `id` field of the `GuardianInvitation` being requested.
    :return: A JSON string of the guardian invitation.
    """
    try:
        service = get_service()
        response = service.userProfiles().guardianInvitations().get(studentId=student_id, invitationId=invitation_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get guardian invitation '{invitation_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def patch_guardian_invitation(student_id: str, invitation_id: str, update_mask: str, body: str) -> JsonStringToolResponse:
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
        service = get_service()
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
def get_guardian(student_id: str, guardian_id: str) -> JsonStringToolResponse:
    """
    Returns a specific guardian.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The student whose guardian is being requested.
    :param guardian_id: The `id` field of the `Guardian` being requested.
    :return: A JSON string of the guardian.
    """
    try:
        service = get_service()
        response = service.userProfiles().guardians().get(studentId=student_id, guardianId=guardian_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to get guardian '{guardian_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})

@mcp.tool()
def list_guardians(student_id: str, invited_email_address: str = None, page_size: int = None, page_token: str = None) -> JsonStringToolResponse:
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
        service = get_service()
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
def delete_guardian(student_id: str, guardian_id: str) -> JsonStringToolResponse:
    """
    Deletes a guardian.

    :param token_data: The JSON string of the user's access token.
    :param student_id: The student whose guardian is to be deleted.
    :param guardian_id: The `id` of the guardian to be deleted.
    :return: An empty JSON string if successful.
    """
    try:
        service = get_service()
        response = service.userProfiles().guardians().delete(studentId=student_id, guardianId=guardian_id).execute()
        return json.dumps(response)
    except Exception as e:
        logger.error(f"Failed to delete guardian '{guardian_id}' for student '{student_id}': {e}")
        return json.dumps({"error": str(e)})
