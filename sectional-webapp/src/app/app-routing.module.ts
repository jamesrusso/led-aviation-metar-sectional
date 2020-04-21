import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { SetupComponent } from './setup/setup.component'
import { ConfigComponent } from './config/config.component';

const routes: Routes = [
 { path: 'setup', component: SetupComponent },
 { path: 'config', component: ConfigComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
