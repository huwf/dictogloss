<template>
    <div>
        <transcribe-modes @emitMode="setViewMode" />
        <b-container v-if="transcript">
            <b-card  v-if="this.viewMode === 'simple'">
                <b-card-header>
                    Transcript retrieved with confidence {{confidence}}
                </b-card-header>
                <b-card-body>{{transcript}}</b-card-body>
            </b-card>
        </b-container>
        <b-container v-else>
            <p>
                There does not appear to be a transcript associated with this segment. <b-button type="submit" @click="transcribe">Retrieve one</b-button>
                <b-spinner v-if="busy" />
            </p>
        </b-container>
    </div>
</template>

<script>
    import {api} from "../api";
    import TranscribeModes from "./TranscribeModes";

    export default {
        'name': 'transcribe-segment',
        'components': {TranscribeModes},
        'watch': {
            $route: function (newVal) {
                this.position = this.$router.currentRoute.params.position;

                console.debug('Transcribe mounted getTranscript position', newVal);
                api.getTranscript(this.file, this.position).then(resp => {
                    console.log('Transcribe mounted resp.data', resp.data);
                    this.busy = false;
                    this.transcript = resp.data.transcript;
                    this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                    this.$emit('got-transcript', this.transcript);
                });
            },
            viewMode: function (newVal) {
                console.log('viewMode changed to ', newVal);
            }
        },
        data: function() {
            return {
                transcript: '',
                confidence: '',
                viewMode: 'simple',
                busy: false,
                file: this.$router.currentRoute.params.file_id,
                position: this.$router.currentRoute.params.position,
                show: false
            }
        },
        methods: {
            transcribe() {
                console.log('clicked transcribe this', this);
                // this.busy = true;
                // const resp = await api.transcribe(this.file, this.position);
                // console.log('Finished transcribing', resp.data);
                // this.transcript = resp.data.transcript;
                // this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                // this.busy = false;
                // console.debug('this.transcript, this.confidence', this.transcript, this.confidence);
                api.transcribe(this.file, this.position).then(resp => {
                    // resp = resp.data;
                    console.log('Finished transcribing', resp.data);
                    console.log('api.transcribe this', this);

                    this.transcript = resp.data.transcript;
                    this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                    this.busy = false;
                    console.debug('this.transcript, this.confidence', this.transcript, this.confidence);
                    console.log('this', this);
                });
            },
            setViewMode: function (event) {
                // alert('Hello');
                console.log('setViewMode', event);
                this.viewMode = event;
            }
        },
        async mounted() {
            api.getTranscript(this.file, this.position).then(resp => {
                console.log('Transcribe mounted resp.data', resp.data);
                this.busy = false;
                this.transcript = resp.data.transcript;
                this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                this.$emit('got-transcript', this.transcript);
            });
        }
    };
</script>