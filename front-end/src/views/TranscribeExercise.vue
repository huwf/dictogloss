<template>
    <div>
        <template v-if="false">
        <b-form-textarea id="textarea" v-model="userAnswer" placeholder="Enter the transcript of the text" rows="4">
        </b-form-textarea>
        <b-button type="submit" @click="diffTranscript">Submit</b-button>
        </template>

        <transcribe-segment :segmentId="segmentId" @got-transcript="updateTranscript" />
        <b-container id="diff">
            <!--<h3>Diff</h3>-->
            <!--<div v-html="diffHtml"></div>-->
        </b-container>
    </div>
</template>

<script>
    import TranscribeSegment from "./Transcribe";
    import * as Diff2Html from 'diff2html';
    import 'diff2html/bundles/css/diff2html.min.css';
    require('colors');
    const jsdiff = require('diff');

    export default {
        name: 'transcribe-exercise',
        components: {TranscribeSegment},
        props: ['segmentId'],
        data: function () {
            return {
                userAnswer: '',
                actualAnswer: '',
                diffHtml: ''
            }
        },
        methods: {
            diffTranscript: function () {
                console.debug('diffTranscript method running');

                let diff = jsdiff.createPatch('transcript', this.actualAnswer, this.userAnswer);
                console.log('diff', diff);
                // let ret = [];
                // console.log('diff', diff);
                // diff.forEach(function(part){
                //   // green for additions, red for deletions grey for common parts
                //   let colour = part.added ? 'green' : part.removed ? 'red' : 'grey';
                //   console.log('part: ', part, 'colour', colour);
                // });
                this.diffHtml = Diff2Html.html(diff, {
                    outputFormat: 'side-by-side', drawFileList: false
                });
            },
            updateTranscript(value) {
                this.actualAnswer = value;
                console.debug('updateTranscript called with update ', this.actualAnswer);
            },
        },
        watch: {
            userAnswer: function (newVal) {
                console.log('userAnswer changed to ', newVal);
            }
        },
    }
</script>