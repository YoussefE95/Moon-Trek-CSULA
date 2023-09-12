<script setup>
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
</script>

<template>
    <NavBar />
    <RouterView />
</template>

<style>
* {
    font-family: Nunito;
    color: #d8dee9;
    background: #13161c;
}

a {
    color: #5e81ac;
}

a:hover {
    color: #b48ead;
}
</style>
