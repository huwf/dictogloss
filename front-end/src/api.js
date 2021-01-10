import axios from 'axios';
// import Vue from 'vue';
// import VueFlashMessage from 'vue-flash-message';
// import 'vue-flash-message/dist/vue-flash-message.min.css';

// const vm = new Vue();

const baseURL = process.env.VUE_APP_API ? process.env.VUE_APP_API : 'http://172.17.0.1:5000';
// const baseURL = 'http://172.17.0.1:5000';
console.log('baseURL', baseURL);
console.log('process.env', process.env);
// const handleError = fn => (...params) =>
//     fn(...params).catch(error => {
//         console.log(error);
//         vm.flash(`${error.response.status}`);
//     });

export const api = {
    getLanguages: async () => {
        console.debug('getLanguages api called');
        const res = await axios.get(baseURL + '/info/languages/speech');
        console.debug('res: ', res.data.data);
        return res.data.data;
    },
    getFile: async id => {
        const res = await axios.get(baseURL + '/file/' + id);
        console.debug('getFile res.data', res.data);
        return res.data;
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
            res = await axios.get(baseURL + `/file/${fileId}?fields=url`);
        }

        console.debug('getAudioSrc res.data', res.data);
        return res.data;
    },
    getTranscript: async (fileId, position) => {
        console.debug('getTranscript fileId position', fileId, position);
        // const res = await axios.get(baseURL + `/segment/${id}/transcript`);
        const res = await axios.get(baseURL + `/transcript/${fileId}/${position}`);
        console.log('getTranscript res.data', res.data);
        return res.data;
    },

    getDiff: async (user, google, first) => {
        console.debug('Calling getDiff with arguments ', user, google, first);
        const argsString = `?user=${user}&google=${google}&first=${first}`;
        const res = await axios.get(`${baseURL}/tools/differ${argsString}`);
        return res.data;

    },

    // Create/Update methods
    upload: obj => {
        return axios.post(baseURL + '/file/upload', obj);
        // return res.data.data;
    },
    splitFile: async (id, length) => {
        const res = await axios.post(baseURL + `/file/${id}/split`, {'segment_length': length});
        return res.data;
    },
    transcribe: async (fileId, position) => {
        const res = await axios.put(baseURL + `/transcript/${fileId}/${position}`);
        // return await axios.put(baseURL + `/transcript/${fileId}/${position}`);  // .data;
        return res.data;
    },
    translate: async (fileId, position, text) => {
        console.debug('translate fileId position', fileId, position, text);
        let obj = {
            text: text
        };
        const res = await axios.post(baseURL + `/translate/${fileId}/${position}`, obj);
        console.debug('translate returns res.data', res.data);

        return res.data;
    },

    // RSS
    addChannel: async (newChannel) => {
        const res = await axios.post(baseURL + '/rss/channels/new', newChannel);
        console.log('addChannel res.data', res.data);
        return res.data;
    },
    getChannels: async () => {
        const res = await axios.get(baseURL + '/rss/channels');
        // return axios.get(baseURL + '/rss/channels');
        console.log('getChannels res.data', res.data);
        return res.data;
    },

    getTracksByChannel: async channel => {
        const res = await axios.get(baseURL + `/rss/${channel}/tracks`);
        console.debug('getTracksByChannel res.data', res.data);
        return res.data;
    },

    getChannelByName: async channelName => {
        const res = await axios.get(baseURL + `/rss/channels/${channelName}`);
        console.debug(`getChannelByName ${channelName} res.data`, res.data);
        return res.data;
    },

    parseChannel: async url => {
        let obj = {
            'url': url
        };
        const res = await axios.post(baseURL + `/rss/parse`, obj);
        console.debug('parseChannel ${url} res.data', res.data);
        return res.data;
    },

    // Text
    addToAnki: async obj => {

        const res = await axios.post(baseURL + '/text/anki', obj);
        console.debug('addToAnki res.data: ', res.data);
        return res.data;
    },
    importText: async obj => {
        const res = await axios.post(baseURL + '/text/import', obj);
        console.debug('importText res.data: ', res.data);
        return res.data
    },
    getArticle: async id => {
        const res = await axios.get(baseURL + `/text/article/${id}`)
        console.debug('getArticle res.data: ', res.data);
        return res.data;
    }


};