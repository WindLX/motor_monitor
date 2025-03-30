<script lang="ts">
  import { onMount } from "svelte";
  import { slide } from "svelte/transition";
  import { Tween } from "svelte/motion";
  import { cubicOut } from "svelte/easing";

  import { FontAwesomeIcon } from "fontawesome-svelte";

  import { notify } from "../store/notify";
  import { NotifyIcon, NotifyLevel } from "../lib/model/notify";

  import { notify as notifyConfig } from "../assets/config.json";

  let title = $state("");
  let message = $state("");
  let level: NotifyLevel = $state(NotifyLevel.INFO);
  let icon: NotifyIcon = $state(NotifyIcon.EVENT);
  let duration = notifyConfig.default_timeout; // Duration in milliseconds

  let visible = $state(false);
  let progress = new Tween(100, { duration: 0 });
  let timer = setTimeout(() => {
    close();
  }, duration);

  const close = () => {
    visible = false;
  };

  onMount(() => {
    $notify.error = (
      newMessage: string,
      option?: {
        title?: string;
        icon?: NotifyIcon;
      }
    ) => {
      _notify(
        option?.title,
        newMessage,
        option?.icon || NotifyIcon.ALERT,
        NotifyLevel.ERROR,
        notifyConfig.default_timeout
      );
    };
    $notify.warning = (
      newMessage: string,
      option?: {
        title?: string;
        icon?: NotifyIcon;
      }
    ) => {
      _notify(
        option?.title,
        newMessage,
        option?.icon || NotifyIcon.ALERT,
        NotifyLevel.WARNING,
        notifyConfig.default_timeout
      );
    };
    $notify.success = (
      newMessage: string,
      option?: {
        title?: string;
        icon?: NotifyIcon;
      }
    ) => {
      _notify(
        option?.title,
        newMessage,
        option?.icon || NotifyIcon.EVENT,
        NotifyLevel.SUCCESS,
        notifyConfig.default_timeout
      );
    };
    $notify.info = (
      newMessage: string,
      option?: {
        title?: string;
        icon?: NotifyIcon;
      }
    ) => {
      _notify(
        option?.title,
        newMessage,
        option?.icon || NotifyIcon.EVENT,
        NotifyLevel.INFO,
        notifyConfig.default_timeout
      );
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

  function _notify(
    newTitle?: string,
    newMessage: string = "",
    newIcon: NotifyIcon = NotifyIcon.EVENT,
    newLevel: NotifyLevel = NotifyLevel.INFO,
    newDuration: number = notifyConfig.default_timeout
  ) {
    if (newTitle) {
      title = newTitle;
    } else {
      title = newLevel.toUpperCase();
    }

    message = newMessage;
    level = newLevel;
    icon = newIcon;
    duration = newDuration;
    visible = true;
    progress.set(100, { duration: 0 });
    progress.set(0, { duration: newDuration, easing: cubicOut });

    clearInterval(timer);
    timer = setTimeout(() => {
      close();
    }, newDuration);
  }

  function iconConverter(icon: NotifyIcon): [string, string] {
    switch (icon) {
      case NotifyIcon.EVENT:
        return ["fas", "info"];
      case NotifyIcon.MOTOR:
        return ["fas", "gear"];
      case NotifyIcon.STATE_MACHINE:
        return ["fas", "hexagon-nodes"];
      case NotifyIcon.PLATFORM:
        return ["fas", "plane"];
      case NotifyIcon.ALERT:
        return ["fas", "exclamation"];
      case NotifyIcon.CONFIG:
        return ["fas", "wrench"];
      default:
        return ["fas", "info"];
    }
  }
</script>

{#if visible}
  <div class="notify-container {getLevelClass()}" transition:slide>
    <div class="left">
      <span class="notify-icon">
        <FontAwesomeIcon icon={iconConverter(icon)}></FontAwesomeIcon>
      </span>
    </div>

    <div class="right">
      <div class="head">
        <h3>{title}</h3>
        <button onclick={close} aria-label="Close" class="notify-close">
          <span class="notify-close-icon">
            <FontAwesomeIcon icon={["fas", "xmark"]}></FontAwesomeIcon>
          </span>
        </button>
      </div>

      <div class="body">
        <span>{message}</span>
      </div>

      <div class="notify-progress-bar" style="width: {progress.current}%"></div>
    </div>
  </div>
{/if}

<style>
  .notify-container {
    position: fixed;
    width: 250px;
    top: 1rem;
    right: 1rem;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    border-radius: 0.5rem;
    box-shadow: 0 0 8px 0 var(--main-white-color-3);
    z-index: 1000;
    transition:
      opacity 0.3s ease,
      transform 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    border-bottom-left-radius: 0%;
    border-bottom-right-radius: 0%;
  }

  .notify-container .left {
    width: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .notify-container .left .notify-icon {
    font-size: 1.2rem;
  }

  .notify-container .right {
    display: flex;
    flex-direction: column;
    width: 200px;
  }

  .notify-container .right .head {
    display: flex;
  }

  .notify-container .right .head h3 {
    font-size: 16px;
    margin: 0rem;
    margin-top: 0.5rem;
    padding: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .notify-container .right .body {
    display: flex;
    align-items: center;
  }

  .notify-container .right .body span {
    font-size: 14px;
    margin-bottom: 0.5rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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

  .notify-close:hover {
    animation: rotate 1s infinite ease;
  }

  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
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

  .notify-info .notify-progress-bar {
    background-color: var(--notify-info-color);
  }

  .notify-success .notify-progress-bar {
    background-color: var(--notify-success-color);
  }

  .notify-warning .notify-progress-bar {
    background-color: var(--notify-warning-color);
  }

  .notify-error .notify-progress-bar {
    background-color: var(--notify-error-color);
  }
</style>
