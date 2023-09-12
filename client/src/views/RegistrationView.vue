<script setup>
import ModelGenerator from '../components/ModelGenerator.vue'
import { ref } from 'vue'
import { data } from '../data.js'

let algorithm = ref('SURF')

// Returns the URL to the given processed image type
const getUrl = (type) => {
    if (type === 'resized') {
        return `http://localhost:8888/static/processed/${type}-${data.relativeImageName}`
    } else {
        return `http://localhost:8888/static/processed/${type}-${algorithm.value}-${data.relativeImageName}`
    }
}
</script>

<template>
    <main>
        <!-- data.newUpload is only set to true when the user uploads a new image -->
        <!-- and is set to false when ModelGenerator in "registrate" mode finishes -->
        <ModelGenerator mode="registrate" v-if="data.newUpload" />
        <div v-else-if="data.relativeImageName !== ''">
            <div class="columns is-centered">
                <div class="column has-text-centered is-5">
                    <div class="select">
                        <select v-model="algorithm">
                            <option value="SURF">SURF</option>
                            <option value="SIFT">SIFT</option>
                            <option value="ORB">ORB</option>
                            <option value="AKAZE">AKAZE</option>
                            <option value="BRISK">BRISK</option>
                        </select>
                    </div>
                </div>
            </div>
            <div class="columns is-centered">
                <div class="column has-text-centered is-5">
                    <img :src="data.images.user.src" />
                </div>
                <div class="column has-text-centered is-5">
                    <img :src="getUrl('resized')" />
                </div>
            </div>
            <div class="columns is-centered">
                <div class="column has-text-centered is-5">
                    <img :src="data.images.model.src" />
                </div>
                <div class="column has-text-centered is-5">
                    <img :src="data.images.layer.src" />
                </div>
            </div>
            <div class="columns is-centered">
                <div class="column has-text-centered is-10">
                    <img :src="getUrl('registration')" />
                </div>
            </div>
            <div class="columns is-centered">
                <div class="column has-text-centered is-5">
                    <img :src="getUrl('transformed')" />
                </div>
                <div class="column has-text-centered is-5">
                    <img :src="getUrl('layered')" />
                </div>
            </div>
            <div class="columns is-centered">
                <div class="column has-text-centered is-3">
                    <img :src="getUrl('green')" />
                </div>
                <div class="column has-text-centered is-3">
                    <img :src="getUrl('red')" />
                </div>
                <div class="column has-text-centered is-3">
                    <img :src="getUrl('stacked')" />
                </div>
            </div>
        </div>
    </main>
</template>

<style scoped>
main {
    min-height: 100vh;
    padding: 1rem;
}
</style>
