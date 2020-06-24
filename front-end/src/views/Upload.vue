<template>
  <b-container fluid>
    <form action="#" @submit.prevent="formSubmit">
      <b-form-group
              label="URL"
              label-for="url"
              description="The URL to retrieve the audio file from">
        <b-form-input
                type="text"
                id="url"
                v-model="file.source_url"
        ></b-form-input>
      </b-form-group>

      <b-form-group
              label-for="languagesList"
              label="Language"
              description="The language to transcribe the input file in">
        <b-form-select id="languagesList" v-model="file.language">
          <b-form-select-option v-for="(lang, index) in languages"
                                v-bind:key="index"
                                v-bind:value="lang.code">
            {{lang.language}}
          </b-form-select-option>
        </b-form-select>
      </b-form-group>

      <b-form-group label="Display name"
                    label-for="prettyName"
                    description="The name which the file will be referred to in future">
        <b-form-input type="text"
                      id="prettyName"
                      v-model="file.pretty_name"></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
    </form>

  </b-container>

</template>

<script>
    import {api} from "../api";

    export default {
        name: 'upload-file',
        async mounted() {
            console.log('debug');
            this.languages = await api.getLanguages();
        },
        data() {
            return {
                languages: [],
                file: {
                    required: true,
                    type: Object,
                    default: () => {
                        return {
                            source_url: '',
                            language: 'sv-SE',
                            pretty_name: ''
                        };
                    }
                },
            }
        },
        methods: {
            formSubmit(e) {
                e.preventDefault();
                console.log('File: ', this.file);
                api.upload(this.file).then(response => {
                    console.debug(response.data);
                    this.$router.push({name: "file", params: {file_id: response.data.id}});
                });
            }
        },
    }
</script>