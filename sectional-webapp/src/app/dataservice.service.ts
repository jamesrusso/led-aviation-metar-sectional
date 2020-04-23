import { Injectable } from '@angular/core'
import { Observable, throwError } from 'rxjs'
import { catchError } from 'rxjs/operators' 
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http' 

@Injectable({
  providedIn: 'root'
})

export class DataserviceService {

  constructor( private http: HttpClient ) { 
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(error);
  };

  public get_pixelcount() : Observable<any> { 
    return this.http.get('/api/pixelcount').pipe(catchError(this.handleError))
  }

  public set_pixelcount(pixelcount: number) : any { 
    return this.http.post('/api/pixelcount', { 'pixelcount': pixelcount }).pipe(catchError(this.handleError))
  }

  public selftest() { 
    return this.http.post('/api/selftest', null).pipe(catchError(this.handleError))
  }

  public getairportforpixel(idx: number) { 
    return this.http.get('/api/pixel/'+idx).pipe(catchError(this.handleError))
  }
  
  public setairportforpixel(idx: number, airport: string) { 
    return this.http.post('/api/pixel/'+idx, { 'icao_airport_code': airport }).pipe(catchError(this.handleError))
  }

  public setpixelcolor(idx: number, color: string) { 
    return this.http.post('/api/setpixel/'+idx, { 'color': color }).pipe(catchError(this.handleError))
  }

  public clearpixels() { 
    return this.http.post('/api/clearpixels', {}).pipe(catchError(this.handleError))
  }

  public airportsearch(value: string) {
    return this.http.get('/api/airportsearch',{ params: { 'q': value } }).pipe(catchError(this.handleError))
  }

  public setupcomplete(val:boolean) { 
    return this.http.post('/api/setup_complete', { 'setup_complete': true }).pipe(catchError(this.handleError))

  }
  public load_metar(airport: string) {
    return this.http.get('/api/metar/'+airport).pipe(catchError(this.handleError))
  }

  public refreshsunrisedata() { 
    return this.http.post('/api/refreshsunrise', null).pipe(catchError(this.handleError))
  }
  
  public refreshmetars() { 
    return this.http.post('/api/refreshmetars', null).pipe(catchError(this.handleError))
  }

  public get_airports() : any { 
  	return this.http.get('/api/airports').pipe(catchError(this.handleError))
  }

  public get_conditions() : any { 
    return this.http.get('/api/conditions').pipe(catchError(this.handleError))
  }

  public set_condition(condition, color) : any { 
    return this.http.post('/api/condition/'+condition, { 'color': color.color, 'blink': color.blink });
  }

  public get_option(option) : any { 
    return this.http.get('/api/option/'+option).pipe(catchError(this.handleError))
  }

  public set_option(option, val) : any { 
    return this.http.post('/api/option/'+option, { 'value': val }).pipe(catchError(this.handleError))
  }

  public reset_colors() : any { 
    return this.http.post('/api/reset_colors', {}).pipe(catchError(this.handleError))
  }

}
