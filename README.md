**Manage Google Classroom courses, assignments, and students with Agents.**

A Model Context Protocol (MCP) server that exposes Google Classroom's API for managing courses, coursework, announcements, rosters, submissions, and guardians.


## Overview

The Google Classroom MCP Server provides full lifecycle management of your Google Classroom environment:

- Create and manage courses, topics, announcements, and coursework
- Manage student and teacher rosters, invitations, and guardian links
- Read and grade student submissions

Perfect for:

- Educators automating course setup and content distribution
- Administrators managing rosters and guardian communications at scale
- Developers building learning management integrations on top of Google Classroom


## Tools

### Courses

<details>
<summary><code>list_courses</code> — List courses the user can view</summary>

Returns a list of courses the requesting user is permitted to view, optionally filtered by student, teacher, or course state.

**Inputs:**
```
- `student_id`     (string, optional)  — Restrict to courses with this student
- `teacher_id`     (string, optional)  — Restrict to courses with this teacher
- `course_states`  (string, optional)  — Restrict to courses in these states (e.g. ACTIVE, ARCHIVED)
- `page_size`      (integer, optional) — Maximum number of courses to return
- `page_token`     (string, optional)  — Token for the next page of results
```

**Output:**

```json
{
  "courses": [
    {
      "id": "123456789",
      "name": "Introduction to Python",
      "section": "Period 1",
      "ownerId": "987654321",
      "courseState": "ACTIVE",
      "enrollmentCode": "abc123",
      "updateTime": "2025-01-15T10:00:00.000Z"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_course</code> — Get a single course</summary>

Returns a course by its identifier.

**Inputs:**
```
- `id` (string, required) — Identifier of the course
```

**Output:**

```json
{
  "id": "123456789",
  "name": "Introduction to Python",
  "section": "Period 1",
  "ownerId": "987654321",
  "courseState": "ACTIVE",
  "enrollmentCode": "abc123",
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>create_course</code> — Create a course</summary>

Creates a new course. The requesting user becomes the owner.

**Inputs:**
```
- `body` (string, required) — JSON string representing the Course object to create
```

**Output:**

```json
{
  "id": "123456789",
  "name": "Introduction to Python",
  "section": "Period 1",
  "ownerId": "987654321",
  "courseState": "PROVISIONED",
  "enrollmentCode": "abc123",
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>update_course</code> — Replace a course</summary>

Replaces all fields of a course with the provided values.

**Inputs:**
```
- `id`   (string, required) — Identifier of the course to update
- `body` (string, required) — JSON string representing the updated Course object
```

**Output:**

```json
{
  "id": "123456789",
  "name": "Advanced Python",
  "section": "Period 2",
  "ownerId": "987654321",
  "courseState": "ACTIVE",
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_course</code> — Partially update a course</summary>

Updates only the fields specified in `update_mask`.

**Inputs:**
```
- `id`           (string, required) — Identifier of the course to patch
- `update_mask`  (string, required) — Comma-separated list of fields to update (e.g. name,section)
- `body`         (string, required) — JSON string with the fields to update
```

**Output:**

```json
{
  "id": "123456789",
  "name": "Advanced Python",
  "section": "Period 1",
  "ownerId": "987654321",
  "courseState": "ACTIVE",
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>delete_course</code> — Delete a course</summary>

Permanently deletes a course. Only course owners may delete a course.

**Inputs:**
```
- `id` (string, required) — Identifier of the course to delete
```

**Output:**

```json
{}
```

</details>


### Course Aliases

<details>
<summary><code>create_course_alias</code> — Create a course alias</summary>

Creates an alias for a course so it can be referenced by an alternative identifier.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `body`      (string, required) — JSON string representing the CourseAlias object
```

**Output:**

```json
{
  "alias": "d:intro-python-2025"
}
```

</details>

<details>
<summary><code>list_course_aliases</code> — List course aliases</summary>

Returns all aliases for a course.

**Inputs:**
```
- `course_id`   (string, required)  — Identifier of the course
- `page_size`   (integer, optional) — Maximum number of aliases to return
- `page_token`  (string, optional)  — Token for the next page of results
```

**Output:**

```json
{
  "aliases": [
    { "alias": "d:intro-python-2025" },
    { "alias": "d:py101" }
  ]
}
```

</details>

<details>
<summary><code>delete_course_alias</code> — Delete a course alias</summary>

Removes an alias from a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `alias`     (string, required) — The alias to delete
```

**Output:**

```json
{}
```

</details>


### Announcements

<details>
<summary><code>create_announcement</code> — Create an announcement</summary>

Posts a new announcement to a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `body`      (string, required) — JSON string representing the Announcement object
```

**Output:**

```json
{
  "id": "111222333",
  "courseId": "123456789",
  "text": "Welcome to the course! Please review the syllabus.",
  "state": "PUBLISHED",
  "updateTime": "2025-01-15T10:00:00.000Z",
  "creationTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>list_announcements</code> — List announcements</summary>

Returns announcements in a course, optionally filtered by state.

**Inputs:**
```
- `course_id`            (string, required)  — Identifier of the course
- `announcement_states`  (string, optional)  — Filter by state (PUBLISHED, DRAFT, DELETED)
- `order_by`             (string, optional)  — Sort order (e.g. updateTime desc)
- `page_size`            (integer, optional) — Maximum number of results
- `page_token`           (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "announcements": [
    {
      "id": "111222333",
      "courseId": "123456789",
      "text": "Welcome to the course!",
      "state": "PUBLISHED",
      "updateTime": "2025-01-15T10:00:00.000Z"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_announcement</code> — Get an announcement</summary>

Returns a single announcement.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the announcement
```

**Output:**

```json
{
  "id": "111222333",
  "courseId": "123456789",
  "text": "Welcome to the course! Please review the syllabus.",
  "state": "PUBLISHED",
  "updateTime": "2025-01-15T10:00:00.000Z",
  "creationTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_announcement</code> — Update an announcement</summary>

Updates only the fields specified in `update_mask`.

**Inputs:**
```
- `course_id`    (string, required) — Identifier of the course
- `id`           (string, required) — Identifier of the announcement
- `update_mask`  (string, required) — Fields to update (e.g. text,state)
- `body`         (string, required) — JSON string with updated fields
```

**Output:**

```json
{
  "id": "111222333",
  "courseId": "123456789",
  "text": "Updated announcement text.",
  "state": "PUBLISHED",
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>delete_announcement</code> — Delete an announcement</summary>

Deletes an announcement. Only draft announcements may be deleted; published announcements must be archived first.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the announcement
```

**Output:**

```json
{}
```

</details>

<details>
<summary><code>modify_announcement_assignees</code> — Modify announcement assignees</summary>

Changes which students an announcement is assigned to.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the announcement
- `body`      (string, required) — JSON string with assignee mode and student IDs
```

**Output:**

```json
{
  "id": "111222333",
  "courseId": "123456789",
  "text": "Welcome to the course!",
  "state": "PUBLISHED",
  "assigneeMode": "INDIVIDUAL_STUDENTS",
  "individualStudentsOptions": {
    "studentIds": ["555111", "555222"]
  },
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>


### Course Work

<details>
<summary><code>create_course_work</code> — Create a coursework item</summary>

Creates an assignment, short-answer question, or multiple-choice question in a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `body`      (string, required) — JSON string representing the CourseWork object
```

**Output:**

```json
{
  "id": "222333444",
  "courseId": "123456789",
  "title": "Assignment 1: Hello World",
  "description": "Write your first Python program.",
  "workType": "ASSIGNMENT",
  "state": "PUBLISHED",
  "maxPoints": 100,
  "dueDate": { "year": 2025, "month": 2, "day": 1 },
  "dueTime": { "hours": 23, "minutes": 59 },
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>list_course_work</code> — List coursework</summary>

Returns coursework items in a course, optionally filtered by state.

**Inputs:**
```
- `course_id`           (string, required)  — Identifier of the course
- `course_work_states`  (string, optional)  — Filter by state (PUBLISHED, DRAFT, DELETED)
- `order_by`            (string, optional)  — Sort order (e.g. updateTime desc)
- `page_size`           (integer, optional) — Maximum number of results
- `page_token`          (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "courseWork": [
    {
      "id": "222333444",
      "courseId": "123456789",
      "title": "Assignment 1: Hello World",
      "workType": "ASSIGNMENT",
      "state": "PUBLISHED",
      "maxPoints": 100,
      "updateTime": "2025-01-15T10:00:00.000Z"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_course_work</code> — Get a coursework item</summary>

Returns a single coursework item.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the coursework item
```

**Output:**

```json
{
  "id": "222333444",
  "courseId": "123456789",
  "title": "Assignment 1: Hello World",
  "workType": "ASSIGNMENT",
  "state": "PUBLISHED",
  "maxPoints": 100,
  "dueDate": { "year": 2025, "month": 2, "day": 1 },
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_course_work</code> — Update a coursework item</summary>

Updates only the fields specified in `update_mask`.

**Inputs:**
```
- `course_id`    (string, required) — Identifier of the course
- `id`           (string, required) — Identifier of the coursework item
- `update_mask`  (string, required) — Fields to update (e.g. title,maxPoints)
- `body`         (string, required) — JSON string with updated fields
```

**Output:**

```json
{
  "id": "222333444",
  "courseId": "123456789",
  "title": "Assignment 1: Hello World (Updated)",
  "workType": "ASSIGNMENT",
  "state": "PUBLISHED",
  "maxPoints": 50,
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>delete_course_work</code> — Delete a coursework item</summary>

Deletes a coursework item.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the coursework item
```

**Output:**

```json
{}
```

</details>

<details>
<summary><code>modify_course_work_assignees</code> — Modify coursework assignees</summary>

Changes which students a coursework item is assigned to.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the coursework item
- `body`      (string, required) — JSON string with assignee mode and student IDs
```

**Output:**

```json
{
  "id": "222333444",
  "courseId": "123456789",
  "title": "Assignment 1: Hello World",
  "workType": "ASSIGNMENT",
  "assigneeMode": "INDIVIDUAL_STUDENTS",
  "individualStudentsOptions": {
    "studentIds": ["555111", "555222"]
  },
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>


### Student Submissions

<details>
<summary><code>list_student_submissions</code> — List student submissions</summary>

Returns submissions for a coursework item, optionally filtered by user or state.

**Inputs:**
```
- `course_id`       (string, required)  — Identifier of the course
- `course_work_id`  (string, required)  — Identifier of the coursework item (use `-` for all)
- `user_id`         (string, optional)  — Restrict to submissions by this student
- `states`          (string, optional)  — Filter by state (TURNED_IN, RETURNED, CREATED)
- `page_size`       (integer, optional) — Maximum number of results
- `page_token`      (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "studentSubmissions": [
    {
      "id": "333444555",
      "courseId": "123456789",
      "courseWorkId": "222333444",
      "userId": "555111",
      "state": "TURNED_IN",
      "assignedGrade": 95,
      "late": false,
      "updateTime": "2025-01-31T22:00:00.000Z"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_student_submission</code> — Get a student submission</summary>

Returns a single student submission.

**Inputs:**
```
- `course_id`       (string, required) — Identifier of the course
- `course_work_id`  (string, required) — Identifier of the coursework item
- `id`              (string, required) — Identifier of the submission
```

**Output:**

```json
{
  "id": "333444555",
  "courseId": "123456789",
  "courseWorkId": "222333444",
  "userId": "555111",
  "state": "TURNED_IN",
  "assignedGrade": 95,
  "late": false,
  "updateTime": "2025-01-31T22:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_student_submission</code> — Update a student submission</summary>

Updates fields on a submission, such as the assigned grade. Only certain fields may be updated by students or teachers.

**Inputs:**
```
- `course_id`       (string, required) — Identifier of the course
- `course_work_id`  (string, required) — Identifier of the coursework item
- `id`              (string, required) — Identifier of the submission
- `update_mask`     (string, required) — Fields to update (e.g. assignedGrade,draftGrade)
- `body`            (string, required) — JSON string with updated fields
```

**Output:**

```json
{
  "id": "333444555",
  "courseId": "123456789",
  "courseWorkId": "222333444",
  "userId": "555111",
  "state": "RETURNED",
  "assignedGrade": 95,
  "draftGrade": 95,
  "updateTime": "2025-02-02T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>return_student_submission</code> — Return a submission to the student</summary>

Returns a turned-in submission to the student. The submission state changes to RETURNED.

**Inputs:**
```
- `course_id`       (string, required) — Identifier of the course
- `course_work_id`  (string, required) — Identifier of the coursework item
- `id`              (string, required) — Identifier of the submission
```

**Output:**

```json
{}
```

</details>

<details>
<summary><code>reclaim_student_submission</code> — Reclaim a submitted assignment</summary>

Allows a student to reclaim a turned-in submission for further editing. The submission state changes back to NEW.

**Inputs:**
```
- `course_id`       (string, required) — Identifier of the course
- `course_work_id`  (string, required) — Identifier of the coursework item
- `id`              (string, required) — Identifier of the submission
```

**Output:**

```json
{}
```

</details>


### Course Work Materials

<details>
<summary><code>create_course_work_material</code> — Create a course material</summary>

Creates a material resource (document, video, link, etc.) in a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `body`      (string, required) — JSON string representing the CourseWorkMaterial object
```

**Output:**

```json
{
  "id": "444555666",
  "courseId": "123456789",
  "title": "Week 1 Reading: Python Basics",
  "description": "Required reading for Week 1.",
  "state": "PUBLISHED",
  "updateTime": "2025-01-15T10:00:00.000Z",
  "creationTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>list_course_work_materials</code> — List course materials</summary>

Returns materials in a course, optionally filtered by Drive item or URL.

**Inputs:**
```
- `course_id`          (string, required)  — Identifier of the course
- `material_drive_id`  (string, optional)  — Filter by Google Drive item ID
- `material_link`      (string, optional)  — Filter by material URL
- `page_size`          (integer, optional) — Maximum number of results
- `page_token`         (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "courseWorkMaterial": [
    {
      "id": "444555666",
      "courseId": "123456789",
      "title": "Week 1 Reading: Python Basics",
      "state": "PUBLISHED",
      "updateTime": "2025-01-15T10:00:00.000Z"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_course_work_material</code> — Get a course material</summary>

Returns a single course material.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the material
```

**Output:**

```json
{
  "id": "444555666",
  "courseId": "123456789",
  "title": "Week 1 Reading: Python Basics",
  "description": "Required reading for Week 1.",
  "state": "PUBLISHED",
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_course_work_material</code> — Update a course material</summary>

Updates only the fields specified in `update_mask`.

**Inputs:**
```
- `course_id`    (string, required) — Identifier of the course
- `id`           (string, required) — Identifier of the material
- `update_mask`  (string, required) — Fields to update (e.g. title,description)
- `body`         (string, required) — JSON string with updated fields
```

**Output:**

```json
{
  "id": "444555666",
  "courseId": "123456789",
  "title": "Week 1 Reading: Python Basics (Updated)",
  "state": "PUBLISHED",
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>delete_course_work_material</code> — Delete a course material</summary>

Deletes a course material.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the material to delete
```

**Output:**

```json
{}
```

</details>


### Students

<details>
<summary><code>create_student</code> — Enroll a student</summary>

Adds a user as a student of a course using an enrollment code.

**Inputs:**
```
- `course_id`        (string, required) — Identifier of the course
- `enrollment_code`  (string, required) — Enrollment code of the course
- `body`             (string, required) — JSON string representing the Student object
```

**Output:**

```json
{
  "courseId": "123456789",
  "userId": "555111",
  "profile": {
    "id": "555111",
    "name": { "fullName": "Jane Smith" },
    "emailAddress": "jane.smith@school.edu"
  }
}
```

</details>

<details>
<summary><code>list_students</code> — List students</summary>

Returns all students enrolled in a course.

**Inputs:**
```
- `course_id`   (string, required)  — Identifier of the course
- `page_size`   (integer, optional) — Maximum number of results
- `page_token`  (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "students": [
    {
      "courseId": "123456789",
      "userId": "555111",
      "profile": {
        "id": "555111",
        "name": { "fullName": "Jane Smith" },
        "emailAddress": "jane.smith@school.edu"
      }
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_student</code> — Get a student</summary>

Returns a specific student in a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `user_id`   (string, required) — Identifier of the student
```

**Output:**

```json
{
  "courseId": "123456789",
  "userId": "555111",
  "profile": {
    "id": "555111",
    "name": { "givenName": "Jane", "familyName": "Smith", "fullName": "Jane Smith" },
    "emailAddress": "jane.smith@school.edu"
  }
}
```

</details>

<details>
<summary><code>delete_student</code> — Remove a student</summary>

Removes a student from a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `user_id`   (string, required) — Identifier of the student to remove
```

**Output:**

```json
{}
```

</details>


### Teachers

<details>
<summary><code>create_teacher</code> — Add a teacher</summary>

Adds a user as a co-teacher of a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `body`      (string, required) — JSON string representing the Teacher object
```

**Output:**

```json
{
  "courseId": "123456789",
  "userId": "666111",
  "profile": {
    "id": "666111",
    "name": { "fullName": "Prof. Jones" },
    "emailAddress": "jones@school.edu"
  }
}
```

</details>

<details>
<summary><code>list_teachers</code> — List teachers</summary>

Returns all teachers of a course.

**Inputs:**
```
- `course_id`   (string, required)  — Identifier of the course
- `page_size`   (integer, optional) — Maximum number of results
- `page_token`  (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "teachers": [
    {
      "courseId": "123456789",
      "userId": "666111",
      "profile": {
        "id": "666111",
        "name": { "fullName": "Prof. Jones" },
        "emailAddress": "jones@school.edu"
      }
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_teacher</code> — Get a teacher</summary>

Returns a specific teacher of a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `user_id`   (string, required) — Identifier of the teacher
```

**Output:**

```json
{
  "courseId": "123456789",
  "userId": "666111",
  "profile": {
    "id": "666111",
    "name": { "givenName": "Robert", "familyName": "Jones", "fullName": "Prof. Jones" },
    "emailAddress": "jones@school.edu"
  }
}
```

</details>

<details>
<summary><code>delete_teacher</code> — Remove a teacher</summary>

Removes a teacher from a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `user_id`   (string, required) — Identifier of the teacher to remove
```

**Output:**

```json
{}
```

</details>


### Topics

<details>
<summary><code>create_topic</code> — Create a topic</summary>

Creates a topic in a course to organize coursework and materials.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `body`      (string, required) — JSON string representing the Topic object
```

**Output:**

```json
{
  "courseId": "123456789",
  "topicId": "777888999",
  "name": "Unit 1: Variables and Data Types",
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>list_topics</code> — List topics</summary>

Returns all topics in a course.

**Inputs:**
```
- `course_id`   (string, required)  — Identifier of the course
- `page_size`   (integer, optional) — Maximum number of results
- `page_token`  (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "topic": [
    {
      "courseId": "123456789",
      "topicId": "777888999",
      "name": "Unit 1: Variables and Data Types",
      "updateTime": "2025-01-15T10:00:00.000Z"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_topic</code> — Get a topic</summary>

Returns a single topic.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the topic
```

**Output:**

```json
{
  "courseId": "123456789",
  "topicId": "777888999",
  "name": "Unit 1: Variables and Data Types",
  "updateTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_topic</code> — Update a topic</summary>

Updates only the fields specified in `update_mask`.

**Inputs:**
```
- `course_id`    (string, required) — Identifier of the course
- `id`           (string, required) — Identifier of the topic
- `update_mask`  (string, required) — Fields to update (e.g. name)
- `body`         (string, required) — JSON string with updated fields
```

**Output:**

```json
{
  "courseId": "123456789",
  "topicId": "777888999",
  "name": "Unit 1: Introduction to Python",
  "updateTime": "2025-01-16T09:00:00.000Z"
}
```

</details>

<details>
<summary><code>delete_topic</code> — Delete a topic</summary>

Deletes a topic from a course.

**Inputs:**
```
- `course_id` (string, required) — Identifier of the course
- `id`        (string, required) — Identifier of the topic to delete
```

**Output:**

```json
{}
```

</details>


### Invitations

<details>
<summary><code>create_invitation</code> — Invite a user to a course</summary>

Creates an invitation and sends an email asking the user to join a course as a student or teacher.

**Inputs:**
```
- `body` (string, required) — JSON string representing the Invitation object (userId, courseId, role)
```

**Output:**

```json
{
  "id": "888999111",
  "userId": "555222",
  "courseId": "123456789",
  "role": "STUDENT"
}
```

</details>

<details>
<summary><code>list_invitations</code> — List invitations</summary>

Returns pending invitations, optionally filtered by user or course.

**Inputs:**
```
- `user_id`     (string, optional)  — Restrict to invitations for this user
- `course_id`   (string, optional)  — Restrict to invitations for this course
- `page_size`   (integer, optional) — Maximum number of results
- `page_token`  (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "invitations": [
    {
      "id": "888999111",
      "userId": "555222",
      "courseId": "123456789",
      "role": "STUDENT"
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_invitation</code> — Get an invitation</summary>

Returns a specific invitation.

**Inputs:**
```
- `id` (string, required) — Identifier of the invitation
```

**Output:**

```json
{
  "id": "888999111",
  "userId": "555222",
  "courseId": "123456789",
  "role": "STUDENT"
}
```

</details>

<details>
<summary><code>delete_invitation</code> — Delete an invitation</summary>

Deletes a pending invitation.

**Inputs:**
```
- `id` (string, required) — Identifier of the invitation to delete
```

**Output:**

```json
{}
```

</details>

<details>
<summary><code>accept_invitation</code> — Accept an invitation</summary>

Accepts an invitation, adding the invited user to the course as a student or teacher and removing the invitation.

**Inputs:**
```
- `id` (string, required) — Identifier of the invitation to accept
```

**Output:**

```json
{}
```

</details>


### Registrations

<details>
<summary><code>create_registration</code> — Create a push notification registration</summary>

Registers a Cloud Pub/Sub feed to receive Classroom push notifications.

**Inputs:**
```
- `body` (string, required) — JSON string representing the Registration object (feed, cloudPubsubTopic)
```

**Output:**

```json
{
  "registrationId": "999111222",
  "feed": {
    "feedType": "COURSE_ROSTER_CHANGES",
    "courseRosterChangesInfo": { "courseId": "123456789" }
  },
  "cloudPubsubTopic": {
    "topicName": "projects/my-project/topics/classroom-notifications"
  },
  "expiryTime": "2025-02-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>delete_registration</code> — Delete a registration</summary>

Deletes a push notification registration.

**Inputs:**
```
- `registration_id` (string, required) — Identifier of the registration to delete
```

**Output:**

```json
{}
```

</details>


### User Profiles

<details>
<summary><code>get_user_profile</code> — Get a user profile</summary>

Returns the profile of a user in the context of the authenticated user's courses.

**Inputs:**
```
- `user_id` (string, required) — Identifier of the user (or `me` for the authenticated user)
```

**Output:**

```json
{
  "id": "987654321",
  "name": {
    "givenName": "John",
    "familyName": "Doe",
    "fullName": "John Doe"
  },
  "emailAddress": "john.doe@school.edu",
  "photoUrl": "https://lh3.googleusercontent.com/a/photo"
}
```

</details>


### Guardians

<details>
<summary><code>create_guardian_invitation</code> — Invite a guardian</summary>

Sends an email invitation to a guardian asking them to confirm their relationship to a student.

**Inputs:**
```
- `student_id` (string, required) — Identifier of the student
- `body`       (string, required) — JSON string with the guardian's email address
```

**Output:**

```json
{
  "studentId": "555111",
  "invitationId": "aaa111bbb",
  "invitedEmailAddress": "parent@email.com",
  "state": "PENDING",
  "creationTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>get_guardian_invitation</code> — Get a guardian invitation</summary>

Returns a specific guardian invitation.

**Inputs:**
```
- `student_id`     (string, required) — Identifier of the student
- `invitation_id`  (string, required) — Identifier of the guardian invitation
```

**Output:**

```json
{
  "studentId": "555111",
  "invitationId": "aaa111bbb",
  "invitedEmailAddress": "parent@email.com",
  "state": "PENDING",
  "creationTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>patch_guardian_invitation</code> — Update a guardian invitation</summary>

Updates a guardian invitation (e.g. cancel it by setting state to COMPLETE).

**Inputs:**
```
- `student_id`     (string, required) — Identifier of the student
- `invitation_id`  (string, required) — Identifier of the guardian invitation
- `update_mask`    (string, required) — Fields to update (e.g. state)
- `body`           (string, required) — JSON string with updated fields
```

**Output:**

```json
{
  "studentId": "555111",
  "invitationId": "aaa111bbb",
  "invitedEmailAddress": "parent@email.com",
  "state": "COMPLETE",
  "creationTime": "2025-01-15T10:00:00.000Z"
}
```

</details>

<details>
<summary><code>list_guardians</code> — List guardians</summary>

Returns all confirmed guardians for a student.

**Inputs:**
```
- `student_id`             (string, required)  — Identifier of the student
- `invited_email_address`  (string, optional)  — Filter by guardian email address
- `page_size`              (integer, optional) — Maximum number of results
- `page_token`             (string, optional)  — Token for the next page
```

**Output:**

```json
{
  "guardians": [
    {
      "studentId": "555111",
      "guardianId": "bbb222ccc",
      "invitedEmailAddress": "parent@email.com",
      "guardianProfile": {
        "id": "bbb222ccc",
        "name": { "fullName": "Jane Parent" },
        "emailAddress": "parent@email.com"
      }
    }
  ],
  "nextPageToken": "token_for_next_page"
}
```

</details>

<details>
<summary><code>get_guardian</code> — Get a guardian</summary>

Returns a specific confirmed guardian for a student.

**Inputs:**
```
- `student_id`   (string, required) — Identifier of the student
- `guardian_id`  (string, required) — Identifier of the guardian
```

**Output:**

```json
{
  "studentId": "555111",
  "guardianId": "bbb222ccc",
  "invitedEmailAddress": "parent@email.com",
  "guardianProfile": {
    "id": "bbb222ccc",
    "name": { "givenName": "Jane", "familyName": "Parent", "fullName": "Jane Parent" },
    "emailAddress": "parent@email.com"
  }
}
```

</details>

<details>
<summary><code>delete_guardian</code> — Remove a guardian</summary>

Removes a guardian from a student, revoking their access to student progress emails.

**Inputs:**
```
- `student_id`   (string, required) — Identifier of the student
- `guardian_id`  (string, required) — Identifier of the guardian to remove
```

**Output:**

```json
{}
```

</details>


## API Parameters Reference

<details>
<summary><strong>Common Parameters</strong></summary>

- `page_size` — Maximum number of items to return in a single response. The server may return fewer.
- `page_token` — Token from a previous response's `nextPageToken` field. Pass it to retrieve the next page of results.
- `update_mask` — Comma-separated list of field paths to update in a PATCH call. Only the listed fields are changed; omitted fields are left as-is.

</details>

<details>
<summary><strong>Resource Identifiers</strong></summary>

**Course ID:**
```
Numeric string assigned by Classroom, or an alias prefixed with "d:"
Example: 123456789  or  d:intro-python-2025
```

**User ID:**
```
Numeric Google user ID, email address, or the literal "me" for the authenticated user
Example: 987654321  or  student@school.edu  or  me
```

**Coursework ID:**
```
Numeric string assigned by Classroom.
Use "-" as a wildcard to list submissions across all coursework in list_student_submissions.
Example: 222333444
```

</details>


## Troubleshooting

<details>
<summary><strong>Missing or Invalid Headers</strong></summary>

- **Cause:** OAuth token not provided in request headers or incorrect format
- **Solution:**
  1. Verify `Authorization: Bearer YOUR_TOKEN` and `X-Mewcp-Credential-Id: CREDENTIAL-ID` headers are present
  2. Check that your Google credential is active in your MewCP account

</details>

<details>
<summary><strong>Insufficient Credits</strong></summary>

- **Cause:** API calls have exceeded your request limits
- **Solution:**
  1. Check credit usage in your Curious Layer dashboard
  2. Upgrade to a paid plan or add credits for higher limits
  3. Contact support for credit adjustments

</details>

<details>
<summary><strong>Credential Not Connected</strong></summary>

- **Cause:** No Google Classroom credential linked to your account
- **Solution:**
  1. Go to **Credentials** in your MewCP dashboard
  2. Connect your Google account via OAuth
  3. Retry the request with the correct `X-Mewcp-Credential-Id` header

</details>

<details>
<summary><strong>Malformed Request Payload</strong></summary>

- **Cause:** JSON payload passed to a `body` parameter is invalid or missing required fields
- **Solution:**
  1. Validate JSON syntax before sending
  2. Ensure all required fields for the resource type are included
  3. Check parameter types match the Google Classroom API schema

</details>

<details>
<summary><strong>Server Not Found</strong></summary>

- **Cause:** Incorrect server name in the API endpoint
- **Solution:**
  1. Verify endpoint format: `{server-name}/mcp/{tool-name}`
  2. Use correct server name from documentation
  3. Check available servers in your Curious Layer account

</details>

<details>
<summary><strong>Google Classroom API Error</strong></summary>

- **Cause:** Upstream Google Classroom API returned an error (e.g. 403 Forbidden, 404 Not Found)
- **Solution:**
  1. Check the Google Workspace Status Dashboard for outages
  2. Verify your Google account has the required role (teacher/admin) for the operation
  3. Ensure the requested course or resource exists and you have access to it

</details>

---

<details>
<summary><strong>Resources</strong></summary>

- **[Google Classroom API Documentation](https://developers.google.com/classroom/guides/get-started)** — Official getting started guide
- **[Google Classroom API Reference](https://developers.google.com/classroom/reference/rest)** — Complete endpoint reference
- **[FastMCP Docs](https://gofastmcp.com/v2/getting-started/welcome)** — FastMCP specification
- **[FastMCP Credentials](https://pypi.org/project/fastmcp-credentials/)** — Credential handling package

</details>
