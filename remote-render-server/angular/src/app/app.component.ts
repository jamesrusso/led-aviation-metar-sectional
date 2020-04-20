import { Component } from '@angular/core';
import * as io from 'socket.io-client';
import { environment } from './../environments/environment'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
	public pixels: number[][]
	private ledCount: number
 	private socket;

	constructor() {   
  		this.setupSocketConnection();
  	}

  setupSocketConnection() {
    this.socket = io(environment.SOCKET_ENDPOINT);
    this.socket.on('connection', x => { 
		console.log("got connection");
    });
    this.socket.on('led:set', item => { 
    	console.log("got message ",item);
    	this.setLed(item.index, item.color)
    });
  }


	ngOnInit(): void { 
		this.ledCount = 20
		this.pixels = []
		for (var i=0;i<this.ledCount;i++) {
			this.pixels[i] = [Math.random()*256,Math.random()*256,Math.random()*256]
		}
	}

	setLed(index: number, color: number[]) { 
		this.pixels[index]  = color
	}
}
