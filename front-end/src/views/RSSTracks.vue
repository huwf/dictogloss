<template>
  <b-container>
    <h2>{{this.channel}}</h2>
    <button @click="update">Update</button>
    <b-list-group class="col-sm-9 float-left overflow-auto" style="max-height: 95vh;">
      <b-list-group-item v-for="track in this.tracks" v-bind:key="track.id">
        <h3><a :href="track.url">{{track.title}}</a></h3>
        <form v-if="!!track.is_added" @submit="formSubmit" v-bind:track="track">
          <input type="hidden" name="source_url" v-bind:source_url="track.source_url" />
          <input type="hidden" name="language" v-bind:language="track.language" />
          <input type="hidden" name="pretty_name" v-bind:pretty_name="track.pretty_name" />
          <input type="hidden" name="track_id" v-bind:track_id="track.id" />
          <button>Add to Dictogloss</button>
        </form>

        <p>{{track.description}}</p>

      </b-list-group-item>
    </b-list-group>

  </b-container>
</template>

<script>
    import {api} from "../api";
    export default {
        name: "RSSTracks",
        data: function () {
            return {
                tracks: [],
                channel: this.$router.currentRoute.params.channel,
                url: ''
            }
        },
        async mounted() {
          let res = await api.getTracksByChannel(this.channel);
          this.tracks = res.data;
          let res2 = await api.getChannelByName(this.channel);
          this.url = res2.data.url;
          console.log('this.url', this.url);
        },
        methods: {
            formSubmit(e) {
                e.preventDefault();
                // console.log('formSubmit value: ', value);
                console.log('formSubmit e: ', e);
                // console.log('File: ', this.file);
                // api.upload(this.file).then(response => {
                //     console.debug(response.data);
                //     this.$router.push({name: "file", params: {file_id: response.data.id}});
                // });
            },
            async update(e) {
                e.preventDefault();
                // console.log('parseChannel this.url', this.url);
                const res = api.parseChannel(this.url);
                console.log('parseChannel res', res);
            }
        },
    }
</script>

<style scoped>

</style>