declare module '@kangc/v-md-editor' {
  import { DefineComponent } from 'vue'
  const VMdEditor: DefineComponent<any, any, any>
  export default VMdEditor
}

declare module '@kangc/v-md-editor/lib/theme/github.js' {
  const theme: any
  export default theme
}
