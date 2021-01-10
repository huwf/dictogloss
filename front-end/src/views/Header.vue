<template>
    <b-navbar type="dark" variant="info">
        <!--<b-navbar-brand :to="{name: 'home'}">Dictogloss</b-navbar-brand>-->
        <b-navbar-nav>
            <b-nav-item :to="{name: 'upload'}">Upload</b-nav-item>
            <b-nav-item :to="{name: 'about'}">About</b-nav-item>
            <b-nav-item :to="{name: 'media'}">Media</b-nav-item>
            <b-nav-item :to="{name: 'rss'}">feeds</b-nav-item>
        </b-navbar-nav>

        <b-navbar-nav class="ml-auto">
            <!--<b-nav-item :to="{name: 'user'}">Account</b-nav-item>-->
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
    export default {
        'name': 'app-header'
    }
</script>