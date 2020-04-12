<template>
    <div>
        <b-container>
            <b-card v-if="transcript">
                <b-card-header>
                    Transcript retrieved with confidence {{confidence}}
                </b-card-header>
                <b-card-body>{{transcript}}</b-card-body>
            </b-card>
            <p v-else>
                There does not appear to be a transcript associated with this segment. <b-button type="submit" @click="transcribe">Retrieve one</b-button>
                <b-spinner v-if="busy" />
            </p>
        </b-container>
    </div>
</template>

<script>
    import {api} from "../api";

    export default {
        'name': 'transcribe-segment',

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


            }
        },
        data: function() {
            return {
                transcript: '',
                confidence: '',
                busy: false,
                file: this.$router.currentRoute.params.file_id,
                position: this.$router.currentRoute.params.position,

            }
        },
        methods: {
            transcribe: function () {
                console.log('clicked transcribe');
                this.busy = true;
                api.transcribe(this.file, this.position).then(resp => {
                    console.log('Finished transcribing');
                    this.transcript = resp.data.transcript;
                    this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                    this.busy = false;
                });
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