<template>
  <div>
    <h2>RSS Feeds</h2>
    <p>
      Here is a list of all the RSS feeds you've saved in the database.
      <b-form @submit="addChannel">
        <b-form-group label="Channel name" description="The name of the channel" label-for="channelName">
          <b-form-input id="channelName" v-model="newChannel.feed_name"></b-form-input>
        </b-form-group>
        <b-form-group label="Channel description" description="Description of the channel (parsed from XML if not specified)" label-for="channelDescription">
          <b-form-input id="channelDescription" v-model="newChannel.feed_description"></b-form-input>
        </b-form-group>
        <b-form-group label="Channel type" description="The type of RSS feed (audio or text)">
          <b-form-select :options="['audio', 'text']" v-model="newChannel.feed_type"></b-form-select>
        </b-form-group>
        <b-form-group label="RSS feed" description="The URL of the RSS feed" label-for="rssUrl">
          <b-form-input id="rssUrl" v-model="newChannel.feed_url"></b-form-input>
        </b-form-group>

        <b-button type="submit">Add channel</b-button>
      </b-form>

    </p>
    <b-list-group class="col-sm-9 float-left overflow-auto" style="max-height: 95vh;">
      <b-list-group-item v-for="channel in this.channels" v-bind:key="channel.id"
                         :to="{name: 'rssTracks', params: {channel: channel.name}}">
        <h3>{{channel.name}}</h3>
        <p>{{channel.description}}</p>
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
            newChannel: {
                feed_url: '',
                feed_name: '',
                feed_description: '',
                feed_type: ''
            }
          }
        },
        async created() {
          console.log('this: ', this);
          let res = await api.getChannels();
          this.channels = res.data;
        },
        methods: {
            async addChannel(e) {
              e.preventDefault();
              console.log('obj: ', this.newChannel);
              await api.addChannel(this.newChannel);
              // Update the display again...
              let res = await api.getChannels();
              this.channels = res.data;
            }
        }
    }
</script>

<style scoped>

</style>