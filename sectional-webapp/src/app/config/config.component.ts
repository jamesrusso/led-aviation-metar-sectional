import { Component, OnInit } from '@angular/core';
import { DataserviceService } from '../dataservice.service';
import { MatCheckboxChange } from '@angular/material/checkbox';
import { debounceTime, distinctUntilChanged, filter } from 'rxjs/operators';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms'


@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.scss']
})

export class ConfigComponent implements OnInit {
  private static configurationOptionNames: string[] = ["metar_invalid_age", "metar_inop_age", "sunrise_refresh_interval", "metar_refresh_interval", "night_lights", "pixel_count" ];
  public configLoaded: boolean = false
  public conditions: any
  public configurationOptions: FormGroup

  constructor(private dataservice: DataserviceService, private formBuilder: FormBuilder) { 
    this.configurationOptions = this.formBuilder.group( {} );
    for (var item in ConfigComponent.configurationOptionNames) { 
      let name = ConfigComponent.configurationOptionNames[item]
      this.configurationOptions.addControl(name, this.formBuilder.control(null, Validators.required))
      this.configurationOptions.get(name)
      .valueChanges
      .pipe(debounceTime(350), distinctUntilChanged(), filter((val) => val != null))
      .subscribe( (val) => { 
        this.dataservice.set_option(name, val).subscribe()
      })
    }
  }

  colorSelected(key, color) {
    this.conditions[key].color = color
    this.dataservice.set_condition(key, this.conditions[key]).subscribe()
  }

  refreshMetars() { 
    this.dataservice.refreshmetars().subscribe()
  }

  resetColors() { 
    this.dataservice.reset_colors().subscribe(() => {
      this.dataservice.get_conditions().subscribe((data) => this.conditions = data)
    })
  }

  refreshSunrise() { 
    this.dataservice.refreshsunrisedata().subscribe();
  }

  blinkChanged(key, blink: MatCheckboxChange) { 
    this.conditions[key].blink = blink.checked
    this.dataservice.set_condition(key, this.conditions[key]).subscribe()
  }

  ngOnInit(): void {
    var tasks = []
    this.dataservice.get_conditions().subscribe((data) => this.conditions = data)
   
    for (let item in ConfigComponent.configurationOptionNames) {
        let optionName: string = ConfigComponent.configurationOptionNames[item]
        this.dataservice.get_option(optionName).subscribe((data) => {  
          this.configurationOptions.get(data.results.name).setValue(data.results.value)
        })
    }
  }
}