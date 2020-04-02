
<template>
    <div>
        Segment ID: {{segmentId}}
        <b-form-group label="Display mode">
            <b-form-radio-group v-model="viewMode">
                <b-form-radio value="simple">Simple</b-form-radio>
                <b-form-radio value="practice-first">Practice</b-form-radio>
                <b-form-radio value="test" disabled>Test</b-form-radio>
            </b-form-radio-group>
        </b-form-group>
        <!--TODO: move boolean to a method or something-->
        <transcribe-exercise />
        <!--<transcribe-segment :segmentId="segmentId" v-if="viewMode === 'simple' || answerGiven" />-->
    </div>

</template>

<script>
// Here we can add different modes such as simple transcription, practice, test


import TranscribeExercise from "./TranscribeExercise";
    export default {
        name: "transcribe-modes",
        components: {TranscribeExercise},
        props: ['segmentId'],
        watch: {
            segmentId: function (newVal) {
                console.log('TranscribeSegment newVal: ', newVal);
                this.segmentId = newVal;
            },
            viewMode: function (newVal) {
                console.debug('Checkbox selected or deselected', newVal);
            }
        },
        data: function () {
            return {
                viewMode: "simple",
                answerGiven: false,

            }
        },

    }
</script>

<style scoped>

</style>