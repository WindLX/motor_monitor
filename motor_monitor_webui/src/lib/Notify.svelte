<script lang="ts">
    import { onMount } from "svelte";
    import { slide } from "svelte/transition";
    import { Tween } from "svelte/motion";
    import { cubicOut } from "svelte/easing";

    import cancel from "../assets/cancel.svg";
    import { notify } from "../store/notify";
    import { NotifyLevel } from "./utils";

    let message = $state("");
    let level: NotifyLevel = $state(NotifyLevel.INFO);
    let duration = 2000; // Duration in milliseconds

    let visible = $state(false);
    let progress = new Tween(100, { duration: 0 });
    let timer = setTimeout(() => {
        close();
    }, duration);

    const close = () => {
        visible = false;
    };

    onMount(() => {
        $notify.notify = _notify;
        $notify.error = (newMessage: string, newDuration = 2000) => {
            _notify(newMessage, NotifyLevel.ERROR, newDuration);
        };
        $notify.warning = (newMessage: string, newDuration = 2000) => {
            _notify(newMessage, NotifyLevel.WARNING, newDuration);
        };
        $notify.success = (newMessage: string, newDuration = 2000) => {
            _notify(newMessage, NotifyLevel.SUCCESS, newDuration);
        };
        $notify.info = (newMessage: string, newDuration = 2000) => {
            _notify(newMessage, NotifyLevel.INFO, newDuration);
        };

        timer = setTimeout(() => {
            close();
        }, duration);

        return () => clearTimeout(timer);
    });

    const getLevelClass = () => {
        switch (level) {
            case NotifyLevel.SUCCESS:
                return "notify-success";
            case NotifyLevel.WARNING:
                return "notify-warning";
            case NotifyLevel.ERROR:
                return "notify-error";
            default:
                return "notify-info";
        }
    };

    const getLevelProgressBarClass = () => {
        switch (level) {
            case NotifyLevel.SUCCESS:
                return "notify-progress-bar-success";
            case NotifyLevel.WARNING:
                return "notify-progress-bar-warning";
            case NotifyLevel.ERROR:
                return "notify-progress-bar-error";
            default:
                return "notify-progress-bar-info";
        }
    };

    function _notify(
        newMessage: string,
        newLevel: NotifyLevel = NotifyLevel.INFO,
        newDuration = 2000,
    ) {
        message = newMessage;
        level = newLevel;
        duration = newDuration;
        visible = true;
        progress.set(100, { duration: 0 });
        progress.set(0, { duration: newDuration, easing: cubicOut });

        clearInterval(timer);
        timer = setTimeout(() => {
            close();
        }, newDuration);
    }
</script>

{#if visible}
    <div class="notify-container {getLevelClass()}" transition:slide>
        <span>{message}</span>
        <button onclick={close} aria-label="Close" class="notify-close">
            <img src={cancel} alt="Close" />
        </button>
        <div
            class="notify-progress-bar {getLevelProgressBarClass()}"
            style="width: {progress.current}%"
        ></div>
    </div>
{/if}

<style>
    .notify-container {
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
        border-bottom-left-radius: 0%;
        border-bottom-right-radius: 0%;
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

    .notify-success {
        background-color: #dff0d8;
        color: #3c763d;
    }

    .notify-warning {
        background-color: #fcf8e3;
        color: #8a6d3b;
    }

    .notify-error {
        background-color: #f2dede;
        color: #a94442;
    }

    .notify-progress-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
    }

    .notify-progress-bar-info {
        background-color: #31708f;
    }

    .notify-progress-bar-success {
        background-color: #3c763d;
    }

    .notify-progress-bar-warning {
        background-color: #8a6d3b;
    }

    .notify-progress-bar-error {
        background-color: #a94442;
    }
</style>
