import { Component, OnInit } from '@angular/core';
import { DataserviceService } from '../dataservice.service';
import { map } from 'rxjs/operators'
import { MatCheckboxChange } from '@angular/material/checkbox';

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.scss']
})

export class ConfigComponent implements OnInit {
  public conditions: any
  constructor(private dataservice: DataserviceService) { }

  colorSelected(key, color) {
    this.conditions[key].color = color
    this.dataservice.set_condition(key, this.conditions[key]).subscribe()
  }

  refreshMetars() { 
    this.dataservice.refreshmetars().subscribe()
  }

  refreshSunrise() { 
    this.dataservice.refreshsunrisedata().subscribe();
  }

  blinkChanged(key, blink: MatCheckboxChange) { 
    this.conditions[key].blink = blink.checked
    this.dataservice.set_condition(key, this.conditions[key]).subscribe()
  }

  ngOnInit(): void {
    this.dataservice.get_conditions().subscribe((data) => this.conditions = data)
  }

}
