const router = require('express').Router();
const jpl = require('jpl'); // Module to interact with Natalie's API

// Returns all positions to build our model in the client
router.get('/', async (req, res) => {
    try {
        const { latitude, longitude, timeStamp } = req.query;

        // Get the closest point on the moon relative to the given coordinates at the given time
        const nearestPoint = await jpl.nearestPoint('earth', 'moon', longitude, latitude, timeStamp);

        res.status(200).json({
            // Give success message
            status: 'Successfully retrieved positions',
            // Convert lat and lon to (x, y, z) positions at given time (relative to Earth)
            person: await jpl.latToRect('earth', 'earth', longitude, latitude, timeStamp),
            // Get Sun's position at given time (relative to Earth)
            sun: await jpl.planetVector('earth', 'sun', timeStamp),
            moon: {
                // Get Moon's position at given time (relative to Earth)
                ...(await jpl.planetVector('earth', 'moon', timeStamp)),
                // Get Moon's libration (wobble) at given time
                libration: await jpl.lunarLibration(timeStamp),
                points: { 
                    // Get positions of points of interest at given time (relative to Moon)
                    nearest: await jpl.latToRect('moon', 'moon', nearestPoint.longitude, nearestPoint.latitude, timeStamp),
                    copernicus: await jpl.latToRect('moon', 'moon', -20.08, 9.62, timeStamp),
                    tycho: await jpl.latToRect('moon', 'moon', -11.22, -43.3, timeStamp),
                    crisium: await jpl.latToRect('moon', 'moon', 59.1, 17, timeStamp)
                }
            }
        });
    } catch(error) {
        res.status(500).json({
            status: 'Failed to retrieve positions',
            error
        });
    }
});

module.exports = router;
