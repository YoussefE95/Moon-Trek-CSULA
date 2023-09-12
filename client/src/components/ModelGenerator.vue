<script setup>
import { ref, reactive, onMounted } from 'vue'
import { data } from '../data.js'
import axios from 'axios'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { ZonedDateTime, ZoneId } from '@js-joda/core'
import '@js-joda/timezone'
import EarthMoonAnimation from '../assets/EarthMoonAnimation.json'
import { Vue3Lottie } from 'vue3-lottie'

// Mode will be used to decide if we want our model to create images and perform registration
// or if we want it to render to the page for the user to interact with
const props = defineProps(['mode'])

// Processing will be used to display the loading animation gif
let processing = ref(true)

// Split timeStamp string on all non-digit characters
// YYYY-MM-DDTHH:MM:SS -> [YYYY, MM, DD, HH, MM, SS]
// 2023-08-25T04:20:00 -> [2023, 08, 25, 4, 20, 0]
const splitDate = data.timeStamp.split(/\D/)

const modelData = reactive({
    anchor: 'moon',
    texture: 'real',
    light: 'real',
    time: {
        stamp: new ZonedDateTime.of(
            splitDate[0], // year
            splitDate[1], // month
            splitDate[2], // day
            splitDate[3], // hour
            splitDate[4], // minute
            splitDate[5], // second
            0, // nanosecond
            ZoneId.of('UTC')
        ),
        increment: 1,
        multiplier: 1
    },
    positions: {},
    intervalId: -1
})

// Create all of our threejs objects
const scene = new THREE.Scene()
const camera = new THREE.PerspectiveCamera(45, 2000 / 2000, 1, 100000000)
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    preserveDrawingBuffer: true
})
const light = new THREE.DirectionalLight(0xffffff, 2.5, 1000000)
const ambientLight = new THREE.AmbientLight(0x404040, 5)
const earth = new THREE.Mesh(
    new THREE.SphereGeometry(6.371, 30, 30),
    new THREE.MeshPhongMaterial({
        map: new THREE.TextureLoader().load(
            'http://localhost:8888/static/assets/textures/earth.jpg'
        ),
        shininess: 0
    })
)
const moon = new THREE.Mesh(
    new THREE.SphereGeometry(1.737, 30, 30),
    new THREE.MeshPhongMaterial({
        map: new THREE.TextureLoader().load(
            'http://localhost:8888/static/assets/textures/moon-2k.jpg'
        ),
        shininess: 0
    })
)
const moonLayer = new THREE.Mesh(
    new THREE.SphereGeometry(1.737, 30, 30),
    new THREE.MeshBasicMaterial({
        map: new THREE.TextureLoader().load(
            'http://localhost:8888/static/assets/textures/overlay.png'
        )
    })
)
const person = new THREE.Mesh(
    new THREE.SphereGeometry(0.05),
    new THREE.MeshBasicMaterial({
        color: 0xe62117
    })
)
const nearestPoint = new THREE.Mesh(
    new THREE.SphereGeometry(0.03),
    new THREE.MeshBasicMaterial({
        color: 0xe62117
    })
)
const copernicusPoint = new THREE.Mesh(
    new THREE.SphereGeometry(0.03),
    new THREE.MeshBasicMaterial({
        color: 0x00ff00
    })
)
const tychoPoint = new THREE.Mesh(
    new THREE.SphereGeometry(0.03),
    new THREE.MeshBasicMaterial({
        color: 0xff8800
    })
)
const crisiumPoint = new THREE.Mesh(
    new THREE.SphereGeometry(0.03),
    new THREE.MeshBasicMaterial({
        color: 0x00ffcc
    })
)

// Formats ZonedDateTime object to date string
const formattedDate = () => {
    const year = modelData.time.stamp.year()
    const month = modelData.time.stamp.monthValue()
    const day = modelData.time.stamp.dayOfMonth()
    const hour = modelData.time.stamp.hour()
    const minute = modelData.time.stamp.minute()
    const second = modelData.time.stamp.second()

    return `${year}-${month}-${day}T${hour}:${minute}:${second}`
}

// Updates positions
const getPositions = async () => {
    const positionSearch = await axios.get('http://localhost:8888/positions', {
        params: {
            latitude: data.latitude,
            longitude: data.longitude,
            timeStamp: formattedDate()
        }
    })

    modelData.positions = positionSearch.data
}

// Sets positions for all threejs objects
const setPositions = () => {
    light.position.set(
        modelData.positions.sun.x,
        modelData.positions.sun.y,
        modelData.positions.sun.z
    )

    if (modelData.anchor === 'moon') {
        camera.position.set(
            camera.position.x + (modelData.positions.moon.x - moon.position.x),
            camera.position.y + (modelData.positions.moon.y - moon.position.y),
            camera.position.z + (modelData.positions.moon.z - moon.position.z)
        )
    }

    moon.position.set(
        modelData.positions.moon.x,
        modelData.positions.moon.y,
        modelData.positions.moon.z
    )
    moonLayer.position.set(
        modelData.positions.moon.x,
        modelData.positions.moon.y,
        modelData.positions.moon.z
    )
    person.position.set(
        modelData.positions.person.x,
        modelData.positions.person.y,
        modelData.positions.person.z
    )
    nearestPoint.position.set(
        modelData.positions.moon.points.nearest.x,
        modelData.positions.moon.points.nearest.y,
        modelData.positions.moon.points.nearest.z
    )
    copernicusPoint.position.set(
        modelData.positions.moon.points.copernicus.x,
        modelData.positions.moon.points.copernicus.y,
        modelData.positions.moon.points.copernicus.z
    )
    tychoPoint.position.set(
        modelData.positions.moon.points.tycho.x,
        modelData.positions.moon.points.tycho.y,
        modelData.positions.moon.points.tycho.z
    )
    crisiumPoint.position.set(
        modelData.positions.moon.points.crisium.x,
        modelData.positions.moon.points.crisium.y,
        modelData.positions.moon.points.crisium.z
    )

    // Makes blue axis face the earth.
    moon.lookAt(0, 0, 0) // assuming earth center is (0, 0, 0)
    // Rotate to point red axis to earth's center
    moon.rotateOnAxis(new THREE.Vector3(0, 1, 0), (-90 * Math.PI) / 180)
    // Next - get the "Wobble" by using lunar librations call from API.
    // First we rotate by negative "longitude" about the moon's y axis.
    moon.rotateOnAxis(
        new THREE.Vector3(0, 1, 0),
        (-modelData.positions.moon.libration.lon * Math.PI) / 180
    )
    // Finally we rotate by negate "latitude" about the moon's Z axis
    moon.rotateOnAxis(
        new THREE.Vector3(0, 0, 1),
        (-modelData.positions.moon.libration.lat * Math.PI) / 180
    )

    moonLayer.lookAt(0, 0, 0) // assuming earth center is (0, 0, 0)
    moonLayer.rotateOnAxis(new THREE.Vector3(0, 1, 0), (-90 * Math.PI) / 180)
    moonLayer.rotateOnAxis(
        new THREE.Vector3(0, 1, 0),
        (-modelData.positions.moon.libration.lon * Math.PI) / 180
    )
    moonLayer.rotateOnAxis(
        new THREE.Vector3(0, 0, 1),
        (-modelData.positions.moon.libration.lat * Math.PI) / 180
    )
}

// Converts Image Objects to File Objects
// Used when submitting for registration
const toFile = async (imageSrc, imageFileName, mimeType) => {
    const image = await fetch(imageSrc)
    const buffer = await image.arrayBuffer()

    return await new File([buffer], imageFileName, { type: mimeType })
}

// Updates the orbit control position
// Only called in "animate" mode
const setOrbit = (orbit) => {
    const newFocusPosition = {}

    if (modelData.anchor === 'earth') {
        newFocusPosition.x = 0
        newFocusPosition.y = 0
        newFocusPosition.z = 0
    } else {
        newFocusPosition.x = modelData.positions.moon.x
        newFocusPosition.y = modelData.positions.moon.y
        newFocusPosition.z = modelData.positions.moon.z
    }

    const newWorldBox = new THREE.Box3().setFromCenterAndSize(
        new THREE.Vector3(newFocusPosition.x, newFocusPosition.y, newFocusPosition.z),
        new THREE.Vector3(0.1, 0.1, 0.1)
    )
    newWorldBox.getCenter(orbit.target)
    orbit.update()
}

// Changes camera anchor between Earth and Moon
// Only visible in "animate" mode
const toggleAnchor = () => {
    modelData.anchor = modelData.anchor === 'earth' ? 'moon' : 'earth'
}

// Changes between real and ambient lighting
// Only visible in "animate" mode
const toggleLight = () => {
    if (modelData.light === 'real') {
        scene.remove(light)
        scene.add(ambientLight)
        modelData.light = 'ambient'
    } else {
        scene.remove(ambientLight)
        scene.add(light)
        modelData.light = 'real'
    }
}

// Changes between real and layer texture on Moon
// Only visible in "animate" mode
const toggleTexture = () => {
    if (modelData.texture === 'real') {
        scene.remove(moon)
        scene.add(moonLayer)
        modelData.texture = 'layer'
    } else {
        scene.remove(moonLayer)
        scene.add(moon)
        modelData.texture = 'real'
    }
}

// Toggles time pass
// Only visible in "animate" mode
const togglePlay = () => {
    if (modelData.intervalId === -1) {
        // If time is passing, fetch and set positions every second
        modelData.intervalId = setInterval(async () => {
            await getPositions()
            setPositions()
            modelData.time.stamp = modelData.time.stamp.plusHours(
                modelData.time.increment * modelData.time.multiplier
            )
        }, 1000)
    } else {
        clearInterval(modelData.intervalId)
        modelData.intervalId = -1
    }
}

onMounted(async () => {
    // These objects will be added to scene despite the given mode
    scene.add(light)
    scene.add(moon)
    scene.add(earth)
    earth.add(person)
    moonLayer.add(nearestPoint)
    moonLayer.add(copernicusPoint)
    moonLayer.add(tychoPoint)
    moonLayer.add(crisiumPoint)

    // Their positions will be fetched and set at least once
    await getPositions()
    setPositions()

    // The camera is set to the person's position
    camera.position.set(
        modelData.positions.person.x,
        modelData.positions.person.y,
        modelData.positions.person.z
    )

    if (props.mode === 'registrate') {
        // Set the renderer to 2000x2000
        renderer.setSize(2000, 2000)

        // Adjust zoom to match what a telescope would do
        camera.zoom = 85

        // Look at the Moon
        camera.lookAt(moon.position)
        camera.updateProjectionMatrix()

        // Render one frame
        renderer.render(scene, camera)
        // Take a snapshot (model) and save
        data.images.model.src = renderer.domElement.toDataURL()

        // Remove Moon and real lighting
        scene.remove(moon)
        scene.remove(light)

        // Added Moon layer with points of interest
        scene.add(moonLayer)
        moonLayer.add(ambientLight)

        // Adjust zoom a little more
        camera.zoom = 86.75
        camera.updateProjectionMatrix()

        // Render another frame
        renderer.render(scene, camera)
        // Take a snapshot (layer) and save
        data.images.layer.src = renderer.domElement.toDataURL()

        // Append user, model, and layer images to Form Data object
        const formData = new FormData()
        formData.append('images', await toFile(data.images.user.src, 'userImage', 'image/png'))
        formData.append('images', await toFile(data.images.model.src, 'modelImage', 'image/png'))
        formData.append('images', await toFile(data.images.layer.src, 'layerImage', 'image/png'))

        // Send all to registration endpoint
        const response = await axios.post('http://localhost:8888/registration/performAll', formData)
        const { status, relativeImageName } = response.data

        console.log(status, relativeImageName)
        data.relativeImageName = relativeImageName

        // Hide loading animation gif
        processing.value = false
        data.newUpload = false
    } else if (props.mode === 'animate') {
        // Hide loading animation gif
        processing.value = false

        // Set camera zoom to default
        camera.zoom = 1
        camera.updateProjectionMatrix()

        // Append renderer to html element
        const canvas = document.getElementById('moon-canvas')
        canvas.appendChild(renderer.domElement)

        // Add orbit controls
        const orbit = new OrbitControls(camera, renderer.domElement)

        // Begin animation loop
        renderer.setAnimationLoop(async () => {
            // Get window dimensions
            const width = window.innerWidth * 0.97
            const height = window.innerHeight * 0.75

            // Set renderer to window dimensions
            renderer.setSize(width, height)
            camera.aspect = width / height
            camera.updateProjectionMatrix()

            // Update orbit anchor
            setOrbit(orbit)

            // Render new frame
            renderer.render(scene, camera)
        })
    }
})
</script>

<template>
    <div v-if="processing">
        <Vue3Lottie :animationData="EarthMoonAnimation" :height="400" :width="400" />
    </div>
    <div v-else>
        <div class="columns is-centered">
            <div class="column has-text-centered">
                <button class="button" @click="toggleAnchor()">
                    Anchor {{ modelData.anchor === 'earth' ? 'Moon' : 'Earth' }}
                </button>
                <button class="button" @click="toggleLight()">
                    Set {{ modelData.light === 'real' ? 'Ambient' : 'Real' }} Lighting
                </button>
                <button class="button" @click="toggleTexture()">
                    Set {{ modelData.texture === 'real' ? 'Layer' : 'Real' }} Texture
                </button>
            </div>
        </div>
        <div class="columns is-centered is-vcentered">
            <div class="column has-text-centered is-1">
                <button
                    class="button"
                    :class="modelData.intervalId === -1 ? 'play' : 'pause'"
                    @click="togglePlay()"
                >
                    {{ modelData.intervalId === -1 ? 'Play' : 'Pause' }}
                </button>
            </div>
            <div class="column has-text-centered is-1">
                <input class="input" type="number" v-model="modelData.time.increment" />
            </div>
            <div class="column has-text-centered is-1">
                <select class="input" v-model="modelData.time.multiplier">
                    <option value="1">Hours</option>
                    <option value="24">Days</option>
                </select>
            </div>
        </div>
        <div class="columns is-centered is-vcentered">
            <div class="column has-text-centered is-2">
                <p>
                    {{ formattedDate() }}
                </p>
            </div>
        </div>
    </div>

    <div id="moon-canvas"></div>
</template>

<style scoped>
.input {
    margin: -1rem 0.25rem;
}

p {
    font-size: 1.25rem;
    margin-top: -0.5rem;
    margin-bottom: -1rem;
}

button {
    margin: -1rem 0.25rem;
    background: #5e81ac;
    border: #5e81ac;
}

button:hover {
    background: #b48ead;
    border: #b48ead;
}

.play {
    background: #a3be8c;
    border: #a3be8c;
}

.pause {
    background: #bf616a;
    border: #bf616a;
}

#moon-canvas {
    margin-top: 2rem;
}
</style>
