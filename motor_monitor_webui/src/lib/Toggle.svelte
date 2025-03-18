<script lang="ts">
    let {
        checked = $bindable(false),
        disabled = false,
        oninput,
    }: {
        checked: boolean;
        disabled: boolean;
        oninput: (checked: boolean) => void;
    } = $props();

    function toggle() {
        if (!disabled) {
            checked = !checked;
            oninput(checked);
        }
    }
</script>

<div
    class="toggle-container {disabled ? 'disabled' : ''}"
    onclick={toggle}
    role="checkbox"
    aria-checked={checked}
    tabindex="0"
>
    <input type="checkbox" bind:checked {disabled} />
    <div class="slider"></div>
    <slot></slot>
</div>

<style>
    .toggle-container {
        display: inline-flex;
        align-items: center;
        cursor: pointer;
    }

    .toggle-container.disabled {
        cursor: not-allowed;
        opacity: 0.5;
    }

    .toggle-container input {
        display: none;
    }

    .toggle-container .slider {
        position: relative;
        width: 50px;
        height: 25px;
        background-color: var(--main-white-color-3);
        border-radius: 25px;
        transition: background-color 0.2s;
    }

    .toggle-container .slider:before {
        content: "";
        position: absolute;
        width: 21px;
        height: 21px;
        background-color: var(--main-white-color-0);
        border-radius: 50%;
        top: 2px;
        left: 2px;
        transition: transform 0.2s;
    }

    .toggle-container input:checked + .slider {
        background-color: var(--primary-color);
    }

    .toggle-container input:checked + .slider:before {
        transform: translateX(25px);
    }
</style>
