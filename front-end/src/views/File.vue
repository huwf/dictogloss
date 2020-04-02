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
                <transcribe-modes />
            </template>
        </b-container>

        <segments-list :segments="file.segments" :file="file" :position="this.position" @selectSegment="selectSegment" />
    </div>

</template>

<script>

    import SegmentsList from "./Segments";
    import {api} from "../api";
    import AudioPlayer from "./Player";
    import TranscribeModes from "./TranscribeModes";

    export default {
        name: 'segment',
        components: {TranscribeModes, AudioPlayer, SegmentsList},
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
                // this.position = to.params.position;
                // let newPosition =
                // // this.selectedPosition = newPosition;
                this.position = this.$router.currentRoute.params.position;
            },
        },
        async mounted() {
            // let id = ;
            // axios.get('http://localhost:5000/file/' + this.id).then(response => {
            //     console.log('Response: ', response);
            //     this.file = response.data;
            //     console.log(this);
            // });
            console.log('mounted this.id this.selectedPosition', this.id, this.selectedPosition);
            api.getFile(this.id).then(resp => {
               console.log('getFile response', resp.data);
               this.file = resp.data;
            });

            // const res = await api.getSegment(this.id, this.selectedPosition);
            // console.log('getSegment data: ', res.data);
            // this.selectedSegment = res.data.id;


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
            selectSegment: function (segmentId) {
                console.log('Selected segment ID: ', segmentId);
                this.selectedSegment = segmentId;
            }
        }
    }

</script>