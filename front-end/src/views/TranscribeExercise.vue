<template>
    <div>
        <template v-if="true">
        <b-form-textarea id="textarea" v-model="userAnswer" placeholder="Enter the transcript of the text" rows="4">
        </b-form-textarea>
        <b-button type="submit" @click="diffTranscript">Show answer</b-button>
        </template>

        <b-container id="diff" v-if="this.isSubmitted">
            <h3>Answer</h3>
<!--             <a href="#answerInfo" data-target="#answerInfo" data-toggle="collapse" role="button" @click="answerInfo">[?]</a>-->
            <div id="answerInfo"  class="collapse">
                <div>
                <h4>What does all this mean?</h4>
                <p>
                   This display is a comparison of the answer you submitted, and the extra steps that you would need to have
                    done to have it match the transcript that was obtained from Google Speech to Text. The key is as follows:
                </p>
                <ul>
                    <li><ins>Text with a green background is text which would need to be added</ins></li>
                    <li><del>Text with a pink background is text which should have been removed</del></li>
                    <li>Text without any background does not need to be changed. Well done!</li>
                </ul>
                </div>

            </div>

            <div v-html="diffHtml"></div>
        </b-container>
    </div>
</template>

<style>
    /*These classes are in Diff2Html    */
    ins {
        background-color: #E6FFE6;
    }
    del {
        background-color: #FFE6E6;
    }
    #answerInfo {
        border: solid 2px gray;
        padding: 5px;
        margin: 10px;
    }
</style>

<script>
    // import TranscribeSegment from "./Transcribe";
    // import * as Diff2Html from 'diff2html';
    import 'diff2html/bundles/css/diff2html.min.css';
    import {api} from "../api";
    require('colors');

    export default {
        name: 'transcribe-exercise',
        // components: {TranscribeSegment},

        props: ['segmentId', 'actualAnswer'],
        data: function () {
            return {
                userAnswer: '',
                // actualAnswer: '',
                diffHtml: '',
                isSubmitted: false
            }
        },
        methods: {
            answerInfo: function(event) {
                console.debug('Trying to find the answer info');
                event.preventDefault();
            },
            diffTranscript: function () {
                console.debug('diffTranscript method running');
                api.getDiff(this.userAnswer, this.actualAnswer, 'user').then(response => {
                    console.log('getDiff response ', response);
                    console.debug('actualAnswer', this.actualAnswer);
                    let ret = '';
                    response.data.forEach(elem => {
                        console.log('elem', elem);
                        let symbol = elem[0];
                        let string = elem[1];
                        switch (symbol) {
                            case '-':
                                ret += `<del>${string}</del>`;
                                break;
                            case '+':
                                ret += `<ins>${string}</ins>`;
                                break;
                            default:
                                ret += `<span class="same">${string}</span>`;
                        }
                    });
                    this.diffHtml = ret;
                });
                this.isSubmitted = true;
            },
            // updateTranscript(value) {
            //     this.actualAnswer = value;
            //     console.debug('updateTranscript called with update ', this.actualAnswer);
            // },
        },
        watch: {
            userAnswer: function (newVal) {
                console.log('userAnswer changed to ', newVal);
            },
            actualAnswer: function (newVal) {
                console.log('actualAnswer changed to ', newVal);
            }


        },
    }
</script>