<template>
    <div>
        <b-container class="col-sm-9 float-right">
            <h2>{{file.pretty_name}}</h2>
            <p>Language: {{file.language}}</p>

            <audio-player :file="file" :fileId="this.id" :position="position" />

            <template v-if="file.segments.length === 0">
                <p>There are no segments associated with this file.</p>
                <form class="d-inline" @submit.prevent="splitFile">
                    <label for="segment-length">Segment length</label>
                    <input id="segment-length" type="text" v-model="segmentLength"/>
                    <b-button @click="splitFile" type="submit">Split it</b-button>
                </form>
            </template>

            <template v-if="position">
                <h3>Transcribe</h3>
                <transcribe />
                <h3>Translate</h3>
                <translate file="file" />
            </template>
        </b-container>

        <segments-list :segments="file.segments" :file="file" :position="this.position" />
    </div>

</template>

<script>

    import SegmentsList from "./Segments";
    import {api} from "../api";
    import AudioPlayer from "./Player";
    import Transcribe from "./Transcribe";

    export default {
        name: 'segment',
        components: {Transcribe, AudioPlayer, SegmentsList},
        data() {
            return {
                file: {
                    segments: [],
                },
                id: this.$router.currentRoute.params.file_id,
                position: this.$router.currentRoute.params.position,
                segmentLength: '',
                selectedPosition: this.$router.currentRoute.params.position,
                selectedSegment: ''
            };
        },
        watch: {
            $route(to, from) {
                console.debug(`route change to from:`, to, from);
                this.position = this.$router.currentRoute.params.position;
            },
        },
        async mounted() {
            console.log('mounted this.id this.selectedPosition', this.id, this.selectedPosition);
            api.getFile(this.id).then(resp => {
               console.log('getFile response', resp.data);
               this.file = resp.data;
            });

        },
        methods: {
            splitFile: function (e) {
                e.preventDefault();
                console.log('segmentLength: ', this.segmentLength);
                api.splitFile(this.id, this.segmentLength);
            },
            selectPosition: function (segmentPosition) {
                console.debug('router', this.$router.currentRoute.params);
                console.log('Selected position ', segmentPosition);
                this.selectedPosition = segmentPosition;
                console.debug('this: ', this);
            },
        }
    }

</script>