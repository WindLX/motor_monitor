<script lang="ts">
    import { onMount } from "svelte";
    import { Chart, registerables } from "chart.js";
    Chart.register(...registerables);
    import "chartjs-adapter-date-fns";

    export let chartId: string;
    export let labels: string[] = [];
    export let datasets: any[] = [];

    let chart: Chart | null = null;

    onMount(() => {
        const ctx = document.getElementById(chartId) as HTMLCanvasElement;
        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets,
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        type: "linear",
                        title: {
                            display: true,
                            text: "Time (seconds)",
                        },
                    },
                },
            },
        });
    });

    $: if (chart) {
        chart.data.labels = labels;
        chart.data.datasets = datasets;
        chart.update();
    }
</script>

<canvas id={chartId}></canvas>

<style>
    canvas {
        width: 100%;
        max-width: 800px;
        height: 400px;
        margin-top: 20px;
    }
</style>
