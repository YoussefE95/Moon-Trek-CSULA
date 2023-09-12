<script setup>
import BasicMoon from '../components/BasicMoon.vue'
</script>

<template>
    <main>
        <div class="columns is-centered">
            <div class="column has-text-centered is-11">
                <h1>Moon Trek Telescope</h1>
                <h2>Apply data from Nasa JPL to your images of the Moon!</h2>
            </div>
        </div>

        <BasicMoon />

        <div class="columns is-centered">
            <div class="column has-text-centered is-8">
                <h2>How Does it Work?</h2>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-8">
                <p>
                    Moon Trek Telescope is an application that allows you to submit your own images
                    of the moon and receive useful information within the field of view, such as
                    annotations, layering, etc.
                </p>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-8">
                <p>
                    Begin by selecting your image of the moon. For best registration results
                    consider: clear, non blurry images with at least 50% of the moon.
                </p>
            </div>
        </div>
        <div class="columns is-centered">
            <div class="column is-8">
                <p>
                    Our application will attempt image registration. If the image registers
                    properly, we will be able to annotate your image. If registration fails, then
                    you will have to resubmit a better image.
                </p>
            </div>
        </div>

        <div class="columns is-centered">
            <div class="column has-text-centered">
                <router-link to="upload"> Get Started </router-link>
            </div>
        </div>
    </main>
</template>

<style scoped>
main {
    min-height: 100vh;
    padding: 1rem;
}

h1 {
    font-size: 4.5rem;
}

h2 {
    font-size: 1.75rem;
}

p,
a {
    font-size: 1.3rem;
}
</style>
