const router = require('express').Router();
const multer = require('multer'); // Module to save files
const { spawn } = require('child_process'); // Module to execute terminal commands

// Set up Multer middleware
// All uploaded files are stored in static/uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'static/uploads');
    },
    filename: (req, file, cb) => {
        // Add current date as prefix to file name to prevent duplicate file names
        const fileExtension = file.mimetype.split('/')[1];
        cb(null, `${Date.now()}--${file.originalname.replace(/\s/g, '')}.${fileExtension}`);
    }
});
const upload = multer({
    storage: storage,
});

// Calls python script which performs all five registration algorithms on uploaded images
// The python script outputs all files to static/processed
router.post('/performAll', upload.array('images'), async (req, res) => {
    try {
        const images = req.files;

        // Call python script in anaconda environment like we would through the command line
        const spawnedProcess = spawn(
            `conda run -n MoonTrek python registration.py ${images[0].filename} ${images[1].filename} ${images[2].filename}`,
            { shell: true }
        );

        // Once the script is done, we respond with the new name we gave the file when saving
        // This allows the client to call this endpoint with files and have a reference to
        // what was output in static/processed
        spawnedProcess.on('exit', () => {
            res.status(200).json({
                status: 'Success',
                relativeImageName: images[0].filename,
            });
        });
    } catch (error) {
        res.status(500).json({
            status: 'Failed to perform registration'
        });
    }
});

module.exports = router;