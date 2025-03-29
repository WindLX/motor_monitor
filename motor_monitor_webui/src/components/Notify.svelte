<script lang="ts">
    import { onMount } from "svelte";
    import { slide } from "svelte/transition";
    import { Tween } from "svelte/motion";
    import { cubicOut } from "svelte/easing";

    import { FontAwesomeIcon } from "fontawesome-svelte";
    import { notify } from "../store/notify";
    import { NotifyLevel } from "../lib/utils";

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
            <span class="notify-close-icon">
                <FontAwesomeIcon icon={["fas", "xmark"]}></FontAwesomeIcon>
            </span>
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
        min-width: 200px;
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
        width: fit-content;
    }

    .notify-info {
        background-color: var(--notify-info-bg);
        color: var(--notify-info-color);
    }

    .notify-success {
        background-color: var(--notify-success-bg);
        color: var(--notify-success-color);
    }

    .notify-warning {
        background-color: var(--notify-warning-bg);
        color: var(--notify-warning-color);
    }

    .notify-error {
        background-color: var(--notify-error-bg);
        color: var(--notify-error-color);
    }

    .notify-info .notify-close-icon {
        color: var(--notify-info-color);
    }

    .notify-success .notify-close-icon {
        color: var(--notify-success-color);
    }

    .notify-warning .notify-close-icon {
        color: var(--notify-warning-color);
    }

    .notify-error .notify-close-icon {
        color: var(--notify-error-color);
    }

    .notify-progress-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 3px;
    }

    .notify-progress-bar-info {
        background-color: var(--notify-info-color);
    }

    .notify-progress-bar-success {
        background-color: var(--notify-success-color);
    }

    .notify-progress-bar-warning {
        background-color: var(--notify-warning-color);
    }

    .notify-progress-bar-error {
        background-color: var(--notify-error-color);
    }
</style>
