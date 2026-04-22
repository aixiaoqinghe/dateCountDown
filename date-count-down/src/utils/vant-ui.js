import { Toast, Tabbar, TabbarItem, Search, Sidebar, SidebarItem } from 'vant'

export default {
  install: (app) => {
    app.use(Toast)
    app.use(Tabbar)
    app.use(TabbarItem)
    app.use(Search)
    app.use(Sidebar)
    app.use(SidebarItem)
  }
}
