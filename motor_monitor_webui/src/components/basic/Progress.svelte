<script lang="ts">
  let { progress = $bindable(0) }: { progress: number } = $props();

  let saturatedProgress = $derived.by(() => {
    if (progress < 0) return 0;
    if (progress > 100) return 100;
    return progress;
  });
</script>

<div class="progress">
  <div class="progress-bar" style="width: {saturatedProgress}%"></div>
</div>

<style>
  .progress {
    width: 100%;
    height: 16px;
    border: 2px solid var(--primary-color);
    border-radius: 8px;
    margin-top: 10px;
    padding: 4px;
  }

  .progress-bar {
    height: 100%;
    background-color: var(--primary-color);
    border-radius: 4px;
    transition: width 0.5s ease;
  }
</style>
