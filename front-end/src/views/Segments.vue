<template>
    <b-list-group class="col-sm-3 float-left">
        <b-list-group-item  v-for="segment in this.$props.segments" v-bind:key="segment.position">Segment {{segment.position}}</b-list-group-item>
<!--        <b-list-group-item>Test 1</b-list-group-item>-->
<!--        <b-list-group-item>Test 2</b-list-group-item>-->
<!--        <b-list-group-item>Test 3</b-list-group-item>-->
    </b-list-group>
</template>

<script>
    export default {
        name: 'segments-list',
        // data: function(){
        //     console.log('this', this.data);
        //     return {
        //         segments: []
        //     };
        // },
        props: ['segments']
    }
</script>