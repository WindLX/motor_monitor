<script lang="ts">
  // components
  import Status from "./Status.svelte";
  import State from "./CurrentState.svelte";
  import Sidebar from "./Sidebar.svelte";
  import Operation from "./Operation.svelte";
  import Notify from "./Notify.svelte";

  let notify: Notify;
</script>

<div class="container">
  <Notify bind:this={notify} />

  <header class="header">
    <Status />
  </header>

  <div class="content">
    <aside class="sidebar">
      <Sidebar />
    </aside>

    <main class="main">
      <Operation />
      <State />
    </main>
  </div>

  <footer class="footer"></footer>
</div>

<style>
  .container {
    display: flex;
    flex-direction: column;
    height: 100vh;
  }

  .header,
  .footer {
    background-color: var(--main-bg);
    text-align: center;
    border-radius: 5px;
    margin: 10px;
  }

  .content {
    display: flex;
    flex: 1;
    gap: 10px;
  }

  .sidebar {
    width: 200px;
    border-radius: 5px;
    border: 1px solid green;
  }

  .main {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid red;
  }
</style>
