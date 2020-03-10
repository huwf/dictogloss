<template>
    <b-container>
        <h2>Available media</h2>
        <p>
            This page contains a list of all the media available on the server.
        </p>
        <h3>My Media</h3>
        <b-card v-for="file in this.media" v-bind:key="file.key">
            <b-link :to="{name: 'file', params: {file_id: file.id}}">{{file.pretty_name}}</b-link>
        </b-card>
    </b-container>
</template>

<script>
    import {api} from "../api";
    export default {
        data: function () {
            return {
                media: []
            }
        },
        async mounted() {
            let res = await api.getDownloads();
            console.log('res: ', res.data);
            this.media = res.data;
        }
    }
</script>