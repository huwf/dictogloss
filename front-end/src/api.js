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
        console.log('getFile res', res.data);
        return res.data.data;
    },
    upload: async obj => {
        const res = await axios.post(baseURL + '/file/upload', obj);
        return res.data.data;
    },
    splitFile: async id => {
        const res = await axios.post(baseURL + `/file/${id}/split`);
        return res.data;
    }

};