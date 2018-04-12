import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';


@Injectable()
export class ConnectionService {

  private url='http://146.86.79.28:1134';
  private socket;

  constructor() { }

  ngOnInit(){
    this.socket = new WebSocket(this.url,JSON.stringify({username:'Noah'}));
  }

  sendMessage(message:Message){
    this.socket.send(JSON.stringify(message));
  }

  getMessage(){
    let observ = new Observable(observer => {
      this.socket.onMessage = (message) => {
        observer.next(message.data);
      };
    });
    return observ;
  }

}

export interface Message{
  username: string,
  dm: string,
  message: string
  length: number,
  date?: Date
}
