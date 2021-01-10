<template>
  <b-container>
    <h2>{{this.article.pretty_name}}</h2>
    <b-container @mouseup="handleMouseUp" v-html="this.article.content"></b-container>
    <anki-modal :selectedText="this.selectedText" :blobText="this.article.content.text"></anki-modal>

  </b-container>
</template>

<script>
  import {api} from "../api";
  import AnkiModal from "./AnkiModal";
    export default {
        name: "Article",
        components: {AnkiModal},
        data: function() {
            return {
                id: this.$router.currentRoute.params.articleId,
                title: '',
                selectedText: '',
                article: {
                    type: Object,
                    default: {}
                }
            }
        },
        async mounted() {
            let res = await api.getArticle(this.id);
            console.log('res.article: ', res.article);
            this.article = res.article;
            this.title = this.article.pretty_name;
        },
        methods: {
            handleMouseUp: function(event) {
                console.log('mouseup: ', event);
                let selectedText = window.getSelection();
                this.selectedText = selectedText.toString();
                // console.log('mouseup selectedText text', this.selectedText.toString());
                if (window.getSelection().toString() !== '') {
                    console.log('selectedText: ', selectedText);
                    this.$bvModal.show('modal-1');
                }
                else {
                    console.log('No text selected')
                }
                console.log('this.selectedText: ', this.selectedText);
            }
        }


    }
</script>

<style scoped>

</style>