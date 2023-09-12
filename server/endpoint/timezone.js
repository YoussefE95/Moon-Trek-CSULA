const router = require('express').Router();
const { find } = require('geo-tz'); // Module which gives timezone based on lat and lon
const { ZonedDateTime, ZoneId } = require('@js-joda/core'); // DateTime object with timezone
require('@js-joda/timezone');

// Accepts a ZonedDateTime and returns a formatted string
//      YYYY-MM-DDTHH:MM:SS
const formatTimeStamp = (timeStampObject) => {
    const timeStampValues = [
        timeStampObject.year(),
        timeStampObject.monthValue(),
        timeStampObject.dayOfMonth(),
        timeStampObject.hour(),
        timeStampObject.minute(),
        timeStampObject.second(),
    ];

    for (let i = 0; i < timeStampValues.length; i++) {
        timeStampValues[i] = timeStampValues[i].toLocaleString('en-US', {
            minimumIntegerDigits: 2,
            useGrouping: false
        })
    }

    return `${timeStampValues[0]}-${timeStampValues[1]}-${timeStampValues[2]}T${timeStampValues[3]}:${timeStampValues[4]}:${timeStampValues[5]}`
};

// Converts a local time to UTC
router.get('/toUTC', async (req, res) => {
    try {
        const { latitude, longitude, timeStamp } = req.query;

        // Split timeStamp string on all non-digit characters
        // YYYY-MM-DDTHH:MM:SS -> [YYYY, MM, DD, HH, MM, SS]
        // 2023-08-25T04:20:00 -> [2023, 08, 25, 4, 20, 0]
        const splitStamp = timeStamp.split(/\D/);

        // Build ZonedDateTime with info from split timeStamp
        const localStamp = new ZonedDateTime.of(
            splitStamp[0], // year
            splitStamp[1], // month
            splitStamp[2], // day
            splitStamp[3], // hour
            splitStamp[4], // minute
            splitStamp[5], // second
            0,             // millisecond
            ZoneId.of(find(latitude, longitude)[0])
        );

        // Convert to UTC
        const timeStampUTC = localStamp.withZoneSameInstant(ZoneId.of('UTC'));

        // Return formatted UTC time stamp string
        res.status(200).json({
            status: 'Converted Successfully',
            timeStampUTC: formatTimeStamp(timeStampUTC)
        });
    } catch (error) {
        res.status(500).json({
            status: 'Failed to convert',
            error
        });
    }
});

module.exports = router;
