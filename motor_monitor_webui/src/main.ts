import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'

import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faPlay, fa0, faDownLeftAndUpRightToCenter, faBan,
  faGaugeHigh, faStop, faRotateRight, faTrashCan,
  faPlus, faCrosshairs
} from '@fortawesome/free-solid-svg-icons'

library.add(faPlay, fa0, faDownLeftAndUpRightToCenter, faBan,
  faGaugeHigh, faStop, faRotateRight, faTrashCan,
  faPlus, faCrosshairs
);

const app = mount(App, {
  target: document.getElementById('app')!,
})

export default app
