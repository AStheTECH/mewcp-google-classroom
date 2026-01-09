# Google Classroom MCP Server

This server provides a set of tools to interact with the Google Classroom API, allowing you to manage courses, announcements, coursework, and more.

## Authentication

All tools require a `token_data` parameter. This is a JSON string containing your OAuth 2.0 credentials. The structure of the JSON should be as follows:

```json
{
  "token": "YOUR_ACCESS_TOKEN",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "token_uri": "https://oauth2.googleapis.com/token",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "scopes": ["https://www.googleapis.com/auth/classroom..."]
}
```

---

## Available Tools

### Courses

#### `list_courses`
Returns a list of courses that the requesting user is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, optional): Restricts returned courses to those having a student with the specified identifier.
*   `teacher_id` (string, optional): Restricts returned courses to those having a teacher with the specified identifier.
*   `course_states` (string, optional): Restricts returned courses to those in one of the specified states.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_course`
Returns a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the course to return.

#### `create_course`
Creates a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `body` (string, required): A JSON string representing the course to create.

#### `update_course`
Updates a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the course to update.
*   `body` (string, required): A JSON string representing the updated course.

#### `patch_course`
Updates a course. This method is an alias for update(), but only fields specified in updateMask are updated.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the course to update.
*   `update_mask` (string, required): Mask that identifies which fields on the course to update.
*   `body` (string, required): A JSON string representing the updated course.

#### `delete_course`
Deletes a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the course to delete.

### Course Aliases

#### `create_course_alias`
Creates an alias for a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): The identifier of the course.
*   `body` (string, required): A JSON string representing the alias to create.

#### `list_course_aliases`
Returns a list of aliases for a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): The identifier of the course.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `delete_course_alias`
Deletes an alias of a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): The identifier of the course.
*   `alias` (string, required): The alias to delete.

### Announcements

#### `create_announcement`
Creates an announcement.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `body` (string, required): A JSON string representing the announcement to create.

#### `list_announcements`
Returns a list of announcements that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `announcement_states` (string, optional): Restriction on the work status to return.
*   `order_by` (string, optional): Sort order for results.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_announcement`
Returns an announcement.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the announcement to return.

#### `patch_announcement`
Updates an announcement.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the announcement to update.
*   `update_mask` (string, required): Mask that identifies which fields on the announcement to update.
*   `body` (string, required): A JSON string representing the updated announcement.

#### `delete_announcement`
Deletes an announcement.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the announcement to delete.

#### `modify_announcement_assignees`
Modifies assignee mode and options of an announcement.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the announcement.
*   `body` (string, required): A JSON string with the modifications.

### Course Work

#### `create_course_work`
Creates course work.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `body` (string, required): A JSON string representing the course work to create.

#### `list_course_work`
Returns a list of course work that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `course_work_states` (string, optional): Restriction on the work status to return.
*   `order_by` (string, optional): Sort order for results.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_course_work`
Returns course work.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work to return.

#### `patch_course_work`
Updates course work.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work to update.
*   `update_mask` (string, required): Mask that identifies which fields on the course work to update.
*   `body` (string, required): A JSON string representing the updated course work.

#### `delete_course_work`
Deletes course work.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work to delete.

#### `modify_course_work_assignees`
Modifies assignee mode and options of a course work.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work.
*   `body` (string, required): A JSON string with the modifications.

### Student Submissions

#### `get_student_submission`
Returns a student submission.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `course_work_id` (string, required): Identifier of the course work.
*   `id` (string, required): Identifier of the student submission.

#### `list_student_submissions`
Returns a list of student submissions that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `course_work_id` (string, required): Identifier of the course work.
*   `user_id` (string, optional): Restrict returned student submissions to those owned by the student with the specified user ID.
*   `states` (string, optional): Requested submission states.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `patch_student_submission`
Updates a student submission.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `course_work_id` (string, required): Identifier of the course work.
*   `id` (string, required): Identifier of the student submission.
*   `update_mask` (string, required): Mask that identifies which fields on the student submission to update.
*   `body` (string, required): A JSON string representing the updated student submission.

#### `return_student_submission`
Returns a student submission.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `course_work_id` (string, required): Identifier of the course work.
*   `id` (string, required): Identifier of the student submission.

#### `reclaim_student_submission`
Reclaims a student submission on behalf of the student that owns it.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `course_work_id` (string, required): Identifier of the course work.
*   `id` (string, required): Identifier of the student submission.

### Course Work Materials

#### `create_course_work_material`
Creates course work material.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `body` (string, required): A JSON string representing the course work material to create.

#### `list_course_work_materials`
Returns a list of course work materials that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `material_drive_id` (string, optional): Google Drive item ID.
*   `material_link` (string, optional): URL of the material.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_course_work_material`
Returns a course work material.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work material.

#### `patch_course_work_material`
Updates a course work material.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work material.
*   `update_mask` (string, required): Mask that identifies which fields on the course work material to update.
*   `body` (string, required): A JSON string representing the updated course work material.

#### `delete_course_work_material`
Deletes a course work material.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the course work material to delete.

### Students

#### `create_student`
Adds a user as a student of a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course to create the student in.
*   `enrollment_code` (string, required): Enrollment code of the course to create the student in.
*   `body` (string, required): A JSON string representing the student to create.

#### `list_students`
Returns a list of students of this course that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_student`
Returns a student of a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `user_id` (string, required): Identifier of the student.

#### `delete_student`
Deletes a student of a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `user_id` (string, required): Identifier of the student to delete.

### Teachers

#### `create_teacher`
Creates a teacher in a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `body` (string, required): A JSON string representing the teacher to create.

#### `list_teachers`
Returns a list of teachers of this course that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_teacher`
Returns a teacher of a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `user_id` (string, required): Identifier of the teacher.

#### `delete_teacher`
Deletes a teacher of a course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `user_id` (string, required): Identifier of the teacher to delete.

### Topics

#### `create_topic`
Creates a topic.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `body` (string, required): A JSON string representing the topic to create.

#### `list_topics`
Returns the list of topics that the requester is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_topic`
Returns a topic.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the topic.

#### `patch_topic`
Updates a topic.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the topic.
*   `update_mask` (string, required): Mask that identifies which fields on the topic to update.
*   `body` (string, required): A JSON string representing the updated topic.

#### `delete_topic`
Deletes a topic.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `course_id` (string, required): Identifier of the course.
*   `id` (string, required): Identifier of the topic to delete.

### Invitations

#### `create_invitation`
Creates an invitation. Only course teachers are permitted to create invitations.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `body` (string, required): A JSON string representing the invitation to create.

#### `list_invitations`
Returns a list of invitations that the requesting user is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `user_id` (string, optional): Restricts returned invitations to those for a specific user.
*   `course_id` (string, optional): Restricts returned invitations to those for a specific course.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `get_invitation`
Returns an invitation.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the invitation to return.

#### `delete_invitation`
Deletes an invitation.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the invitation to delete.

#### `accept_invitation`
Accepts an invitation, removing it and adding the invited user to the teachers or students (as appropriate) of the specified course.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `id` (string, required): Identifier of the invitation to accept.

### Registrations

#### `create_registration`
Creates a `Registration`.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `body` (string, required): A JSON string representing the registration to create.

#### `delete_registration`
Deletes a `Registration`.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `registration_id` (string, required): The `registration_id` of the `Registration` to be deleted.

### User Profiles

#### `get_user_profile`
Returns a user profile.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `user_id` (string, required): The identifier of the user.

### Guardian Invitations

#### `create_guardian_invitation`
Creates a guardian invitation, and sends an email to the guardian asking them to confirm that they are the student's guardian.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, required): The ID of the student (the user) for whom to create a guardian invitation.
*   `body` (string, required): A JSON string representing the guardian invitation to create.

#### `get_guardian_invitation`
Returns a specific guardian invitation.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, required): The ID of the student whose guardian invitation is being requested.
*   `invitation_id` (string, required): The `id` field of the `GuardianInvitation` being requested.

#### `patch_guardian_invitation`
Modifies a guardian invitation.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, required): The ID of the student whose guardian invitation is to be modified.
*   `invitation_id` (string, required): The `id` field of the `GuardianInvitation` to be modified.
*   `update_mask` (string, required): Mask that identifies which fields on the guardian invitation to update.
*   `body` (string, required): A JSON string representing the updated guardian invitation.

### Guardians

#### `get_guardian`
Returns a specific guardian.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, required): The student whose guardian is being requested.
*   `guardian_id` (string, required): The `id` field of the `Guardian` being requested.

#### `list_guardians`
Returns a list of guardians that the requesting user is permitted to view.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, required): The student whose guardians are to be returned.
*   `invited_email_address` (string, optional): If specified, only results with the specified `invited_email_address` are returned.
*   `page_size` (integer, optional): Maximum number of items to return.
*   `page_token` (string, optional): `nextPageToken` value from a previous list call.

#### `delete_guardian`
Deletes a guardian.

*   `token_data` (string, required): The JSON string of the user's access token.
*   `student_id` (string, required): The student whose guardian is to be deleted.
*   `guardian_id` (string, required): The `id` of the guardian to be deleted.
