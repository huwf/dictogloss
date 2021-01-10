<template>
  <div>
    <transcribe-modes @emitMode="setViewMode" :transcript="transcript"/>
    <b-container v-if="transcript">
      <b-card v-if="this.viewMode === 'simple'">
        <b-card-header>
          Transcript retrieved with confidence {{confidence}}
        </b-card-header>
        <b-card-body @mouseup="handleMouseUp" v-html="this.transcript"></b-card-body>
      </b-card>
    </b-container>
    <b-container v-else>
      <p>
        There does not appear to be a transcript associated with this segment.
        <b-button type="submit" @click="transcribe">Retrieve one</b-button>
        <b-spinner v-if="busy"/>
      </p>
    </b-container>
    <b-button v-b-modal.modal-1 >Launch modal</b-button>
    <anki-modal :selectedText="this.selectedText" :blobText="this.transcript" @hide="this.getTranscript"></anki-modal>

  </div>
</template>

<script>
    import {api} from "../api";
    import TranscribeModes from "./TranscribeModes";
    import AnkiModal from "./AnkiModal";

    export default {
        // 'name': 'transcribe-segment',
        'components': {AnkiModal, TranscribeModes},
        'watch': {
            $route: function (newVal) {
                this.position = this.$router.currentRoute.params.position;

                console.debug('Transcribe watch riyte getTranscript position', newVal);
                this.getTranscript();

            },
            transcript: function(newVal) {
                console.log(`TRANSCRIPT CHANGED! ${newVal}`);
            },
            viewMode: function (newVal) {
                console.log('viewMode changed to ', newVal);
            }
        },
        data: function () {
            return {
                transcript: '',
                confidence: '',
                viewMode: 'simple',
                busy: false,
                file: this.$router.currentRoute.params.file_id,
                position: this.$router.currentRoute.params.position,
                show: false,
                selectedText: {
                    default: '', type: String
                }
            }
        },
        methods: {
            getTranscript() {
                api.getTranscript(this.file, this.position).then(resp => {
                    console.log('Transcribe mounted resp.data', resp.data);
                    this.busy = false;
                    this.transcript = resp.data.transcript;
                    this.confidence = resp.data.confidence ? resp.data.confidence.toFixed(2) : resp.data.confidence;
                    this.$emit('got-transcript', this.transcript);
                });
            },
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
                console.log('setViewMode', event);
                this.viewMode = event;
            },
            handleMouseUp: function(event) {
                console.log('mouseup: ', event);
                let selected = window.getSelection();

                // console.log('mouseup selectedText text', this.selectedText.toString());
                if (window.getSelection().toString() !== '') {
                    this.selectedText = selected.toString();
                    console.log('selected: ', selected);
                    this.$bvModal.show('modal-1');
                }
                else {
                    console.log('No text selected')
                }
                console.log('this.selectedText: ', this.selectedText);
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