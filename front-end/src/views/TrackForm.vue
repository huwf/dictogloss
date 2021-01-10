<template>
  <b-container>
    <h3><a :href="track.url">{{track.title}}</a></h3>
    <form @submit="formSubmit" v-bind:track="track">
      <input type="hidden" name="source_url" v-bind:source_url="track.source_url" />
      <input type="hidden" name="language" v-bind:language="track.language" />
      <input type="hidden" name="pretty_name" v-bind:pretty_name="track.pretty_name" />
      <input type="hidden" name="track_id" v-bind:track_id="track.id" />

      <button>Add to Dictogloss</button>
    </form>
    <p>{{track.description}}</p>
  </b-container>
</template>

<script>
    import {api} from "../api";

    export default {
        name: "TrackForm",
        props: ['track', 'channelType'],
        // data() {
        //     // return {
        //     //     file: {
        //     //         required: true,
        //     //         type: Object,
        //     //         default: () => {
        //     //             return {
        //     //                 source_url: '',
        //     //                 language: 'sv-SE',
        //     //                 pretty_name: '',
        //     //                 track_id: null
        //     //             };
        //     //         }
        //     //     },
        //     // }
        // },

        methods: {
            formSubmit(e) {
                e.preventDefault();
                console.log('this.track: ', this.track);
                if(this.channelType === 'audio') {
                  api.upload(this.track).then(response => {
                      console.debug('upload segment response.data: ', response.data);
                      this.$router.push({name: "file", params: {file_id: response.data.id}});
                  });
                }
                else if (this.channelType === 'text') {
                    console.log('this.track: ', this.track);
                    api.importText(this.track).then(response => {
                        console.debug('upload article response data: ', response.data);
                      this.$router.push({name: "article", params: {articleId: response.article.id}});
                    });
                }

            },
        }
    }
</script>

<style scoped>

</style>
