
<template>
    <div>
        Segment ID: {{segmentId}}
        <transcribe-segment  :segmentId="segmentId" />
    </div>

</template>

<script>
// Here we can add different modes such as simple transcription, practice, test

    import TranscribeSegment from "./Transcribe";
    export default {
        name: "transcribe-modes",
        components: {TranscribeSegment},
        props: ['segmentId'],
        watch: {
            segmentId: function (newVal) {
                console.log('TranscribeSegment newVal: ', newVal);
                this.segmentId = newVal;
            }
        },
    }
</script>

<style scoped>

</style>