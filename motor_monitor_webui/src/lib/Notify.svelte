<script lang="ts">
    import { onMount } from "svelte";
    import { writable } from "svelte/store";

    export let message = "";
    export let level = "info"; // 'info', 'warning', 'error'
    export let duration = 2000; // Duration in milliseconds

    let visible = writable(false);

    const close = () => {
        visible.set(false);
    };

    onMount(() => {
        const timer = setTimeout(() => {
            close();
        }, duration);

        return () => clearTimeout(timer);
    });

    const getLevelClass = () => {
        switch (level) {
            case "warning":
                return "notify-warning";
            case "error":
                return "notify-error";
            default:
                return "notify-info";
        }
    };

    export function notify(
        newMessage: string,
        newLevel = "info",
        newDuration = 2000,
    ) {
        message = newMessage;
        level = newLevel;
        duration = newDuration;
        visible.set(true);

        setTimeout(() => {
            close();
        }, newDuration);
    }
</script>

<div class="notify {getLevelClass()} {$visible ? '' : 'notify-hidden'}">
    <span>{message}</span>
    <button on:click={close} aria-label="Close" class="notify-close">
        <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            width="16"
            height="16"
        >
            <path d="M0 0h24v24H0z" fill="none" />
            <path
                d="M18 6L6 18M6 6l12 12"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
            />
        </svg>
    </button>
</div>

<style>
    .notify {
        position: fixed;
        top: 1rem;
        right: 1rem;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        transition:
            opacity 0.3s ease,
            transform 0.3s ease;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .notify-close {
        background-color: transparent;
        border: none;
        cursor: pointer;
        padding: 0;
        margin-left: auto;
        outline: none;
    }

    .notify-info {
        background-color: #d9edf7;
        color: #31708f;
    }

    .notify-warning {
        background-color: #fcf8e3;
        color: #8a6d3b;
    }

    .notify-error {
        background-color: #f2dede;
        color: #a94442;
    }

    .notify-hidden {
        opacity: 0;
        transform: translateY(-1rem);
    }
</style>
