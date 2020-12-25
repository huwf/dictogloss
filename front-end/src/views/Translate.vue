<template>
        <b-container v-if="transcript">
            <b-card  v-if="this.viewMode === 'simple'">
                <b-card-header>
                    Transcript retrieved with confidence {{confidence}}
                </b-card-header>
                <b-card-body>{{transcript}}</b-card-body>
            </b-card>
        </b-container>
        <b-container v-else>
            <p>
                There does not appear to be any translations associated with this segment. <b-button type="submit" @click="translate">Retrieve one</b-button>
            </p>
        </b-container>
</template>

<script>
    import {api} from "../api";

    export default {
        name: "Translate",
        props: ['file'],
        data() {

        },
        methods: {
            translate: () => {
                res = api.translate(fileId, position)


            }
        }
    }

</script>