import Vue from 'vue';
import Router from 'vue-router';
import File from './views/File';
import About from './views/About';
import Home from './views/Home';
import Upload from "./views/Upload";

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    linkActiveClass: 'active',
    routes: [
        {
            path: '/', component: Home, name: 'home'
        },
        {
            path: '/about', component: About, name: 'about'
        },

        {
            path: '/file/:file_id/', component: File
        },
        {
            path: '/upload', component: Upload, name: 'upload'
        }
    ]
});