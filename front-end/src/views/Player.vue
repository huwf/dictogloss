<template>
    <div>
        <audio v-bind:src="playerSource" controls>
            Your device does not support the audio format
        </audio>
    </div>

</template>

<script>
    import {api} from "../api";

    export default {
        name: 'audio-player',
        props: ['file','fileId', 'position'],
        watch: {
            position: function(newVal, oldVal) {
                console.log('watch positionnewVal', newVal, 'oldVal', oldVal);
                api.getAudioSrc(this.segment, this.fileId, this.position).then(resp => {
                    console.log('resp.data', resp.data);
                    this.playerSource = resp.data.url;
                });
            },
            file: function (newVal) {
                console.debug('file prop changed: ', newVal);
                if (!this.position) {
                    this.playerSource = newVal.url;
                }
            }
        },
        data: function () {
            return {
                playerSource: ''
            }
        },
        async mounted() {
            console.log('mounted', this.fileId, this.position);

            if (this.fileId && this.position) {
                console.debug('fileId and position');
                api.getAudioSrc(this.segment, this.fileId, this.position).then(resp => {
                    console.log('mounted: resp', resp.data);
                    this.playerSource = resp.data.url;
                });
            }
            else if (this.file) {
                console.debug('Fallback to playing the whole file', this.file.url);
                this.playerSource = this.file.url;
            }
            else {
                console.debug('mounted this', this);
            }
        },
    };
</script>