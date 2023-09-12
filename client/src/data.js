import { reactive } from 'vue'

export const data = reactive({
    newUpload: false,
    longitude: 0,
    latitude: 0,
    timeStamp: '',
    relativeImageName: '',
    images: {
        user: new Image(),
        model: new Image(),
        layer: new Image()
    }
})
