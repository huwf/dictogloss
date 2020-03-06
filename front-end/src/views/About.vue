<template>
    <v-container>
        <h2>About</h2>
        <p>
            This website is centred around using media to practice speaking and understanding a foreign language.
            The primary function that it does is to take an audio file and split it into equal parts. These parts may be
            uploaded (if requested) to Google Cloud to obtain a transcript of the text in the original language so that a
            language learner can check to see if their assessment of a piece of media was accurate.
        </p>
        <p>
            If using in "exercise" mode, the answer (transcript) will not be displayed until the learner has attempted to
            write the text, whereupon it will be displayed in a "diff" format indicating text which was incorrectly added,
            text which was missing, and text which was spelt incorrectly.
        </p>
        <p>
            It is also possible to translate the retrieved text to your own language, although this is not done by default.
        </p>
    </v-container>
</template>