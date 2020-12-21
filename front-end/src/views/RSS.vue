<template>
  <div>
    <h2>RSS Feeds</h2>
    <p>
      Here is a list of all the RSS feeds you've saved in the database, including a bunch of episodes from them.
      When it's finished, you will be able to click "add to dictogloss", and it will split into segments and be available
      for your listening pleasure.
    </p>
    <b-list-group class="col-sm-9 float-left overflow-auto" style="max-height: 95vh;">
      <b-list-group-item v-for="channel in this.channels" v-bind:key="channel.id"
                         :to="{name: 'rssTracks', params: {channel: channel.name}}">
        <h3>{{channel.name}}</h3>
        <p>{{channel.description}}</p>
        <!--<p>{{channel.tracks}}</p>-->
        <!--<b-list-group v-for="track in channel.tracks" v-bind:key="track.id">-->
          <!--<b-list-group-item>{{track.name}}</b-list-group-item>-->
        <!--</b-list-group>-->
        <!--&lt;!&ndash;<b-list-group class="col-sm-3 float-left overflow-auto" style="max-height: 95vh;">&ndash;&gt;-->
          <!--&lt;!&ndash;<b-list-group-item v-for="track in this.tracks" v-bind:key="track.id">&ndash;&gt;-->
            <!--&lt;!&ndash;{{track.name}}&ndash;&gt;-->
          <!--&lt;!&ndash;</b-list-group-item>&ndash;&gt;-->
        <!--&lt;!&ndash;</b-list-group>&ndash;&gt;-->
      </b-list-group-item>
    </b-list-group>

  </div>



</template>

<script>
    import {api} from "../api"

    const baseURL = process.env.VUE_APP_API ? process.env.VUE_APP_API : 'http://172.17.0.1:5000';
    console.log('baseURL', baseURL);
    export default {
        channels: [],
        data: function() {
            return{
              name: "RSS",
              channels: [],
              tracks: {},
            }
        },
        async mounted() {
            // this.channels = [];
            console.log('this: ', this);
            let res = await api.getChannels();
            this.channels = res.data;
            for(let i=0; i < this.channels.length; i++) {
                console.log('this.channels', this.channels);
                let channel = this.channels[i];
                let tracks = await api.getTracksByChannel(channel.name);
                channel.tracks = tracks.data;
                console.log('channel.tracks', channel.tracks);
                this.channels[i] = channel;
                // this.tracks[channel] = tracks.data;
            }
            console.log('this.tracks', this.tracks);
            // console.log(res);
            // this.channels = res;
            // .then((res) => {
            //     console.log(res);
            //     this.channels = res.data.data;
            // });
            // this.channels = res;

            //     .then(function(res) {
            //     let data = res.data.data;
            // //     this.channels = data;
            //     alert(JSON.stringify(data));
            // });
            // console.log('res: ', res.data);
            // this.channels = res.data;
            // res.forEach(channel => {
            //    console.log(api.getTracksByChannel(channel));
            // });



        }
    }
</script>

<style scoped>

</style>