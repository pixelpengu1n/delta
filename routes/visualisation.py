from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io

router = APIRouter()

class DataVisualizer:
    def __init__(self, analysis_results):
        self.analysis_results = analysis_results

    def visualize_summary_statistics(self, category, statistics):
        fig, ax = plt.subplots(figsize=(12, 7))
        keys = list(statistics.keys())
        means = [statistics[k]['mean'] for k in keys]
        medians = [statistics[k]['median'] for k in keys]
        std_devs = [statistics[k]['std_dev'] for k in keys]

        x = range(len(keys))
        ax.bar(x, means, width=0.2, label='Mean', color='skyblue')
        ax.bar([p + 0.2 for p in x], medians, width=0.2, label='Median', color='lightgreen')
        ax.bar([p + 0.4 for p in x], std_devs, width=0.2, label='Std Dev', color='salmon')

        ax.set_xticks([p + 0.2 for p in x])
        ax.set_xticklabels(keys, rotation=45)
        ax.set_title(f"Summary Statistics for {category}")
        ax.set_ylabel("Values")
        ax.legend()
        plt.tight_layout()
        return fig

    def visualize_event_trends(self, category, trends):
        fig, ax = plt.subplots(figsize=(8, 5))
        labels = ['First Event', 'Last Event']
        times = [trends.get("first_event", "N/A"), trends.get("last_event", "N/A")]

        sns.barplot(x=labels, y=[1, 1], ax=ax, palette="viridis")
        for idx, time in enumerate(times):
            ax.text(idx, 0.5, time, ha='center', color='white', fontsize=12)

        ax.set_title(f"Event Timeline for {category}")
        ax.get_yaxis().set_visible(False)
        plt.tight_layout()
        return fig

    def generate_visualizations(self):
        figures = []
        for category, insights in self.analysis_results.items():
            if insights.get("summary") and insights["summary"].get("statistics"):
                figures.append(self.visualize_summary_statistics(category, insights["summary"]["statistics"]))
            if insights.get("trends"):
                figures.append(self.visualize_event_trends(category, insights["trends"]))
        return figures

@router.post("/visualize/")
async def visualize_analysis(file: UploadFile = File(...)):
    try:
        data = json.loads(await file.read())
        analysis_results = data.get("analysis_results", {})
        if not analysis_results:
            raise HTTPException(status_code=400, detail="No analysis results provided.")

        visualizer = DataVisualizer(analysis_results)
        figures = visualizer.generate_visualizations()

        if not figures:
            raise HTTPException(status_code=400, detail="No visualizations could be generated.")

        # Combine multiple figures into one image vertically
        buf = io.BytesIO()
        combined_height = sum(fig.get_size_inches()[1] for fig in figures)
        width = max(fig.get_size_inches()[0] for fig in figures)

        combined_fig, combined_ax = plt.subplots(len(figures), 1, figsize=(width, combined_height))

        if len(figures) == 1:
            combined_ax = [combined_ax]

        for ax, fig in zip(combined_ax, figures):
            canvas = fig.canvas
            canvas.draw()
            ax.imshow(canvas.buffer_rgba())
            ax.axis('off')

        plt.tight_layout()
        combined_fig.savefig(buf, format='png')
        plt.close('all')
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
