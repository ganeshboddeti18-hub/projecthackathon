import io
import time
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from main import run_simulation


st.set_page_config(
    page_title="Agentic Project Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- SESSION STATE ----------------------
if "logo_bytes" not in st.session_state:
    st.session_state.logo_bytes = None

if "show_logo_uploader" not in st.session_state:
    st.session_state.show_logo_uploader = False


# ---------------------- PDF REPORT ----------------------
def generate_pdf_report(project_name, board, total_days):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(40, y, "Agentic AI Project Management Report")

    y -= 30
    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, y, f"Project Name: {project_name}")

    total_tasks = len(board.tasks)
    completed_tasks = sum(1 for t in board.tasks if t.status == "Done")
    total_bugs = sum(t.bugs_found for t in board.tasks)

    y -= 25
    pdf.drawString(40, y, f"Total Tasks: {total_tasks}")
    y -= 20
    pdf.drawString(40, y, f"Completed Tasks: {completed_tasks}")
    y -= 20
    pdf.drawString(40, y, f"Days Taken: {total_days}")
    y -= 20
    pdf.drawString(40, y, f"Total Bugs Found: {total_bugs}")

    y -= 35
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Task Summary")

    y -= 25
    pdf.setFont("Helvetica", 10)

    for task in board.tasks:
        line = (
            f"{task.name} | Status: {task.status} | Assigned To: {task.assigned_to} | "
            f"Bugs: {task.bugs_found} | Worked: {task.days_worked}/{task.estimated_days}"
        )

        if y < 60:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 10)

        pdf.drawString(40, y, line[:110])
        y -= 18

    y -= 20
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Agent Logs")

    y -= 20
    pdf.setFont("Helvetica", 9)

    for log in board.logs:
        if y < 60:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 9)

        pdf.drawString(40, y, log[:115])
        y -= 14

    pdf.save()
    buffer.seek(0)
    return buffer


# ---------------------- CSS ----------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 45%, #ecfeff 100%);
    }

    .hero-box {
        background: linear-gradient(135deg, #1e1b4b, #4338ca, #0891b2);
        padding: 34px;
        border-radius: 26px;
        color: white;
        box-shadow: 0 18px 40px rgba(15,23,42,0.20);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.28s ease;
    }

    .hero-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 24px 48px rgba(15,23,42,0.24);
    }

    .hero-box::after {
        content: "";
        position: absolute;
        top: -45px;
        right: -45px;
        width: 190px;
        height: 190px;
        background: rgba(255,255,255,0.10);
        border-radius: 50%;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 18px;
        opacity: 0.96;
        line-height: 1.65;
        max-width: 900px;
    }

    .logo-chip {
        display: inline-block;
        background: rgba(255,255,255,0.16);
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 14px;
        backdrop-filter: blur(10px);
    }

    .control-panel {
        background: rgba(255,255,255,0.80);
        backdrop-filter: blur(14px);
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 12px 28px rgba(15,23,42,0.10);
        border: 1px solid rgba(255,255,255,0.70);
        transition: all 0.25s ease;
        margin-bottom: 18px;
    }

    .control-panel:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 34px rgba(15,23,42,0.14);
    }

    .glass-box {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(14px);
        padding: 22px;
        border-radius: 24px;
        box-shadow: 0 12px 28px rgba(15,23,42,0.10);
        border: 1px solid rgba(255,255,255,0.70);
        margin-bottom: 18px;
        transition: all 0.25s ease;
    }

    .glass-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 18px 34px rgba(15,23,42,0.14);
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .muted-text {
        color: #475569;
        font-size: 14px;
    }

    .metric-card {
        background: rgba(255,255,255,0.88);
        backdrop-filter: blur(10px);
        border-radius: 22px;
        padding: 20px;
        box-shadow: 0 10px 24px rgba(15,23,42,0.10);
        border: 1px solid rgba(255,255,255,0.60);
        transition: all 0.22s ease;
        margin-bottom: 10px;
    }

    .metric-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 34px rgba(15,23,42,0.14);
    }

    .metric-title {
        color: #475569;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #0f172a;
        font-size: 34px;
        font-weight: 800;
    }

    .equal-card-container {
        display: flex;
        gap: 18px;
        margin-bottom: 18px;
        align-items: stretch;
    }

    .equal-card {
        flex: 1;
        min-height: 180px;
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 18px rgba(15,23,42,0.06);
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .equal-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 14px 24px rgba(15,23,42,0.10);
    }

    .equal-card h4 {
        margin: 0 0 10px 0;
        font-size: 20px;
        color: #0f172a;
        font-weight: 800;
    }

    .equal-card p {
        margin: 0;
        font-size: 15px;
        color: #475569;
        line-height: 1.7;
    }

    .log-box {
        background: linear-gradient(135deg, #0f172a, #111827);
        color: #e5e7eb;
        padding: 14px 16px;
        border-radius: 16px;
        margin-bottom: 10px;
        font-family: Consolas, monospace;
        font-size: 14px;
        border-left: 5px solid #22d3ee;
        box-shadow: 0 8px 18px rgba(15,23,42,0.18);
        transition: all 0.2s ease;
    }

    .log-box:hover {
        transform: translateX(4px);
    }

    .success-chip {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }

    .warn-chip {
        display: inline-block;
        background: #fef3c7;
        color: #92400e;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 14px;
    }

    .footer-note {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        margin-top: 12px;
    }

    .sidebar-logo-title {
        text-align: center;
        font-size: 24px;
        font-weight: 800;
        color: #1e293b;
        margin-top: 4px;
        margin-bottom: 8px;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #e0e7ff 0%, #f8fafc 100%);
    }

    .stButton > button {
        background: linear-gradient(135deg, #4f46e5, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 0.9rem 1.2rem !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        box-shadow: 0 12px 24px rgba(79,70,229,0.28) !important;
        transition: all 0.22s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 18px 30px rgba(79,70,229,0.34) !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #0f172a, #334155) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.1rem !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown("""
<div class="hero-box">
    <div class="logo-chip">🤖 Multi-Agent System</div>
    <div class="hero-title">🚀 Agentic AI Project Management Simulator</div>
    <div class="hero-subtitle">
        This project transforms project management from human-driven coordination into an intelligent, 
      self-operating ecosystem powered by Agentic AI.
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR ----------------------
if st.session_state.logo_bytes is not None:
    st.sidebar.image(st.session_state.logo_bytes, use_container_width=True)
else:
    st.sidebar.markdown(
        '<div class="sidebar-logo-title">🤖 Agentic AI</div>',
        unsafe_allow_html=True,
    )

logo_col1, logo_col2 = st.sidebar.columns(2)
with logo_col1:
    if st.button("+", key="logo_add_button", use_container_width=True):
        st.session_state.show_logo_uploader = True

with logo_col2:
    if st.button("-", key="logo_remove_button", use_container_width=True):
        st.session_state.logo_bytes = None
        st.session_state.show_logo_uploader = False
        st.rerun()

if st.session_state.show_logo_uploader:
    uploaded_logo = st.sidebar.file_uploader(
        "Choose logo",
        type=["png", "jpg", "jpeg"],
        key="sidebar_logo_upload",
        label_visibility="collapsed",
    )
    if uploaded_logo is not None:
        st.session_state.logo_bytes = uploaded_logo.read()
        st.session_state.show_logo_uploader = False
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Configure the project setup and simulation settings.")

project_name = st.sidebar.text_input(
    "Project Name",
    value="E-commerce App",
    key="sidebar_project_name",
)
developer_count = st.sidebar.number_input(
    "Number of Developers",
    min_value=1,
    max_value=10,
    value=2,
    key="sidebar_developer_count",
)
max_days = st.sidebar.number_input(
    "Maximum Simulation Days",
    min_value=1,
    max_value=50,
    value=15,
    key="sidebar_max_days",
)
task_count = st.sidebar.number_input(
    "Number of Tasks",
    min_value=1,
    max_value=10,
    value=5,
    key="sidebar_task_count",
)

st.sidebar.markdown("---")
st.sidebar.success("Recommended demo: 2 developers • 5 tasks • 15 days")
st.sidebar.info("Use exact dependency names to unlock tasks correctly.")

# ---------------------- TOP CARDS ----------------------
st.markdown("""
<div class="equal-card-container">
    <div class="equal-card">
        <h4>🎯 Goal</h4>
        <p>Simulate planning, development, testing, and client feedback using multiple agents.</p>
    </div>
    <div class="equal-card">
        <h4>🧩 Input</h4>
        <p>Project name, team size, tasks, priorities, deadlines, dependencies, and simulation days.</p>
    </div>
    <div class="equal-card">
        <h4>📊 Output</h4>
        <p>Metrics, task board, bug chart, completion report, logs, and downloadable PDF.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------- TASK DESIGNER ----------------------
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Task Designer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="muted-text">Design tasks below, then launch the simulation.</div>',
    unsafe_allow_html=True,
)

task_inputs = []

for i in range(int(task_count)):
    with st.expander(f"Task {i+1} Configuration", expanded=(i == 0)):
        left, right = st.columns(2)

        with left:
            name = st.text_input(
                "Task Name",
                value=f"Task {i+1}",
                key=f"task_name_{i}",
            )
            description = st.text_area(
                "Description",
                value=f"Description for Task {i+1}",
                key=f"task_desc_{i}",
            )
            priority = st.number_input(
                "Priority",
                min_value=1,
                max_value=10,
                value=min(i + 1, 10),
                key=f"task_priority_{i}",
            )

        with right:
            deadline = st.number_input(
                "Deadline Days",
                min_value=1,
                max_value=50,
                value=min(i + 2, 50),
                key=f"task_deadline_{i}",
            )
            estimated_days = st.number_input(
                "Estimated Days",
                min_value=1,
                max_value=20,
                value=2,
                key=f"task_estimated_days_{i}",
            )
            dependencies_text = st.text_input(
                "Dependencies (comma separated)",
                value="",
                key=f"task_dependencies_{i}",
            )

        dependencies = [dep.strip() for dep in dependencies_text.split(",") if dep.strip()]

        task_inputs.append(
            {
                "name": name,
                "description": description,
                "priority": int(priority),
                "deadline": int(deadline),
                "estimated_days": int(estimated_days),
                "dependencies": dependencies,
            }
        )

st.markdown("</div>", unsafe_allow_html=True)

run_button = st.button("▶ Run Simulation", use_container_width=True, key="run_simulation_button")

# ---------------------- OUTPUT ----------------------
if run_button:
    with st.spinner("Launching agents and generating simulation..."):
        time.sleep(1.2)
        board, total_days = run_simulation(
            task_inputs=task_inputs,
            developer_count=int(developer_count),
            max_days=int(max_days),
        )

    total_tasks = len(board.tasks)
    completed_tasks = sum(1 for task in board.tasks if task.status == "Done")
    total_bugs = sum(task.bugs_found for task in board.tasks)
    completion_percent = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    pdf_buffer = generate_pdf_report(project_name, board, total_days)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-title">📊 Simulation Result: {project_name}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="muted-text">Project summary generated from your custom input.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    b1, b2 = st.columns([4, 1])
    with b2:
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name=f"{project_name.replace(' ', '_').lower()}_report.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_pdf_button",
        )

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📌 Total Tasks</div>
            <div class="metric-value">{total_tasks}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 8px solid #16a34a;">
            <div class="metric-title">✅ Completed</div>
            <div class="metric-value">{completed_tasks}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 8px solid #f59e0b;">
            <div class="metric-title">⏳ Days Taken</div>
            <div class="metric-value">{total_days}</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 8px solid #ef4444;">
            <div class="metric-title">🐞 Bugs Found</div>
            <div class="metric-value">{total_bugs}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Project Completion</div>', unsafe_allow_html=True)
    st.progress(completion_percent / 100)

    if completion_percent == 100:
        st.markdown('<span class="success-chip">✅ Project completed successfully</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="warn-chip">⚠ Project not fully completed</span>', unsafe_allow_html=True)

    st.markdown(
        f"<p class='muted-text' style='margin-top:8px;'>Completion: <b>{completion_percent}%</b></p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Task Board</div>', unsafe_allow_html=True)

    task_data = []
    for task in board.tasks:
        if task.status == "Done":
            status_label = "✅ Done"
        elif task.status == "In Progress":
            status_label = "🟡 In Progress"
        else:
            status_label = "🔴 Pending"

        task_data.append(
            {
                "Task Name": task.name,
                "Priority": task.priority,
                "Assigned To": task.assigned_to,
                "Status": status_label,
                "Deadline": task.deadline,
                "Worked Days": f"{task.days_worked}/{task.estimated_days}",
                "Bugs Found": task.bugs_found,
                "Dependencies": ", ".join(task.dependencies) if task.dependencies else "None",
            }
        )

    df = pd.DataFrame(task_data)
    st.dataframe(df, use_container_width=True, height=320)
    st.markdown("</div>", unsafe_allow_html=True)

    left_chart, right_chart = st.columns(2)

    with left_chart:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📊 Status Breakdown</div>', unsafe_allow_html=True)
        status_counts = df["Status"].value_counts()
        st.bar_chart(status_counts)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_chart:
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🐞 Bugs Per Task</div>', unsafe_allow_html=True)
        bug_df = pd.DataFrame(
            {
                "Task Name": [task.name for task in board.tasks],
                "Bugs Found": [task.bugs_found for task in board.tasks],
            }
        ).set_index("Task Name")
        st.bar_chart(bug_df)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧩 Incomplete Tasks</div>', unsafe_allow_html=True)
    incomplete_tasks = [task for task in board.tasks if task.status != "Done"]

    if incomplete_tasks:
        for task in incomplete_tasks:
            st.warning(
                f"Task: {task.name} | Status: {task.status} | Dependencies: {task.dependencies}"
            )
    else:
        st.success("All tasks completed successfully.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🖥 Agent Logs Console</div>', unsafe_allow_html=True)

    for log in board.logs:
        st.markdown(f'<div class="log-box">{log}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    '<div class="footer-note">Built with Streamlit • Agentic AI Dashboard</div>',
    unsafe_allow_html=True,
)