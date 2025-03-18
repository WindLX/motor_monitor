<script lang="ts">
    let {
        min,
        max,
        value = $bindable(0),
        safeMin,
        safeMax,
        showTicks = true,
        oninput,
    }: {
        min: number;
        max: number;
        value: number;
        safeMin: number;
        safeMax: number;
        showTicks: boolean;
        oninput: (value: number) => void;
    } = $props();

    let track: HTMLDivElement;
    let thumb: HTMLDivElement;
    let isDragging = false;

    $effect(() => {
        const handleMove = (e: any) => {
            if (!isDragging) return;
            updateValue(e);
        };

        const handleUp = () => {
            isDragging = false;
        };

        document.addEventListener("mousemove", handleMove);
        document.addEventListener("mouseup", handleUp);

        return () => {
            document.removeEventListener("mousemove", handleMove);
            document.removeEventListener("mouseup", handleUp);
        };
    });

    function updateValue(e: any) {
        const rect = track.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        let newValue = min + percent * (max - min);
        newValue = Math.max(min, Math.min(max, newValue));
        value = Math.round(newValue);

        oninput(value);
    }

    function getPosition(val: number) {
        return ((val - min) / (max - min)) * 100;
    }
</script>

<div class="slider-container">
    <div
        class="slider-track"
        bind:this={track}
        onmousedown={updateValue}
        role="slider"
        tabindex="0"
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
    >
        <div
            class="safe-zone"
            style="left: {getPosition(safeMin)}%; right: {100 -
                getPosition(safeMax)}%"
        ></div>

        <div class="marker" style="left: {getPosition(safeMin)}%"></div>
        <div class="marker" style="left: 50%"></div>
        <div class="marker" style="left: {getPosition(safeMax)}%"></div>

        {#if showTicks}
            <div class="ticks">
                {#each Array(max - min + 1) as _, i}
                    <div
                        class="tick"
                        style="left: {(i / (max - min)) * 100}%"
                    ></div>
                {/each}
            </div>
        {/if}

        <div
            class="slider-thumb"
            style="left: {getPosition(value)}%"
            bind:this={thumb}
            onmousedown={() => (isDragging = true)}
            role="slider"
            tabindex="0"
            aria-valuemin={min}
            aria-valuemax={max}
            aria-valuenow={value}
        ></div>
    </div>
</div>

<style>
    .slider-container {
        position: relative;
        padding: 20px 0;
        width: 300px;
    }

    .slider-container .slider-track {
        position: relative;
        height: 4px;
        background: var(--primary-color-light);
        cursor: pointer;
    }

    .slider-container .slider-thumb {
        position: absolute;
        width: 6px;
        height: 24px;
        background: var(--primary-color);
        border-radius: 2px;
        top: 50%;
        transform: translate(-50%, -50%);
        cursor: grab;
        transition: transform 0.2s;
        z-index: 5;
    }

    .slider-container .slider-thumb:active,
    .slider-container .slider-thumb:hover {
        transform: translate(-50%, -50%) scale(1.2);
        box-shadow: 0 0 6px 0 var(--primary-color);
        cursor: grabbing;
    }

    .slider-container .safe-zone {
        position: absolute;
        height: 100%;
        background: var(--primary-color-light);
        z-index: 1;
    }

    .slider-container .marker {
        position: absolute;
        width: 2px;
        height: 16px;
        background: var(--primary-color);
        top: 50%;
        transform: translate(-50%, -50%);
        z-index: 2;
    }

    .slider-container .ticks {
        position: absolute;
        width: 100%;
        height: 100%;
    }

    .slider-container .tick {
        position: absolute;
        width: 8px;
        height: 8px;
        background: var(--main-white-color-2);
        top: 50%;
        border-radius: 4px;
        transform: translate(-50%, -50%);
    }
</style>
