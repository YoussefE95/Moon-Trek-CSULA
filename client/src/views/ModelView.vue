<script setup>
import { data } from '../data.js'
import ModelGenerator from '../components/ModelGenerator.vue'
</script>

<template>
    <main>
        <div v-if="data.timeStamp !== ''">
            <ModelGenerator mode="animate" />
        </div>
    </main>
</template>

<style scoped>
main {
    min-height: 100vh;
    padding: 1rem;
}
</style>
