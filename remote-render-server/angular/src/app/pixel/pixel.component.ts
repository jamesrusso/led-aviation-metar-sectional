import { Component, OnInit, ViewChild, ElementRef, Input} from '@angular/core';

@Component({
  selector: 'app-pixel',
  templateUrl: './pixel.component.html',
  styleUrls: ['./pixel.component.css']
})

export class PixelComponent implements OnInit {
	@ViewChild('canvas', { static: true })
 	canvas: ElementRef<HTMLCanvasElement>;
	private ctx: CanvasRenderingContext2D;
	private _color: Array<Number>;

  	constructor() { }


  	@Input()
  	set color(color) { 
  		this._color = color;
  		this.draw();
  	}
	
	ngOnInit(): void {
		this.draw()
	}

	  draw(): void { 
		this.ctx = this.canvas.nativeElement.getContext('2d');
	  	this.ctx.fillStyle = 'rgb('+this._color[0]+','+this._color[1]+','+this._color[2]+')'
	  	this.ctx.arc(25, 21, 18, 0, 2 * Math.PI);
	  	this.ctx.fill()
  }

}
