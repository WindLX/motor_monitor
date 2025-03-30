<!-- <script lang="ts">
  let {
    direction = "top",
    offset = 8,
  }: {
    direction: string;
    offset: number;
  } = $props();

  let show = $state(false);
  let triggerEl = $state(null);

  const arrowStyle = {
    top: () => ({ "border-bottom-color": "rgba(0,0,0,0.75)", bottom: "-10px" }),
    right: () => ({ "border-left-color": "rgba(0,0,0,0.75)", left: "-10px" }),
    bottom: () => ({ "border-top-color": "rgba(0,0,0,0.75)", top: "-10px" }),
    left: () => ({ "border-right-color": "rgba(0,0,0,0.75)", right: "-10px" }),
  }[direction];
</script>

<div class="relative inline-block">
  <div
    bind:this={triggerEl}
    on:mouseenter={() => (show = true)}
    on:mouseleave={() => (show = false)}
  >
    <slot name="trigger" />
  </div>

  {#if show && triggerEl}
    <div
      class="tooltip"
      style={`
        transform: ${["top", "bottom"].includes(direction) ? "translateX(-50%)" : "translateY(-50%)"};
        {positionStyle(triggerEl.getBoundingClientRect())}
      `}
    >
      <slot />
      <div class="arrow" style={arrowStyle()} />
    </div>
  {/if}
</div>

<style>
  .relative {
    position: relative;
  }

  .tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.75);
    color: white;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 0.875rem;
    z-index: 100;
    white-space: nowrap;
    backdrop-filter: blur(2px);
  }

  .arrow {
    position: absolute;
    width: 0;
    height: 0;
    border: 5px solid transparent;
  }
</style> -->
