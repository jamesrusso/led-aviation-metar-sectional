import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms'
import { StepperSelectionEvent } from '@angular/cdk/stepper';
import { DataserviceService } from '../dataservice.service'
import { MatAutocompleteSelectedEvent } from '@angular/material/autocomplete'
import { debounceTime, tap, switchMap, finalize, filter } from 'rxjs/operators';

interface AirportForPixelResponse {
  icao_airport_code: string
}

interface MetarResponse {
  icao_airport_code: string
  metar: string
}

@Component({
  selector: 'app-setup',
  templateUrl: './setup.component.html',
  styleUrls: ['./setup.component.scss'],
})

export class SetupComponent implements OnInit {
  public initialSetupFormGroup: FormGroup
  public airportSelectionFormGroup: FormGroup
  public ledCount: number = 0
  public filteredAirports = []
  public isLoading = false
  public errorMsg = ""
  public pixel_count = 0
  public pixelIndex = 0
  public metar: string = null
  public metar_loading: boolean = false
  public metar_error: string = null

  constructor(private dataservice: DataserviceService, private formBuilder: FormBuilder) {
    this.initialSetupFormGroup = this.formBuilder.group({
      pixel_count: [null, [Validators.required, Validators.min(1), Validators.max(999)]]
    });

    this.airportSelectionFormGroup = this.formBuilder.group({
      airport: [null, [Validators.required]]
    });
  }

  completeSetup() { 
    this.dataservice.setupcomplete(true).subscribe()
  }


  stepChanged(event: StepperSelectionEvent) {
    if (event.selectedStep.label == "setpixelcount") {

    } else if (event.selectedStep.label == "testleds") {
      this.dataservice.set_option('pixel_count', this.initialSetupFormGroup.get('pixel_count'))
      this.dataservice.selftest().subscribe()

    } else if (event.selectedStep.label == "airportassignment") {
      this.dataservice.clearpixels().subscribe()
      this.pixelIndex = 0
      this.loadPixelData()
    } else if (event.selectedStep.label == "finish") {
    }
  }

  loadPixelData() {
    this.metar = null
    this.metar_error = null
    this.metar_loading = null;

    this.dataservice.setpixelcolor(this.pixelIndex, '#f00').subscribe()
    this.dataservice.getairportforpixel(this.pixelIndex).subscribe((data: AirportForPixelResponse) => {
      this.airportSelectionFormGroup.get('airport').setValue(data.icao_airport_code)
      this.airportSelectionFormGroup.markAsUntouched()
    })

  }

  nextPixel() {
    if (!this.airportSelectionFormGroup.valid && !this.airportSelectionFormGroup.pristine) {
      this.airportSelectionFormGroup.markAllAsTouched()
      return
    }

    if (this.airportSelectionFormGroup.get('airport').value != null) {
      this.dataservice.setairportforpixel(this.pixelIndex, this.airportSelectionFormGroup.get('airport').value.icao_airport_code).subscribe()
    }

    this.dataservice.setpixelcolor(this.pixelIndex, '#000').subscribe()

    if (this.pixelIndex < this.pixel_count) {
      this.pixelIndex = this.pixelIndex + 1
      this.loadPixelData()
    }
  }

  previousPixel() {
    if (!this.airportSelectionFormGroup.valid && !this.airportSelectionFormGroup.pristine) {
      this.airportSelectionFormGroup.markAllAsTouched()
      return
    }

    if (this.airportSelectionFormGroup.get('airport').value != null) {
      this.dataservice.setairportforpixel(this.pixelIndex, this.airportSelectionFormGroup.get('airport').value.icao_airport_code).subscribe()
    }
    this.dataservice.setpixelcolor(this.pixelIndex, '#000').subscribe()

    if (this.pixelIndex > 0) {
      this.pixelIndex = this.pixelIndex - 1
      this.loadPixelData()
    }
  }

  displayFn(obj: any) {
    return obj
  }

  airportSelected(event: MatAutocompleteSelectedEvent) {
    this.loadMetar(event.option.value.icao_airport_code)
  }

  RequireMatch(control: AbstractControl) {
    const selection: any = control.value;
    if (typeof selection === 'string') {
      return { incorrect: true };
    }
    return null;
  }

  loadMetar(icao_airport_code: string) {
    if (icao_airport_code == null) {
      return
    }
    this.metar_loading = true
    this.metar = null
    this.metar_error = null
    this.dataservice.load_metar(icao_airport_code).subscribe((results: MetarResponse) => {
      this.metar_loading = false
      this.metar = results.metar
    }, (error) => {
      console.log("METAR Error", error)
      this.metar_error = error.error.message
      this.metar = null
      this.metar_loading = false
    });
  }


  ngOnInit() {

    this.airportSelectionFormGroup.get('airport').valueChanges.pipe(debounceTime(500)).
    subscribe((data) => { 
      this.loadMetar(data)
    });

    this.airportSelectionFormGroup.get('airport').valueChanges
      .pipe(
        debounceTime(500),
        filter((x: string) => x && x.length >= 2),

        tap(() => {
          this.errorMsg = "";
          this.filteredAirports = [];
          this.isLoading = true;
        }),
        switchMap(value => this.dataservice.airportsearch(value)
          .pipe(
            finalize(() => {
              this.isLoading = false
            }),
          )
        )
      )
      .subscribe(data => {
        if (data == undefined) {
          this.errorMsg = "Unable to get airport data"
          this.filteredAirports = [];
        } else {
          this.errorMsg = "";
          this.filteredAirports = data as any[]
        }
      });

    this.dataservice.get_option('pixel_count').subscribe((data) => {
      this.pixel_count = data.results.value
      this.initialSetupFormGroup.get("pixel_count").setValue(data.results.value)
    })
  }
}
