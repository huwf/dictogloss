<template>
    <div>
        <template v-if="true">
        <b-form-textarea id="textarea" v-model="userAnswer" placeholder="Enter the transcript of the text" rows="4">
        </b-form-textarea>
        <b-button type="submit" @click="diffTranscript">Submit</b-button>
        </template>

        <transcribe-segment @got-transcript="updateTranscript" />
        <b-container id="diff">
            <h3>Diff</h3>
            <div v-html="diffHtml"></div>
        </b-container>
    </div>
</template>

<style>
    /*These classes are in Diff2Html    */
    .d2h-code-line, .d2h-code-side-line {
        width: 100%;
        display: inline-block;
        overflow: auto;
        word-wrap: break-spaces;
    }
    .d2h-code-line ins, .d2h-code-side-line ins {
        display: inline;
    }
</style>

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
                // Put the user's answer first, then this.actualAnswer shows what they need to do to get it right
                let diff = jsdiff.createPatch('transcript', this.userAnswer, this.actualAnswer);
                // Or maybe this way around is better...
                // let diff = jsdiff.createPatch('transcript', this.actualAnswer, this.userAnswer);
                // let diff = jsdiff.createTwoFilesPatch('Your answer', "Google's answer", this.userAnswer, this.actualAnswer);
                let outputDiffHtml = Diff2Html.html(diff, {
                    outputFormat: 'line-by-line', drawFileList: false, diffStyle: "char",
                    rawTemplates: {
                        'generic-empty-diff': '<h2>100% match!</h2>',
                        'line-by-line-numbers.mustache': '',
                        'line-by-line-file-diff': `<div id="{{fileHtmlId}}" class="d2h-file-wrapper" data-lang="{{file.language}}">
                            <div class="d2h-file-diff">
                                <div class="d2h-code-wrapper">
                                    <div class="d2h-diff-table">
                                        <div class="d2h-diff-tbody">{{{diffs}}}</div>
                                    </div>
                                </div>
                            </div>
                        </div>`,
                        'generic-line': `
                            <div class="{{contentClass}} {{type}}">
                            <!--{{#prefix}}-->
                                <!--<span class="d2h-code-line-prefix">{{{prefix}}}</span>-->
                            <!--{{/prefix}}-->
                            <!--{{^prefix}}-->
                                <!--<span class="d2h-code-line-prefix">&nbsp;</span>-->
                            <!--{{/prefix}}-->
                            {{#content}}
                                <span class="d2h-code-line-ctn">{{{content}}}</span>
                            {{/content}}
                            {{^content}}
                                <span class="d2h-code-line-ctn"><br></span>
                            {{/content}}
                            </div>
`
                    }
                });
                this.diffHtml = outputDiffHtml; //.replace(/<td/g, '<div').replace(/<\/td/g, '</div').replace(/<tr>/g, '').replace(/<\/tr>/g, '');
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