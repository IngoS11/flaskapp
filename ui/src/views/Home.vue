<template>
  <div class="home">
    <SignupForm />
  </div>
</template>

<script>
// @ is an alias to /src
import SignupForm from '@/components/SignupForm.vue'

export default {
  name: 'App',
  components: {
      SignupForm,
  },
  data() {
    return {
      something: false,
    }
  },
  methods: {} 
}
</script>
