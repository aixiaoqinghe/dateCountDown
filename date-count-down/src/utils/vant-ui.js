import { Toast, Tabbar, TabbarItem, Search, Sidebar, SidebarItem, Uploader, Dialog, Button, Popup } from 'vant'

export default {
  install: (app) => {
    app.use(Toast)
    app.use(Tabbar)
    app.use(TabbarItem)
    app.use(Search)
    app.use(Sidebar)
    app.use(SidebarItem)
    app.use(Uploader)
    app.use(Dialog)
    app.use(Button)
    app.use(Popup)
  }
}
