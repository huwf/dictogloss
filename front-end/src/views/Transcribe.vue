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
        'props': ['segmentId'],
        'watch': {
            segmentId: function (newVal) {
                this.segmentId = newVal;

                console.debug('Transcribe mounted getTranscript segmentId', newVal);
                api.getTranscript(this.segmentId).then(resp => {
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
                busy: false
            }
        },
        methods: {
            transcribe: function () {
                console.log('clicked transcribe');
                this.busy = true;
                api.transcribe(this.segmentId).then(resp => {
                    console.log('Finished transcribing');
                    this.transcript = resp.data.transcript;
                    this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                    this.busy = false;
                });
            }
        },
        async mounted() {

        }
    };
</script>