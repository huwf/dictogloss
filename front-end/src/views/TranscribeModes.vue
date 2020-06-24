<template>
    <div>
        <b-form-group label="Display mode">
            <b-form-radio-group v-model="viewMode" @load="$emit('emitMode', 'fsdfdsfsdfds')">
                <b-form-radio value="simple">Simple</b-form-radio>
                <b-form-radio value="practice-first">Practice</b-form-radio>
<!--                <b-form-radio value="test" disabled>Test</b-form-radio>-->
            </b-form-radio-group>
        </b-form-group>
        <transcribe-exercise v-if="viewMode === 'practice-first'" />
<!--        <transcribe-segment :segmentId="segmentId" v-else />-->
    </div>
</template>

<script>
// Here we can add different modes such as simple transcription, practice, test


import TranscribeExercise from "./TranscribeExercise";
// import TranscribeSegment from "./Transcribe"
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
                this.$emit('emitMode', newVal);
            }
        },
        data: function () {
            return {
                viewMode: "simple",
                answerGiven: false,
                showAnswer: function () {
                    return this.viewMode === "simple" || this.answerGiven;
                }

            }
        },
        methods:{
            // emitMode: function () {
            //     alert('emitMode');
            //     console.debug('Emiting transcript mode as:', this.viewMode);
            //     this.$emit('viewMode', this.viewMode);
            // }
        }

    }
</script>

<style scoped>

</style>