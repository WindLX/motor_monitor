<script lang="ts">
    // assets
    import { chart as chartConfig } from "../assets/config.json";
    // svelte
    import { onMount, onDestroy } from "svelte";
    // chart.js
    import { Chart, registerables } from "chart.js";
    Chart.register(...registerables);

    let {
        chartTitle,
        labels,
        datasets,
        yUnit = "",
    }: {
        chartTitle: string;
        labels: number[];
        datasets: any[];
        yUnit: string;
    } = $props();

    let chart: Chart | null = null;

    function truncateDatasets(
        labels: any[],
        datasets: any[],
        maxLength: number,
    ) {
        const truncatedLabels = labels.slice(-maxLength);
        const truncatedDatasets = datasets.map((dataset) => ({
            ...dataset,
            data: dataset.data.slice(-maxLength),
        }));
        return { truncatedLabels, truncatedDatasets };
    }

    onMount(() => {
        const ctx = document.getElementById(
            `${chartTitle}-chart`,
        ) as HTMLCanvasElement;

        const {
            truncatedLabels: initialLabels,
            truncatedDatasets: initialDatasets,
        } = truncateDatasets(labels, datasets, chartConfig.max_data_points);

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: initialLabels,
                datasets: initialDatasets,
            },
            options: {
                responsive: true,
                animation: {
                    duration: 0,
                    easing: "easeOutQuint",
                },
                plugins: {
                    title: {
                        display: true,
                        text: chartTitle,
                    },
                },
                elements: {
                    line: {
                        tension: 0.4, // This will smooth the lines
                    },
                },
                scales: {
                    x: {
                        type: "linear",
                        title: { display: true, text: "Time (seconds)" },
                        ticks: {
                            callback: function (value) {
                                return Number(value).toFixed(1) + "s";
                            },
                        },
                    },
                    y: {
                        title: { display: true, text: yUnit },
                    },
                },
            },
        });
    });

    $effect(() => {
        if (chart) {
            // 截断为新长度
            const { truncatedLabels, truncatedDatasets } = truncateDatasets(
                labels,
                datasets,
                chartConfig.max_data_points,
            );

            // 保留图表的隐藏状态
            const visibility = chart.data.datasets.map(
                (dataset) => dataset.hidden,
            );
            // 更新数据
            chart.data.labels = truncatedLabels;
            chart.data.datasets = truncatedDatasets.map((dataset, index) => ({
                ...dataset,
                hidden: visibility[index] ?? dataset.hidden ?? false,
            }));
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
