<template>
    <v-layout wrap align-center>
        <v-flex xs12 sm6 d-flex>
            <form action="#" @submit.prevent="formSubmit">
                <label for="url">URL</label><input type="text" id="url" v-model="file.source_url"><br />
                <label for="language">Language</label>
<!--                <select v-model="this.languages" id="language">-->
<!--                    <option v-for="(lang, index) in languages" v-bind:key="index" v-bind:value="lang.code">-->
<!--                        {{lang.language}}-->
<!--                    </option>-->
<!--                </select>-->
                <input type="text" value="sv-SE" v-model="file.language" id="language"/>
                <br />
                <label for="prettyName">Display name</label><input type="text" id="prettyName" v-model="file.pretty_name"><br />
                <button type="submit">Submit</button>
            </form>
        </v-flex>
    </v-layout>

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
                languages: [],// () => {return []},
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
            formSubmit: function(e) {
                e.preventDefault();
                console.log('File: ', this.file);
                api.upload(this.file);
            }
        },
    }
</script>