import sqlite3

# Connect to the database
conn = sqlite3.connect(
    r'C:\Users\liviu\FAFHackathon\fafhack2023\container\src\database\Source.db')

# Define the group_id
group_id = 1

# Fetch all information for group_id = 1, including room information
query = """
    SELECT gs.group_id, gs.subject_id, s.name AS subject_name, s.theory, s.seminar, s.lab, s.project, s.year, s.semester,
           g.name AS group_name, g.students,
           r.id AS room_id, r.is_lab, r.capacity
    FROM groups_subjects gs
    JOIN subjects s ON gs.subject_id = s.id
    JOIN groups g ON gs.group_id = g.id
    LEFT JOIN rooms r ON r.is_lab = 1 AND s.lab > 0  -- Join labs if labs are needed for the subject
                     OR r.is_lab = 0 AND s.lab = 0  -- Join non-labs if no labs are needed
    WHERE gs.group_id = ?
"""

# Execute the query and fetch all rows
rows = conn.execute(query, (group_id,)).fetchall()

# Process the results to find the best options for each pair
for row in rows:
    group_id, subject_id, subject_name, theory, seminar, lab, project, year, semester, group_name, students, room_id, is_lab, capacity = row

    # Check if lab is needed for the subject
    lab_needed = lab > 0

    # Check if the room is suitable for the subject
    room_suitable = is_lab == lab_needed

    # Check if the room has enough capacity for the students
    capacity_sufficient = capacity >= students

    # Print information about the group, subject, and room
    if room_suitable and capacity_sufficient:
        print(f"Group ID: {group_id}, Subject ID: {subject_id}, Group Name: {group_name}, Subject Name: {
              subject_name}, Semester: {semester}, Room ID: {room_id}, Capacity: {capacity}")
    else:
        print(f"No suitable room found for Group ID: {group_id}, Subject ID: {
              subject_id}, Group Name: {group_name}, Subject Name: {subject_name}, Semester: {semester}")

# Close the connection
conn.close()
