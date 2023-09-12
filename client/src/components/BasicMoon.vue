<script setup>
import { onMounted } from 'vue'
import * as THREE from 'three'

// Create threejs renderer, camera, and scene
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
const camera = new THREE.PerspectiveCamera(45, 850 / 350, 0.1, 850)
const scene = new THREE.Scene()

const moon = new THREE.Mesh(
    new THREE.SphereGeometry(1.737, 30, 30),
    new THREE.MeshPhongMaterial({
        map: new THREE.TextureLoader().load(
            'http://localhost:8888/static/assets/textures/moon-1k.jpg'
        ),
        shininess: 0
    })
)

onMounted(() => {
    // Set render size
    renderer.setSize(850, 350)

    // Append render to html element
    const canvas = document.getElementById('moon-canvas')
    canvas.appendChild(renderer.domElement)

    // Set camera position
    camera.position.set(0, 0, 5)

    // Create light and adjust it's position
    const light = new THREE.DirectionalLight(0xffffff, 3.5, 200)
    light.position.set(-30, 0, 30)

    // Add light and Moon to scene
    scene.add(light)
    scene.add(moon)

    // Pass a function to renderer which will be called every frame
    renderer.setAnimationLoop(() => {
        // Rotate the Moon a little
        moon.rotation.y += 0.001

        // Render the new frame
        renderer.render(scene, camera)
    })
})
</script>

<template>
    <div class="columns is-centered">
        <div id="moon-canvas"></div>
    </div>
</template>

<style scoped>
#moon-canvas {
    z-index: 7;
    margin: -1.15rem 1rem;
}
</style>
