import Vue from 'vue';
import Router from 'vue-router';
import File from './views/File';
import About from './views/About';
import Home from './views/Home';
import Upload from "./views/Upload";
import Media from './views/Media';
import RSS from './views/RSS';
import RSSTracks from './views/RSSTracks';
import Article from './views/Article';

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
            path: '/media', component: Media, name: 'media'
        },
        {
            path: '/article/:articleId', component: Article, 'name': 'article'
        },
        {
            path: '/rss', component: RSS, name: 'rss'
        },
        {
            path: '/rss/:channel', component: RSSTracks, name: 'rssTracks'
        },
        {
            path: '/file/:file_id/:position', component: File, name: 'filePosition'
        },
        {
            path: '/file/:file_id', component: File, name: 'file'
        },
        {
            path: '/upload', component: Upload, name: 'upload'
        }
    ]
});