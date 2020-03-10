<template>
    <b-list-group class="col-sm-3 float-left overflow-auto" style="max-height: 95vh;">
        <b-list-group-item :to="{name: 'file', params: {file_id: file.id}}">
            Whole file
        </b-list-group-item>
        <b-list-group-item @click="selectSegment"
                           :to="{name: 'filePosition', params: {file_id: file.id, position: segment.position}}"
                           v-for="segment in $props.segments"
                           v-bind:key="segment.id"
                           v-bind:position="segment.position"
                           v-bind:id="segment.id">
            Segment {{segment.position}}
        </b-list-group-item>
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
        props: ['segments', 'file', 'position'],
        methods: {
            selectSegment: function(event) {
                // TODO: There HAS to be a better way to do this
                console.debug('event.target', event.target.attributes.position.value);
                let selectedPosition = event.target.attributes.position.value;
                let selectedSegment = event.target.attributes.id.value;
                this.$emit('selectSegment', selectedSegment);
                this.$emit('selectPosition', selectedPosition);
            }
        }
    }
</script>