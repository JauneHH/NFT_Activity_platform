var app = new Vue({
el: '#app',
    delimiters:['[[', ']]'],
  methods: {
      toggleSelection() {
          alert("hahaha")
      },
      test() {
          console.log('test')
      }
    },
    data: {
        name: '可爱的按钮',
        visible: false
    }
})
