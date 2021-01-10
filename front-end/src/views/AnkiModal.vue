<template>
    <b-modal id="modal-1" title="New modal">
      <form>
        <b-form-group
                label="Note type"
                label-for="noteType"
                description="The type of note, as written in Anki, e.g. Cloze">
          <b-form-input id="noteType" v-model="this.noteType"></b-form-input>
        </b-form-group>
        <b-form-group
                label="Deck"
                label-for="decky"
                description="The deck in Anki that the note should be stored in">
          <b-form-input id="decky" v-model="this.deck" placeholder="Swedish 2"></b-form-input>
        </b-form-group>
        <b-form-group
                class="my-4"
                label="Note"
                label-for="texty"
                description="The note to be added to Anki (including the cloze if appropriate)">
          <b-form-textarea class="my-4" v-model="text" id="texty"> </b-form-textarea>
        </b-form-group>

      <b-form-group
              label="Translation"
              label-for="tran"
              description="The translation of the phrase to be added to Anki">
        <b-form-textarea id="tran" v-model="translatedText" ></b-form-textarea>
        <button v-if="!this.translatedText" @click="getTranslation">Get translation</button>
      </b-form-group>

      <button type="submit" @click="addToAnki">Add to Anki</button>
      </form>

    </b-modal>
</template>

<script>
  import {api} from "../api";
  export default {
    name: "AnkiModal",
    computed: {
    },
    watch: {
      selectedText: function(newVal){
        this.cloze = newVal;
        this.setSentenceParts();
        this.text = this.clozeSentence(true);
        this.fullText = this.clozeSentence(false);

        // // TODO: Remove these hardcoded values
        this.noteType = 'Cloze Reversed';
        this.deck = 'Swedish 2';
        // this.translatedText = '';
        // this.note = '';

        console.log('this.note ', this.note);
      },
      text: function(newVal) {
          // If text changes, we need to modify fullText accordingly
          console.debug('text changed to ', newVal);
          this.setSentenceParts();
          this.fullText = this.clozeSentence(false);
      }
    },
    props: ['selectedText', 'blobText'],
    data: function () {
        return {
            // Bits to calculate cloze sentence
            sentenceLeft: '',
            sentenceRight: '',
            cloze: '',
            // Form fields
            noteType: '',
            deck: '',
            note: '',
            text: '',
            fullText: '',
            translatedText: ''
        }
    },
    methods: {
        async addToAnki(e){
            e.preventDefault();
            let obj = {
              note_type: this.noteType,
              deck: this.deck,
              fields: [this.fullText, this.text, this.translatedText]
            };
            console.log(`Sending to server:`, obj);
            let res = await api.addToAnki(obj);
            console.log('addToAnki returns res', res);

        },
        clozeSentence(includeCloze) {
          let clozeText = includeCloze ? `{{c1::${this.cloze.trim()}}}` : this.cloze.trim();

          // fullText does NOT have {{c1::}}, text does have {{c1::}}
          // let leftIndex = this.blobText.indexOf(this.cloze);
          // let ret = `${this.blobText.substr(0, leftIndex)} ${clozeText.trim()} ${this.blobText.substr(leftIndex + this.cloze.length)}`;

          console.log('clozeSentence Left Right: ', this.sentenceLeft, this.sentenceRight);
          let ret =`${this.sentenceLeft} ${clozeText} ${this.sentenceRight}`;
          console.log('Calling clozeSentence() function:, ret is: ', ret);
          return ret;
        },
        async getTranslation(e) {
            e.preventDefault();
            let file = this.$router.currentRoute.params.file_id;
            let position = this.$router.currentRoute.params.position;
            let text = this.fullText;
            let res = await api.translate(file, position, text);
            this.translatedText = res.translation.result;

        },
        setSentenceParts() {
        // This takes the cloze, and forms a sentence around it as this.leftSentence and this.rightSentence
        // Neither of these include the cloze (stored as this.cloze)
        // Need to get the clozeSentence around the word. Unlikely to work every time, but we can make some eduated guesses
        let i = 0;
        while(!this.blobText || !this.cloze ) {
            console.debug('Waiting for blobText to load');
            i++;
            if (i >= 5000) {
                console.log('Error obtaining blobText or cloze.');
                return false;
            }
        }
        let clozeSel = this.cloze;
        console.debug('this.blobText: ', this.blobText);
        let startIndex = this.blobText.indexOf(clozeSel);
        let startSentence, endSentence = 0;
        let textContent = this.blobText;
        let endIndex = startIndex + clozeSel.length;

        // Start at beginning, and work back to the start of the clozeSentence
        let currentLetter, previousLetter = '';
        i = startIndex;
        while (i >= 0) {
          currentLetter = textContent[i];
          if (this.isStartSentence(previousLetter, currentLetter)) {
            startSentence = i + 2;
            break;
          }
          previousLetter = currentLetter;
          i -= 1;
        }
        // Fall back to the starting the clozeSentence at the of the node
        if(!startSentence) {
            startSentence = 0;
        }
        this.sentenceLeft = textContent.substr(startSentence, (startIndex - startSentence));

        // Calculate to the end of the clozeSentence
        i = endIndex;
        previousLetter = '';
        while(i < textContent.length) {
          currentLetter = textContent[i];
          // endSentence will always be i, it's just a case of when we break
          endSentence= i;

          if (this.isEndSentence(previousLetter, currentLetter)){ // && previousLetter === '.') {
            // Assume we've reached the end of the clozeSentence
            break;
          }
          previousLetter = currentLetter;
          i += 1;
        }
        this.sentenceRight = textContent.substr(endIndex + 1, endSentence - (endIndex + 1));
    },
        isStartSentence(prev, current) {
            if (prev.match(/!?:/g)){
                return true;
            }
            if (prev + current === '  ') {
                return true;
            }
            if (current === '.' && prev === ' ') {
                return true;
            }
        },
        isEndSentence(prev, current) {
            if (current.match(/!?:/g)) {
                return true;
            }
            if (prev + current === '  ') {
                return true;
            }
            if (current === ' ' && prev === '.') {
                return true;
            }
            return false;
        }
    }
  }
</script>

<style scoped>

</style>