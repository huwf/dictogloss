<template>
  <b-container>
    <h2>{{this.channel}}</h2>
    <button @click="update">Update</button>
    <b-list-group class="col-sm-9 float-left overflow-auto" style="max-height: 95vh;">
      <b-list-group-item v-for="track in this.tracks" v-bind:key="track.id">

        <track-form :track="track" :channelType="channelType" />

      </b-list-group-item>
    </b-list-group>

  </b-container>
</template>

<script>
    import {api} from "../api";
    import TrackForm from './TrackForm';
    export default {
        name: "RSSTracks",
        components: {TrackForm},
        data: function () {
            return {
                tracks: [],
                channel: this.$router.currentRoute.params.channel,
                url: '',
                channelType: ''
            }
        },
        async mounted() {
          let res = await api.getTracksByChannel(this.channel);
          this.tracks = res.data;
          let res2 = await api.getChannelByName(this.channel);

          this.url = res2.data.url;
          this.channelType = res2.data.type;
          console.log('this.url', this.url, `this.channelType: ${this.channelType}`);
        },
        methods: {
            async update(e) {
                e.preventDefault();
                const res = await api.parseChannel(this.url);
                console.log('parseChannel res', res);
                this.tracks = res.data.concat(this.tracks);
                console.log('tracks: ', this.tracks);
            }
        },
    }
</script>

<style scoped>

</style>