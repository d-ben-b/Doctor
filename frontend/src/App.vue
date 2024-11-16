<!-- @format -->

<template>
  <div id="app">
    <!-- Navbar 放在全局 -->
    <Navbar v-if="$route.name !== 'Login'" />
    <!-- 單一 router-view -->
    <router-view />
  </div>
</template>

<script>
  import Navbar from "@/components/Navbar.vue";

  export default {
    name: "App",
    components: {
      Navbar,
    },
  };
</script>

<style>
  #app {
    font-family: Arial, sans-serif;
  }
</style>
