var PORT=8889;
var http=require('http');
var fs=require('fs');
var url=require('url');
var querystring=require('querystring');
    exec = require("child_process").exec;

function onRequest(request, response) {
  console.log("Request received.");
  response.writeHead(200, {"Content-Type": "text/html"});
  var params = querystring.parse(url.parse(request.url).query);
  var data = { name : 'undefined package' };
  if ('name' in params) {
    data['name'] = params['name'];
	   }
  //executes my shell script - provision_new.sh when a request is posted to the server
  exec('bash resolv.sh '+params['name']+'', function (err, stdout, stderr) {

      //Print stdout/stderr to console
          console.log(stdout);
          console.log(stderr);

      //Simple response to user whenever localhost:8888 is accessed
          response.write(stdout);
          response.end();
                              });
                           }
 http.createServer(onRequest).listen(8889,"0.0.0.0",function () {
 console.log("Server has started.");
                     });
 
