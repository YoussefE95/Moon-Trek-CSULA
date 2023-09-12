<script setup>
import axios from 'axios'
import ExifReader from 'exifreader'
import { useRouter } from 'vue-router'
import { reactive } from 'vue'
import { data } from '../data.js'

const router = useRouter()
const imageData = reactive({
    name: 'Select Image',
    previewImage: new Image(),
    hasExif: true,
    longitude: 0,
    latitude: 0,
    date: '',
    time: ''
})

// This is called whenever a new image is selected
const imageSelected = async () => {
    try {
        // Get the image from input
        const file = document.getElementById('moonImage').files[0]
        // Read the exif meta data
        const tags = await ExifReader.load(file)

        // Update the input text to the selected image's name
        imageData.name = file.name
        // Update the preview to the selected image
        imageData.previewImage.src = URL.createObjectURL(
            document.getElementById('moonImage').files[0]
        )

        // Check if the meta data we want is present
        if (tags.GPSLongitude && tags.GPSLatitude && tags.DateTimeOriginal) {
            // If so, keep imageData.hasExif true
            imageData.hasExif = true
            // Set the date
            imageData.date = tags.DateTimeOriginal.description

            // Keep all North latitude values positive
            // and make South latitude values negative
            if (tags.GPSLatitudeRef.value[0] === 'N') {
                imageData.latitude = tags.GPSLatitude.description
            } else {
                imageData.latitude = -1 * tags.GPSLatitude.description
            }

            // Keep all East longitude values positive
            // and make West longitude values negative
            if (tags.GPSLongitudeRef.value[0] === 'E') {
                imageData.longitude = tags.GPSLongitude.description
            } else {
                imageData.longitude = -1 * tags.GPSLongitude.description
            }
        } else {
            // If no meta data, reset all values and display the form
            imageData.hasExif = false
            imageData.longitude = 0
            imageData.latitude = 0
            imageData.date = ''
            imageData.time = ''
        }
    } catch (error) {
        console.log(error)
    }
}

// This is called whenever an image is submitted
const imageSubmitted = async () => {
    let local

    // Date is read differently from exif meta data and html inputs
    // so we'll adjust our string based on the case
    if (imageData.hasExif) {
        const splt = imageData.date.split(/\D/g)
        local = `${splt[0]}-${splt[1]}-${splt[2]}T${splt[3]}:${splt[4]}:${splt[5]}`
    } else {
        local = `${imageData.date}T${imageData.time}:00`
    }

    // Convert the local time stamp to UTC
    const convert = await axios.get('http://localhost:8888/timezone/toUtc', {
        params: {
            latitude: imageData.latitude,
            longitude: imageData.longitude,
            timeStamp: local
        }
    })

    console.log(`\nCoordinates: ${imageData.latitude}, ${imageData.longitude}`)
    console.log(`Local Date: ${local}`)
    console.log(`UTC Date: ${convert.data.timeStampUTC}`)

    // Set data.newUpload so ModelGenerator knows registration needs to be performed
    data.newUpload = true

    // Store all submitted data
    data.latitude = imageData.latitude
    data.longitude = imageData.longitude
    data.timeStamp = convert.data.timeStampUTC
    data.images.user = imageData.previewImage

    // Forward to registration page
    router.push('/registration')
}
</script>

<template>
    <main>
        <div class="columns is-centered">
            <div class="column has-text-centered">
                <h1>Upload Your Moon Image</h1>
            </div>
        </div>
        <form @submit.prevent="imageSubmitted">
            <div class="field file has-addons has-addons-centered">
                <label class="file-label">
                    <div class="control">
                        <input
                            class="file-input"
                            type="file"
                            id="moonImage"
                            @change="imageSelected"
                        />
                        <span class="file-cta">
                            <span class="file-icon">
                                <i class="fas fa-upload"></i>
                            </span>
                            <span class="file-label">
                                {{ imageData.name }}
                            </span>
                        </span>
                    </div>
                </label>
                <div class="control">
                    <input class="button" type="submit" value="Upload" />
                </div>
            </div>
            <div v-if="!imageData.hasExif" class="columns is-centered">
                <div class="column is-3-tablet is-2-desktop is-2-fullhd">
                    <div class="field">
                        <label class="label">Latitude:</label>
                        <div class="control">
                            <input
                                class="input"
                                type="number"
                                placeholder="latitude"
                                v-model="imageData.latitude"
                            />
                        </div>
                    </div>
                </div>
                <div class="column is-3-tablet is-2-desktop is-2-fullhd">
                    <div class="field">
                        <label class="label">Longitude:</label>
                        <div class="control">
                            <input
                                class="input"
                                type="number"
                                placeholder="longitude"
                                v-model="imageData.longitude"
                            />
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="!imageData.hasExif" class="columns is-centered">
                <div class="column is-3-tablet is-2-desktop is-2-fullhd">
                    <div class="field">
                        <label class="label">Date:</label>
                        <div class="control">
                            <input class="input" type="date" v-model="imageData.date" />
                        </div>
                    </div>
                </div>
                <div class="column is-3-tablet is-2-desktop is-2-fullhd">
                    <div class="field">
                        <label class="label">Time:</label>
                        <div class="control">
                            <input class="input" type="time" v-model="imageData.time" />
                        </div>
                    </div>
                </div>
            </div>
        </form>

        <div class="columns is-centered">
            <div class="column has-text-centered">
                <img :src="imageData.previewImage.src" />
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
    font-size: 1.5rem;
}

img {
    margin: 1rem;
    max-width: 50%;
    max-height: 50%;
}

::placeholder,
file-cta,
label,
input {
    color: #d8dee9;
}

.file-cta {
    border-radius: 0.5rem 0rem 0rem 0.5rem;
}

input {
    border-radius: 0.5rem;
}

.file-cta,
.file-cta:hover,
input,
input:hover {
    background: #13161c;
}

.file-cta,
input {
    border-color: #5e81ac;
}

.file-cta:hover,
input:hover {
    border-color: #b48ead;
}

.button,
.button:hover {
    border-radius: 0rem 0.5rem 0.5rem 0rem;
}

.button {
    background: #5e81ac;
    border-color: #5e81ac;
    color: #13161c;
}

.button:hover {
    background: #b48ead;
    border-color: #b48ead;
}
</style>
