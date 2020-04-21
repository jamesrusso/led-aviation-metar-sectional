import { Component, OnInit } from '@angular/core';
import { DataserviceService } from '../dataservice.service';
import { map } from 'rxjs/operators'

@Component({
  selector: 'app-config',
  templateUrl: './config.component.html',
  styleUrls: ['./config.component.scss']
})

export class ConfigComponent implements OnInit {
  public conditions: any
  constructor(private dataservice: DataserviceService) { }

  colorSelected(condition, color) {
    this.dataservice.set_condition(condition, color).subscribe()
  }

  ngOnInit(): void {
    this.dataservice.get_conditions().pipe(map((data: any) => {

      var rgbToHex = function (rgb) {
        var hex = Number(rgb).toString(16);
        if (hex.length < 2) {
          hex = "0" + hex;
        }
        return hex;
      };

      for (let key in data) {
        data[key] = '#' + rgbToHex(data[key][0]) + rgbToHex(data[key][1]) + rgbToHex(data[key][2]);
      }
      return data
    })).subscribe((data) => this.conditions = data)


  }

}
