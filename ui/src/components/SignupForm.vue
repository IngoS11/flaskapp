<template>
  <form @submit.prevent="handleSubmit">
    <label>Email:</label>
    <input type="email" required v-model="email">
    <label>Password:</label>
    <input type="password" required v-model="password">
    <div v-if="passwordError" class="error">{{ passwordError }}</div>
    <div class="terms">
      <input type="checkbox" required v-model="terms">
      <label>Accept terms and conditions</label>
    </div>
    <div class="submit">
      <button>Create an Account</button>
    </div>
  </form>
</template>

<script>
export default {
    data() {
        return {
            email: 'peter.pan@neverland.org',
            password: '',
            terms: false,
            passwordError: '',
        }
    },
    methods: {
        handleSubmit(){
          console.log(this.password.length)
          this.passwordError = this.password.length > 5 ?
            '' : 'The password must be at least 5 characters'
          console.log(this.passwordError)
        }
    }


}
</script>

<style>
  form {
    max-width: 420px;
    margin: 30px auto;
    background: white;
    text-align: left;
    padding: 40px;
    border-radius: 10px
  }
  label {
    color: #aaa;
    display: 25px 0 15px;
    font-size: 0.6em;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: bold;
  }
  input {
    display: block;
    padding: 10px 6px;
    width: 100%;
    box-sizing: border-box;
    border: none;
    border-bottom: 1px solid #ddd;
    color: #555;
  }
  input[type="checkbox"]{
    display: inline-block;
    width: 16px;
    margin: 0 10px 0 0;
    position: relative;
    top: 2px;
  }
  button {
    background: #0b6dff;
    border: 0;
    padding: 10px 20px;
    margin-top: 20px;
    color: white;
    border-radius: 20px;
  }
  .submit {
    text-align: center;
  }
  .error {
    color: #ff0062;
    margin-top: 10px;
    font-size: 0.8em;
    font-weight: bold;
  }
</style>