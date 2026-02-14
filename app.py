import numpy as np
import gradio as gr


def generate_students(n):
    n = int(n)

    names = np.array([f"Student {i+1}" for i in range(n)])
    scores = np.random.randint(0, 101, size=(n, 3))

    table = np.column_stack((names, scores))

    return table, table


def student_summary(data):
    data = np.array(data)

    names = data[:, 0]
    scores = data[:, 1:].astype(float)

    total = np.sum(scores, axis=1)
    avg = np.mean(scores, axis=1)

    summary_table = np.column_stack((names, total, avg))

    return summary_table


def subject_averages(data):
    data = np.array(data)

    scores = data[:, 1:].astype(float)

    subject_names = np.array(["Math", "Science", "English"])
    averages = np.mean(scores, axis=0)

    return np.column_stack((subject_names, averages))


def rank_students(data):
    data = np.array(data)

    names = data[:, 0]
    scores = data[:, 1:].astype(float)

    totals = np.sum(scores, axis=1)
    sorted_idx = np.argsort(totals)[::-1]

    ranked_names = names[sorted_idx]
    ranked_totals = totals[sorted_idx]

    ranks = np.arange(1, len(names) + 1)

    return np.column_stack((ranks, ranked_names, ranked_totals))


def filter_above_average(data, threshold):
    data = np.array(data)

    names = data[:, 0]
    scores = data[:, 1:].astype(float)
    threshold = float(threshold)

    avg = np.mean(scores, axis=1)

    mask = avg > threshold

    return np.column_stack((names[mask], avg[mask]))


with gr.Blocks(title="Multi-Subject Student Analyzer") as demo:

    gr.Markdown("# 🎓 Multi-Subject Student Analyzer")

    data_state = gr.State()

    with gr.Row():
        count_input = gr.Number(value=10, label="Number of Students")
        generate_btn = gr.Button("Generate Students", variant="primary")

    students_table = gr.Dataframe(
        headers=["Student", "Math", "Science", "English"],
        interactive=False
    )

    generate_btn.click(
        generate_students,
        inputs=count_input,
        outputs=[data_state, students_table]
    )

    gr.Markdown("---")

    with gr.Tab("📊 Student Totals & Averages"):
        summary_btn = gr.Button("Compute Student Summary", variant="primary")
        summary_output = gr.Dataframe(
            headers=["Student", "Total", "Average"],
            interactive=False
        )
        summary_btn.click(student_summary, inputs=data_state, outputs=summary_output)

    with gr.Tab("📈 Subject Averages"):
        subject_btn = gr.Button("Compute Subject Averages", variant="primary")
        subject_output = gr.Dataframe(
            headers=["Subject", "Class Average"],
            interactive=False
        )
        subject_btn.click(subject_averages, inputs=data_state, outputs=subject_output)

    with gr.Tab("🏆 Rankings"):
        rank_btn = gr.Button("Rank Students", variant="primary")
        rank_output = gr.Dataframe(
            headers=["Rank", "Student", "Total"],
            interactive=False
        )
        rank_btn.click(rank_students, inputs=data_state, outputs=rank_output)

    with gr.Tab("🔍 Filter by Average"):
        threshold_input = gr.Number(value=70, label="Average Threshold")
        filter_btn = gr.Button("Filter Students", variant="primary")
        filter_output = gr.Dataframe(
            headers=["Student", "Average"],
            interactive=False
        )
        filter_btn.click(
            filter_above_average,
            inputs=[data_state, threshold_input],
            outputs=filter_output
        )

demo.launch(theme=gr.themes.Soft())
