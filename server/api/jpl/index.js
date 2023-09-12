const config = require('./config.json');
const axios = require('axios');

const adjustPositions = (positions) => {
    // -------swap-------
    // x, y, z = x, z, -y
    const temp = -1 * positions.y;
    positions.y = positions.z;
    positions.z = temp;

    // ------scale------
    positions.x /= 1000;
    positions.y /= 1000;
    positions.z /= 1000;

    return positions;
};

const latToRect = async (origin, destination, longitude, latitude, timeStamp) => {
    try {
        const response = await axios.get(
            `http://${ config.dataServer.ip }:${ config.dataServer.port }/lat-to-rect/${ origin }/${ destination }/${ longitude }/${ latitude }/${ timeStamp }`
        );

        return adjustPositions(response.data.positions[destination]);
    } catch (error) {
        console.log(error);
    }
};

const planetVector = async (origin, destination, timeStamp) => {
    try {
        const response = await axios.get(
            `http://${ config.dataServer.ip }:${ config.dataServer.port }/planet-vector-search/${ origin }/${ destination }/${ timeStamp }`
        );

        return adjustPositions(response.data.positions[destination]);
    } catch (error) {
        console.log(error);
    }
};

const nearestPoint = async (origin, destination, longitude, latitude, timeStamp) => {
    try {
        const response = await axios.get(
            `http://${ config.dataServer.ip }:${ config.dataServer.port }/nearest-point/${ origin }/${ destination }/${ longitude }/${ latitude }/${ timeStamp }`
        );

        return response.data;
    } catch (error) {
        console.log(error);
    }
};

const lunarLibration = async (timeStamp) => {
    try {
        const response = await axios.get(
            `http://${ config.dataServer.ip }:${ config.dataServer.port }/get-lunar-librations/${ timeStamp }`
        );

        return response.data;
    } catch (error) {
        console.log(error);
    }
};

module.exports = {
    latToRect,
    planetVector,
    nearestPoint,
    lunarLibration
};
