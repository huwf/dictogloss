<template>
    <div>
        <router-link :to="{name: 'filePosition', params: {file_id: file.id, position: parseInt(position) - 1}}"
                     v-if="position > 1" class="nextPrev" title="Previous segment">
            <b-icon-skip-start></b-icon-skip-start>
        </router-link>
        <div class="nextPrev" v-else disabled="disabled">
            <b-icon-skip-start></b-icon-skip-start>
        </div>
        <audio v-bind:src="playerSource" controls>
            Your device does not support the audio format
        </audio>
        <router-link :to="{name: 'filePosition', params: {file_id: file.id, position: parseInt(position) + 1}}"
                     v-if="position && position < file.segments.length" class="nextPrev" title="Next segment">
            <b-icon-skip-end style=""></b-icon-skip-end>
        </router-link>
        <div class="nextPrev" v-else disabled="disabled">
            <b-icon-skip-end></b-icon-skip-end>
        </div>
    </div>

</template>

<script>
    import {api} from "../api";

    export default {
        name: 'audio-player',
        props: ['file','fileId', 'position'],
        watch: {
            position: function(newVal, oldVal) {
                console.log('watch position newVal', newVal, 'oldVal', oldVal);
                api.getAudioSrc(this.segment, this.fileId, this.position).then(resp => {
                    console.log('getAudioSrc resp.data', resp.data);
                    this.playerSource = resp.data.url;
                });
            },
            file: function (newVal) {
                console.debug('file prop changed: ', newVal);
                if (!this.position) {
                    this.playerSource = newVal.url;
                }
            },

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
                    console.log('mounted getAudioSrc: resp', resp.data);
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
        // watch: {
        //
        //     // selectSegmentUp() {
        //     //     this.position += 1;
        //     //     this.$emit('selectPosition', this.position);
        //     // }
        // }
    };
</script>

<style>
    .nextPrev {
        background-color: #1b1e21;
        font-size: 2.2rem;
        position: relative;
        bottom: 8px;
        display: inline;
    }
</style>