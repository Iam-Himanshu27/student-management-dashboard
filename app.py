
import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# DASHBOARD HEADER
# ==================================

st.title("Student Management Dashboard - version 2")
st.success("Successfully deployed using Docker Version 2!")
st.write("Welcome to my first dashboard!")

st.header("Student Overview")
st.subheader("Academic Performance")

# ==================================
# INITIALIZE STUDENT RECORDS
# ==================================

if "students" not in st.session_state:
    st.session_state.students = [
        {"ID": 101, "Name": "Rahul", "Course": "Python", "Marks": 85},
        {"ID": 102, "Name": "Priya", "Course": "Java", "Marks": 90},
        {"ID": 103, "Name": "Amit", "Course": "Docker", "Marks": 75},
        {"ID": 104, "Name": "Sneha", "Course": "Python", "Marks": 80}
    ]

# ==================================
# DASHBOARD METRICS
# ==================================

students = st.session_state.students

total_students = len(students)

average_marks = (
    sum(s["Marks"] for s in students) / total_students
    if total_students > 0 else 0
)

total_courses = len(set(s["Course"] for s in students))

col1, col2, col3 = st.columns(3)

col1.metric("Total Students", total_students)
col2.metric("Average Marks", f"{average_marks:.2f}%")
col3.metric("Courses", total_courses)

# ==================================
# SIDEBAR NAVIGATION
# ==================================

st.sidebar.title("Navigation")

menu = st.sidebar.selectbox(
    "Select Menu",
    ["Dashboard", "Students", "Report"]
)

st.sidebar.write("Student Management System")

# ==================================
# STUDENT RECORDS
# ==================================

st.subheader("Student Records")

st.table(students)

# ==================================
# ADD NEW STUDENT FORM
# ==================================

st.subheader("Add New Student")

with st.form("student_form"):

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    student_name = st.text_input("Student Name")

    course = st.selectbox(
        "Select Course",
        ["Python", "Java", "Docker", "Node.js"]
    )

    marks = st.number_input(
        "Enter Marks",
        min_value=0,
        max_value=100,
        step=1
    )

    submit = st.form_submit_button("Add Student")

# ==================================
# ADD STUDENT VALIDATION
# ==================================

if submit:

    if student_name.strip() == "":
        st.error("Please enter student name")

    elif any(
        s["ID"] == student_id
        for s in st.session_state.students
    ):
        st.error("Student ID already exists")

    else:

        new_student = {
            "ID": student_id,
            "Name": student_name.strip(),
            "Course": course,
            "Marks": marks
        }

        st.session_state.students.append(new_student)

        st.success("Student added successfully!")

        st.rerun()

# ==================================
# STUDENT ANALYTICS & VISUALIZATION
# ==================================

st.header("Student Analytics Dashboard")

students_data = st.session_state.students

if len(students_data) > 0:

    # Convert records into DataFrame

    df = pd.DataFrame(students_data)

    # ==================================
    # 1. COMPARISON CHART
    # ==================================

    st.subheader("1. Student Marks Comparison")

    comparison_chart = px.bar(
        df,
        x="Name",
        y="Marks",
        color="Course",
        text="Marks",
        title="Marks Comparison Between Students",
        labels={
            "Name": "Student Name",
            "Marks": "Total Marks"
        }
    )

    comparison_chart.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        comparison_chart,
        use_container_width=True
    )

    # ==================================
    # 2. DISTRIBUTION CHART
    # ==================================

    st.subheader("2. Course Distribution")

    course_data = (
        df["Course"]
        .value_counts()
        .rename_axis("Course")
        .reset_index(name="Students")
    )

    distribution_chart = px.pie(
        course_data,
        names="Course",
        values="Students",
        hole=0.4,
        title="Students Distribution by Course"
    )

    st.plotly_chart(
        distribution_chart,
        use_container_width=True
    )

    # ==================================
    # 3. PERFORMANCE CHART
    # ==================================

    st.subheader("3. Student Performance Analysis")

    average_marks = df["Marks"].mean()

    performance_chart = px.line(
        df,
        x="Name",
        y="Marks",
        markers=True,
        title="Individual Student Performance",
        labels={
            "Name": "Student Name",
            "Marks": "Marks Obtained"
        }
    )

    performance_chart.add_hline(
        y=average_marks,
        line_dash="dash",
        annotation_text=f"Class Average: {average_marks:.2f}"
    )

    performance_chart.update_layout(
        yaxis_range=[0, 100]
    )

    st.plotly_chart(
        performance_chart,
        width="Stretch"
    )

else:

    st.warning("No student records available for analytics.")

