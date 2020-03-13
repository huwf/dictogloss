import axios from 'axios';
// import Vue from 'vue';
// import VueFlashMessage from 'vue-flash-message';
// import 'vue-flash-message/dist/vue-flash-message.min.css';

// const vm = new Vue();
const baseURL = 'http://172.17.0.1:5000';

// const handleError = fn => (...params) =>
//     fn(...params).catch(error => {
//         console.log(error);
//         vm.flash(`${error.response.status}`);
//     });

export const api = {
    getLanguages: async () => {
        const res = await axios.get(baseURL + '/info/languages/speech');
        console.log('res: ', res.data.data);
        return res.data.data;
    },
    getFile: async id => {
        const res = await axios.get(baseURL + '/file/' + id);
        console.debug('getFile res', res.data.data);
        return res.data.data;
    },
    getSegment: async (fileId, position) => {
        console.debug('API: getSegment fileId, position', fileId, position);
        const res = await axios.get(baseURL + `/segment?file_id=${fileId}&position=${position}`);
        console.debug('getSegment res.data: ', res.data);
        return res.data;
    },
    getDownloads: async () => {
        const res = await axios.get(baseURL + '/file/downloads');
        console.log('res.data', res.data);
        return res.data;
    },
    getAudioSrc: async (segmentId, fileId, position) => {
        console.log('getAudioSrc', segmentId, fileId, position);
        let res;
        if(segmentId) {
            console.debug('API: getAudioSrc segmentId', segmentId);
            res = await axios.get(baseURL + `/segment?id=${segmentId}&fields=url`);
        }
        else if (fileId && position) {
            console.debug('API: getAudioSrc fileId, position', fileId, position);
            res = await axios.get(baseURL + `/segment?file_id=${fileId}&position=${position}&fields=url`);
        }
        else {
            console.debug('API: getAudioSrc fileId only', fileId);
            res = await axios.get(baseURL + `/file/id?fields=${fileId}`);
        }

        console.debug('getAudioSrc res.data', res.data);
        return res.data;
    },
    getTranscript: async id => {
        console.debug('getTranscript id', id);
        const res = await axios.get(baseURL + `/segment/${id}/transcript`);
        console.log('getTranscript res.data', res.data);
        return res.data;
    },

    // Create/Update methods
    upload: async obj => {
        const res = await axios.post(baseURL + '/file/upload', obj);
        return res.data.data;
    },
    splitFile: async id => {
        const res = await axios.post(baseURL + `/file/${id}/split`);
        return res.data;
    },
    transcribe: async id => {
        const res = await axios.put(baseURL + `/segment/${id}/transcript`);
        return res.data;
    },
};