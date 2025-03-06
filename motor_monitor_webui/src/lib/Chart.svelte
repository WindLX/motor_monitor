<script lang="ts">
    // svelte
    import { onMount, onDestroy } from "svelte";

    // chart.js
    import { Chart, registerables } from "chart.js";
    // import "chartjs-adapter-date-fns";
    Chart.register(...registerables);

    let {
        chartTitle,
        labels,
        datasets,
    }: {
        chartTitle: string;
        labels: number[];
        datasets: any[];
    } = $props();

    let chart: Chart | null = null;

    onMount(() => {
        const ctx = document.getElementById(
            `${chartTitle}-chart`,
        ) as HTMLCanvasElement;
        chart = new Chart(ctx, {
            type: "line",
            data: { datasets },
            options: {
                responsive: true,
                animation: {
                    duration: 0,
                    easing: "easeOutQuint",
                },
                scales: {
                    x: {
                        type: "linear",
                        title: { display: true, text: "Time (seconds)" },
                        ticks: {
                            callback: function (value) {
                                return Number(value).toFixed(1) + "s"; // 数值转带秒的标签
                            },
                        },
                    },
                },
            },
        });
    });

    $effect(() => {
        if (chart) {
            // 保存当前的隐藏状态
            const visibility = chart.data.datasets.map(
                (dataset) => dataset.hidden,
            );
            // 更新标签和数据
            chart.data.labels = labels;
            // 将新数据集与旧隐藏状态合并
            chart.data.datasets = datasets.map((dataset, index) => ({
                ...dataset,
                hidden: visibility[index] ?? dataset.hidden ?? false,
            }));
            // 更新图表以应用新数据和隐藏状态
            chart.update();
        }
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
            chart = null;
        }
    });
</script>

<canvas id={chartTitle + "-chart"} style="width: 100%; height: 400px;"></canvas>

<style>
    canvas {
        width: 100%;
        max-width: 800px;
        height: 400px;
        margin-top: 20px;
    }
</style>
