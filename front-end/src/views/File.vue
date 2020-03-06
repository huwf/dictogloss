<template>
    <div>
        <b-container class="col-sm-9 float-right">
            <h2>{{file.pretty_name}}</h2>
            <p>Language: {{file.language}}</p>
            <p>There are no segments associated with this file.</p>
            <template v-if="file.segments.length === 0">
                <form class="d-inline" @submit.prevent="splitFile">
                    <label for="segment-length">Segment length</label>
                    <input id="segment-length" type="text" v-model="segmentLength"/>
                    <b-button @click="splitFile" type="submit">Split it</b-button>
                </form>
            </template>

        </b-container>

        <segments-list :segments="file.segments" />
    </div>

</template>

<script>

    import SegmentsList from "./Segments";
    import {api} from "../api";

    export default {
        name: 'segment',
        components: {SegmentsList},
        data() {
            return {
                file: {
                    segments: [],
                },
                id: this.$router.currentRoute.params.file_id,
                segmentLength: ''
            };
        },
        async mounted() {
            // let id = ;
            // axios.get('http://localhost:5000/file/' + this.id).then(response => {
            //     console.log('Response: ', response);
            //     this.file = response.data;
            //     console.log(this);
            // });
            this.file = await api.getFile(this.id);

        },
        methods: {
            splitFile: function (e) {
                e.preventDefault();
                console.log('segmentLength: ', this.segmentLength);
                api.splitFile(this.id, this.segmentLength);
            }
        }
    }

</script>