import { Component } from '@angular/core';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {


  username:String = ''
  password:String = ''
  getUsername(val:String){
    this.username
  }
  getPassword(val:String){
    this.password
  }


  loginFunc(){
    alert(this.password);
  }






}
