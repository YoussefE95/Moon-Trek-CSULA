<script setup>
import { ref } from 'vue'
let active = ref(false)
</script>

<template>
    <nav class="navbar" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a
                role="button"
                class="navbar-burger"
                :class="active ? 'is-active' : ''"
                @click="active = !active"
                data-target="nav"
                aria-label="menu"
                aria-expanded="false"
            >
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
                <span aria-hidden="true"></span>
            </a>
        </div>

        <div id="nav" class="navbar-menu" :class="active ? 'is-active' : ''">
            <div class="navbar-start">
                <router-link to="/" class="nav-link"> Home </router-link>
                <router-link to="upload" class="nav-link"> Upload </router-link>
                <router-link to="registration" class="nav-link"> Registration </router-link>
                <router-link to="model" class="nav-link"> Model </router-link>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.nav-link {
    font-size: 1.25rem;
    margin: 0.25rem 0.5rem;
}
</style>
